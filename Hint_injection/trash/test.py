# # input_query = """
# # WITH filtered_parts AS (
# #     SELECT p_partkey 
# #     FROM part 
# #     WHERE p_brand = 'Brand#32' 
# #     AND p_container = 'WRAP PKG'
# # )
# # SELECT SUM(l.l_extendedprice) / 7.0 AS avg_yearly
# # FROM filtered_parts p
# # JOIN lineitem l ON p.p_partkey = l.l_partkey
# # JOIN (
# #     SELECT l_partkey, 0.2 * AVG(l_quantity) AS avg_quantity
# #     FROM lineitem l
# #     JOIN filtered_parts p ON l.l_partkey = p.p_partkey
# #     GROUP BY l_partkey
# # ) subq ON l.l_partkey = subq.l_partkey
# # WHERE l.l_quantity < subq.avg_quantity;
# # """

# # inline_hints = [{
# #     "CTE_name": "filtered_parts",
# #     "inline_pg_hint_plan": "/*+ Inline(filtered_parts) Rows(filtered_parts 2127) */"
# # }]

# # outline_hint = "/*+ Leading(filtered_parts lineitem subq) HashJoin(filtered_parts lineitem) HashJoin(lineitem subq) */"

# input_query ="WITH filtered_parts AS (\n    SELECT p_partkey, p_mfgr\n    FROM part\n    WHERE p_size = 6 AND p_type LIKE '%NICKEL'\n),\nmin_supply_cost AS (\n    SELECT ps_partkey, MIN(ps_supplycost) as min_cost\n    FROM partsupp ps\n    JOIN supplier s ON ps.ps_suppkey = s.s_suppkey\n    JOIN nation n ON s.s_nationkey = n.n_nationkey\n    JOIN region r ON n.n_regionkey = r.r_regionkey\n    WHERE r.r_name = 'EUROPE'\n    GROUP BY ps_partkey\n)\nSELECT s.s_acctbal, s.s_name, n.n_name, p.p_partkey, p.p_mfgr, \n       s.s_address, s.s_phone, s.s_comment\nFROM filtered_parts p\nJOIN partsupp ps ON p.p_partkey = ps.ps_partkey\nJOIN min_supply_cost msc ON ps.ps_partkey = msc.ps_partkey AND ps.ps_supplycost = msc.min_cost\nJOIN supplier s ON ps.ps_suppkey = s.s_suppkey\nJOIN nation n ON s.s_nationkey = n.n_nationkey\nORDER BY s.s_acctbal DESC, n.n_name, s.s_name, p.p_partkey\nLIMIT 100;"

# inline_hints =     [
#         {
#             "CTE_name": "filtered_parts",
#             "inline_pg_hint_plan": "/*+ Inline(filtered_parts) */"
#         },
#         {
#             "CTE_name": "min_supply_cost",
#             "inline_pg_hint_plan": " "
#         }
#     ]

# outline_hint = "/*+ HashJoin(s n) HashJoin(ps s) Leading(filtered_parts ps msc s n) Rows(ps 3333282) Rows(s 99999) */"

# # print(type(inline_hints))
# import re

#         # pattern = re.compile(
#         #     rf'((?:WITH|,)\s+){cte_name}\s+AS\s*(?=\()',
#         #     re.IGNORECASE
#         # )

# def refine_func(input_sql: str, inline_pg_hint_plan: list, outline_pg_hint_plan: str) -> str:
#     # 处理外部提示
#     hinted_sql = f"{outline_pg_hint_plan}\n{input_sql.strip()}"
    
#     # 处理内联提示
#     for cte_hint in inline_pg_hint_plan:
#         cte_name = cte_hint["CTE_name"]
#         hint_str = cte_hint["inline_pg_hint_plan"].strip()
        
#         # 匹配两种模式：
#         # 1. WITH + CTE_NAME + AS + (
#         # 2. 逗号 + CTE_NAME + AS + (

#         pattern = re.compile(
#             rf'''
#             (                       # 捕获组1：前缀（WITH或逗号及空格）
#                 (?:WITH\s+|,\s*)
#             )
#             ({re.escape(cte_name)})  # 捕获组2：CTE名称
#             \s+AS\s*                # 匹配 AS 及空格
#             (\()                    # 捕获组3：左括号
#             ''',
#             re.IGNORECASE | re.VERBOSE
#         )
        
#         # 处理提示
#         if f"Inline({cte_name})" in hint_str:
#             hint_str = hint_str.replace(f"Inline({cte_name}) ", "").strip()
#             if hint_str != "/*+ */":
#                 replacement = rf'\1{cte_name} AS NOT MATERIALIZED ( {hint_str}'
#             else:
#                 replacement = rf'\1{cte_name} AS NOT MATERIALIZED ('
#         else:
#             if hint_str != "/*+ */":
#                 replacement = rf'\1{cte_name} AS ( {hint_str}'
#             else:
#                 replacement = rf'\1{cte_name} AS ('
            
            
#         # 执行替换
#         hinted_sql = pattern.sub(replacement, hinted_sql, count=1)
    
#     return hinted_sql
# # def refine_func(input_sql: str, inline_pg_hint_plan: list, outline_pg_hint_plan: str) -> str:
# #     # 处理外部提示
# #     hinted_sql = f"{outline_pg_hint_plan}\n{input_sql.strip()}"
    
# #     # 处理内联提示
# #     for cte_hint in inline_pg_hint_plan:
# #         cte_name = cte_hint["CTE_name"]
# #         hint_str = cte_hint["inline_pg_hint_plan"].strip()
        
# #         # 正则匹配模式：WITH + 空格 + CTE名称 + 空格 + AS + 空格 + (
# #         pattern = re.compile(
# #             rf'(WITH\s+{cte_name}\s+AS\s*)(?=\()',
# #             re.IGNORECASE
# #         )
        
# #         # 检查是否需要添加 NOT MATERIALIZED
# #         if f"Inline({cte_name})" in hint_str:
# #             hint_str = hint_str.replace(f"Inline({cte_name}) ", "")
# #             replacement = rf'\1NOT MATERIALIZED {hint_str} '
# #         else:
# #             replacement = rf'\1 {hint_str}'
            
# #         # 执行替换
# #         hinted_sql = pattern.sub(replacement, hinted_sql, count=1)
    
# #     return hinted_sql

# result = refine_func(input_query, inline_hints, outline_hint)
# print(result)



import json
import re


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

# 示例使用
text = '''
```json
{
    "flag": false,
    "CTE_flag": false,
    "analysis": "Based on the analysis report, the current execution plan already uses Hash Joins for all table combinations, which is appropriate given the large table sizes involved. The planner has correctly chosen efficient join methods considering the cardinality differences between the tables (customer: 1.5M rows, orders: 15M rows, lineitem: 60M rows, nation: 24 rows). While there is a minor overestimation of the nation table size, this doesn't significantly impact the overall plan efficiency. Since the join methods are already optimal and the join order appears reasonable, there's no need to add pg_hint_plan hints for this query.",
    "inline_pg_hint_plan": [
        {
            "CTE_name": "",
            "inline_pg_hint_plan": ""
        }
    ],
    "outline_pg_hint_plan": ""
}
```
'''
json_obj = extract_json(text)
print(json_obj)
print(type(json_obj))