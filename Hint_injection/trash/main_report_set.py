import sys
sys.path.append("../")
sys.path.append("./")
import re
import json
from gpt import * 
from tools import *
import textwrap
# file = "/root/syy/MARter_hint/input/MARter_dsb_53.json"
file = "/root/syy/MARter_hint/input/MARter_tpch_66.json"
save_file_path = "/root/syy/MARter_hint/output/"

with open(file, "r") as f:
    ori_data = json.load(f)

# tpch
data_statics = '[["customer", "1499999"], ["lineitem", "59986051"], ["nation", "24"], ["orders", "14999999"], ["part", "1999999"], ["partsupp", "7999999"], ["region", "4"], ["supplier", "99999"]]'
 
# dsb
# data_statics = "[['call_center', '24'], ['catalog_page', '12000'], ['customer_address', '250000'], ['customer_demographics', '1920800'], ['date_dim', '73049'], ['dbgen_version', '1'], ['household_demographics', '7200'], ['income_band', '20'], ['item', '102000'], ['reason', '45'], ['ship_mode', '20'], ['store', '102'], ['time_dim', '86400'], ['warehouse', '10'], ['web_site', '42'], ['catalog_returns', '1439749'], ['catalog_sales', '14401261'], ['inventory', '133110000'], ['promotion', '500'], ['web_page', '200'], ['web_returns', '719217'], ['web_sales', '7197566'], ['store_sales', '28800991'], ['customer', '500000'], ['store_returns', '2875432']]"
  
# calcite

def count_pg_hint_plan(pg_hint_plans):
    # 使用正则表达式匹配 pg hint plan
    pg_hint_plans_list = re.findall(r'\b(Parallel|HashJoin|IndexOnlyScan|NoSeqScan|MergeJoin|Leading)\b', pg_hint_plans)

    # 统计匹配到的 pg hint plan 的个数
    return len(pg_hint_plans_list)



def extract_total_cost(query_plan):
    # 定义正则表达式来匹配cost的值
    cost_pattern = re.compile(r'\(cost=\d+\.\d+\.\.(\d+\.\d+)')

    # 初始化最大cost值
    max_cost = 0.0

    # 遍历每一行，提取cost值
    for row in query_plan:
        query_plan_text = row['QUERY PLAN']
        match = cost_pattern.search(query_plan_text)
        if match:
            cost_value = float(match.group(1))  # 提取cost的上限值
            if cost_value > max_cost:
                max_cost = cost_value

    return max_cost


# 2. Syntax: /*+ Parallel(table_name parallel_degree) */
# Scenario: Full scan or aggregation on large data volume tables (>1 million rows).
# Example: /*+ Parallel(logs 4) */ SELECT COUNT(*) FROM logs WHERE date>'2023-01-01';
#         2. Syntax: /*+ Parallel(table_name parallel_degree) */
# Scenario: Full scan or aggregation on large data volume tables (>1 million rows).
# Example: /*+ Parallel(logs 4) */ SELECT COUNT(*) FROM logs WHERE date>'2023-01-01';

#         3. Note that you should use the most effective pg_hint_plans as less as possible.

# def get_prompt(input_sql,physical_plan,historical_hint):
#     # if historical_hint:
#     #     prompt = textwrap.dedent(f"""
#     #     <mission>
#     #     You are an experienced DBA, and your mission is to give some most efficient SQL pg_hint_plan to the following SQL query.
#     #     You have been given a table of how to use pg_hint_plan and the data statics about the database.
                                 
#     #     <steps>
#     #     1. Read input_sql from <input_sql>, SQL physical plan from <physical_plan> and database info in <data statics>
#     #     2. analysis the sql phsical plans and think about most effient pg_hint_plan to make the query more efficient. You have been give historical_hint, which is the hint you have given before, try to avoid the bad examples, improve good examples.
#     #     3. if you think the query is worthing to add pg_hint_plans, return the pg_hint_plan in json format as bellow. Otherwise, retrurn null.

#     #     <notation>
#     #     1. Note that you should only return the pg_hint_plan, not the whole SQL query.
#     #     2. Note that you only can give no more than TWO hints, and return them as a string, not a list.

#     #     you also have benn give a table of how to use pg_hint_plan as bellow:
                                
                                
#     #     Scan Methods
#     #     1. Syntax: /*+ IndexScan(table_name index_name) */
#     #         Scenario: WHERE clause contains highly selective fields (e.g., unique values, date ranges).
#     #     2. Syntax: /*+ IndexOnlyScan(table_name index_name) */
#     #         Scenario: Query fields are fully covered by the index.
#     #     3. Syntax: /*+ NoSeqScan(table_name) */
#     #     Scenario: Forcefully avoid full table scan (ensure effective indexes exist).
        
#     #     Join Methods
#     #     1. Syntax: /*+ HashJoin(table1 table2) */
#     #         Scenario: Equi-join on large tables with sufficient memory.
#     #     2. Syntax: /*+ MergeJoin(table1 table2) */
#     #         Scenario: Join keys are pre-sorted (e.g., time series, auto-incremented IDs).
#     #     3. Syntax: /*+ NoNestedLoop(table1 table2) */
#     #         Scenario: Avoid nested loop joins from big tables join.
        
#     #     Advanced Control
#     #     1. Syntax: /*+ Leading(main_table (sub_table1 sub_table2)) */
#     #         Scenario: Prioritize filtering tables with smaller cardinality in multi-table JOINs.
#     #     2. Syntaxx: /*+ Rows(table_name rows) */
#     #         Scenario: Forcefully set the number of rows to be scanned.

                                          
#     #     <historical_hint>
#     #     {historical_hint}
    
#     #     <input_sql>
#     #     {input_sql}

#     #     <physical_plan>
#     #     {physical_plan}

#     #     <data statics>
#     #     {data_statics}

#     #     Please return the answer in the following format:
#     #     {{
#     #         "flag": {{flag}}, //Fill in the flag to indicate whether the query is worth adding pg_hint_plan, true or false 
#     #         "analysis": {{analysis}} //Fill in the analysis of the SQL query
#     #         "pg_hint_plan": {{pg_hint_plan}} //Fill in the pg_hint_plan of the SQL query if flag is true.
#     #     }}
#     #     """)  
#     # else:
#     prompt = textwrap.dedent(f"""
#         <mission>
#         You are an experienced DBA, and your mission is to give some most efficient SQL pg_hint_plan to the following SQL query.
#         You have been given a table of how to use pg_hint_plan and the data statics about the database.
                                 
#         <steps>
#         1. Read input_sql from <input_sql>, SQL physical plan from <physical_plan> and database info in <data statics>
#         2. analysis the sql phsical plans and think about most effient pg_hint_plan to make the query more efficient. You have been give historical_hint, which is the hint you have given before, try to avoid the bad examples, improve good examples.
#         3. if you think the query is worthing to add pg_hint_plans, return the pg_hint_plan in json format as bellow. Otherwise, retrurn null.

#         <notation>
#         1. Note that you should only return the pg_hint_plan, not the whole SQL query.
#         2. Note that you could only use the hints below, and you should return hints as less as prossible with string format, not a list.
#         you also have benn give a table of how to use pg_hint_plan as bellow:
                                
                                
#         Scan Methods
#         1. Syntax: /*+ IndexScan(table_name index_name) */
#             Scenario: WHERE clause contains highly selective fields (e.g., unique values, date ranges).
#         2. Syntax: /*+ IndexOnlyScan(table_name index_name) */
#             Scenario: Query fields are fully covered by the index.
#         3. Syntax: /*+ NoSeqScan(table_name) */
#         Scenario: Forcefully avoid full table scan (ensure effective indexes exist).
        
#         Join Methods
#         1. Syntax: /*+ HashJoin(table1 table2) */
#             Scenario: Equi-join on large tables with sufficient memory.
#         2. Syntax: /*+ MergeJoin(table1 table2) */
#             Scenario: Join keys are pre-sorted (e.g., time series, auto-incremented IDs).
#         3. Syntax: /*+ NoNestedLoop(table1 table2) */
#             Scenario: Avoid nested loop joins from big tables join.
        
#         Advanced Control
#         1. Syntax: /*+ Leading(main_table (sub_table1 sub_table2)) */
#             Scenario: Prioritize filtering tables with smaller cardinality in multi-table JOINs.
#         2. Syntaxx: /*+ Rows(table_name rows) */
#             Scenario: Forcefully set the number of rows to be scanned.
                                 
#         <input_sql>
#         {input_sql}

#         <physical_plan>
#         {physical_plan}

#         <data statics>
#         {data_statics}

#         Please return the answer in the following format:
#         {{
#             "flag": {{flag}}, //Fill in the flag to indicate whether the query is worth adding pg_hint_plan, true or false 
#             "analysis": {{analysis}} //Fill in the analysis of the SQL query
#             "pg_hint_plan": {{pg_hint_plan}} //Fill in the pg_hint_plan of the SQL query if flag is true.
#         }}
#         """)

#     return prompt

            # Scan Methods:
                # Index scan, index only scan, avoid sequential scan
                #                 Leading join orders,
                             
def get_analysis_prompt(input_sql,physical_plan):
    prompt = textwrap.dedent(f"""

        <Mission>    
        You are an experienced DBA, and your mission is to analyze the SQL physical plan and identify costly scan/join operations. Your goal is to provide suggestions for improving query performance.
        You have been given the following:
        - <input_sql>
        - <physical_plan>
        - <data_statistics> (for the database)
                                 
        <Steps>
        1. Analyze the SQL physical plan and identify potential costly scan/join operations.
        2. Provide a suggestion report on how to improve the query performance, based on the following aspects:
            # Join Methods:
                Hash join,
                merge join,
                nested loop join,
                             
            # Advanced Control:
                Cardinality estimation(rows) correction
                             
        3. If you believe the query isn't worth optimizing with pg_hint_plans, please mention it in your report.
        4. Return the results in the following JSON format:
        {{
                "analysis": {{analysis}}, //Fill in the analysis of the SQL query
                "report": {{report}} //Fill in the report of the SQL query
        }}
        

        
        <input_sql>
        {input_sql}

        <physical_plan>
        {physical_plan}

        <data_statistics>
        {data_statics}

    """)
    return prompt

            # /*+ SET (enable_indexscan off) SET (enable_mergejoin off) */
            # /*+ SET (enable_nestloop off) SET (enable_indexscan off) SET (enable_mergejoin off) */
    
        # GUC:
        #     /*+ SET (enable_nestloop off) */
        #     /*+ SET (enable_hashjoin off) */
        #     /*+ SET (enable_mergejoin off) */
#          /* NestLoop(table table[ table...]) */
#      /*+ 	HashJoin(table table[ table...]) */ 
# /*+ MergeJoin(table table[ table...]) */
# 1. Syntax: /*+ Leading(main_table (sub_table1 sub_table2)) */  or /*+ Leading(table1 table2) */
        
def get_selection_prompt(input_sql,report):
    prompt = textwrap.dedent(f"""
        <Mission>
        You are an experienced DBA, and your mission is to provide the most efficient pg_hint_plan for the following SQL query based on the analysis report.
        You have been given a table for how to use pg_hint_plan and the <data_statistics> about the database.
                                 
        <Steps>
        1. Based on the <report>, find the most efficient pg_hint_plan to improve SQL performance.
        2. If the report mentions that the query is worth optimizing with pg_hint_plan, return the pg_hint_plan in JSON format as shown below. Otherwise, return null.

        <Notation>
        1. Note that you should only return the pg_hint_plan, not the whole SQL query.
        2. You can only use the hints in <pg_hint_plan_table>, and you should return as few hints as possible, in string format, not a list.

        <pg_hint_plan_table>                                

        Join Methods
        1. Syntax: /*+ NoHashJoin(table table[ table...])	 */

        2. Syntax:  /*+ NoMergeJoin(table table[ table...])	*/

        3. Syntax: /*+ NoNestLoop(table table[ table...]) */
                             
        Advanced Control
        
        1. Syntax: /*+ Rows(table_name rows) */
                                 
        <input_sql>
        {input_sql}

        <report>
        {report}

        <data statistics>
        {data_statics}

        Please return the answer in the following format:
        {{
            "flag": {{flag}}, //Fill in the flag to indicate whether the query is worth adding pg_hint_plan, true or false 
            "analysis": {{analysis}} //Fill in the analysis of the SQL query
            "pg_hint_plan": {{pg_hint_plan}} //Fill in the pg_hint_plan of the SQL query if flag is true.
        }}
        """)
    return prompt


dbms = DBMS_PLUS()
llm = GPT()
ans = []
count = 0
batch = 0
temp_file = None
money_cost = 0.0
for item in ori_data:
    count += 1
    print("################################################")
    print(f"this is the query {item['id']}")
    input_sql = item["rewritten_query"]
    operation = dbms.get_pure_plan(input_sql)
    # print(operation)
    original_cost = extract_total_cost(operation)
    print(f"cost is : ",original_cost)

    report_prompt = get_analysis_prompt(input_sql,operation)
    report = llm.get_GPT_response(report_prompt, json_format=True)
    money_cost += llm.calc_money(report_prompt, report)

    prompt = get_selection_prompt(input_sql, report["report"])
    result = llm.get_GPT_response(prompt, json_format=True)
    money_cost += llm.calc_money(prompt,result)

    res = {}
    if result["flag"]:
        pg_hint_plan = result["pg_hint_plan"]
    
        hint_query = pg_hint_plan + input_sql

        hint_operation = dbms.get_pure_plan(hint_query)
        hint_cost = extract_total_cost(hint_operation)
        print(f"hint_cost is : ",hint_cost)
        res = {
            "id": item["id"],
            "original_query": item["rewritten_query"],
            "rewritten_query": hint_query,
            "original_cost": original_cost,
            "hint_cost": hint_cost,
        }
    else:
        res = {
            "id": item["id"],
            "original_query": item["rewritten_query"],
            "rewritten_query": item["rewritten_query"],
            "original_cost": original_cost,
            "hint_cost": original_cost
            }
    print("********************************")
    print(json.dumps(res, indent=4))
    print("money cost is : ",money_cost)
    print("********************************")
    ans.append(res)

    if count % 3 == 0:  
        batch += 1
    with open(f"{save_file_path}/batch_{batch}.json", "w") as f:
        json.dump(ans, f, indent=2)




    # MAX_ITERATION_LOOP = 3
    # MIN_COST = original_cost
    # HINT_FLAG = False
    # MIN_PG_HINT_PLAN = ""
    # MIN_HINT_SQL = ""

    
    # historical_hint = []
    
    # for i in range(MAX_ITERATION_LOOP):
    #     count += 1
    #     print(f"----------loop {i}-th iteration: ------------")
    #     prompt = get_prompt(input_sql,operation,historical_hint)
    #     result = llm.get_GPT_response(prompt, json_format=True)
    #     money_cost += llm.calc_money(input_sql, result["pg_hint_plan"])
    #     # print(result)
    #     flag = result["flag"]
    #     if flag:
    #         pg_hint_plan = result["pg_hint_plan"] 
    #         print(f"pg_hint_plan is : ",pg_hint_plan)
    #         hint_query = pg_hint_plan + input_sql

    #         hint_operation = dbms.get_pure_plan(hint_query)
    #         hint_cost = extract_total_cost(hint_operation)
    #         print(f"hint_cost is : ",hint_cost)

    #         current_hint_count = count_pg_hint_plan(pg_hint_plan)
    #         min_hint_count = count_pg_hint_plan(MIN_PG_HINT_PLAN)
            
    #         if (hint_cost < original_cost and hint_cost < MIN_COST) or (hint_cost < 1.05 * MIN_COST and current_hint_count < min_hint_count):
    #             MIN_COST = hint_cost
    #             MIN_PG_HINT_PLAN = pg_hint_plan
    #             MIN_HINT_SQL = hint_query
    #             HINT_FLAG = True
    #             historical_hint.append(
    #                 {
    #                     "original_cost": original_cost,
    #                     "pg_hint_plan": pg_hint_plan,
    #                     "hint_plus_cost": hint_cost,
    #                 }
    #             )
    #         else:
    #             historical_hint.append(
    #                 {
    #                     "original_cost": original_cost,
    #                     "pg_hint_plan": pg_hint_plan,
    #                     "hint_plus_cost": hint_cost,
    #                 }
    #             )
    #     else:
    #         break
    
    # res = {}
    # if HINT_FLAG:
    #     res = {
    #         "id": item["id"],
    #         "original_query": item["rewritten_query"],
    #         "rewritten_query": MIN_HINT_SQL,
    #         "original_cost": original_cost,
    #         "hint_cost": MIN_COST,
    #     }

    # else:
    #     res = {
    #         "id": item["id"],
    #         "original_query": item["rewritten_query"],
    #         "rewritten_query": item["rewritten_query"],
    #     }
    # print("********************************")
    # print(json.dumps(res, indent=4))
    # print("********************************")
    # ans.append(res)
    
    # 每5条保存一次
    # if count % 3 == 0:  
    #     batch += 1
    #     with open(f"{save_file_path}/batch_{batch}.json", "w") as f:
    #         json.dump(ans, f, indent=2)
        
        # 保存终端输出到txt文件
        # temp_file = save_terminal_output_to_file(save_file_path, batch, original_stdout, temp_file)

       #  result = [] # 清空结果列表


# 保存剩余结果
ans.append({
    "money_cost": money_cost
})
print(f"Total money cost: {money_cost}")
with open(f"{save_file_path}_final_hint.json", "w") as f:
    json.dump(ans, f, indent=2)














# def get_summary_prompt(nave_result):
#     prompt = textwrap.dedent(f"""
#     you are an experinced database sumamry assistant, your mission is to summary the result in <summary> and return the result in json format as bellow:

#     <summary>
#     {nave_result}

#     <json_format>
#     Please return the answer in the following format:
#     {{
#         "flag": {{flag}}, //Fill in the flag to indicate whether the query is worth adding pg_hint_plan, true or false 
#         "analysis": {{analysis}} //Fill in the analysis of the SQL query
#         "pg_hint_plan": {{pg_hint_plan}} //Fill in the pg_hint_plan of the SQL query if flag is true. note that fill this in str, not a list.
#     }}
# """)
#     return prompt

# reasoning_llm = Reasoning()
# assistent_llm = GPT_Summary()

# for item in ori_data:
#     print("################################################")
#     print(f"this is the query {item['id']}")
#     input_sql = item["rewritten_query"]
#     operation = dbms.get_pure_plan(input_sql)
#     # print(operation)
#     original_cost = extract_total_cost(operation)
#     print(f"cost is : ",original_cost)

#     MAX_ITERATION_LOOP = 3
#     MIN_COST = original_cost
#     HINT_FLAG = False
#     MIN_PG_HINT_PLAN = ""
#     MIN_HINT_SQL = ""

    
#     historical_hint = []
#     prompt = get_prompt(input_sql,operation,historical_hint)
#     nave_result = reasoning_llm.get_GPT_response(prompt)
#     sumamry_prompt = get_summary_prompt(nave_result)
#     result =  assistent_llm.get_GPT_response(sumamry_prompt, json_format=True)
#     # print(result)
#     flag = result["flag"]
#     if flag:
#         pg_hint_plan = result["pg_hint_plan"] 
#         print(f"pg_hint_plan is : ",pg_hint_plan)
#         hint_query = pg_hint_plan + input_sql

#         hint_operation = dbms.get_pure_plan(hint_query)
#         hint_cost = extract_total_cost(hint_operation)
#         print(f"hint_cost is : ",hint_cost)

#         current_hint_count = count_pg_hint_plan(pg_hint_plan)
#         min_hint_count = count_pg_hint_plan(MIN_PG_HINT_PLAN)
        
#         if (hint_cost < original_cost and hint_cost < MIN_COST) or (hint_cost < 1.05 * MIN_COST and current_hint_count < min_hint_count):
#             MIN_COST = hint_cost
#             MIN_PG_HINT_PLAN = pg_hint_plan
#             MIN_HINT_SQL = hint_query
#             HINT_FLAG = True
        
    
#     res = {}
#     if HINT_FLAG:
#         res = {
#             "id": item["id"],
#             "original_query": item["rewritten_query"],
#             "rewritten_query": MIN_HINT_SQL,
#             "original_cost": original_cost,
#             "hint_cost": MIN_COST,
#         }
#     else:
#         res = {
#             "id": item["id"],
#             "original_query": item["rewritten_query"],
#             "rewritten_query": item["rewritten_query"],
#             "original_cost": original_cost,
#             "hint_cost": original_cost
#             }
#     print("********************************")
#     print(json.dumps(res, indent=4))
#     print("********************************")
#     ans.append(res)
    
#     # 每5条保存一次
#     if count % 3 == 0:  
#         batch += 1
#         with open(f"{save_file_path}/batch_{batch}.json", "w") as f:
#             json.dump(ans, f, indent=2)
        
#         # 保存终端输出到txt文件
#         # temp_file = save_terminal_output_to_file(save_file_path, batch, original_stdout, temp_file)

#        #  result = [] # 清空结果列表


# # 保存剩余结果
# ans.append({
#     "money_cost": money_cost
# })
# print(f"Total money cost: {money_cost}")
# with open(f"{save_file_path}_final_hint.json", "w") as f:
#     json.dump(ans, f, indent=2)