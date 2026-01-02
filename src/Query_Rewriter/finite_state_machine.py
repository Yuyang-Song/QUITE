import asyncio
import sys
import threading

# Setup project paths
from src.utils.path_config import setup_python_path
setup_python_path()

from src.Rewrite_Middleware.middleware import DBMS_EXPLAIN_Tool, DBMS_Syntax_Tool, Knowledge_Base_Tool, Equivalence_Check_Tool, DBMS
from src.Rewrite_Middleware.Agent_Memory_Buffer.memory_buffer import AgentMemoryBuffer, OutputCollector, create_memory_buffer
from src.Query_Rewriter.agent_definition import ReasoningAgent, AssistantAgent, DecisionAgent
from src.utils.agent_template import MessageContent, Message, MemoryWindow, MessageQueue


class QueryRewriter:
    """SQL Rewrite Finite State Machine"""
    def __init__(self, message_queue: MessageQueue, dbms: DBMS, data_statistics, schema_file, MAX_ITERATION_LOOP=3):
        self.current_state = "REASONING"
        self.memory = create_memory_buffer(data_statistics, schema_file)

        self.dbms = dbms
        self.iteration = 0
        self.MAX_ITERATION_LOOP = MAX_ITERATION_LOOP    
        self.terminal_output = None
        self.output_collector = OutputCollector()

        # Initialize each agent
        self.reasoning_agent = ReasoningAgent(message_queue)
        self.assistant_agent = AssistantAgent(message_queue)
        self.decision_agent = DecisionAgent(message_queue)

        # Set up observation relationships
        self.decision_agent.watch(["ReasoningAgent","ExplainAgent"])
        self.assistant_agent.watch(["SummaryAgent","ExplainAgent"])

        # Parallel processing related
        self.parallel_threads = 2
        self.parallel_reasoning_results = []
        self.parallel_verification_results = []
        self._stop_event = threading.Event()
        self.llm_semaphore = asyncio.Semaphore(3)  # Control LLM concurrency
        self.db_semaphore = asyncio.Semaphore(5)   # Control database concurrency

    @property
    def data_statistics(self):
        return self.memory.data_statistics
    
    @property
    def initial_sql(self):
        return self.memory.initial_sql
    
    @initial_sql.setter
    def initial_sql(self, value):
        self.memory.initial_sql = value
    
    @property
    def optimization_advice(self):
        return self.memory.optimization_advice
    
    @optimization_advice.setter
    def optimization_advice(self, value):
        self.memory.optimization_advice = value
    
    @property
    def produced_sql(self):
        return self.memory.produced_sql
    
    @produced_sql.setter
    def produced_sql(self, value):
        self.memory.produced_sql = value
    
    @property
    def enhanced_sql(self):
        return self.memory.enhanced_sql
    
    @enhanced_sql.setter
    def enhanced_sql(self, value):
        self.memory.enhanced_sql = value
    
    @property
    def re_explain_result(self):
        return self.memory.re_explain_result
    
    @re_explain_result.setter
    def re_explain_result(self, value):
        self.memory.re_explain_result = value
    
    @property
    def ori_explain_result(self):
        return self.memory.ori_explain_result
    
    @ori_explain_result.setter
    def ori_explain_result(self, value):
        self.memory.ori_explain_result = value
    
    @property
    def imp_explain_result(self):
        return self.memory.imp_explain_result
    
    @imp_explain_result.setter
    def imp_explain_result(self, value):
        self.memory.imp_explain_result = value
    
    @property
    def guide_info(self):
        return self.memory.guide_info
    
    @guide_info.setter
    def guide_info(self, value):
        self.memory.guide_info = value
    
    @property
    def report(self):
        return self.memory.report
    
    @report.setter
    def report(self, value):
        self.memory.report = value
    
    @property
    def schema_file(self):
        return self.memory.schema_file
    
    async def clear(self):
        """Clear all initialization variables - using a simplified memory buffer"""
        # Use memory buffer's clearing method
        self.memory.clear_volatile_memory()

        # Reset FSM state
        self.current_state = "REASONING"
        self.iteration = 0
        self.parallel_reasoning_results = []
        self.parallel_verification_results = []
        self._stop_event.clear()
        
        print(f"🧹 Memory cleared. Buffer status: {self.memory}")
    
    async def clear_log(self):
        if hasattr(self, 'terminal_output'):
            del self.terminal_output
        
    async def run(self):
        self.output_collector.start_collecting()

        while self.current_state != "TERMINATED":

            if self.current_state == "REASONING":
                await self.state_reasoning_parallel()

            elif self.current_state == "VERIFICATION":
                await self.state_verification_parallel()

            elif self.current_state == "DECISION":
                await self.state_decision()
            await asyncio.sleep(0.1)  # Prevent event loop blocking

        terminal_output = self.output_collector.stop_collecting()
        # Store the output in FSM's attributes
        self.terminal_output = terminal_output
        
        return self.enhanced_sql
    
    async def parallel_reasoning_worker(self, worker_id: int):
        """Parell reasoning worker"""
        try:
            print(f"\n=== Worker {worker_id}: Start Reasoning Stage ===")
            
            async with self.db_semaphore:
                explain_info = await DBMS_EXPLAIN_Tool(self.dbms, self.initial_sql)
            async with self.llm_semaphore:
                if self.report is None:
                    reasoning_result = await self.reasoning_agent.analyze_sql(
                        self.initial_sql, self.data_statistics, explain_info
                    )
                else:
                    reasoning_result = await self.reasoning_agent.analyze_sql_report(
                        self.initial_sql, self.data_statistics, self.report, explain_info
                    )

            # Extract structured results
            print(f"\n=== Worker {worker_id}: Start Rewrite ===")
            chain = self.decision_agent.retrieve_reasoning_chain()
            async with self.llm_semaphore:
                summary = await self.decision_agent.summarize_chain(
                    chain, self.initial_sql, self.data_statistics
                )
            
            produced_sql = self.decision_agent.extract_sql_candidate_content(summary)
            enhanced_sql = self.decision_agent.extract_enhanced_sql_content(summary)
            optimization_advice = self.decision_agent.extract_advice_content(summary)

            # Check if there is any actual optimization content
            if enhanced_sql and enhanced_sql.strip() and enhanced_sql != self.initial_sql:
                # If there is valid optimized SQL, use it
                print(f"Worker {worker_id}: Found optimized SQL")
                return {
                    "worker_id": worker_id,
                    "status": "success",
                    "produced_sql": produced_sql,
                    "enhanced_sql": enhanced_sql,
                    "optimization_advice": optimization_advice
                }
            elif "TERMINATE" in reasoning_result:
                # Only early stop when there is no optimized SQL and a clear request to terminate
                print(f"Worker {worker_id}: Early stop - no need to optimize")
                return {
                    "worker_id": worker_id,
                    "status": "early_stop",
                    "produced_sql": self.initial_sql,
                    "enhanced_sql": self.initial_sql,
                    "optimization_advice": "No need to optimize"
                }
            else:
                # There are optimization suggestions but no SQL extracted, still considered a success
                print(f"Worker {worker_id}: Using extracted results")
                return {
                    "worker_id": worker_id,
                    "status": "success",
                    "produced_sql": produced_sql or self.initial_sql,
                    "enhanced_sql": enhanced_sql or self.initial_sql,
                    "optimization_advice": optimization_advice or "No specific advice"
                }
            
        except Exception as e:
            print(f"Worker {worker_id}: Reasoning error occurred: {str(e)}")
            return {
                "worker_id": worker_id,
                "status": "error",
                "error": str(e),
                "equivalence_passed": False
            }
        
    async def state_reasoning_parallel(self):
        """Parallel reasoning state"""
        print(f"######################################################################################")
        print(f"\n=== Start Parallel Reasoning (Number of Threads: {self.parallel_threads}) ===")

        # Clear results
        new_reasoning_results = []

        # Create and run parallel tasks
        tasks = []
        for worker_id in range(self.parallel_threads):
            task = asyncio.create_task(self.parallel_reasoning_worker(worker_id))
            tasks.append(task)

        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        for result in results:
            if result is not None and not isinstance(result, Exception):
                if result.get("status") in ["success", "early_stop"]:
                    new_reasoning_results.append(result)
                else:
                    # Skip failed workers
                    worker_id = result.get("worker_id", "unknown")
                    print(f"## Worker {worker_id} Reasoning failed. Skipping this worker.##")
        
        self.parallel_reasoning_results = new_reasoning_results
        
        if not self.parallel_reasoning_results:
            print("## All the parallel reasoning workers failed. Use the original SQL.##")
            self.produced_sql = self.initial_sql
            self.enhanced_sql = self.initial_sql
            self.optimization_advice = "No need to optimize"
            self.current_state = "TERMINATED"
        else:
            success_count = len([r for r in self.parallel_reasoning_results if r["status"] == "success"])
            early_stop_count = len([r for r in self.parallel_reasoning_results if r["status"] == "early_stop"])
            print(f"## Parallel reasoning completed, obtained {len(self.parallel_reasoning_results)} Effective results (Suceess: {success_count}, Early Stop: {early_stop_count})##")
            
            self.current_state = "VERIFICATION"

    async def parallel_verification_worker(self, reasoning_result: dict):
        """verification worker"""
        worker_id = reasoning_result["worker_id"]
        enhanced_sql = reasoning_result["enhanced_sql"]
        produced_sql = reasoning_result["produced_sql"]
        optimization_advice = reasoning_result["optimization_advice"]
        
        try:
            print(f"\n=== Worker {worker_id}: Start Verification Stage ===")
            
            # Syntax Check
            async with self.db_semaphore:
                syntax_check = await DBMS_Syntax_Tool(self.dbms, enhanced_sql)
            MAX_CORRECT_TIMES = 0
            MAX_CORRECT_FLAG = False
            
            if not syntax_check["flag"]:
                print(f"## Worker {worker_id}: grammar mistake: {syntax_check['error']}, try to correct it ##")
                CHECK_FLAG = False
                current_error = syntax_check["error"]  # Record the current error to be corrected
                
                while CHECK_FLAG == False and MAX_CORRECT_TIMES < 3:
                    if self._stop_event.is_set():
                        print(f"Worker {worker_id}: interrupted")
                        return None
                        
                    print(f"Worker {worker_id}: ################ Start correct the error ################")
                    print(f"Worker {worker_id}: Current error to fix: {current_error}")
                    async with self.llm_semaphore:
                        checked_sql = await self.assistant_agent._correct_sql(
                            self.initial_sql, enhanced_sql, current_error  # Always modify the initial version, but use the current error
                        )
                    async with self.db_semaphore:
                        check_result = await DBMS_Syntax_Tool(self.dbms, checked_sql)
                    MAX_CORRECT_TIMES += 1
                    
                    if check_result["flag"]:
                        CHECK_FLAG = True
                        MAX_CORRECT_FLAG = True
                        print(f"-- Worker {worker_id}: ✓ THE GRAMMAR CHECK HAS BEEN PASSED.--")
                        enhanced_sql = checked_sql
                    else:
                        # Update the error information to the current attempted error for reference in the next correction
                        current_error = check_result["error"]
                        print(f"-- Worker {worker_id}: X Grammar check failed again. New error: {current_error}--")
                
                if MAX_CORRECT_FLAG == False:
                    print(f"-- Worker {worker_id}: X The grammar check failed. Please go back and review the reasoning.--")
                    return {
                        "worker_id": worker_id,
                        "status": "syntax_failed",
                        "equivalence_passed": False
                    }
            else:
                print(f"-- Worker {worker_id}: ✓ THE GRAMMAR CHECK HAS BEEN PASSED.--")
            
            # Equivalence Check
            MAX_EQUIV_TIMES = 0
            MAX_EQUIV_FLAG = False
            
            print(f"-- Worker {worker_id}: Perform SQL equivalence check--")
            
            result = await Equivalence_Check_Tool(
                self.initial_sql, enhanced_sql, self.schema_file, timeout=10
            )
            
            if result is not None and "EQ" in result:
                print(f"-- Worker {worker_id}: ✓ Through the optimizer verification, the optimized SQL is equivalent to the original SQL.--")
                MAX_EQUIV_FLAG = True
            else:
                print(f"-- Worker {worker_id}: X Not verified by the optimizer, calling LLM to rewrite process--")
                CHECK_EQUIV_FLAG = False
                tmp_checked_sql = enhanced_sql
                
                while CHECK_EQUIV_FLAG == False and MAX_EQUIV_TIMES < 3:
                    if self._stop_event.is_set():
                        print(f"-- Worker {worker_id}: interrupted--")
                        return None
                        
                    async with self.llm_semaphore:
                        checked_report = await self.decision_agent.check_equivalence(
                            self.initial_sql, tmp_checked_sql, optimization_advice
                        )
                    CHCKED_FLAG = self.decision_agent.extract_equivalence_content(checked_report)
                    MAX_EQUIV_TIMES += 1
                    
                    if "true" in CHCKED_FLAG or "True" in CHCKED_FLAG:
                        CHECK_EQUIV_FLAG = True
                        MAX_EQUIV_FLAG = True
                        enhanced_sql = tmp_checked_sql
                        print(f"-- Worker {worker_id}: ✓ Optimize SQL to be equivalent to the original SQL--")
                    else:
                        print(f"-- Worker {worker_id}: X Optimize SQL not be equivalent to the original SQL (try {MAX_EQUIV_TIMES}/3)--")
                        corrected_sql = self.decision_agent.extract_corrected_sql_content(checked_report)
                        if corrected_sql:
                            tmp_checked_sql = corrected_sql
                            print(f"-- Worker {worker_id}: The revised and optimized SQL query: {tmp_checked_sql}--")
                
                if MAX_EQUIV_FLAG == False:
                    print(f"-- Worker {worker_id}: X The equivalence check failed. The maximum number of attempts has been reached. Using the original SQL.--")
                    enhanced_sql = self.initial_sql
                    self.optimization_advice = "No need to optimize"
            
            print(f"-- Worker {worker_id}: Verification completed")
            return {
                "worker_id": worker_id,
                "status": "success",
                "produced_sql": produced_sql,
                "enhanced_sql": enhanced_sql,
                "optimization_advice": optimization_advice,
                "equivalence_passed": MAX_EQUIV_FLAG
            }
            
        except Exception as e:
            print(f"Worker {worker_id}: Verification errors: {str(e)}")
            return {
                "worker_id": worker_id,
                "status": "error",
                "error": str(e),
                "equivalence_passed": False
            }
    

    async def state_verification_parallel(self):
        """Parallel verification state"""
        print(f"######################################################################################")
        print(f"\n=== Start Parallel Verification ===")

        # Reset results and stop event
        new_verification_results = []
        self._stop_event.clear()

        # Only successful reasoning results are subject to verification
        successful_reasoning = [r for r in self.parallel_reasoning_results
                               if r["status"] == "success"]
        early_stop_reasoning = [r for r in self.parallel_reasoning_results 
                               if r["status"] == "early_stop"]

        # Early stop results can be directly added to the final results
        for early_stop in early_stop_reasoning:
            new_verification_results.append({
                "worker_id": early_stop["worker_id"],
                "status": "success",
                "produced_sql": early_stop["produced_sql"],
                "enhanced_sql": early_stop["enhanced_sql"],
                "optimization_advice": early_stop["optimization_advice"]
            })

        # Create tasks for workers that need verification
        tasks = []
        for reasoning_result in successful_reasoning:
            task = asyncio.create_task(self.parallel_verification_worker(reasoning_result))
            tasks.append(task)

        if tasks:  # If there are tasks that need verification
            # Wait for all verification tasks to complete
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Process verification results
            for result in results:
                if result is not None and not isinstance(result, Exception):
                    if result.get("status") == "success":
                        new_verification_results.append(result)
                    else:
                        # Skip failed workers
                        worker_id = result.get("worker_id", "unknown")
                        print(f"## Worker {worker_id} Verification failed. Skipping this worker.##")

        # Determine the next state
        if new_verification_results:
            # If there are successful verification results, proceed to decision 
            print(f"## Parallel verification complished, obtains {len(new_verification_results)} effective results##")
            self.parallel_verification_results = new_verification_results
            self.current_state = "DECISION"
        else:
            # All verification attempts failed, terminate using the original SQL
            print("## All the parallel verification workers failed. Using the original SQL.##")
            self.produced_sql = self.initial_sql
            self.enhanced_sql = self.initial_sql
            self.optimization_advice = "No need to optimize"
            self.current_state = "TERMINATED"



    async def state_decision(self):
        """Decision state - includes selection and decision logic"""
        print(f"######################################################################################")
        print(f"\n=== Start Decision Stage: (Iteration: {self.iteration}/{self.MAX_ITERATION_LOOP}) ===")

        # Step 1: Select the optimal SQL (if there are multiple verification results)
        if len(self.parallel_verification_results) == 1:
            # Only one result, use it directly
            selected_result = self.parallel_verification_results[0]
            print(f"## There is only one valid option, so choose it directly Worker {selected_result['worker_id']}##")
        else:
            # Multiple results, need to select
            print(f"##  {len(self.parallel_verification_results)} results, try to select the best one ##")
            query_pairs = []
            for result in self.parallel_verification_results:
                query_pairs.append({
                    "id": result["worker_id"],
                    "enhanced_sql": result["enhanced_sql"],
                })
            
            async with self.llm_semaphore:
                selected_advice = await self.decision_agent.select_sql(self.initial_sql, query_pairs)
            selected_id = self.decision_agent.extract_selected_id_content(selected_advice)

            # Find the corresponding result
            selected_result = None
            for result in self.parallel_verification_results:
                if result["worker_id"] == selected_id:
                    selected_result = result
                    break
            
            if selected_result is None:
                print(f"## Do not find selected worker {selected_id}, use the first result instead ##")
                selected_result = self.parallel_verification_results[0]
            else:
                print(f"## selected Worker {selected_id}##")

        # Set the selected result
        self.produced_sql = selected_result["produced_sql"]
        self.enhanced_sql = selected_result["enhanced_sql"]
        self.optimization_advice = selected_result["optimization_advice"]

        print(f"## Selected Rewritten SQL: {self.enhanced_sql} ##")
        print(f"## Rewrite Proposals: {self.optimization_advice} ##")


        # Generate report
        print(f"## Generate optimization report... ##")
        async with self.db_semaphore:
            # Execute the two explain tasks in parallel
            ori_explain_task = asyncio.create_task(DBMS_EXPLAIN_Tool(self.dbms, self.initial_sql))
            enhanced_explain_task = asyncio.create_task(DBMS_EXPLAIN_Tool(self.dbms, self.enhanced_sql))
            
            ori_explain_result, enhanced_explain_result = await asyncio.gather(
                ori_explain_task, enhanced_explain_task
            )
        async with self.llm_semaphore:
            report = await self.assistant_agent.generate_report(
                ori_explain_result, enhanced_explain_result, enhanced_explain_result
            )
        
        analysis_report = self.assistant_agent.extract_analysis_content(report)
        self.report = analysis_report
        print(f"## Report generation completed ##")

        # Step 2: Make a decision
        # Collect equivalence flags from all verification results
        worker_equivalence_flags = []
        for result in self.parallel_verification_results:
            equivalence_passed = result.get("equivalence_passed", True)  # Default to True for backward compatibility
            worker_equivalence_flags.append(equivalence_passed)
        
        async with self.llm_semaphore:
            decision = await self.decision_agent.evaluate(
                self.initial_sql,
                self.enhanced_sql,
                self.report,
                worker_equivalence_flags
            )
        
        if self.iteration < self.MAX_ITERATION_LOOP:
            self.iteration += 1
            if "true" in decision or "True" in decision:
                print(f"## The decision has been made. Optimization  is terminated (iteration: {self.iteration}/{self.MAX_ITERATION_LOOP}) ##")
                self.current_state = "TERMINATED"
            else:
                print(f"## The decision was not approved. Further optimization is required (iteration: {self.iteration}/{self.MAX_ITERATION_LOOP}) ##")
                
                print("## Start a new round of complete iteration ## ")
                rag_knowledge = await Knowledge_Base_Tool(self.enhanced_sql, self.optimization_advice)
                async with self.llm_semaphore:
                    self.optimization_advice = await self.decision_agent.merge_advice(
                        self.enhanced_sql, 
                        self.optimization_advice,
                        rag_knowledge
                    )
                input_report = {
                    "decision": decision,
                    "pre_rewrite_sql": self.enhanced_sql,
                    "corrected_guide_knowledge": rag_knowledge,
                }
                self.guide_info = input_report
                self.report = input_report

                # Restart the entire process and reset all states
                self.parallel_reasoning_results = []
                self.parallel_verification_results = []
                self.current_state = "REASONING"
        else:
            print(f"## Reach the maximum number of iterations ({self.MAX_ITERATION_LOOP}),print Terminate optimization ##")
            self.enhanced_sql = self.initial_sql
            self.current_state = "TERMINATED"
            self.optimization_advice = "No need to optimize"




# Save terminal output to txt file each time a JSON file is saved
def save_terminal_output_to_file(save_file_path, batch, original_stdout, temp_file):
    # Restore standard output
    sys.stdout = original_stdout
    temp_file.close()

    # Copy the contents of the temporary file to the final file
    with open(f"{save_file_path}/batch_{batch}.txt", "w") as f:
        with open("temp_output.txt", "r") as temp_f:
            f.write(temp_f.read())

    # Redirect standard output to temporary file again
    temp_file = open("temp_output.txt", "w")
    sys.stdout = temp_file
    return temp_file


