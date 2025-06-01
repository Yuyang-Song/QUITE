
from openai import OpenAI
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
sys.path.append('../utils')
sys.path.append('./')
from utils.agent_template import MessageContent, Message, MemoryWindow, MessageQueue,  Agent
from utils.gpt_request import GPT

from dotenv import load_dotenv
load_dotenv(dotenv_path='/root/syy/MARter_5/config_file/.env')  # Load environment variables from .env file, here is the running path

class ReasoningAgent(Agent):
    """SQL重写推理Agent"""
    def __init__(self, mq: MessageQueue, gpt: GPT):
        super().__init__("ReasoningAgent", mq, gpt)
        
        
        self.api_key = os.getenv("REASONING_MODEL_API_KEY")  # Get the API key from the environment variable
        self.model = os.getenv("REASONING_MODEL")
        # self.api_key = api_key # Get the API key from the environment variable
        # self.model = model
        self.base_url = os.getenv("REASONING_MODEL_URL")
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )

    # async def get_answer(self, prompt):
    #     messages= []
    #     result_content = ""
    #     chain_content = ""
    #     # messages.append({"role": "system", "content": "Initiate your response with '<think>\\n' at the beginning of every output."})
    #     messages.append(({"role": "user", "content": prompt}))

    #     completion = self.client.chat.completions.create(
    #         model=self.model,
    #         messages=messages,
    #         stream=True,
    #         # response_format={'type': 'json_object'} if json_format else None,
    #         temperature=0.0
    #     )
    #     # Loop over the streamed chunks
    #     for chunk in completion:
    #         if not chunk.choices:
    #             continue
            
    #         # Check if reasoning_content exists
    #         reasoning_content = getattr(chunk.choices[0].delta, 'reasoning_content', None)
    #         if reasoning_content:
    #             chain_content += reasoning_content
    #             print(reasoning_content, end="")
            
    #         # Check if content exists
    #         content = getattr(chunk.choices[0].delta, 'content', None)
    #         if content:
    #             result_content += content
    #             print(content, end="")

    #     # return completion.choices[0].message.content, completion.choices[0].message.reasoning_content
    #     return result_content,chain_content

    async def get_answer(self, prompt):
        reasoning_content = ""  # 
        answer_content = ""     # 
        is_answering = False   # 
        messages= []

        # messages.append({"role": "system", "content": "Initiate your response with '<think>\\n' at the beginning of every output."})
        messages.append(({"role": "user", "content": prompt}))

        completion = self.client.chat.completions.create(
        model=self.model,
        messages=messages,
        stream=True,
        # response_format={'type': 'json_object'} if json_format else None,
        temperature=0.0
    )

        for chunk in completion:
            # chunk.choicesusage
            if not chunk.choices:
                print("\nUsage:")
                print(chunk.usage)
            else:
                delta = chunk.choices[0].delta
                # 
                if hasattr(delta, 'reasoning_content') and delta.reasoning_content != None:
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
            - Note: Do not always consider creating CTEs, especially when there are numerous WHERE/JOIN conditions or when there are fewer redundant subquery calculations.
        2. Rewrite the SQL query if necessary, ensuring the following standards are met for query rewriting:
            - Executability
            - Equivalence
            - Efficiency
            - Readability

        IMPORTANT:            
        If you find the SQL query is already well-optimized or too simple to require any changes, 
        you can simply mention the final version of the SQL query, conclude that it doesn’t need further optimization, and include the word "TERMINATE" at the end of your response.
                                 
                                 
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
        #         MessageContent(text="需要分析2龄分布"), 
        #         role="Engineer",
        #         receiver="DataAnalyst"
        # 发送消息
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
            - Note: Do not always consider creating CTEs, especially when there are numerous WHERE/JOIN conditions or when there are fewer redundant subquery calculations.
        2. Rewrite the SQL query if necessary, ensuring the following standards are met for query rewriting:
            - Executability
            - Equivalence
            - Efficiency
            - Readability

        3. Notably, you have been provided with the preivous rewrite report.
            - "pre_rewrite_sql": previous rewritten SQL query
            - "decision": Decisions made in the previous iteration
            - "corrected_guide_knowledge": revised rewrite guide knowledge


        IMPORTANT:            
        If you find the SQL query is already well-optimized or too simple to require any changes, 
        you can simply mention the final version of the SQL query, conclude that it doesn’t need further optimization, and include the word "TERMINATE" at the end of your response.
                                 
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
        #         MessageContent(text="需要分析2龄分布"), 
        #         role="Engineer",
        #         receiver="DataAnalyst"
        # 发送消息
        self.send_message(
            MessageContent(text=thought_chain),
            role="ReasoiningAgent",
            receiver="SummaryAgent"
        )

        return thought_chain


        # Stage1. If the rewritten SQL is equivalent to the original SQL or not.  If not, try to correct it. (little error like rows name error, predicate value error; big error like non-equivalence to original)           
        # Stage2. If the rewritten SQL has syntax error or not.  If not, try to correct it. (little error like rows name error, predicate value error; big error like non-equivalence to original)
class DecisionAgent(Agent):
    """总结优化建议Agent"""
    def __init__(self, mq: MessageQueue):
        super().__init__("DecisionAgent", mq, gpt = GPT(
    api_key=os.getenv("DECISION_MODEL_API_KEY"),
    model=os.getenv("DECISION_MODEL"),
    base_url=os.getenv("DECISION_MODEL_URL")
))
        self.watch(["ReasoningAgent", "ExplainAgent"])
    
        #     2. Then check the "ori_SQL" in two stages:  
        # Stage1. If the rewritten SQL is equivalent to the original SQL or not. If not, try to correct it. (little error like rows name error, predicate value error; big error like non-equivalence to original)
        # Stage2. If the rewritten SQL has another little potential rewritten improvement, try to futher improve it meanwhile keep equivalence ( like create CTE, make the CTE structure more efficient, considering constant folding or predicate optmization to make the sql more effcient)
        # Note that do not make the SQL too complex and redundancy, try to avoid to make to many exchanges.
        # These message can be outputed of "analysis" and "sql_candidate" in [format]

    async def summarize_chain(self, chain: str, original_sql: str, data_statistics) -> dict:
        # print("chain:",chain)
        prompt = textwrap.dedent(f"""
        <Mission>
        You are an experienced database administrator. Your mission is to
        1. Summarize the rewrite suggestions and the newly rewritten SQL query based on the detailed SQL rewrite report from [chain].
        Each suggestion should be grouped under one of the following categories:
        - Predicate_simplification
        - Query_optimization
        - Join_optimization
        - Constant_folding
        - Other
                                 
        These messages should be output with "sql_candidate" and "advice" in the format provided. The original SQL query will be provided in <original_sql>.

        2. Then check the "sql_candidate", try to find more potential rewritten improvement, try to futher improve it meanwhile keep equivalence ( like Early Filtering Conditions in FROM part as JOIN, make the CTE structure more efficient with maintaining the filter condition in main query, constant folding or calculate the date/num, redundant predicate siplification, etc.) 
        
        
        In this stage, you can also consider the data_statistics to make the SQL more efficient. 
        Especially if you want to need create CTE. 
                                 
        Note that you should not always make CTE to make the SQL more complex and redundancy, try to avoid to make too many exchanges especially in plenty of WHERE/JOIN conditions / less redundent subquery calculation situations. 
        {data_statistics} 

        These message can be outputed with "analysis" and "enhanced_sql" in [format]. If the SQL is well down or too easy to give a rewrite process, no need to optimize, just put [sql_candidatg] into [enhanced_sql] and [advice] into [analysis].
        Note that do not contain annotation in the SQL, and try to avoid to make to many exchanges.
                                 

        3. please strictly follow the format provided below:
        [format]
        </sql_candidate>
        ```sql
                                 
        ```
        </sql_candidate>
        
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
        
        response = await self.llm.get_GPT_response_async(
            prompt=prompt,
            json_format= False
        )
        return response 
    
    async def check_equivalence(self, ori_sql: str, rewritten_sql: str, rewrite_advice) -> dict:
        prompt = textwrap.dedent(f"""
        You are an experienced database administrator. 
        1. Your mission is to check the equivalence of the original SQL and the rewritten SQL. If you think the rewritten SQL is not equivalent to the original SQL, please provide the corrected SQL.
        2. And you have the rewritten proposals that describe the rewrite process.         
        3. If both are not equivalent, do not contain annotation in the corrected SQL, and try to avoid to make to many exchanges.

        * Note that If the SQL variable contains double quotes, do not ignore them and keep them as they are.
        <original_sql>: 
        {ori_sql}

        <rewritten_sql>:
        {rewritten_sql}

        <rewrite_idea_process>:
        {rewrite_advice}


        3. please strictly follow the format provided below:
        [format]
        </analysis>

        </analysis>
        
        </equivalence>
            // True/False
        </equivalence>
        
        </corrected_sql>
            // If the rewritten SQL is not equivalent to the original SQL, provide the corrected SQL here. Else, leave it empty.
        </corrected_sql>
        """)
        
        response = await self.llm.get_GPT_response_async(
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
        
        response = await self.llm.get_GPT_response_async(
            prompt=prompt,
            json_format=False
        )
        return response

    
    async def evaluate(self, ori_sql: str, enhanced_sql: str, report: str) -> dict:
        prompt = textwrap.dedent(f"""
            Please base your decision on the following information:
            Do you want to terminate the process?
            * Note that the execution time for rewritten sql and original sql is provided by the optimizer of the database, and this value is not very accurate in some cases. Please make decision based on your detailed analysis. 
            * Please objectively estimate whether the enhanced sql has completed the indicators of query rewrite.
                                 
            The TERMINATE condition:
            [True]: 
                1. If enhanced_sql execution time cost < ori_sql execution time cost,  and the enhanced_sql is executable without any errors.
                2. If enhanced_sql execution time >= ori_sql execution time cost as a result of inaccuracy cardinary estimation, but you think the rewritten sql has improvement compared to the original sql.
                                 
            [False]: 
                If the enhanced_sql execution time cost >= ori_sql execution time cost, or the enhanced_sql is not executable without any errors, then you should not terminate the process.
                                 

            * Note that the execution time for enhanced sql and original sql is provided by the optimizer of the database, and this value is not very accurate in some cases.!!!!!!                     
            Note that you must return the answer in the following format:
            {{  
                {{
                    "terminate":  True/False,
                    "reason": //Fill the reason 
                }}
            }}
            <original_sql>:
            {ori_sql}

            <enhanced_sql>:
            {enhanced_sql}

            <report>
            {report}

        """)
        
        response = await self.llm.get_GPT_response_async(
            prompt=prompt,
            system_message="You are responsible for evaluating whether SQL optimization is up to standard",
            json_format=False
        )
        return response

    
    def extract_advice_content(self, text: str) -> str:
        """
        提取文本中从 </advice> 到 </advice> 之间的内容。
        """
        pattern = r'</advice>\s*(.*?)\s*</advice>'
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return json.loads(match.group(1).strip())
        return ""
    
    async def extract_selected_id_content(self, text: str) -> str:
        """
        提取文本中从 </selected_id> 到 </selected_id> 之间的内容。
        """
        pattern = r'</selected_id>\s*(.*?)\s*</selected_id>'
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return json.loads(match.group(1).strip())
        return ""
    

    def extract_sql_candidate_content(self, text: str) -> str:
        """
        提取文本中从 </sql_candidate>```sql 到 ```</sql_candidate> 之间的内容。
        """
        pattern = r'</sql_candidate>\s*```sql\s*(.*?)\s*```\s*</sql_candidate>'
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return "" 

    def extract_enhanced_sql_content(self, text: str) -> str:
        """
        提取文本中从 </enhanced_sql>```sql 到 ```</enhanced_sql> 之间的内容。
        """
        pattern = r'</enhanced_sql>\s*```sql\s*(.*?)\s*```\s*</enhanced_sql>'
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return ""
    
    def extract_equivalence_content(self, text: str) -> str:
        """
        提取文本中从 </equivalence> 到 </equivalence> 之间的内容。
        """
        pattern = r'</equivalence>\s*(.*?)\s*</equivalence>'
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return ""
    
    def extract_corrected_sql_content(self, text: str) -> str:
        """
        提取文本中从 </corrected_sql>```sql 到 ```</corrected_sql> 之间的内容。
        """
        pattern = r'</corrected_sql>\s*```sql\s*(.*?)\s*```\s*</corrected_sql>'
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return ""

    async def merge_advice(self, base_sql: str, optimizations: List[str], rag_optimizations: List[str]) -> str:
        """合并优化建议到SQL"""
        optimizations_str = [
            json.dumps(opt) if isinstance(opt, dict) else str(opt)
            for opt in optimizations
        ]
        prompt = textwrap.dedent(f"""
        You are an experienced database administrator. Your mission is to merge the rag_optmizations from expert knowledge into original optimizations, and return the final rewrite suggestions. 、
        Carefully condier the ground truth of the original optimization suggestions and rag suggestions and return the answer in the format below.
        
        The original SQL statement is provided below:
        {base_sql}

        The original optimization suggestions:
        {optimizations_str}
        
        The rag_optimizations from expert knowledge:
        {rag_optimizations}        
        
        You must return the json format as bellow:
        {{
            {{
                "group": "",
                "produced_suggestion": ""  //merged suggestions
            }}
        }}                         
        
        """)
        response = await self.llm.get_GPT_response_async(
            prompt=prompt,
            system_message="You are proficient in translating optimization suggestions into actual SQL rewriting",
            json_format=False
        )
        # return self._extract_sql(response)
        return response
    
    def retrieve_reasoning_chain(self) -> str:
        """从消息队列获取推理链"""
        messages = self.retrieve_memories(k=1)
        return [msg.content.text for msg in messages if msg.content and msg.content.text]


class AssistantAgent(Agent):
    """执行计划分析Agent"""
    def __init__(self, mq: MessageQueue, gpt: GPT):
        super().__init__("AssistantAgent", mq, gpt)
        self.watch(["SummaryAgent"])
    
    async def extract_corrected_sql_content(self, text: str) -> str:
        """
        提取文本中从 </corrected_sql>```sql 到 ```</corrected_sql> 之间的内容。
        """
        pattern = r'</corrected_sql>\s*```sql\s*(.*?)\s*```\s*</corrected_sql>'
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return ""
    
    async def _correct_sql(self, original_sql: str, rewritten_sql: str, error: str) -> str:
        """修正SQL语法错误"""
        prompt = textwrap.dedent(f"""
        You are an expert in SQL syntax and are good at fixing SQL syntax errors. 
        Please help fix the following SQL statement with the error message provided.
                                 
        * Note that If the SQL variable contains double quotes, do not ignore them and keep them as they are.
        <rewritten_sql>
        {rewritten_sql}
        
        error message: {error}

        and the following sql is the original format of the rewritten SQL, you can read it to know about the original schema info.
        Notice that you should only correct the rewritten_sql syntax error, do not make it similar to original sql, and DO NOT CONTAIN "EXPLAIN (FORMAT JSON)" PART  !!!
        
        <original_sql>
        {original_sql}

        please strictly follow the format provided below:
        [format]
        </analysis>

        </analysis>
    
        </corrected_sql>
            // Fill in the corrected SQL here.
        </corrected_sql>

        """)
        
        response = await self.llm.get_GPT_response_async(
            prompt=prompt
        )
        
        corrected_sql = await self.extract_corrected_sql_content(response)
        return corrected_sql
    
    async def extract_analysis_content(self, text: str) -> str:
        """
        提取文本中从 </analysis> 到 </analysis> 之间的内容。
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

    
    async def  generate_report(self, ori_explain_result: list,  imp_explain_result: list) -> str:
        prompt = textwrap.dedent(f"""
        <Mission>
        You are a professional database administrator. Your mission is to generate a detailed report based on the original EXPLAIN analysis, and the rewritten EXPLAIN analysis.
        You should consider and compare them with a report that contains these parts:
        

        1. Cost Changes:
         - Total cost change percentage
         - Cost change of the most expensive node
        
        2. Execution Strategy Changes:
         - Scan type improvement (Seq Scan -> Index Scan)
         - Join algorithm optimization (Hash Join -> Merge Join)
         - Parallelism adjustment
        
        3. Resource Consumption Changes:
         - Memory usage (changes in Hash/Buffer nodes)
         - Worker count adjustment
        
        4.Improved Filtering Efficiency:
         - Increased accuracy of post-filter row estimates
         - Predicate pushdown scenarios
        
        5. Key Optimization Indicators:
         - Elimination of explicit sorting
         - Reduction of intermediate result sets
         - Improved parallelism utilization
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

        <rew_explain_result>
        {imp_explain_result}

        """)
        return await self.llm.get_GPT_response_async(
            prompt=prompt
        )


