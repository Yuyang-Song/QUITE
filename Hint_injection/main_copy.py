import sys
sys.path.append("../")
sys.path.append("./")
import re
import json
from gpt import * 
from tools import *
import textwrap
# file = "/root/syy/MARter_hint/input/MARter_dsb_53.json"
file = "/root/syy/machine1/query/dsb/dsb_156.json"
# file = "/root/syy/MARter_hint/input/MARter_calcite.json"
save_file_path = "/root/syy/code/QUITE/Hint_injection/output/dsb_largerspace"

with open(file, "r") as f:
    ori_data = json.load(f)

# calcite
# data_statistics = "[['BONUS', '29999999'],['DEPT', '299999'],['EMP_B', '29999999'],['EMP', '29999999'],['EMPNULLABLES_20', '55'],['EMPNULLABLES', '29999999']]"
# tpch_s10
# data_statistics = '[["customer", "1499999"], ["lineitem", "59986051"], ["nation", "24"], ["orders", "14999999"], ["part", "1999999"], ["partsupp", "7999999"], ["region", "4"], ["supplier", "99999"]]'
# dsb
data_statistics = "[['call_center', '24'], ['catalog_page', '12000'], ['customer_address', '250000'], ['customer_demographics', '1920800'], ['date_dim', '73049'], ['dbgen_version', '1'], ['household_demographics', '7200'], ['income_band', '20'], ['item', '102000'], ['reason', '45'], ['ship_mode', '20'], ['store', '102'], ['time_dim', '86400'], ['warehouse', '10'], ['web_site', '42'], ['catalog_returns', '1439749'], ['catalog_sales', '14401261'], ['inventory', '133110000'], ['promotion', '500'], ['web_page', '200'], ['web_returns', '719217'], ['web_sales', '7197566'], ['store_sales', '28800991'], ['customer', '500000'], ['store_returns', '2875432']]"
# job
# data_statistics = "[['aka_name', '901343'], ['aka_title', '361472'], ['cast_info', '36244344'], ['char_name', '3140339'], ['comp_cast_type', '4'], ['company_name', '234997'], ['company_type', '4'], ['complete_cast', '135086'], ['info_type', '113'], ['keyword', '134170'], ['kind_type', '7'], ['link_type', '18'], ['movie_companies', '2609129'], ['movie_info_idx', '1380035'], ['movie_keyword', '4523930'], ['movie_link', '29997'], ['name', '4167491'], ['role_type', '12'], ['title', '2528312'], ['movie_info', '14835720'], ['person_info', '2963664']]"

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
    try:
        for row in query_plan:
            print(row['QUERY PLAN'])
            query_plan_text = row['QUERY PLAN']
            match = cost_pattern.search(query_plan_text)
            if match:
                cost_value = float(match.group(1))  # 提取cost的上限值
                if cost_value > max_cost:
                    max_cost = cost_value
    except (KeyError, TypeError) as e:
            print(f"Data type mismatch in extract_total_cost: {e}")
            print(f"Row type: {type(row)}, Row content: {row}")
            # 返回特殊值表示需要重试
            return -1

    return max_cost

def safe_get_cost_with_retry(dbms, sql, max_retries=3):
    """
    安全获取查询成本，带重试机制
    """
    for attempt in range(max_retries + 1):
        try:
            print(f"Attempt {attempt + 1} to get plan for SQL")
            operation = dbms.get_pure_plan(sql)
            print(f"Operation type: {type(operation)}")
            if operation:
                print(f"Operation sample: {operation[:2] if len(operation) > 0 else 'Empty'}")
            
            cost = extract_total_cost(operation)
            
            # 如果返回-1表示数据类型不匹配，需要重试
            if cost == -1:
                print(f"Data type mismatch detected, retrying... (attempt {attempt + 1})")
                continue
            else:
                return cost, operation
                
        except Exception as e:
            print(f"Error in attempt {attempt + 1}: {e}")
            if attempt == max_retries:
                print("Max retries reached, returning default cost 0")
                return 0, []
            continue
    
    return 0, []

def get_analysis_prompt(input_sql,physical_plan):
    prompt = textwrap.dedent(f"""

        <Mission>    
        You are an experienced DBA. Your mission is to analyze the SQL physical plan and identify costly operations to inform efficient query hints。
        You have been given:
        - <input_sql>
        - <physical_plan>
        - <data_statistics> (for the database)
                                 
        <Steps>
        1. Analyze the SQL physical plan and identify the most impactful costly operations that can be addressed using pg_hint_plan hints. Do not modify the query structure, scans, indexes, parallelism, or other advanced features—focus only on hints.

        2. Concentrate on the following hint categories. Report only the most critical items (Recommend MAX 3 hints):
            ## Scan Methods:
                No SeqScan, /*+ NoSeqScan(table) */ (Forces to not do sequential scan on the table.)
                No IndexScan, /*+ NoIndexScan(table) */ (Forces to not do index scan and index-only scan on the table.)
                No IndexOnlyScan, /*+ NoIndexOnlyScan(table) */ (Forces to not do index only scan on the table.)
                No BitmapScan, /*+ NoBitmapScan(table) */ (Forces to not do bitmap scan on the table.)
                             
            ## Join Methods:  (NestLoop is used for small table driving large table, HashJoin is used for large data volume)

                No Hash join, /*+ NoHashJoin(table table[ table...]) */ 
                No Nested loop join, /*+ NoNestLoop(table table[ table...]) */
                No Merge join, /*+ NoMergeJoin(table table[ table...]) */
                             
            ## Join Order:
                Leading, /*+ Leading(table table[ table...]) */ (Sets the join order of the tables, e.g., /*+ Leading(a b c) */)
                             
            ## Behavior control on Join:
                No Memorize, /*+ NoMemorize(table table[ table...]) */ (Inhibits the topmost join of a join among the specified tables from Memoizing the inner result.)
                            
            ##  Advanced Control:
                Cardinality estimation(rows) correction,  changes the row number estimation of joins that comes from restrictions in the planner. 
                If you want to use this hint, please give a detailed calculation process in the analysis.
                    /*+ Rows(a b #10) */ (Sets rows of join result to 10)   

        3. Provide a suggestion report on how to improve query performance using only these methods. If you believe the query is not worth optimizing with pg_hint_plan hints, explicitly state that in your report.
                             
        4. If the SQL uses a CTE and you determine the CTE should NOT be materialized, include the hint `/*+ NO_MATERIALIZE(table) */`. Use the following principles:
        - NO MATERIALIZE if: 
            1) The CTE is referenced multiple times in the query.
            2) The CTE is large and complex.
        - MATERIALIZE if:
            1) The CTE is referenced only once.
            2) The CTE is small and simple.
                                                            
        5. Return the results in the following format:

        </analysis>
            //Fill in with your analysis
        </analysis>

        </report>
            //Fill in your report
        </report>

        
        <input_sql>
        {input_sql}

        <physical_plan>
        {physical_plan}

        <data_statistics>
        {data_statistics}

    """)
    return prompt

     

def get_selection_prompt(input_sql,report):
    prompt = textwrap.dedent(f"""
        <Mission>
            You are an experienced DBA. Your mission is to provide the most efficient pg_hint_plan for the given SQL query based on the analysis report.
            You have been provided with:
            - A reference table illustrating how to use pg_hint_plan
            - <data_statistics> about the database
                                 
        <Steps>
            1. Based on the <report>, determine the single most effective pg_hint_plan to improve SQL performance.
            2. If the report indicates that pg_hint_plan optimization is warranted, return only the pg_hint_plan in JSON format as shown below. Otherwise, return an empty string ("").
            3. Classify hints into "context" hints and "preamble" hints if the SQL includes CTEs:
            - Context hints apply inside a CTE; you must specify the corresponding CTE name. If there are no CTEs, use an empty string ("") for both name and hints.
            - Preamble hints apply at the head of the query (before the main body).

        <Notation>
            1. Return only the pg_hint_plan content (without /*+ */ wrapper), not the entire SQL query.
            2. Provide as few hints as possible, formatted as a single string (not a list).

        <input_sql>
        {input_sql}

        <report>
        {report}

        Please return the answer in the following format:
        ```json
        {{
            "flag": {{flag}},           // true if pg_hint_plan is recommended, false otherwise
            "CTE_flag": {{CTE_flag}},   // true if the query includes CTEs, false otherwise
            "analysis": {{analysis}},   // Your analysis of the SQL query
            "context_pg_hint_plan": [
                {{
                    "CTE_name": "{{name}}",    // The CTE name for the context hint (or "" if none)
                    "pg_hint_plan": "{{hint_content}}"         // ONLY hint content, NO /*+ */ wrapper
                }},
                {{
                    ... // Include additional objects if multiple CTEs exist
                }}   
            ],
            "preamble_pg_hint_plan": "{{hint_content}}"  // ONLY hint content, NO /*+ */ wrapper
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




def refine_func(input_sql: str, context_pg_hint_plan: list, preamble_pg_hint_plan: str) -> str:
    result_sql = input_sql.strip()
    
    # 1. 处理 preamble hints (主查询前的hints)
    if preamble_pg_hint_plan and preamble_pg_hint_plan.strip():
        # 确保 hint 被正确包装
        if not preamble_pg_hint_plan.strip().startswith('/*+'):
            # 如果没有 /*+ 开头，添加完整格式
            formatted_hint = f"/*+ {preamble_pg_hint_plan.strip()} */"
        else:
            # 如果已经有格式，直接使用
            formatted_hint = preamble_pg_hint_plan.strip()
        
        result_sql = f"{formatted_hint}\n{result_sql}"
    
    # 2. 处理 CTE context hints
    for cte_hint in context_pg_hint_plan:
        if not cte_hint.get("CTE_name") or not cte_hint.get("pg_hint_plan"):
            continue
            
        cte_name = cte_hint["CTE_name"].strip()
        hint_str = cte_hint["pg_hint_plan"].strip()
        
        if not hint_str:
            continue
        
        # 确保 hint 格式正确
        if not hint_str.startswith('/*+'):
            hint_str = f"/*+ {hint_str} */"
        
        # 查找 CTE 定义位置
        pattern = re.compile(
            rf'''
            (                       # 捕获组1：前缀
                (?:WITH\s+|,\s*)
            )
            ({re.escape(cte_name)})  # 捕获组2：CTE名称
            \s+AS\s*                # 匹配 AS
            (\()                    # 捕获组3：左括号
            ''',
            re.IGNORECASE | re.VERBOSE
        )
        
        # 处理特殊的 NO_MATERIALIZE hint
        if f"NO_MATERIALIZE({cte_name})" in hint_str:
            hint_str = hint_str.replace(f"NO_MATERIALIZE({cte_name})", "").strip()
            if hint_str in ["/*+", "*/", "/*+ */"]:
                replacement = rf'\1{cte_name} AS NOT MATERIALIZED \3'
            else:
                replacement = rf'\1{cte_name} AS NOT MATERIALIZED \3 {hint_str}\n'
        else:
            replacement = rf'\1{cte_name} AS \3 {hint_str}\n'
        
        result_sql = pattern.sub(replacement, result_sql, count=1)
    
    return result_sql

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
    original_cost, operation = safe_get_cost_with_retry(dbms, input_sql)
    if not operation:
            print("Failed to get execution plan, skipping this query")
            res = {
                "id": item["id"],
                "original_query": item["rewritten_query"],
                "rewritten_query": item["rewritten_query"],
                "original_cost": 0,
                "hint_cost": 0,
                "error": "Failed to get execution plan"
            }
            ans.append(res)
            continue

    report_prompt = get_analysis_prompt(input_sql,operation)
    report_result = llm.get_GPT_response(report_prompt)
    report = extract_func(report_result,"report")
    # money_cost += llm.calc_money(report_prompt, report)

    prompt = get_selection_prompt(input_sql, report)
    # result = llm_assistant.get_GPT_response(prompt,json_format=True)
    result = llm.get_GPT_response(prompt)
    json_list = extract_json(result)
    if json_list and len(json_list) > 0:
        result = json_list[0]
    # print(result)
    # json_list = extract_json(llm.get_GPT_response(prompt))
    # if json_list and len(json_list) > 0:
    #     result = json_list[0]
    # print(result)
    # # money_cost += llm.calc_money(prompt,result)
    # # result = json.loads(llm.get_GPT_response(prompt))

    res = {}
    if result["flag"]:
        if result["CTE_flag"]:
            context_pg_hint_plan = list(result["context_pg_hint_plan"])
        else:
            context_pg_hint_plan = []
            
        preamble_pg_hint_plan = str(result["preamble_pg_hint_plan"])
        pg_hint_query = refine_func(input_sql, context_pg_hint_plan, preamble_pg_hint_plan)

        hint_cost, hint_operation = safe_get_cost_with_retry(dbms, pg_hint_query)
        print(f"hint_cost is : ",hint_cost)
        if hint_cost > original_cost * 1.1:
            res = {
                "id": item["id"],
                "original_query": item["rewritten_query"],
                "rewritten_query": item["rewritten_query"],
                "original_cost": original_cost,
                "hint_cost": hint_cost
            }
        else:
            res = {
                "id": item["id"],
                "original_query": item["rewritten_query"],
                "rewritten_query": pg_hint_query,
                "original_cost": original_cost,
                "hint_cost": hint_cost
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
    json.dump(ans, f, indent=4)
