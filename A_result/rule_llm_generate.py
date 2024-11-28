import json
import csv 
import sys
sys.path.append("../")
sys.path.append("./")
import textwrap
import json
from utils.gpt import GPT
llm = GPT()
language_knowledge_file_path = "./language_knowledge.txt"
save_path = "./calcite_rule_regenerated.py"
result_data = []
def read_file_txt(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

language_knowledge = read_file_txt(language_knowledge_file_path)
analysis = {    "agent_candidate_sql": "WITH min_supplycost AS (\n    SELECT p_partkey, MIN(ps_supplycost) AS min_cost\n    FROM partsupp ps\n    JOIN supplier s ON ps.s_suppkey = s.s_suppkey\n    JOIN nation n ON s.s_nationkey = n.n_nationkey\n    JOIN region r ON n.n_regionkey = r.r_regionkey\n    WHERE r.r_name = 'ASIA'\n    GROUP BY p_partkey\n)\nSELECT s.s_acctbal, s.s_name, n.n_name, p.p_partkey, p.p_mfgr, s.s_address, s.s_phone, s.s_comment\nFROM part p\nJOIN partsupp ps ON p.p_partkey = ps.ps_partkey\nJOIN supplier s ON ps.ps_suppkey = s.s_suppkey\nJOIN nation n ON s.s_nationkey = n.n_nationkey\nJOIN region r ON n.n_regionkey = r.r_regionkey\nJOIN min_supplycost msc ON p.p_partkey = msc.p_partkey AND ps.ps_supplycost = msc.min_cost\nWHERE p.p_size = 46\nAND p.p_type LIKE '%NICKEL'\nAND r.r_name = 'ASIA'\nORDER BY s.s_acctbal DESC, n.n_name, s.s_name, p.p_partkey\nLIMIT 100;",    "agent_analysis": "The original query uses implicit joins and a correlated subquery with a MIN function, which can degrade performance. The subquery is recalculated for each row, which is inefficient. Additionally, the LIKE '%NICKEL' predicate can hinder performance, and the query lacks explicit joins, which can lead to confusion and poor readability. The rewritten query uses explicit joins and optimizes the subquery by converting it into a Common Table Expression (CTE) to precompute the minimum supply cost.",    "is_optimized": "true",    "agent_suggestions": [        "Rewrite the query using explicit JOIN syntax for better clarity and optimization.",        "Convert the subquery with MIN(ps_supplycost) into a CTE to avoid recalculating it for every row in the outer query.",        "Consider indexing on columns used in the joins and where clauses, especially 'p_partkey', 'ps_partkey', 's_suppkey', 'ps_supplycost', and 's_acctbal'.",        "Review the use of the LIKE '%NICKEL' predicate and consider alternatives like full-text indexing if appropriate."    ] }


def get_prompt(original_query, language_knowledge):
    template = textwrap.dedent(f"""
        <Backgroud>
        You are an experenced DBA. You have Learned a new rewrite language named varSQL to describe the SQL rewrite rule.The detailed language defination and demonstraion are in <language_knowledge> part.
                               

        <mission>
        Your role is to generate the query rewrite rule to the varSQL language based on the analysis. You are given the detailed SQL optimization analysis.
        
        Let's think about this questions step by step.
        <steps>
        0. Read the language knowledge in <language_knowledge> part to understand the varSQL language.
        1. Read the orginal query from <original_query> part. Read the detailed SQL analysis from <analysis> part.
        2. Generate the varSQL rule according to the varSQL language. notice that you should genrate the rewrite rule one by one, and the rule should be efficient and concise.
        3. You just need to give the patern and the rewrite part of the rule.
        4. Return your response based on the <json_formate_templete>.

        <language_knowledge>
        {language_knowledge}      

        <original_query>
        {original_query}

        <analysis>
        {analysis}

        <json_format_templete>
        {{
            {{
                "id" : {{id}}, //Fill this 'id' with the rule id.
                "name": "{{name}}", //Fill this 'name' with the rule name you want to add.
                "pattern": "{{pattern_varSQL}}", //Fill this 'pattern_varSQL' with your varSQL pattern.
                "rewrite": {{rewrite_varSQL}},  // Fill this 'rewrite_varSQL' with your varSQL rewrite.
            }},
            {{
                "id" : {{id}}, //Fill this 'id' with the rule id.
                "name": "{{name}}", //Fill this 'name' with the rule name you want to add.
                "pattern": "{{pattern_varSQL}}", //Fill this 'pattern_varSQL' with your varSQL pattern.
                "rewrite": {{rewrite_varSQL}},  // Fill this 'rewrite_varSQL' with your varSQL rewrite.
            }},
            ... // if you can genrate more than one rule, you can add more rule here.
        }}
    """)
    return template

original_query = "select s_acctbal, s_name, n_name, p_partkey, p_mfgr, s_address, s_phone, s_comment from part, supplier, partsupp, nation, region where p_partkey = ps_partkey and s_suppkey = ps_suppkey and p_size = 46 and p_type like '%NICKEL' and s_nationkey = n_nationkey and n_regionkey = r_regionkey and r_name = 'ASIA' and ps_supplycost = ( select min(ps_supplycost) from partsupp, supplier, nation, region where p_partkey = ps_partkey and s_suppkey = ps_suppkey and s_nationkey = n_nationkey and n_regionkey = r_regionkey and r_name = 'ASIA' ) order by s_acctbal desc, n_name, s_name, p_partkey limit 100;"

# prompt = get_prompt(original_query, language_knowledge)

# response = llm.get_GPT_response(prompt, json_format=True)
# # print(response)
# # print(type(response))

# response = response["rules"]
# rule_keys = []
# rules_pool = []
# for rule in response:
#     data ={
#         "id": rule['id'],
#         "name": rule['name'],
#         "key": rule['name'],
#         "pattern": rule['pattern'],
#         "rewrite": rule['rewrite'],
#         "constraints": "",
#         "actions": "",
#         "database": "postgresql"
#     }
#     rule_keys.append(rule['name'])
#     rules_pool.append(data)

# print(rules_pool)
# print(type(rules_pool))

from core.query_patcher import QueryPatcher
from core.query_rewriter import QueryRewriter
from core.rule_parser import RuleParser
from mo_sql_parsing import parse

def get_rule(key: str) -> dict:
    rule = next(filter(lambda x: x['key'] == key, rules_pool), None)
    rule['pattern_json'], rule['rewrite_json'], rule['mapping'] = RuleParser.parse(rule['pattern'], rule['rewrite'])
    rule['constraints_json'] = RuleParser.parse_constraints(rule['constraints'], rule['mapping'])
    rule['actions_json'] = RuleParser.parse_actions(rule['actions'], rule['mapping'])
    return {
        'id': rule['id'],
        'key': rule['key'], 
        'name': rule['name'], 
        'pattern': rule['pattern'], 
        'pattern_json': json.loads(rule['pattern_json']),
        'constraints': rule['constraints'],
        'constraints_json': json.loads(rule['constraints_json']),
        'rewrite': rule['rewrite'],
        'rewrite_json': json.loads(rule['rewrite_json']),
        'actions': rule['actions'],
        'actions_json': json.loads(rule['actions_json']),
        'mapping': json.loads(rule['mapping']),
        'database': rule['database']
    }


rules_pool = [{'id': 1, 'name': 'Convert Implicit Joins to Explicit Joins', 'key': 'Convert Implicit Joins to Explicit Joins', 'pattern': 'SELECT <<s>> FROM <t1>, <t2>, <t3>, <t4>, <t5> WHERE <t1>.<c1> = <t3>.<c1> AND <t2>.<c2> = <t3>.<c2> AND <<p>>', 'rewrite': 'SELECT <<s>> FROM <t1> JOIN <t3> ON <t1>.<c1> = <t3>.<c1> JOIN <t2> ON <t2>.<c2> = <t3>.<c2> WHERE <<p>>', 'constraints': '', 'actions': '', 'database': 'postgresql'}, {'id': 2, 'name': 'Optimize Subquery with CTE', 'key': 'Optimize Subquery with CTE', 'pattern': 'SELECT <<s>> FROM <t1>, <t2>, <t3>, <t4>, <t5> WHERE <<p1>> AND <c1> = (SELECT MIN(<c2>) FROM <t3>, <t4>, <t5> WHERE <<p2>>)', 'rewrite': 'WITH min_supplycost AS (SELECT <c3>, MIN(<c2>) AS min_cost FROM <t3> JOIN <t4> ON <t3>.<c4> = <t4>.<c4> JOIN <t5> ON <t4>.<c5> = <t5>.<c5> WHERE <<p2>> GROUP BY <c3>) SELECT <<s>> FROM <t1> JOIN <t2> ON <t1>.<c6> = <t2>.<c6> JOIN min_supplycost ON <t1>.<c3> = min_supplycost.<c3> AND <t2>.<c2> = min_supplycost.min_cost WHERE <<p1>>', 'constraints': '', 'actions': '', 'database': 'postgresql'}]
# rule_keys = ['Convert Implicit Joins to Explicit Joins', 'Optimize Subquery with CTE']
rule_keys = ['Convert Implicit Joins to Explicit Joins']
rules = [get_rule(k) for k in rule_keys]

database = "postgresql"
rewritten_query, rewriting_path = QueryRewriter.rewrite(original_query, rules)
rewritten_query = QueryPatcher.patch(rewritten_query, database)
formatted_original_query = QueryRewriter.reformat(original_query)
formatted_rewritten_query = QueryRewriter.reformat(rewritten_query)

result_data.append(formatted_original_query)

print(f"original query: {original_query}")
print(f"rewritten query: {rewritten_query}")
print(f"rewriting path:{rewriting_path}")

def save_file(result,save_path):
    with open(save_path, 'w') as f:
        json.dump(result, f, indent=4)


        # 更新 save_path.py 文件
        with open(save_path, 'r') as f:
            content = f.read()

        # print(rules_pool)
        # 替换原有的 rules_pool 定义
        new_content = content.replace("rules_pool = []", f"rules_pool = {json.dumps(rules_pool, indent=4)}")

        # 将更新后的内容写回文件
        with open(save_path, 'w') as f:
            f.write(new_content)

save_file(result_data,save_path)