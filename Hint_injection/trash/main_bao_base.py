import sys
sys.path.append("../")
sys.path.append("./")
import re
import json
from gpt import * 
from tools import *
import textwrap
file = "/root/syy/MARter_hint/input/MARter_dsb_159.json"

save_file_path = "/root/syy/MARter_hint/output/"

with open(file, "r") as f:
    ori_data = json.load(f)

# tpch
# data_statics = '[["customer", "1499999"], ["lineitem", "59986051"], ["nation", "24"], ["orders", "14999999"], ["part", "1999999"], ["partsupp", "7999999"], ["region", "4"], ["supplier", "99999"]]'
 
# dsb
data_statics = "[['call_center', '24'], ['catalog_page', '12000'], ['customer_address', '250000'], ['customer_demographics', '1920800'], ['date_dim', '73049'], ['dbgen_version', '1'], ['household_demographics', '7200'], ['income_band', '20'], ['item', '102000'], ['reason', '45'], ['ship_mode', '20'], ['store', '102'], ['time_dim', '86400'], ['warehouse', '10'], ['web_site', '42'], ['catalog_returns', '1439749'], ['catalog_sales', '14401261'], ['inventory', '133110000'], ['promotion', '500'], ['web_page', '200'], ['web_returns', '719217'], ['web_sales', '7197566'], ['store_sales', '28800991'], ['customer', '500000'], ['store_returns', '2875432']]"
  

def count_pg_hint_plan(pg_hint_plans):
    # 使用正则表达式匹配 pg hint plan
    pg_hint_plans_list = re.findall(r'\b(Parallel|HashJoin|IndexOnlyScan|NoSeqScan|MergeJoin|Leading)\b', pg_hint_plans)

    # 统计匹配到的 pg hint plan 的个数
    return len(pg_hint_plans_list)



def extract_total_cost(query_plan):
    # 定义正则表达式来匹配cost的值
    cost_pattern = re.compile(r'\(cost=\d+\.\d+\.\.(\d+\.\d+)')
    print("#############################################")
    print(query_plan)
    print("#############################################")
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

def get_analysis_prompt(input_sql,physical_plan):
    prompt = textwrap.dedent(f"""

        <Mission>    
        You are an experienced DBA, and your mission is to analyze the SQL physical plan and identify costly scan/join operations to help select effient query hints. Your suggestions will going togenerate high qulity query hints.
        You have been given the following:
        - <input_sql>
        - <physical_plan>
        - <data_statistics> (for the database)
                                 
        <Steps>
        1. Analyze the SQL physical plan and identify potential costly scan/join operations that can be applied in pg hint plan. Note that you don't need consider change query structure, scan, index, parallel, or other advanced features.
        2. you should only use the following methods to optimize the query. You can use any combination of these methods, but you should not use any other methods.     
            ## Scan Methods: 
            SET enable_nestloop = on/off;
            SET enable_indexscan = on/off;
                      
            ## Join Methods:  
            SET enable_mergejoin = on/off;
            SET enable_nestloop = on/off;
            SET enable_hashjoin = on/off;


        3. Provide a suggestion report on how to improve the query performance based on the following aspects. You only can use thess methods. If you believe the query isn't worth optimizing with pg_hint_plans, please mention it in your report.
                             
        4. Return the results in the following format:

        </analysis>
            //Fill in with your analysis
        </analysis>

        </report>
            //Fill in your report, make your report as simple and clear as possible.
        </report>

        
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
         
def get_selection_prompt(input_sql,report):
    prompt = textwrap.dedent(f"""
        <Mission>
        You are an experienced DBA, and your mission is to provide the most efficient query hints for the following SQL query based on the analysis report.
                                 
        <Steps>
        1. Based on the <report>, find and check the most efficient query hints to improve SQL performance.
        2. If the report mentions that the query is worth optimizing with query hints, return the query hints in JSON format as shown below. Otherwise, return "".
        You can only use the following query hints:
        ## Scan Methods: 
        SET enable_nestloop = on/off;
        SET enable_indexscan = on/off;

                    
        ## Join Methods:  
        SET enable_mergejoin = on/off;
        SET enable_nestloop = on/off;
        SET enable_hashjoin = on/off;

        <Notation>
        1. Note that you should only return the query hints, not the whole SQL query. And each query hints should be separated by a comma ";"
        2. You should return as few hints as possible, in string format, not a list.

        <input_sql>
        {input_sql}

        <report>
        {report}

        Please return the answer in the following format:
        ```json
        {{
            "flag": {{flag}}, //Fill in the flag to indicate whether the query is worth adding query hints, true or false 
            "query_hints": {{}} //Fill in the query hints
        }}
        ```
        """)
    return prompt

def  extract_func(text,label):
    pattern = rf'</{label}>\s*(.*?)\s*</{label}>'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""

def extract_json(text):
    pattern = r'```json\s*(.*?)\s*```'
    matches = re.findall(pattern, text, re.DOTALL)
    json_list = []
    for match in matches:
        json_str = match.strip()
        try:
            json_obj = json.loads(json_str)
            json_list.append(json_obj)
        except json.JSONDecodeError:
            print("Invalid JSON format")
            continue
    return json_list

def execute_with_hints(dbms, input_sql, pg_hint_plan):
    """执行带有 PG hints 的 SQL 查询"""
    if not pg_hint_plan:
        return dbms.get_pure_plan(input_sql), None
        
    # 分离 SET 语句
    set_statements = []
    for stmt in pg_hint_plan.split(';'):
        stmt = stmt.strip()
        if stmt and stmt.upper().startswith('SET '):
            set_statements.append(stmt + ";")
            
    try:
        # 执行所有 SET 语句
        for stmt in set_statements:
            result = dbms.execute_query(stmt)
            if isinstance(result, str) and "error" in result.lower():
                return None, f"Error executing SET statement: {result}"
                
        # 执行带计划的查询
        hint_operation = dbms.get_pure_plan(input_sql)
        
        # 重置所有设置
        for stmt in set_statements:
            param_name = stmt.split('=')[0].replace('SET', '').strip()
            dbms.execute_query(f"SET {param_name} = DEFAULT;")
            
        return hint_operation, None
        
    except Exception as e:
        # 确保重置所有设置，即使出现错误
        try:
            for stmt in set_statements:
                param_name = stmt.split('=')[0].replace('SET', '').strip()
                dbms.execute_query(f"SET {param_name} = DEFAULT;")
        except:
            pass
        return None, str(e)
    


    # "context_pg_hint_plan": [
    #     {
    #         "CTE_name": "filtered_parts",
    #         "context_pg_hint_plan": "/*+ Inline(filtered_parts) Rows(filtered_parts 2127) */"
    #     }
    # ],

    # "preamble_pg_hint_plan": "/*+ Leading(filtered_parts lineitem subq) HashJoin(filtered_parts lineitem) HashJoin(lineitem subq) */"
    # "input_query" = "WITH filtered_parts AS (     SELECT p_partkey     FROM part     WHERE p_brand = 'Brand#32'      AND p_container = 'WRAP PKG' ) SELECT SUM(l.l_extendedprice) / 7.0 AS avg_yearly FROM filtered_parts p JOIN lineitem l ON p.p_partkey = l.l_partkey JOIN (     SELECT l_partkey, 0.2 * AVG(l_quantity) AS avg_quantity     FROM lineitem l     JOIN filtered_parts p ON l.l_partkey = p.p_partkey     GROUP BY l_partkey ) subq ON l.l_partkey = subq.l_partkey WHERE l.l_quantity < subq.avg_quantity;"

def refine_func(input_sql: str, pg_hint_plan: str) -> str:
    # 处理外部提示
    if pg_hint_plan and not pg_hint_plan.strip().endswith(";"):
        pg_hint_plan = pg_hint_plan.strip() + ";"
    return pg_hint_plan + " " + input_sql

dbms = DBMS_PLUS()
llm = GPT()
# llm_assistant = GPT_Assistant()
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
    print(operation)
    original_cost = extract_total_cost(operation)
    print(f"cost is : ",original_cost)

    report_prompt = get_analysis_prompt(input_sql,operation)
    report_result = llm.get_GPT_response(report_prompt)
    report = extract_func(report_result,"report")
    # money_cost += llm.calc_money(report_prompt, report)

    prompt = get_selection_prompt(input_sql, report)
    # result = llm_assistant.get_GPT_response(prompt,json_format=True)
    result = llm.get_GPT_response(prompt)
    json_list = extract_json(llm.get_GPT_response(prompt))
    if json_list and len(json_list) > 0:
        result = json_list[0]
    print(result)
    # json_list = extract_json(llm.get_GPT_response(prompt))
    # if json_list and len(json_list) > 0:
    #     result = json_list[0]
    # print(result)
    # # money_cost += llm.calc_money(prompt,result)
    # # result = json.loads(llm.get_GPT_response(prompt))

    res = {}
    if result["flag"]:
        pg_hint_plan = result["query_hints"]
        pg_hint_query = refine_func(input_sql, pg_hint_plan)

        # print("pg_hint_query is : ",pg_hint_query)
    # 使用新函数执行带 hints 的查询
        hint_operation, error = execute_with_hints(dbms, input_sql, pg_hint_plan)
        
        if error:
            print(f"Error executing query with hints: {error}")
            # 如果执行出错，使用原始成本
            hint_cost = original_cost
        else:
            hint_cost = extract_total_cost(hint_operation)
        
        # print(f"hint_cost is : ", hint_cost)

        res = {
            "id": item["id"],
            "original_query": item["rewritten_query"],
            "rewritten_query": pg_hint_query,
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




# 保存剩余结果
ans.append({
    "money_cost": money_cost
})
print(f"Total money cost: {money_cost}")
with open(f"{save_file_path}_final_hint.json", "w") as f:
    json.dump(ans, f, indent=2)
