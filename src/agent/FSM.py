from dotenv import load_dotenv
import json
import os
import asyncio
import sys
import time
from tools import DBMS, RAG
import time
from tools import DBMS_EXPLAIN_Tool, DBMS_Syntax_Tool, Knowledge_Pool_Tool, Equivalence_Check_Tool
import threading

sys.path.append('../')
sys.path.append('../utils')
sys.path.append('./')

from agent_role import ReasoningAgent, AssistantAgent, DecisionAgent
from QUITE.src.utils.llm_client import GPT
from utils.agent_template import MessageContent, Message, MemoryWindow, MessageQueue

class OutputCollector:
    """收集终端输出的工具类"""
    def __init__(self):
        self.outputs = []
        self.original_stdout = sys.stdout
        self.current_output = ""
    
    def start_collecting(self):
        """开始收集输出"""
        self.original_stdout = sys.stdout
        sys.stdout = self
    
    def stop_collecting(self):
        """停止收集输出并返回收集到的内容"""
        sys.stdout = self.original_stdout
        collected = self.current_output
        self.current_output = ""
        return collected
    
    def write(self, text):
        """重写write方法以捕获输出"""
        self.current_output += text
        self.original_stdout.write(text)
    
    def flush(self):
        """实现flush方法以满足stdout接口"""
        self.original_stdout.flush()




class SQLRewriteFSM:
    """SQL重写有限状态机"""
    def __init__(self, message_queue: MessageQueue, gpt: GPT, dbms: DBMS, data_statistics, schema_file, MAX_ITERATION_LOOP=3):
        self.current_state = "REASONING"
        # self.current_state = "SUMMARY"
        # self.current_state = "VERIFICATION"
        self.llm = gpt
        self.data_statistics = data_statistics
        self.initial_sql = None
        self.optimization_advice = None
        self.produced_sql = None
        self.enhanced_sql = None
        self.re_explain_result = None
        self.ori_explain_result = None
        self.imp_explain_result = None
        self.report = None
        self.dbms = dbms
        self.guide_info = None
        self.iteration = 0
        self.schema_file = schema_file
        self.MAX_ITERATION_LOOP = MAX_ITERATION_LOOP    
        self.terminal_output = None
        self.output_collector = OutputCollector()
        
        # 初始化各Agent
        self.reasoning_agent = ReasoningAgent(message_queue, gpt)
        self.assistant_agent = AssistantAgent(message_queue, gpt)
        self.decision_agent = DecisionAgent(message_queue)
        # 指定文件夹路径
        folder_path = '/root/syy/MARter_5/src/knowledge_pool/data/results'
        # 指定 JSON 文件存储路径
        json_file_path = '/root/syy/MARter_5/src/knowledge_pool/data/documents.json'
        self.rag_tool = RAG(folder_path, json_file_path)
        # self.syntax_tool = DBMS_Syntax_Tool()
        # self.explain_tool = DBMS_EXPLAIN_Tool()
        
        # 设置观察关系
        self.decision_agent.watch(["ReasoningAgent","ExplainAgent"])
        self.assistant_agent.watch(["SummaryAgent","ExplainAgent"])

        # 并行处理相关
        self.parallel_threads = 2
        self.parallel_reasoning_results = []
        self.parallel_verification_results = []
        self._stop_event = threading.Event()
        self.llm_semaphore = asyncio.Semaphore(3)  # 控制LLM并发数
        self.db_semaphore = asyncio.Semaphore(5)   # 控制数据库并发数

    
    async def clear(self):
        """清除所有初始化变量"""
        self.initial_sql = None
        self.current_state = "REASONING"
        self.optimization_advice = None
        self.produced_sql = None
        self.enhanced_sql = None
        self.re_explain_result = None
        self.ori_explain_result = None
        self.imp_explain_result = None
        self.guide_info = None
        self.report = None
        self.iteration = 0
        self.parallel_reasoning_results = []
        self.parallel_verification_results = []
        self._stop_event.clear()
    
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
            await asyncio.sleep(0.1)  # 防止事件循环阻塞
        
        terminal_output = self.output_collector.stop_collecting()
        # 将输出存储到FSM的属性中
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

            # 检查是否有实际的优化内容
            if enhanced_sql and enhanced_sql.strip() and enhanced_sql != self.initial_sql:
                # 有有效的优化SQL，使用它
                print(f"Worker {worker_id}: Found optimized SQL")
                return {
                    "worker_id": worker_id,
                    "status": "success",
                    "produced_sql": produced_sql,
                    "enhanced_sql": enhanced_sql,
                    "optimization_advice": optimization_advice
                }
            elif "TERMINATE" in reasoning_result:
                # 只有在没有优化SQL且明确要求终止时才early stop
                print(f"Worker {worker_id}: Early stop - no need to optimize")
                return {
                    "worker_id": worker_id,
                    "status": "early_stop",
                    "produced_sql": self.initial_sql,
                    "enhanced_sql": self.initial_sql,
                    "optimization_advice": "No need to optimize"
                }
            else:
                # 有优化建议但没有提取到SQL，仍然当作成功
                print(f"Worker {worker_id}: Using extracted results")
                return {
                    "worker_id": worker_id,
                    "status": "success",
                    "produced_sql": produced_sql or self.initial_sql,
                    "enhanced_sql": enhanced_sql or self.initial_sql,
                    "optimization_advice": optimization_advice or "No specific advice"
                }
            
        except Exception as e:
            print(f"Worker {worker_id}: Reasoning发生错误: {str(e)}")
            return {
                "worker_id": worker_id,
                "status": "error",
                "error": str(e)
            }
        
    async def state_reasoning_parallel(self):
        """并行推理状态"""
        print(f"######################################################################################")
        print(f"\n=== Start Parallel Reasoning (Number of Threads: {self.parallel_threads}) ===")
        
        # 清空结果
        new_reasoning_results = []
        
        # 创建并运行并行任务
        tasks = []
        for worker_id in range(self.parallel_threads):
            task = asyncio.create_task(self.parallel_reasoning_worker(worker_id))
            tasks.append(task)
        
        # 等待所有任务完成
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # 处理结果
        for result in results:
            if result is not None and not isinstance(result, Exception):
                if result.get("status") in ["success", "early_stop"]:
                    new_reasoning_results.append(result)
                else:
                    # 失败的worker直接跳过
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
        """并行verification worker"""
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
                while CHECK_FLAG == False and MAX_CORRECT_TIMES < 3:
                    if self._stop_event.is_set():
                        print(f"Worker {worker_id}: interrupted")
                        return None
                        
                    print(f"Worker {worker_id}: ################ Start correct the error ################")
                    async with self.llm_semaphore:
                        checked_sql = await self.assistant_agent._correct_sql(
                            self.initial_sql, enhanced_sql, syntax_check["error"]
                        )
                    async with self.db_semaphore:
                        check_result = await DBMS_Syntax_Tool(self.dbms, checked_sql)
                    MAX_CORRECT_TIMES += 1
                    
                    if check_result["flag"]:
                        CHECK_FLAG = True
                        MAX_CORRECT_FLAG = True
                        print(f"-- Worker {worker_id}: ✓ THE GRAMMAR CHECK HAS BEEN PASSED.--")
                        enhanced_sql = checked_sql
                
                if MAX_CORRECT_FLAG == False:
                    print(f"-- Worker {worker_id}: X The grammar check failed. Please go back and review the reasoning.--")
                    return {
                        "worker_id": worker_id,
                        "status": "syntax_failed"
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
                "optimization_advice": optimization_advice
            }
            
        except Exception as e:
            print(f"Worker {worker_id}: Verification errors: {str(e)}")
            return {
                "worker_id": worker_id,
                "status": "error",
                "error": str(e)
            }
    

    async def state_verification_parallel(self):
        """并行验证状态"""
        print(f"######################################################################################")
        print(f"\n=== Start Parallel Verification ===")
        
        # 重置结果和停止事件
        new_verification_results = []
        self._stop_event.clear()
        
        # 只对成功的reasoning结果进行verification
        successful_reasoning = [r for r in self.parallel_reasoning_results 
                               if r["status"] == "success"]
        early_stop_reasoning = [r for r in self.parallel_reasoning_results 
                               if r["status"] == "early_stop"]
        
        # Early stop的结果可以直接加入最终结果
        for early_stop in early_stop_reasoning:
            new_verification_results.append({
                "worker_id": early_stop["worker_id"],
                "status": "success",
                "produced_sql": early_stop["produced_sql"],
                "enhanced_sql": early_stop["enhanced_sql"],
                "optimization_advice": early_stop["optimization_advice"]
            })
        
        # 为需要验证的worker创建任务
        tasks = []
        for reasoning_result in successful_reasoning:
            task = asyncio.create_task(self.parallel_verification_worker(reasoning_result))
            tasks.append(task)
        
        if tasks:  # 如果有需要验证的任务
            # 等待所有验证任务完成
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 处理验证结果
            for result in results:
                if result is not None and not isinstance(result, Exception):
                    if result.get("status") == "success":
                        new_verification_results.append(result)
                    else:
                        # 验证失败的worker直接跳过，不再重试
                        worker_id = result.get("worker_id", "unknown")
                        print(f"## Worker {worker_id} Verification failed. Skipping this worker.##")

        # 判断下一个状态
        if new_verification_results:
        # 有成功的验证结果，直接进入决策
            print(f"## Parallel verification complished, obtains {len(new_verification_results)} effective results##")
            self.parallel_verification_results = new_verification_results
            self.current_state = "DECISION"
        else:
            # 所有验证都失败了，使用原始SQL终止
            print("## All the parallel verification workers failed. Using the original SQL.##")
            self.produced_sql = self.initial_sql
            self.enhanced_sql = self.initial_sql
            self.optimization_advice = "No need to optimize"
            self.current_state = "TERMINATED"



    async def state_decision(self):
        """决策状态 - 包含选择和决策逻辑"""
        print(f"######################################################################################")
        print(f"\n=== Start Decison Stage: (Iteration: {self.iteration}/{self.MAX_ITERATION_LOOP}) ===")
        
        # Step 1: 选择最优SQL（如果有多个verification结果）
        if len(self.parallel_verification_results) == 1:
            # 只有一个结果，直接使用
            selected_result = self.parallel_verification_results[0]
            print(f"## There is only one valid option, so choose it directly Worker {selected_result['worker_id']}##")
        else:
            # 多个结果，需要选择
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
            
            # 找到对应的结果
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
        
        # 设置选中的结果
        self.produced_sql = selected_result["produced_sql"]
        self.enhanced_sql = selected_result["enhanced_sql"]
        self.optimization_advice = selected_result["optimization_advice"]
        
        print(f"## Slected Rewritten SQL: {self.enhanced_sql} ##")
        print(f"## Rewrite Proposals: {self.optimization_advice} ##")

        # # 检查SQL是否相等
        # sql_equal = (self.initial_sql == self.enhanced_sql)
        # if sql_equal:
        #     print(f"## SQL UNCHANGED: enhanced_sql equals initial_sql ##")
        # else:
        #     print(f"## SQL CHANGED: enhanced_sql differs from initial_sql ##")
        
        # 生成report
        print(f"## Generate optimization report... ##")
        async with self.db_semaphore:
            # 并行执行这两个explain
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

        # Step 2: 进行决策
        async with self.llm_semaphore:
            decision = await self.decision_agent.evaluate(
                self.initial_sql,
                self.enhanced_sql,
                self.report
            )
        
        if self.iteration < self.MAX_ITERATION_LOOP:
            self.iteration += 1
            if "true" in decision or "True" in decision:
                print(f"## The decision has been made. Optimization  is terminated (iteration: {self.iteration}/{self.MAX_ITERATION_LOOP}) ##")
                self.current_state = "TERMINATED"
            else:
                print(f"## The decision was not approved. Further optimization is required (iteration: {self.iteration}/{self.MAX_ITERATION_LOOP}) ##")
                
                print("## Start a new round of complete iteration ## ")
                rag_knowledge = await Knowledge_Pool_Tool(self.enhanced_sql, self.optimization_advice)
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
                
                # 重新开始整个流程，重置所有状态
                self.parallel_reasoning_results = []
                self.parallel_verification_results = []
                self.current_state = "REASONING"
        else:
            print(f"## Reach the maximum number of iterations ({self.MAX_ITERATION_LOOP}),print Terminate optimization ##")
            self.enhanced_sql = self.initial_sql
            self.current_state = "TERMINATED"
            self.optimization_advice = "No need to optimize"




# 在每次保存JSON文件时，将终端输出保存到txt文件
def save_terminal_output_to_file(save_file_path, batch, original_stdout, temp_file):
    # 恢复标准输出
    sys.stdout = original_stdout
    temp_file.close()
    
    # 将临时文件的内容复制到最终文件
    with open(f"{save_file_path}/batch_{batch}.txt", "w") as f:
        with open("temp_output.txt", "r") as temp_f:
            f.write(temp_f.read())
    
    # 重新重定向标准输出到临时文件
    temp_file = open("temp_output.txt", "w")
    sys.stdout = temp_file
    return temp_file


                                                                                                                                                                                      
# 初始化运行示例
async def main():
    # tpch_s1
    # data_statistics = '[["region", "4"], ["nation", "24"], ["customer", "149999"], ["lineitem", "6001214"], ["orders", "1499999"], ["part", "199999"], ["partsupp", "799999"], ["supplier", "9999"]]'

    # tpch_s10
    data_statistics = '[["customer", "1499999"], ["lineitem", "59986051"], ["nation", "24"], ["orders", "14999999"], ["part", "1999999"], ["partsupp", "7999999"], ["region", "4"], ["supplier", "99999"]]'
    
    # tpch_s30
    # data_statistics = '[["region", "4"],["nation", "24"],["customer", "4499999"],["lineitem", "179998371"],["orders", "44999999"],["part", "5999999"],["partsupp", "23999999"],["supplier", "299999"]]'
    
    # tpcds
    # data_statistics = "[['call_center', '24'], ['catalog_page', '12000'], ['catalog_returns', '1439749'], ['catalog_sales', '14401261'], ['customer', '500000'], ['customer_address', '250000'], ['customer_demographics', '1920800'], ['date_dim', '73049'], ['dbgen_version', '1'], ['household_demographics', '7200'], ['income_band', '20'], ['inventory', '133110000'], ['item', '102000'], ['promotion', '500'], ['reason', '45'], ['ship_mode', '20'], ['store', '102'], ['store_returns', '2875432'], ['store_sales', '28800991'], ['time_dim', '86400'], ['warehouse', '10'], ['web_page', '200'], ['web_returns', '719217'], ['web_sales', '7197566'], ['web_site', '42']]"
    # dsb
    # data_statistics = "[['call_center', '24'], ['catalog_page', '12000'], ['customer_address', '250000'], ['customer_demographics', '1920800'], ['date_dim', '73049'], ['dbgen_version', '1'], ['household_demographics', '7200'], ['income_band', '20'], ['item', '102000'], ['reason', '45'], ['ship_mode', '20'], ['store', '102'], ['time_dim', '86400'], ['warehouse', '10'], ['web_site', '42'], ['catalog_returns', '1439749'], ['catalog_sales', '14401261'], ['inventory', '133110000'], ['promotion', '500'], ['web_page', '200'], ['web_returns', '719217'], ['web_sales', '7197566'], ['store_sales', '28800991'], ['customer', '500000'], ['store_returns', '2875432']]"
    # calcite
    # data_statistics = "[['BONUS', '29999999'], ['DEPT', '299999'], ['EMP_B', '29999999'], ['EMP', '29999999'], ['EMPNULLABLES_20', '55'], ['EMPNULLABLES', '29999999']]"
    # calcite_new
    
    schema_file = "/root/syy/QUITE/dataset/schemas/tpch_schema.sql"
    # schema_file = "./dsb_schema.sql"
    # schema_file = "./calcite_schema.sql"


    input_path ="/root/syy/machine1/query/tpch/tpch_hard.json"
    save_file_path = "/root/syy/code/QUITE/src/agent/output/tpch_hard" 
    count = 0
    batch = 0
    result = []
    MAX_ITERATION_LOOP = 2

    load_dotenv(dotenv_path='/root/syy/code/QUITE/config_file/.env')
    
    gpt = GPT(
        api_key=os.getenv("ASSISTANT_MODEL_API_KEY"),
        model=os.getenv("ASSISTANT_MODEL"),
        base_url=os.getenv("ASSISTANT_MODEL_URL")
    )
    dbms = DBMS()
    
    mq = MessageQueue(window_size=8)
    
    with open(input_path, "r") as f:
        data = json.load(f)
        
    fsm = SQLRewriteFSM(mq, gpt, dbms, data_statistics, schema_file, MAX_ITERATION_LOOP)


    for item in data:
        print("################################################################################")
        print(f"This is the {count}-th iteration")
        
        initial_sql = item["query"]

        print("Trying to rewrite the SQL query: ", initial_sql)
        
        fsm.initial_sql = initial_sql
        start_time = time.time()
        rewritten_sql = await fsm.run()
        end_time = time.time()
        rewrite_time = end_time - start_time
        print("Rewrite time costs: ", rewrite_time)
        tmp = {
            "id": item["id"],
            "original_query": item["query"],
            "rewritten_query": rewritten_sql,
            "time_cost": end_time - start_time,
            "rewrite_suggestion": fsm.optimization_advice
        }
        result.append(tmp)
        count += 1
        await fsm.clear()
        
        # 每3条保存一次
        if count % 1 == 0:  
            batch += 1
            json_file_name = f"{save_file_path}/batch_{batch}.json"
            txt_file_name = f"{save_file_path}/batch_{batch}.txt"
            with open(json_file_name, "w") as f:
                json.dump(result, f, indent=4)
            
            with open(txt_file_name, "w") as f:
                for r in result:
                    f.write(fsm.terminal_output)
                    f.write("\n")
                
            await fsm.clear_log()

            result = [] # 清空结果列表
    
    # 保存剩余结果
    if result:
        batch += 1
        with open(f"{save_file_path}/batch_{batch}.json", "w") as f:
            json.dump(result, f, indent=4)
        

if __name__ == "__main__":
    asyncio.run(main())


