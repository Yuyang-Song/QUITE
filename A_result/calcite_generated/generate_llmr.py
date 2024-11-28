import json
import csv 
import sys
sys.path.append("../")
sys.path.append("./")
import textwrap
import json
from utils.gpt import GPT
llm = GPT()
rules_pool = []
language_knowledge_file_path = "../language_knowledge.txt"
save_path = "./calcite_rule_regenerated.py"

def read_file_txt(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

language_knowledge = read_file_txt(language_knowledge_file_path)

def get_prompt(method, description, summary, language_knowledge):
    template = textwrap.dedent(f"""
        <Backgroud>
        You are an experenced DBA. You have Learned a new rewrite language named varSQL to describe the SQL rewrite rule.The detailed language defination and demonstraion are in <language_knowledge> part.
                               

        <mission>
        Your role is to rewrite the accrording description rule to the varSQL language. You are given the rule's method name, desctiptions and summary.
        The unuseful rule maybe like:
        unsueful example 1:"pattern": "<x1>","rewrite": "<x1>"
        unsueful example 2:"pattern": "SELECT ","rewrite": "SELECT"
        You should also consider the rule is efficient and concise.
        
        Let's think about this questions step by step.
        <steps>
        0. Read the language knowledge in <language_knowledge> part to understand the varSQL language.
        1. Read the rewrite rule's method,description and summary from <method>, <description> and <summary> part.
        2. Rewrite the rule according to the varSQL language.
        3. You just need to give the patern and the rewrite part of the rule and the following example orginal and rewritten sql.
        4. Return your response based on the <json_formate_templete>.

        <language_knowledge>
        {language_knowledge}      

        <method>
        {method}

        <description>
        {description}

        <summary>
        {summary}

        <json_format_templete>
        {{
            "pattern": "{{pattern_varSQL}}", //Fill this 'pattern_varSQL' with your varSQL pattern.
            "rewrite": {{rewrite_varSQL}},  // Fill this 'rewrite_varSQL' with your varSQL rewrite.
            "example_original_sql": {{sql}}, //Fill this 'sql' with the example original sql that can fit for the varSQL described rule.
            "example_rewritten_sql": {{sql}} //Fill this 'sql' with the example rewritten sql that can fit for the varSQL described rule.
        }}
    """)
    return template

# 读取 JSON 文件
with open('/home/orderheart/syy/sql_rewriter/A_result/calcite_generated/calcite_rule_regenerate.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

result_data = []
# 遍历每个规则类别（Aggregates, Filters, Join 等）
for category, rules in data.items():
    print(f"Category: {category}")
    for rule in rules:
        method = rule["method"]
        description = rule["description"]
        summary = rule["summary"]
        prompt = get_prompt(method, description, summary, language_knowledge)
        response = llm.get_GPT_response(prompt, json_format=True)
        # 打印每个规则的 method、description 和 summary
        print(f"############################################")
        print(f"  Method: {rule['method']}")
        print(f"  Description: {rule['description']}")
        print(f"  Summary: {rule['summary']}")
        print(f"############################################")
        print()  # 添加空行以便阅读
        data = {
            "name": method,
            "key": method,
            "pattern": response["pattern"],
            "rewrite": response["rewrite"],
            "example_original_sql": response["example_original_sql"],
            "example_rewritten_sql": response["example_rewritten_sql"],
            "constraints": "",
            "actions": "",
            "database": "postgresql"
        }
        result_data.append(data)
        # # 打印每个规则的 method、description 和 summary
        # print(f"  Method: {rule['method']}")
        # print(f"  Description: {rule['description']}")
        # print(f"  Summary: {rule['summary']}")
        # print()  # 添加空行以便阅读


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