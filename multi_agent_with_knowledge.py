import os
import json
import textwrap
import sys
from dotenv import load_dotenv
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
load_dotenv(dotenv_path='./config_file/.env')
from utils.gpt import GPT
from concurrent.futures import ThreadPoolExecutor, as_completed
import asyncio
import time
import textwrap
import json

class MultiAgentSQLRewriter:
    def __init__(self, input_sql = None):
        self.input_sql = input_sql
        self.gpt = GPT()
        self.money = 0.0
        self.chat_history = []
        self.iteration_history = []

    async def agent_a_analysis(self):
        # 使用大模型分析 SQL（Agent A 的职责）
        prompt = textwrap.dedent(f"""
            <mission>
            You are Agent A, suppose you are an experenced DBA, and your role is a SQL Analyzer. Your task is to analyze the SQL query and identify potential performance bottlenecks to make the execution time of the sql faster and less costy. Provide suggestions on how to optimize the query.
            
            Let's think about this questions step by step.
            <steps>
            0. Read the original sql to be rewritten from the <input_sql>. 
            1. Read the rewrite history if the <rewrite_history is not empty. If it is not empty, you should consider the last rewritten sql as the <original_sql>.
            2. Analyze the SQL query and identify potential performance bottlenecks.
            3. Given a binary judgement on whether the SQL query is optimized or not. If you think the sql is able to rewrite, Fill "True" in the <is_optimized>. If you think the sql is unable to rewrite, Fill "False" in the <is_optimized>. 
            4. Given the candidate optimization suggestions based on your analysis. Make your suggestions clear and concise. If <is_optimized> is "True", you can provide some suggestions to optimize the SQL query. If <is_optimized> is "False", Fill this field with "None".
            5. Return your response based on the <json_formate_templete>.
            
            <input_sql>
            {self.input_sql}
            

            <json_format_templete>
            {{
                "agent_candidate_sql": {{candidate_sql}},  // Fill this 'candidate_sql' with the candidate SQL query. Note that if the chat history is not empty, you should consider the last rewritten sql as the candidate SQL.
                "is_optimized": {{True/False}},  // Fill this 'is_optimized' with your judgement.
                "agent_analysis": {{analysis}},  // Fill this 'analysis' with the analysis details of the SQL query.
                "agent_suggestions": {{suggestions}}  // Fill this 'suggestions'with the optimization suggestions. If <is_optimized> is "True", you can provide some suggestions to optimize the SQL query. If <is_optimized> is "False", Fill this field with "None".
            }}
        """)
        response = await self.gpt.get_GPT_response_async(prompt, json_format=True)
        self.chat_history.append({"Agent A": response})
        self.chat_history.append("###############################################################################")
        self.money += self.gpt.calc_money(prompt,response)
        # print(self.chat_history)
        return response

    async def agent_a_analysis_with_knowledge(self,knowledge):
        # 使用大模型分析 SQL（Agent A 的职责）
        prompt = textwrap.dedent(f"""
            <mission>
            You are Agent A, suppose you are an experenced DBA, and your role is a SQL Analyzer. Your task is to analyze the SQL query and identify potential performance bottlenecks to make the execution time of the sql faster and less costy. Provide suggestions on how to optimize the query. You have been provided with the following knowledge that may can help you to analyze the SQL query.
            
            Let's think about this questions step by step.
            <steps>
            0. Read the original sql to be rewritten from the <input_sql> and the knwoledge provided from the <knowledge>.
            1. Read the rewrite history if the <rewrite_history is not empty. If it is not empty, you should consider the last rewritten sql as the <original_sql>.
            2. Analyze the SQL query and identify potential performance bottlenecks.
            3. Given a binary judgement on whether the SQL query is optimized or not. If you think the sql is able to rewrite, Fill "True" in the <is_optimized>. If you think the sql is unable to rewrite, Fill "False" in the <is_optimized>. 
            4. Given the candidate optimization suggestions based on your analysis. Make your suggestions clear and concise. If <is_optimized> is "True", you can provide some suggestions to optimize the SQL query. If <is_optimized> is "False", Fill this field with "None".
            5. Return your response based on the <json_formate_templete>.
            
            <input_sql>
            {self.input_sql}
            
            <knowledge>
            {knowledge}

            <json_format_templete>
            {{
                "agent_candidate_sql": {{candidate_sql}},  // Fill this 'candidate_sql' with the candidate SQL query. Note that if the chat history is not empty, you should consider the last rewritten sql as the candidate SQL.
                "is_optimized": {{True/False}},  // Fill this 'is_optimized' with your judgement.
                "agent_analysis": {{analysis}},  // Fill this 'analysis' with the analysis details of the SQL query.
                "agent_suggestions": {{suggestions}}  // Fill this 'suggestions'with the optimization suggestions. If <is_optimized> is "True", you can provide some suggestions to optimize the SQL query. If <is_optimized> is "False", Fill this field with "None".
            }}
        """)
        response = await self.gpt.get_GPT_response_async(prompt, json_format=True)
        self.money += self.gpt.calc_money(prompt,response)
        self.chat_history.append({"Agent A": response})
        self.chat_history.append("###############################################################################")
        # print(self.chat_history)
        return response

    async def agent_b_rewrite(self, analysis_response):
        # 使用大模型重写 SQL（Agent B 的职责）
        print("-----------------------------------------------------------------------------")
        print(f"{analysis_response}")
        print("-----------------------------------------------------------------------------")
        prompt = textwrap.dedent(f"""
            <mission>
            You are Agent B, a SQL Rewriter. Based on the analysis and suggestions provided by Agent A, your task is to rewrite the SQL query to optimize its performance.
            You MUST strictly follow Agent A's suggestions to rewrite the query. Ensure all suggested optimizations are applied.

            Let's think about this step by step.
            
            <steps>
            0. Read the agent A's analysis response from the <analysis_response>. Understand the candidate SQL and suggestions provided by Agent A. 
            1. Rewrite the Candidate SQL based on the suggestions provided by Agent A.
            2. Ensure that you apply the suggestions provided by Agent A, including explicit joins, indexing recommendations, and corrections to the date range condition.
            3. Make sure your rewrite process does not contain any syntax errors or semantic errors.
            4. Return your response based on the <json_format_template>.

            <agent_a_analysis>
            {analysis_response}

            <json_format_template>
            {{
                "agent_candidate_sql": {{candidate_sql}},  // Fill this 'candidate_sql' with the candidate SQL query from the <agent_a_analysis>.
                "agent_rewritten_sql": {{rewritten_sql}},  // Fill this 'rewritten_sql' with the rewritten SQL query based on Agent A's suggestions.
                "agent_explanation": {{explanation}}  // Fill this 'explanation' with the explanation of the rewrite process.
            }}
        """)
        response = await self.gpt.get_GPT_response_async(prompt, json_format=True)
        self.money += self.gpt.calc_money(prompt,response)
        self.chat_history.append({"Agent B": response})
        self.chat_history.append("###############################################################################")
        print(self.chat_history)
        return response

    async def agent_c_summary(self,agent_a_response, agent_b_response):
        # 使用大模型总结 Agent A 和 Agent B 的对话（Agent C 的职责）
        prompt = textwrap.dedent(f"""
            <mission>
            You are Agent C, responsible for summarizing the conversation between Agent A and Agent B, and providing a concise history summary to compress the chat history.
            Let's think about this questions step by step.
            
            1. Read the chat history between Agent A and Agent B.
            2. Provide a concise summary of the conversation between Agent A and Agent B.
            3. Return your response based on the <json_formate_templete>.
            
            <chat_history>
            [agent_a_response]
            {agent_a_response}
            [agent_b_response]
            {agent_b_response}
            
            <json_format_templete>
            {{
                "agent_candidate_sql": {{candidate_sql}},  // Fill this 'candidate_sql' with the candidate SQL query.
                "agent_analysis": {{analysis}},  // Fill this 'analysis' with the analysis details of the SQL query.
                "agent_rewritten_sql": {{rewritten_sql}},  // Fill this 'rewritten_sql' with the rewritten SQL query.
            }}
        """)
        response = await self.gpt.get_GPT_response_async(prompt, json_format=True)
        self.money += self.gpt.calc_money(prompt,response)
        self.iteration_history.append(response)  # 将总结存入历史记录
        print(self.iteration_history)
        self.chat_history.clear()  # 清除当前的聊天记录，准备下一轮迭代
        return response

    # def pipeline(self,iteration):
    #     # 执行一次迭代过程，依次调用 Agent A, B 和 C
    #     result = {}
    #     for i in range(iteration):
    #         agent_a_response = self.agent_a_analysis()
    #         # if agent_a_response["is_optimized"] == "False":
    #         #     return {
    #         #         "Original SQL": self.input_sql,
    #         #         "Rewritten SQL": self.input_sql,
    #         #         "agent_analysis": agent_a_response["agent_analysis"],
    #         #     }
    #         agent_b_response = self.agent_b_rewrite(agent_a_response)
    #         summary = self.agent_c_summary(agent_a_response, agent_b_response)

    #         result = {
    #             "original_query": summary["agent_candidate_sql"],
    #             "rewritten_query": summary["agent_rewritten_sql"],
    #             "agent_analysis": summary["agent_analysis"],
    #         }
    #     print(f"Iteration {iteration} completed.")
    #     # print(f"result: {result}\n")
    #     return result
    
    async def pipeline_with_knowledge(self,iteration,input_sql,knowledge):
        # 执行一次迭代过程，依次调用 Agent A, B 和 C
        result = {}
        for i in range(iteration):
            # agent_a_response = self.agent_a_analysis()
            # if agent_a_response["is_optimized"] == "False":
            #     return {
            #         "Original SQL": self.input_sql,
            #         "Rewritten SQL": self.input_sql,
            #         "agent_analysis": agent_a_response["agent_analysis"],
            #     }
            # agent_b_response = self.agent_b_rewrite(agent_a_response)
            # summary = self.agent_c_summary(agent_a_response, agent_b_response)
            # 确保调用异步函数时使用 await
            if i == 0:
                agent_a_response = await self.agent_a_analysis_with_knowledge(knowledge)
            else:
                agent_a_response = await self.agent_a_analysis()
            agent_b_response = await self.agent_b_rewrite(agent_a_response)
            summary = await self.agent_c_summary(agent_a_response, agent_b_response)

            result = {
                "original_query": input_sql,
                "rewritten_query": summary["agent_rewritten_sql"],
                "agent_analysis": summary["agent_analysis"],
            }
        print(f"Iteration {iteration} completed.")
        # print(f"result: {result}\n")
        return result

# 示例调用：
# input_sql = "select nation, o_year, sum(amount) as sum_profit from ( select n_name as nation, extract(year from o_orderdate) as o_year, l_extendedprice * (1 - l_discount) - ps_supplycost * l_quantity as amount from part,supplier,lineitem,partsupp,orders,nation where s_suppkey = l_suppkey and ps_suppkey = l_suppkey and ps_partkey = l_partkey and p_partkey = l_partkey and o_orderkey = l_orderkey and s_nationkey = n_nationkey and p_name like '%green%' ) as profit group by nation, o_year order by nation, o_year desc;"
# multi_agent = MultiAgentSQLRewriter(input_sql)
# iteration = 2
# result_data = multi_agent.pipeline(iteration)
# print(json.dumps(result_data, indent=4))
    async def process_query(self, query_data):
        input_sql = query_data["query"]
        self.input_sql = input_sql
        iteration = 2
        result_data = await self.pipeline(iteration, input_sql)  # 使用 await 执行异步 pipeline
        return result_data

    async def process_queries_in_parallel(self, input_sql_file, output_sql_file, max_workers=5):
        with open(input_sql_file, 'r') as file:
            data = json.load(file)
        
        results = []
        # 使用 asyncio 的线程池并行执行任务
        tasks = [self.process_query(query_data) for query_data in data]
        # 使用 asyncio.gather 来并行处理所有任务
        results = await asyncio.gather(*tasks)

        # 异步保存结果
        await self.save_results(output_sql_file, results)

    async def save_results(self, output_sql_file, results):
        # 使用异步方式保存结果到文件
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self._write_to_file, output_sql_file, results)

    def _write_to_file(self, output_sql_file, results):
        with open(output_sql_file, 'w') as output_file:
            json.dump(results, output_file, indent=4)
        print(f"Experiment results appended to {output_sql_file}")


if __name__ == "__main__":
    input_sql_file = "./query_template/case/parallel_test.json"
    output_sql_file = "./query_template/case/result_parallel_test.json"
    multi_agent = MultiAgentSQLRewriter()
    # 使用 asyncio 运行异步任务
    start_time = time.time()
    asyncio.run(multi_agent.process_queries_in_parallel(input_sql_file, output_sql_file, max_workers=10))
    end_time = time.time()
    print(f"Money cost: {multi_agent.money}")
    print(f"Time cost: {end_time - start_time} seconds")
# print(json.dumps(result, indent=4))

# with open (input_sql_file, 'r') as file:
#     data = json.load(file)
#     result = []
#     for query_data in data:
#         input_sql = query_data["original_query"]
#         multi_agent = MultiAgentSQLRewriter(input_sql)
#         iteration = 2
#         result_data = multi_agent.pipeline(iteration,input_sql)
#         result.append(result_data)
#     with open(output_sql_file, 'w') as output_file:
#         json.dump(result, output_file, indent=4)
#     print(f"Experiment results appended to {output_sql_file}")