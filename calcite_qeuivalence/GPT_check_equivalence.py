import os
import json
import textwrap
import sys
from dotenv import load_dotenv
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
load_dotenv(dotenv_path='../config_file/.env')
from utils.gpt import GPT

import textwrap
import json

class GPT_check:
    def __init__(self,input_file_path,output_file_path):
        self.gpt = GPT()
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.money = 0.0
    
    def check_equivalence(self,original_query,rewritten_query):
        prompt = textwrap.dedent(f"""
        <mission>
        You are an experienced SQL developer and you are tasked with checking the equivalence of two SQL queries.
        Let's think step by steps to check the equivalence of two SQL queries.
        <steps>
        1. read the original sql query and rewritten sql query first.
        2. analysis the diffece between the original sql query and rewritten sql query.
        3. given the judge of the equivalence of the two SQL queries based on your analysis.
        4. return the json formate as the demand mentioned.
        
        <original_query>
        {original_query}
        
        <rewritten_query>
        {rewritten_query}
        
        <demand>
        <json_format_templete>
        {{
            "analysis": {{analusis}},  // Fill this 'analysis' with your analysis.
            "equivalence": {{equivalence}}  // Fill this 'equivalence' with 'true' or 'false' based on your analysis.
        }}
        """)
        response = self.gpt.get_GPT_response(prompt,json_format=True)
        self.money += self.gpt.calc_money(prompt,response)
        return response
    
    def process(self):
        with open(self.input_file_path, 'r') as file:
            data = json.load(file)
            result = []
            iteration = 1
            for item in data:
                print(f"Processing query {iteration}...")
                iteration += 1
                original_query = item['original_query']
                rewritten_query = item['rewritten_query']
                reanswer = self.check_equivalence(original_query,rewritten_query)
                data = {
                    "original_query": original_query,
                    "rewritten_query": rewritten_query,
                    "equivalence": reanswer['equivalence'] 
                }
                result.append(data)
                print(f"the equivalence of the two SQL queries is {reanswer['equivalence']}")
            with open(self.output_file_path, 'w') as json_file:
                json_file.write(json.dumps(result, indent=4))
            print(f"Processed {len(data)} SQL queries into JSON format.")
            print(f"Output saved to {self.output_file_path}")
    
    def cal_num(self):
        with open(self.output_file_path, 'r') as file:
            data = json.load(file)
            num = 0
            for item in data:
                # bloolean algebra
                if item['equivalence'] == True:
                    num += 1
            return num


input_file_path = "./sql_queries.json"
output_file_path = "./check_result_4omini.json"
model = GPT_check(input_file_path,output_file_path)
model.process()
# Total cost: 0.8967549999999997 model :4o😁
# Total cost:0.031185599999999997 :4o-mini
print(f"Total cost: {model.money}")
# Number of equivalent queries: 177 model :4o
# Number of equivalent queries: 90 model :4o-mini
print(f"Number of equivalent queries: {model.cal_num()}")
