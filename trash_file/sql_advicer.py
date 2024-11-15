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

class sql_advicer:
    def __init__(self,input_sql):
        """
        calcite_path: the path of the calcite overview.json. calcite knowledge pool has 5 fixed rewrite rules based on LR and LLM-R2.
        
        oracle_path: the path of the oracle overview.json. oracle knowledge pool has 9 rewrite methods provided by web crawler.
        
        sql_server_path: the path of the sql_server overview.json. sql_server knowledge pool has 12 rewrite methods provided by web crawler.
        
        """
        self.calcite_rule_path = f"./knowledge_pool/official_documents/calcite/overview.json"
        self.calcite_rule_list = ["Aggregates_rewrite_rules","Filters_rewrite_rules","Join_rewrite_rules","Sort_rewrite_rules","Union_rewrite_rules"]
        
        self.oracle_path = f"./knowledge_pool/official_documents/oracle/overview.json"
        self.sql_server_path = f"./knowledge_pool/official_documents/sql_server/overview.json"
        self.input_sql = input_sql
        self.gpt = GPT()
        
    def read_overview_json(self, path):
        with open(path, 'r') as f:
            data = json.load(f)
        return data
    
    def read_method_text_file(self, path, method):
        text_file_path = os.path.join(path, f"{method}.txt")
        if os.path.exists(text_file_path):
            with open(text_file_path, 'r') as f:
                return f.read()
        else:
            return None
        
    def get_analyse_from_gpt(self,ref_file):
        prompt = textwrap.dedent(f"""
            <mission>
            you are an experenced DBA, your mission is to provide a rewrite suggestion to the input_sql with the reference file.
            Let's think about this questions step by step.
            
            <steps>
            0. Read the original sql to be rewritten from the <input_sql>.
            1. Read the rewrite methods from the <ref_file>. 
            2. Choose the rewrite methods you think are suitable for the <input_sql>.
            3. Analyse the input_sql based on the rewrite methods you have chosen.
            4. Return the rewrite suggestion list and the analyse based on the <json_formate_templete>.
        
            <input_sql>
            {self.input_sql}
            
            <ref_file>
            {ref_file}

            <json_format_templete>
            {{
                "rewrite_suggestion_list": {{list}}, //fill the 'list' with the rewrite methods you have read from the <ref_file>, if you have choose several methods, please use ',' to split them. And if you think these methods are not suitable, please fill the 'list' with 'None'.
                "rewrite_analyse": {{analyse}}, //fill the 'analyse' with the analyse of the input_sql based on the rewrite methods you have chosen. Make the analyse clear and easy to understand. If rewrite_suggestion_list is 'None', please fill the 'analyse' with 'None'.
            }}
        """)
        response = self.gpt.get_GPT_response(prompt,json_format=True)
        return response

        
    def get_calcite_rule_from_gpt(self):
        calcite_data = self.read_overview_json(self.calcite_rule_path)
        prompt = textwrap.dedent(f"""
            <mission>
            you are an experenced DBA, your mission is to provide a rewrite suggestion to the input_sql with the reference file.
            Let's think about this questions step by step.
            
            <steps>
            0. Read the original sql to be rewritten from the <input_sql>.
            1. Read the rewrite methods category from the <rule_list>. 
            2. Roughly chose the potential rewrite methods category, and dive into this category to chose a more concere rewrite rules based on the <ref_file>.
            3. Analyse the input_sql based on the rewrite methods you have chosen.
            4. Return the rewrite suggestion list and the analyse based on the <json_formate_templete>.

            <input_sql>
            {self.input_sql}
            
            <rule_list>
            {self.calcite_rule_list}
            
            <input_sql>
            {calcite_data}

            <json_format_templete>
            {{
                "rewrite_methods_category": {{category}}, //fill the 'category' with the rewrite methods category you have read from the <rule_list>. If you think these methods are not suitable, please fill the 'category' with 'None'.
                "rewrite_detailed_methods": {{list}}, //fill the 'list' with the rewrite methods you have read from the <ref_file>, if you have choose several methods, please use ',' to split them. And if you think these methods are not suitable, please fill the 'list' with 'None'.
                "rewrite_analyse": {{analyse}}, //fill the 'analyse' with the analyse of the input_sql based on the rewrite methods you have chosen. Make the analyse clear and easy to understand. If rewrite_suggestion_list is 'None', please fill the 'analyse' with 'None'.
            }}
        """)
        response = self.gpt.get_GPT_response(prompt,json_format=True)
        return response
    
    def get_reversed_response(self,sql_server_response,oracle_response):
        prompt = textwrap.dedent(f"""
            <mission>
            you are an experenced DBA, your mission is to summary the both sql rewrite suggestions named <sql_server_response> and <oracle_response>, and re-analyse each of the rewrite methods, give a detailed rewrite way to the input_sql.
            Let's think about this questions step by step.
            
            <steps>
            0. Read the original sql to be rewritten from the <input_sql>.
            1. Read the rewrite suggestion from the <sql_server_response> and <oracle_response>. 
            2. Compare the rewrite suggestion from the <sql_server_response> and <oracle_response>, and re-analyse each of the rewrite methods, give a detailed rewrite way to the input_sql.
            3. Return the reversed rewrite suggestion and the analyse based on the <json_formate_templete>.

            <input_sql>
            {self.input_sql}
            
            <sql_server_response>
            {sql_server_response}

            <oracle_response>
            {oracle_response}

            <json_format_templete>
            {{
                "reversed_rewrite_suggestion": {{list}}, //fill the 'list' with the rewrite suggestion you think is more suitable. If you think the sql_server_response is more suitable, please fill the 'list' with the sql_server_response, and vice versa.
                "reversed_rewrite_analyse": {{analyse}}, //fill the 'analyse' with a detailed rewriting procedure. For example, specify which parts of sql need to be rewritten and how to rewrite. Make the analyse clear and easy to understand. If rewrite_suggestion_list is 'None', please fill the 'analyse' with 'None'.
            }}
        """)
        response = self.gpt.get_GPT_response(prompt,json_format=True)
        # print(f"{response["reversed_rewrite_suggestion"]}\n")
        # print(f"{response["reversed_rewrite_analyse"]}\n")
        return response
    
    def pipeline_suggestion(self):
        sql_server_data= self.read_overview_json(self.sql_server_path)
        oracle_data = self.read_overview_json(self.oracle_path)
        
        sql_server_response = self.get_analyse_from_gpt(sql_server_data)
        oracle_response = self.get_analyse_from_gpt(oracle_data)
        
        reversed_response = self.get_reversed_response(sql_server_response,oracle_response)
        return reversed_response
    
    def pipeline_rewrite_rule(self):
        calcite_responce = self.get_calcite_rule_from_gpt()
        return calcite_responce
    
        
# test read file function
# input_sql = "select n_name, sum(l_extendedprice * (1 - l_discount)) as revenue from customer, orders, lineitem, supplier, nation, region where c_custkey = o_custkey and l_orderkey = o_orderkey and l_suppkey = s_suppkey and c_nationkey = s_nationkey and s_nationkey = n_nationkey and n_regionkey = r_regionkey and r_name = 'ASIA' and o_orderdate >= date '1994-01-01' and o_orderdate < date '1994-01-01' + interval '1year' group by n_name order by revenue desc;"
# test_model = sql_advicer(input_sql)
# sql_server_data= test_model.read_overview_json(test_model.sql_server_path)
# oracle_data = test_model.read_overview_json(test_model.oracle_path)
# # print(test_data)

# # test read calcite rule function
# calcite_rule = test_model.get_calcite_rule_from_gpt(oracle_data)
# print(f"{calcite_rule["rewrite_methods_category"]}\n")
# print(f"{calcite_rule["rewrite_detailed_methods"]}\n")
# print(f"{calcite_rule["rewrite_analyse"]}\n")

# # test read text file function and gpt function
# sql_server_response = test_model.get_analyse_from_gpt(sql_server_data)
# oracle_response = test_model.get_analyse_from_gpt(oracle_data)

# print(f"{sql_server_response["rewrite_suggestion_list"]}\n")
# print(f"{sql_server_response["rewrite_analyse"]}\n")

# print(f"{oracle_response["rewrite_suggestion_list"]}\n")
# print(f"{oracle_response["rewrite_analyse"]}\n")

