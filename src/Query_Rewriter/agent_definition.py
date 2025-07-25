
from openai import OpenAI, AsyncOpenAI
from dotenv import load_dotenv
import json
import os
import re
import textwrap
import sys
import json
import textwrap
from typing import List, Dict, Set, Optional, Union
sys.path.append('../')
sys.path.append('./')

from src.utils.agent_template import MessageContent, Message, MemoryWindow, MessageQueue,  Agent
from src.utils.llm_client import GPT

from dotenv import load_dotenv

class ReasoningAgent(Agent):
    """MDP-based Reasoning Agent"""
    def __init__(self, mq: MessageQueue):
        super().__init__("ReasoningAgent", mq, gpt = GPT(
        api_key=os.getenv("REASONING_MODEL_API_KEY"),
        model=os.getenv("REASONING_MODEL"),
        base_url=os.getenv("REASONING_MODEL_URL")
        ))

        self.api_key = os.getenv("REASONING_MODEL_API_KEY")  # Get the API key from the environment variable
        self.model = os.getenv("REASONING_MODEL")
        self.base_url = os.getenv("REASONING_MODEL_URL")
        self.async_client = AsyncOpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )


    async def get_answer(self, prompt):
        reasoning_content = ""  # 
        is_answering = False   # 
        messages= []

        # messages.append({"role": "system", "content": "Initiate your response with '<think>\\n' at the beginning of every output."})
        messages.append(({"role": "user", "content": prompt}))

        completion = await self.async_client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True,
            temperature=0.0
        )

        async for chunk in completion:
            if not chunk.choices:
                if hasattr(chunk, 'usage') and chunk.usage:
                    print("\nUsage:")
                    print(chunk.usage)
            else:
                delta = chunk.choices[0].delta
                if hasattr(delta, 'reasoning_content') and delta.reasoning_content is not None:
                    print(delta.reasoning_content, end='', flush=True)
                    reasoning_content += delta.reasoning_content
                else:
                    if delta.content != "" and is_answering is False:
                        is_answering = True
                        break

        return reasoning_content
        
        
    async def analyze_sql(self, sql: str, data_statistics, explain_info : str) -> dict:

        prompt = textwrap.dedent(f"""
        <Mission>
        You are an experienced DBA, and your mission is to perform high-quality query rewriting for the user.
        1. Identify potential bottlenecks in the SQL query and propose optimization strategies. For each strategy, assign a rewrite score and determine the most efficient way to optimize the SQL.
            - Note: Consider creating CTEs when queries have complex WHERE/JOIN conditions or involve redundant subquery calculations, as CTEs can improve readability and performance. 
                    Avoid overusing CTEs if the query is simple or CTEs do not reduce redundancy, as unnecessary CTEs may add overhead.
        2. Rewrite the SQL query if necessary, ensuring the following standards are met for query rewriting:
            - Executability
            - Equivalence
            - Efficiency
            - Readability

        IMPORTANT:            
        If you find the SQL query is already well-optimized or too simple to require any changes, 
        you can simply mention the final version of the SQL query, conclude that it doesn't need further optimization, and include the word "TERMINATE" at the end of your response.
                                 
                                 
        <sql>
        {sql}

        <data_statistics>
        {data_statistics}

        <explain_info>
        {explain_info}
        """)
        
        thought_chain = await self.get_answer(
            prompt=prompt,
        )
        self.send_message(
            MessageContent(text=thought_chain),
            role="ReasoiningAgent",
            receiver="SummaryAgent"
        )

        return thought_chain

    

    async def analyze_sql_report(self, sql: str, data_statistics, report: dict, explain_info: str) -> dict: 

        prompt = textwrap.dedent(f"""
        <Mission>
        You are an experienced DBA, and your mission is to perform high-quality query rewriting for the user.
        1. Identify potential bottlenecks in the SQL query and propose optimization strategies. For each strategy, assign a rewrite score and determine the most efficient way to optimize the SQL.
            - Note: Consider creating CTEs when queries have complex WHERE/JOIN conditions or involve redundant subquery calculations, as CTEs can improve readability and performance. 
                    Avoid overusing CTEs if the query is simple or CTEs do not reduce redundancy, as unnecessary CTEs may add overhead.
        2. Rewrite the SQL query if necessary, ensuring the following standards are met for query rewriting:
            - Executability
            - Equivalence
            - Efficiency
            - Readability

        3. Notably, you will be provided with the preivous rewrite report.
                                 
        IMPORTANT:            
        If you find the SQL query is already well-optimized or too simple to require any changes, you can conclude that it doesn't need further optimization and then include the word "TERMINATE" at the end of your response.
                                 
        <sql>
        {sql}

        <data_statistics>
        {data_statistics}

        <explain_info>
        {explain_info}

        <report>
        {report}

        """)
        
        thought_chain = await self.get_answer(
            prompt=prompt,
        )
        self.send_message(
            MessageContent(text=thought_chain),
            role="ReasoiningAgent",
            receiver="SummaryAgent"
        )

        return thought_chain

    
class DecisionAgent(Agent):
    """Summarize Optimization Suggestions Agent"""
    def __init__(self, mq: MessageQueue):
        super().__init__("DecisionAgent", mq, gpt = GPT(
    api_key=os.getenv("DECISION_MODEL_API_KEY"),
    model=os.getenv("DECISION_MODEL"),
    base_url=os.getenv("DECISION_MODEL_URL")
))
        self.watch(["ReasoningAgent", "ExplainAgent"])
    

    async def summarize_chain(self, chain: str, original_sql: str, data_statistics) -> dict:
        prompt = textwrap.dedent(f"""
        <Mission>
        You are an experienced database administrator. Your mission is to
        1. Summarize the rewrite suggestions and the newly rewritten SQL query based on the detailed SQL rewrite report from [chain].
        Each suggestion should be grouped under one of the following categories:
        - Predicate_simplification
        - Subquery_optimization
        - Query_optimization
        - Join_optimization
        - Constant_folding
                                 
        These messages should be output with "produced_sql" and "advice" in the format provided. The original SQL query will be provided in <original_sql>.

        2. Then check the "produced_sql", try to find more potential rewritten improvement, try to futher improve it meanwhile keep equivalence ( like Early Filtering Conditions in FROM part as JOIN, make the CTE structure more efficient with maintaining the filter condition in main query, constant folding or calculate the date/num, redundant predicate siplification, etc.) 
        
        
        In this stage, you can also consider the data_statistics to make the SQL more efficient. 
        Especially if you want to create CTE. 
                                 
        Do not always consider creating CTEs, especially when there are numerous WHERE/JOIN conditions or when there are fewer redundant subquery calculations.
        {data_statistics} 

        These message can be outputed with "analysis" and "enhanced_sql" in [format]. If the SQL is well down or too easy to give a rewrite process, no need to optimize, just put [produced_sql] into [enhanced_sql] and [advice] into [analysis].
        Note that do not contain annotation in the SQL, and try to avoid to make to many exchanges.
                                 

        3. please strictly follow the format provided below:
        [format]
        </produced_sql>
        ```sql
                                 
        ```
        </produced_sql>
        
        </advice>
        [
                {{
                    "group": "",
                    "produced_suggestion": ""
                }},
                ... // if more suggestion is available
        ]
        </advice>
                                 
        </analysis>
        // The analysis of the rewritten SQL statement
        </analysis>
        
        </enhanced_sql>
        ```sql
                                 
        ```
        </enhanced_sql>
                                 

        [chain]
            {chain} 

        [oringal_sql]
            {original_sql}
        """)
        
        response = await self.llm.get_LLM_response_async(
            prompt=prompt,
            json_format= False
        )
        return response 
    

    async def check_equivalence(self, ori_sql: str, rewritten_sql: str, rewrite_advice) -> dict:
        prompt = textwrap.dedent(f"""
        You are an experienced database administrator. 
        1. Your mission is to check the equivalence of the original SQL and the improved SQL. If you think the improved SQL is not equivalent to the original SQL, please provide the corrected SQL.
        2. And you have the rewritte idea process to be considered to make the SQL more efficient.         Note that do not contain annotation in the SQL, and try to avoid to make to many exchanges.

        <original_sql>:
        {ori_sql}

        <rewritten_sql>:
        {rewritten_sql}

        <rewritten_idea_process>:
        {rewrite_advice}
        3. please strictly follow the format provided below:
        [format]
        </analysis>

        </analysis>
        
        </equivalence>
            // True/False
        </equivalence>
        
        </corrected_sql>
          // If not equivalent, insert the corrected SQL here; otherwise leave empty.
        </corrected_sql>
        """)
        
        response = await self.llm.get_LLM_response_async(
            prompt=prompt,
            json_format=False
        )
        return response
    
    async def select_sql(self, original_sql:str, query_pairs:list) -> dict:
        prompt = textwrap.dedent(f"""
        You are an experienced database administrator. 
        You have been provided with multiple SQL statements that are equivalent to the original SQL query, and each ehanced SQL statement has its own rewrite process.
        Your mission is to select the most effective enhanced SQL statement. 
        
        The SQL statements are provided below:
        <original_sql>:
        {original_sql}
        <enhanced_sql_pairs>:
        {query_pairs}
        
        Please strictly follow the format provided below:
        [format]
        </analysis>
            // Fill in the analysis of the selected SQL statement.
        </analysis>
        </selected_id>
            // Fill in the selected id you think is the best one.
        </selected_id>
        """)
        
        response = await self.llm.get_LLM_response_async(
            prompt=prompt,
            json_format=False
        )
        return response

    
    async def evaluate(self, ori_sql: str, enhanced_sql: str, report: str) -> dict:
        prompt = textwrap.dedent(f"""
        You are responsible for evaluating whether SQL optimization is up to standard.Please decide whether to terminate the optimization process based on the information below:
        Do you want to terminate the process?

        * Note: Execution times for <original_sql> and <enhanced_sql> come from the database optimizer and may be imprecise. Base your decision on a detailed analysis.
        * Objectively assess whether the enhanced SQL satisfies the key indicators of a successful rewrite.

        TERMINATION CONDITIONS:
        [True]:
            1. enhanced_sql execution time < ori_sql execution time, and enhanced_sql executes without errors.
            2. enhanced_sql execution time ≥ ori_sql execution time due to cardinality estimation inaccuracies, but you still consider the rewrite an improvement.

        [False]:
            enhanced_sql execution time ≥ ori_sql execution time, or enhanced_sql fails to execute without errors.

        Return your answer strictly in this JSON format:
        {{
            "terminate": True/False,
            "reason": ""  // Provide your rationale here.
        }}

        <original_sql>:
        {ori_sql}

        <enhanced_sql>:
        {enhanced_sql}

        <report>:
        {report}
        """)
        
        response = await self.llm.get_LLM_response_async(
            prompt=prompt,
            json_format=False
        )
        return response

    
    def extract_advice_content(self, text: str) -> str:
        """
        Extract content between </advice> and </advice> tags.
        """
        pattern = r'</advice>\s*(.*?)\s*</advice>'
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return json.loads(match.group(1).strip())
        return ""
    
    def extract_selected_id_content(self, text: str) -> str:
        """
        Extract content between </selected_id> and </selected_id> tags.
        """
        pattern = r'</selected_id>\s*(.*?)\s*</selected_id>'
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return json.loads(match.group(1).strip())
        return ""
    

    def extract_sql_candidate_content(self, text: str) -> str:
        """
        Extract content between </sql_candidate> and </sql_candidate> tags.
        """
        # 首先尝试匹配带```sql的格式
        pattern1 = r'</sql_candidate>\s*```sql\s*(.*?)\s*```\s*</sql_candidate>'
        match1 = re.search(pattern1, text, re.DOTALL)
        if match1:
            return match1.group(1).strip()
        
        # 尝试匹配不带```的格式
        pattern2 = r'</sql_candidate>\s*(.*?)\s*</sql_candidate>'
        match2 = re.search(pattern2, text, re.DOTALL)
        if match2:
            sql_content = match2.group(1).strip()
            sql_content = re.sub(r'^```sql\s*', '', sql_content)
            sql_content = re.sub(r'\s*```$', '', sql_content)
            return sql_content.strip()
        
        print(f"Warning: Could not extract SQL candidate from response")
        return ""

    def extract_enhanced_sql_content(self, text: str) -> str:
        """
        Extract content between </enhanced_sql> and </enhanced_sql> tags.
        """
        # 首先尝试匹配带```sql的格式
        pattern1 = r'</enhanced_sql>\s*```sql\s*(.*?)\s*```\s*</enhanced_sql>'
        match1 = re.search(pattern1, text, re.DOTALL)
        if match1:
            return match1.group(1).strip()
        
        # 尝试匹配不带```的格式
        pattern2 = r'</enhanced_sql>\s*(.*?)\s*</enhanced_sql>'
        match2 = re.search(pattern2, text, re.DOTALL)
        if match2:
            sql_content = match2.group(1).strip()
            sql_content = re.sub(r'^```sql\s*', '', sql_content)
            sql_content = re.sub(r'\s*```$', '', sql_content)
            return sql_content.strip()
        
        print(f"Warning: Could not extract enhanced SQL from response")
        return ""
    
    def extract_equivalence_content(self, text: str) -> str:
        """
        Extract content between </equivalence> and </equivalence> tags.
        """
        pattern = r'</equivalence>\s*(.*?)\s*</equivalence>'
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return ""
    
    def extract_corrected_sql_content(self, text: str) -> str:
        """
        Extract content between </corrected_sql> and </corrected_sql> tags.
        Support multiple formats: code blocks with ```sql and plain text without.
        """
        # First, try to match the format with ```sql
        pattern1 = r'</corrected_sql>\s*```sql\s*(.*?)\s*```\s*</corrected_sql>'
        match1 = re.search(pattern1, text, re.DOTALL)
        if match1:
            return match1.group(1).strip()

        # If no match is found, try to match the plain text format without ```
        pattern2 = r'</corrected_sql>\s*(.*?)\s*</corrected_sql>'
        match2 = re.search(pattern2, text, re.DOTALL)
        if match2:
            sql_content = match2.group(1).strip()
            # Remove any ```sql markers
            sql_content = re.sub(r'^```sql\s*', '', sql_content)
            sql_content = re.sub(r'\s*```$', '', sql_content)
            return sql_content.strip()
        
        print(f"Warning: Could not extract corrected SQL from response: {text[:200]}...")
        return ""

    async def merge_advice(self, base_sql: str, optimizations: List[str], rag_optimizations: List[str]) -> str:
        """Merge optimization suggestions into SQL"""
        optimizations_str = [
            json.dumps(opt) if isinstance(opt, dict) else str(opt)
            for opt in optimizations
        ]
        prompt = textwrap.dedent(f"""
        You are an experienced database administrator. Your mission is to merge the RAG optimizations from expert knowledge into the original optimization suggestions and return the final rewrite suggestions.
        Carefully consider the validity of both the original optimization suggestions and the RAG optimizations, and return the result in the format below.

        The original SQL statement:
        {base_sql}

        Original optimization suggestions:
        {optimizations_str}

        RAG optimizations from expert knowledge:
        {rag_optimizations}

        You must return the JSON in the following format:
        {{
            {{
                "group": "",
                "produced_suggestion": ""  // merged suggestions
            }}
        }}
        """)
        response = await self.llm.get_LLM_response_async(
            prompt=prompt,
            json_format=False
        )
        # return self._extract_sql(response)
        return response
    
    def retrieve_reasoning_chain(self) -> str:
        """Retrieve reasoning chain from message queue"""
        messages = self.retrieve_memories(k=1)
        return [msg.content.text for msg in messages if msg.content and msg.content.text]


class AssistantAgent(Agent):
    """Execution Plan Analysis Agent"""
    def __init__(self, mq: MessageQueue):
        super().__init__("AssistantAgent", mq, gpt = GPT(
    api_key=os.getenv("ASSISTANT_MODEL_API_KEY"),
    model=os.getenv("ASSISTANT_MODEL"),
    base_url=os.getenv("ASSISTANT_MODEL_URL")
))
    
    def extract_corrected_sql_content(self, text: str) -> str:
        """
        Extract content between </corrected_sql>```sql and ```</corrected_sql> tags.
        """
        pattern = r'</corrected_sql>\s*```sql\s*(.*?)\s*```\s*</corrected_sql>'
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return ""
    
    async def _correct_sql(self, original_sql: str, rewritten_sql: str, error: str) -> str:
        """Correct SQL syntax errors"""
        prompt = textwrap.dedent(f"""
            You are an expert in SQL syntax and excel at correcting SQL syntax errors.
            Please fix the following SQL statement, using the error message provided.

            * Note: If the SQL contains double quotes, preserve them exactly as they appear.
            <rewritten_sql>
            {rewritten_sql}

            Error message:
            {error}

            Below is the original form of the rewritten SQL for reference to the schema.
            Only correct the syntax in <rewritten_sql>; do not align it with the original SQL,
            and do NOT include any "EXPLAIN (FORMAT JSON)" clause!

            <original_sql>
            {original_sql}

            Please follow the format below exactly:
            [format]
            </analysis>

            </analysis>

            </corrected_sql>
            // Insert the corrected SQL here.
            </corrected_sql>
            """)

        
        response = await self.llm.get_LLM_response_async(
            prompt=prompt
        )
        
        corrected_sql = self.extract_corrected_sql_content(response)
        return corrected_sql
    
    def extract_analysis_content(self, text: str) -> str:
        """
        Extract content between </analysis> and </analysis> tags.
        """
        print(text)
        if text is None:
            print("Error: text is None")
            return None
        pattern = r'</analysis>\s*(.*?)\s*</analysis>'
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()#  match.group(1).strip()
        return ""

    
    async def  generate_report(self, ori_explain_result: list, re_explain_result: list, imp_explain_result: list) -> str:
        prompt = textwrap.dedent(f"""
        <Mission>
        You are a professional database administrator. Your mission is to generate a detailed report based on the original EXPLAIN analysis, the rewritten EXPLAIN analysis, and the enhanced EXPLAIN analysis.
        You should consider and compare them with a report that contains these parts:
        

        1. Cost Efficiency:
            - Overall cost change percentage  
            - Cost change at the most expensive plan node  

        2. Plan Characteristics:
            - Scan type transitions (e.g., Seq Scan → Index Scan)  
            - Join algorithm refinements (e.g., Hash Join → Merge Join)  
            - Elimination of explicit sorting and reduction of intermediate result sets   
                                 
        3. Resource Utilization:
            - Memory usage (changes in Hash/Buffer nodes)
            - Worker count adjustment
        
        4. Other Improvements:
                                 

        Note that in your report, there is no need to copy the EXPLAIN result one more, just analyze and compare them in NLP.
                                 
        Your answer should follow the format below:
        </analysis>
            ...
        </analysis>
                                 
        </report>
            ... // Do not need to remention the EXPLAIN result
        </report>
                                                      
        <ori_explain_result>
        {ori_explain_result}

        <re_explain_result>
        {re_explain_result}

        <imp_explain_result>
        {imp_explain_result}

        """)
        return await self.llm.get_LLM_response_async(
            prompt=prompt
        )


