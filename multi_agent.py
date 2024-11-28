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
import argparse
from collections import Counter


class MultiAgentSQLRewriter:
    def __init__(self, schema = None):
        self.input_sql = []
        self.schema = schema
        self.gpt = GPT()
        self.money = 0.0
        self.chat_history = []
        self.iteration_history = []

    async def agent_a_analysis(self,sql_input):
        # 使用大模型分析 SQL（Agent A 的职责）
        prompt = textwrap.dedent(f"""
            <Backgroud>
            The system is designed to optimize SQL queries. The agents, modeled as virtual assistants, work collaboratively to analyze, rewrite, and validate SQL queries. The objective is to enhance query performance by applying relevant optimization rules while ensuring the query equivalance.

            <mission>
            You are Agent A, suppose you are an experenced DBA, and your role is a SQL Analyzer. Your task is to analyze the SQL query and identify potential performance bottlenecks to make the execution time of the sql faster and less costy. Provide suggestions on how to optimize the query.
            
            Let's think about this questions step by step.
            <steps>
            0. Read the original sql to be rewritten from the <input_sql>, and the corresponding schema from the <schema>.
            1. Analyze the SQL query and identify potential performance bottlenecks.
            2. Given a binary judgement on whether the SQL query is optimized or not. If you think the sql is able to rewrite, Fill "True" in the <is_optimized>. If you think the sql is unable to rewrite, Fill "False" in the <is_optimized>. 
            3. Given the candidate optimization suggestions based on your analysis. Make your suggestions clear and concise. If <is_optimized> is "True", you can provide some suggestions to optimize the SQL query. If <is_optimized> is "False", Fill this field with "None".
            4. Return your response based on the <json_formate_templete>.
            
            <input_sql>
            {sql_input}
            
            <schema>
            {self.schema}

            <json_format_templete>
            {{
                "agent_candidate_sql": {{candidate_sql}},  // Fill this 'candidate_sql' with the candidate SQL query. Note that if the chat history is not empty, you should consider the last rewritten sql as the candidate SQL.
                "agent_analysis": {{analysis}},  // Fill this 'analysis' with the analysis details of the SQL query.
                "is_optimized": {{True/False}},  // Fill this 'is_optimized' with your judgement.
                "agent_suggestions": {{suggestions}}  // Fill this 'suggestions'with the optimization suggestions. If <is_optimized> is "True", you can provide some suggestions to optimize the SQL query. If <is_optimized> is "False", Fill this field with "None".
            }}
        """)
        response = await self.gpt.get_GPT_response_async(prompt, json_format=True)
        self.chat_history.append({"Agent A": response})
        self.chat_history.append("###############################################################################")
        print(f"""
#################################################################################################################################################
Agent A response:
{response}
#################################################################################################################################################
\n""")
        self.money += self.gpt.calc_money(prompt,response)
        # print(self.chat_history)
        return response
    
    # async def agent_a_analysis_rethink(self,history,sql_input):
    #     # 使用大模型分析 SQL（Agent A 的职责）
    #     prompt = textwrap.dedent(f"""
    #         <Backgroud>
    #         The system is designed to optimize SQL queries. The agents, modeled as virtual assistants, work collaboratively to analyze, rewrite, and validate SQL queries. The objective is to enhance query performance by applying relevant optimization rules while ensuring the query equivalance.

    #         <mission>
    #         You are Agent A, suppose you are an experenced DBA, and your role is a SQL Analyzer. Your task is to rethink the inequivalance SQL provided in the <history> and <sql_input>. Your task is to reanalyze the SQL query and identify potential performance bottlenecks to make the execution time of the sql faster and less costy. Provide suggestions on how to optimize the query.
            
    #         Let's think about this questions step by step.
    #         <steps>
    #         0. Read the original sql to be rewritten from the <input_sql>. 
    #         1. Analyze the SQL query and identify potential performance bottlenecks.
    #         2. Given a binary judgement on whether the SQL query is optimized or not. If you think the sql is able to rewrite, Fill "True" in the <is_optimized>. If you think the sql is unable to rewrite, Fill "False" in the <is_optimized>. 
    #         3. Given the candidate optimization suggestions based on your analysis. Make your suggestions clear and concise. If <is_optimized> is "True", you can provide some suggestions to optimize the SQL query. If <is_optimized> is "False", Fill this field with "None".
    #         4. Return your response based on the <json_formate_templete>.
            
    #         <input_sql>
            

    #         <json_format_templete>
    #         {{
    #             "agent_candidate_sql": {{candidate_sql}},  // Fill this 'candidate_sql' with the candidate SQL query. Note that if the chat history is not empty, you should consider the last rewritten sql as the candidate SQL.
    #             "agent_analysis": {{analysis}},  // Fill this 'analysis' with the analysis details of the SQL query.
    #             "is_optimized": {{True/False}},  // Fill this 'is_optimized' with your judgement.
    #             "agent_suggestions": {{suggestions}}  // Fill this 'suggestions'with the optimization suggestions. If <is_optimized> is "True", you can provide some suggestions to optimize the SQL query. If <is_optimized> is "False", Fill this field with "None".
    #         }}
    #     """)
    #     response = await self.gpt.get_GPT_response_async(prompt, json_format=True)
    #     self.chat_history.append({"Agent A": response})
    #     self.chat_history.append("###############################################################################")
    #     self.money += self.gpt.calc_money(prompt,response)
    #     # print(self.chat_history)
    #     return response

    async def agent_a_analysis_with_knowledge(self,knowledge):
        # 使用大模型分析 SQL（Agent A 的职责）
        prompt = textwrap.dedent(f"""
            <Backgroud>
            The system is designed to optimize SQL queries. The agents, modeled as virtual assistants, work collaboratively to analyze, rewrite, and validate SQL queries. The objective is to enhance query performance by applying relevant optimization rules while ensuring the query equivalance.

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
                "agent_analysis": {{analysis}},  // Fill this 'analysis' with the analysis details of the SQL query.
                "is_optimized": {{True/False}},  // Fill this 'is_optimized' with your judgement.
                "agent_suggestions": {{suggestions}}  // Fill this 'suggestions'with the optimization suggestions. If <is_optimized> is "True", you can provide some suggestions to optimize the SQL query. If <is_optimized> is "False", Fill this field with "None".
            }}
        """)
        response = await self.gpt.get_GPT_response_async(prompt, json_format=True)
        self.money += self.gpt.calc_money(prompt,response)
        self.chat_history.append({"Agent A": response})
        self.chat_history.append("###############################################################################")
        # print(self.chat_history)
        return response

    async def agent_b_rewrite(self, analysis_response,sql_input):
        # 使用大模型重写 SQL（Agent B 的职责）
        # print("-----------------------------------------------------------------------------")
        # print(f"{analysis_response}")
        # print("-----------------------------------------------------------------------------")
        prompt = textwrap.dedent(f"""
            <Backgroud>
            The system is designed to optimize SQL queries. The agents, modeled as virtual assistants, work collaboratively to analyze, rewrite, and validate SQL queries. The objective is to enhance query performance by applying relevant optimization rules while ensuring the query equivalance.

            <mission>
            You are Agent B, a SQL Rewriter. Based on the analysis and suggestions provided by Agent A, your task is to rewrite the SQL query to optimize its performance.
            You MUST strictly follow Agent A's suggestions to rewrite the query. Ensure all suggested optimizations are applied.

            Let's think about this step by step.
            
            <steps>
            0. Read the candidate sql from <candidate_sql> and agent A's analysis response from the <analysis_response> and the corresponding schema from <schema>. Understand the suggestions provided by Agent A. 
            1. Rewrite the Candidate SQL based on the suggestions provided by Agent A.
            2. Ensure that you apply the suggestions provided by Agent A.
            3. Make sure your rewrite process does not making any syntax errors or semantic errors.
            4. Return your response based on the <json_format_template>.

            <candidate_sql>
            {sql_input}

            <agent_a_analysis>
            {analysis_response}

            <schema>
            {self.schema}

            <json_format_template>
            {{
                "agent_rewritten_sql": {{rewritten_sql}},  // Fill this 'rewritten_sql' with the rewritten SQL query based on Agent A's suggestions.
                "agent_explanation": {{explanation}}  // Fill this 'explanation' with the explanation of the rewrite process.
            }}
        """)
        response = await self.gpt.get_GPT_response_async(prompt, json_format=True)
        self.money += self.gpt.calc_money(prompt,response)
        self.chat_history.append({"Agent B": response})
        self.chat_history.append("#######################WW########################################################")
        print(f"""
#################################################################################################################################################
Agent B response:
{response}
#################################################################################################################################################
\n""")
        # print(self.chat_history)
        return response

    # async def agent_c_check(self,agent_a_response, agent_b_response):
    #     # 使用大模型总结 Agent A 和 Agent B 的对话（Agent C 的职责）
    #     prompt = textwrap.dedent(f"""
    #         <Backgroud>
    #         The system is designed to optimize SQL queries. The agents, modeled as virtual assistants, work collaboratively to analyze, rewrite, and validate SQL queries. The objective is to enhance query performance by applying relevant optimization rules while ensuring the query equivalance.

    #         <mission>
    #         You are Agent C, responsible for summarizing the conversation between Agent A and Agent B, and providing a concise history summary to compress the chat history.
    #         Let's think about this questions step by step.
            
    #         1. Read the chat history between Agent A and Agent B.
    #         2. Provide a concise summary of the conversation between Agent A and Agent B.
    #         3. Return your response based on the <json_formate_templete>.
            
    #         <chat_history>
    #         [agent_a_response]
    #         {agent_a_response}
    #         [agent_b_response]
    #         {agent_b_response}
            
    #         <json_format_templete>
    #         {{
    #             "agent_candidate_sql": {{candidate_sql}},  // Fill this 'candidate_sql' with the candidate SQL query.
    #             "agent_analysis": {{analysis}},  // Fill this 'analysis' with the analysis details of the SQL query.
    #             "agent_rewritten_sql": {{rewritten_sql}},  // Fill this 'rewritten_sql' with the rewritten SQL query.
    #         }}
    #     """)
    #     response = await self.gpt.get_GPT_response_async(prompt, json_format=True)
    #     self.money += self.gpt.calc_money(prompt,response)
    #     self.iteration_history.append(response)  # 将总结存入历史记录
    #     print(self.iteration_history)
    #     self.chat_history.clear()  # 清除当前的聊天记录，准备下一轮迭代
    #     return response


    async def agent_c_check(self,candidate_sql,rewritten_sql,agent_a_response,agent_b_response):
        # 使用大模型总结 Agent A 和 Agent B 的对话（Agent C 的职责）
        prompt = textwrap.dedent(f"""
            <Backgroud>
            The system is designed to optimize SQL queries. The agents, modeled as virtual assistants, work collaboratively to analyze, rewrite, and validate SQL queries. The objective is to enhance query performance by applying relevant optimization rules while ensuring the query equivalance.

            <mission>
            You are Agent C, responsible for checking wheather the candidate sql and rewritten sql are equivalent.
            
            Let's think about this questions step by step.
            <steps>
            0. Find the candidate sql and the rewritten sql from <candidate_sql> and the <rewritten_sql>, and corresponding schema from <schema>
            1. judge the rewritten analysis from the <agent_a_response> and <agent_b_response>.
            1. Read the chat history between Agent A and Agent B.
            2. Provide a concise summary of the conversation between Agent A and Agent B.

            3. Return your response based on the <json_formate_templete>.

            <candidate_sql>
            {candidate_sql}       
            <rewritten_sql>
            {rewritten_sql}

            <schema>
            {self.schema}                  
            <chat_history>
            [agent_a_response]
            {agent_a_response}
            [agent_b_response]
            {agent_b_response}
            
            <json_format_templete>
            {{
                "agent_analysis": {{analysis}},  // Fill this 'analysis' with the analysis details of the equivalent of the SQL query.
                "equivalence": {{True/False}},  // Fill 'True' if the candidate sql and rewritten sql are equivalent. Otherwise, fill 'False'.
            }}
        """)
        response = await self.gpt.get_GPT_response_async(prompt, json_format=True)
        self.money += self.gpt.calc_money(prompt,response)
        self.iteration_history.append(response)  # 将总结存入历史记录
        print(f"""
#################################################################################################################################################
Agent C response:
{response}
#################################################################################################################################################
\n""")
        # print(self.iteration_history)
        self.chat_history.clear()  # 清除当前的聊天记录，准备下一轮迭代
        return response

    async def vote_for_sql(self,result_data,vote_number = 3):
        # This will store the GPT responses, i.e., the selected SQLs and their analyses
        print(f"############################### This is the vote routation ##################################")
        print(f"-----------------------------------------------------------------------------------------------------------------")
        print(f"{result_data}")
        print(f"-----------------------------------------------------------------------------------------------------------------")
        votes = []
        analyses = []
        prompt = textwrap.dedent(f"""
        <Mission>
        Suppose you are an experienced DBA majoring SQL rewriteing. And now, you are the voter, your task is to vote for the best rewritten sql from the result data.
        Let's think about this questions step by step.

        <steps>    
        0. Read the result data from the <result_data>, determining the input sql and the rewritten sql.
        1. analyze the each rewritten sql from the result data, ensure the best rewritten sql with highest execution performance(including reducing execution time and cost as much as possible).
        2. vote for the best rewritten sql from the result data.
        3. Return your response based on the <json_formate_templete>.
        
        <result_data>
        {result_data}

        <json_formate_templete>
        {{
                "original_query": {{original_sql}},  // Fill this 'original_sql' with the original SQL query.
                "rewritten_query": {{selected_sql}},  // Fill this 'selected_sql' with the rewritten SQL with the best performance.
                "agent_analysis": {{analysis}},  // Fill this 'analysis' with the analysis details of finding the best rewritten SQL.
                
        }}                                                 
        """)
    # Request votes from multiple GPT agents
        for i in range(vote_number):
            response = await self.gpt.get_GPT_response_async(prompt, json_format=True)
            original_sql = response["original_query"]
            selected_sql = response["rewritten_query"]
            analysis = response["agent_analysis"]
            print(f""" the {i} -th / {vote_number} vote:
            "original_query": {original_sql},
            "rewritten_query": {selected_sql},
            "agent_analysis": {analysis}
\n""")
            # Store the analysis and selected SQL
            if selected_sql:
                votes.append(selected_sql)
                analyses.append(analysis)
        
        if not votes:
            raise ValueError("No valid rewritten SQLs were generated for voting.")

        # Count the votes for each SQL and find the one(s) with the most votes
        vote_count = Counter(votes)
        most_common_sqls = vote_count.most_common()

        # Check for ties
        if len(most_common_sqls) > 1 and most_common_sqls[0][1] == most_common_sqls[1][1]:
            # If there is a tie, we can apply a heuristic or fallback logic to resolve it
            # For this example, let's select the SQL that appears first in the result data
            best_sql = most_common_sqls[0][0]  # Default to the first in case of a tie
            for sql in result_data:
                if sql in [item[0] for item in most_common_sqls]:
                    best_sql = sql
                    break
        else:
            # No tie, select the SQL with the highest vote
            best_sql = most_common_sqls[0][0]

        # Compile a comprehensive analysis
        combined_analysis = " | ".join(analyses)
        print(f""""
            "original_query": {original_sql},
            "rewritten_query": {best_sql},
            "agent_analysis": {combined_analysis}
#################################################################################################################################################\n
        """)
        # Return the final result
        return {
            "original_query": original_sql,
            "rewritten_query": best_sql,
            "agent_analysis": combined_analysis
        }

    
    async def pipeline(self,iteration,input_sql):
        # 执行一次迭代过程，依次调用 Agent A, B 和 C
        result_data = []
        for i in range(iteration):
            # 确保调用异步函数时使用 await
            agent_a_response = await self.agent_a_analysis(input_sql)
            agent_b_response = await self.agent_b_rewrite(agent_a_response,input_sql)
            candidate_sql = agent_a_response["agent_candidate_sql"]
            rewritten_sql = agent_b_response["agent_rewritten_sql"]
            agent_c_response = await self.agent_c_check(candidate_sql, rewritten_sql,agent_a_response, agent_b_response)
            equivalance = agent_c_response["equivalence"]
            print(f"equivalance: {equivalance}\n")
            if equivalance == True:
                result = {
                    "original_query": input_sql,
                    "rewritten_query": agent_b_response["agent_rewritten_sql"],
                    "agent_analysis": agent_a_response["agent_analysis"],
                }
                result_data.append(result)
                continue
            else:
                boundery = 3
                iter = 1
                # agent_a_response = None
                # agent_b_response = None
                # agent_c_response = None
                while equivalance != True and iter < boundery:
                    agent_b_response = await self.agent_b_rewrite(agent_a_response,input_sql)
                    rewritten_sql = agent_b_response["agent_rewritten_sql"]
                    agent_c_response = await self.agent_c_check(candidate_sql,rewritten_sql,agent_a_response, agent_b_response)
                    iter += 1
                    equivalance = agent_c_response["equivalence"]
                
                if equivalance == True:
                    result = {
                        "original_query": input_sql,
                        "rewritten_query": agent_b_response["agent_rewritten_sql"],
                        "agent_analysis": agent_a_response["agent_analysis"],
                    }
                    result_data.append(result)
                    break
                
                elif iter == boundery:
                    print("The SQL is unable to rewrite. Boundery reached.")
            
        agent_vote_result = await self.vote_for_sql(result_data)

        return agent_vote_result


# 示例调用：
# input_sql = "select nation, o_year, sum(amount) as sum_profit from ( select n_name as nation, extract(year from o_orderdate) as o_year, l_extendedprice * (1 - l_discount) - ps_supplycost * l_quantity as amount from part,supplier,lineitem,partsupp,orders,nation where s_suppkey = l_suppkey and ps_suppkey = l_suppkey and ps_partkey = l_partkey and p_partkey = l_partkey and o_orderkey = l_orderkey and s_nationkey = n_nationkey and p_name like '%green%' ) as profit group by nation, o_year order by nation, o_year desc;"
# multi_agent = MultiAgentSQLRewriter(input_sql)
# iteration = 2
# result_data = multi_agent.pipeline(iteration)
# print(json.dumps(result_data, indent=4))
    async def process_query(self, query_data):
        input_sql = query_data["query"]
        self.input_sql = input_sql
        iteration = 1
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



def parse_arguments():
    parser = argparse.ArgumentParser(description="SQL Rewriter Script")
    parser.add_argument("-i", "--input", type=str, required=True, help="Path to the input SQL file (JSON format)")
    parser.add_argument("-o", "--output", type=str, required=True, help="Path to the output SQL file (JSON format)")
    parser.add_argument("-s", "--schema", type=str, required=True, help="Path to the schema file (SQL format)")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    input_sql_file = args.input
    output_sql_file = args.output
    schema_file = args.schema
    # input_sql_file = "/home/orderheart/syy/sql_rewriter/query_template/tpch/queries.json"
    # output_sql_file = "/home/orderheart/syy/sql_rewriter/data/result_execution/multi_agent/schema_vote_evalue_result.json"
    # schema_file = "/home/orderheart/syy/sql_rewriter/schema/tpch_schema.sql"
    with open(schema_file, 'r') as file:
        schema = file.read()
    multi_agent = MultiAgentSQLRewriter(schema)
    # 使用 asyncio 运行异步任务
    start_time = time.time()
    asyncio.run(multi_agent.process_queries_in_parallel(input_sql_file, output_sql_file, max_workers=10))
    end_time = time.time()
    print(f"Money cost: {multi_agent.money}")
    print(f"Time cost: {end_time - start_time} seconds")
# print(json.dumps(result, indent=4))