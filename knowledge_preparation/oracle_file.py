"""
structured knowledge about Oracle trnasformisson script with LLM
"""
import os
import json
import textwrap
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from utils.gpt import GPT


class Oracle_file_preparation_model(GPT):
    def __init__(self, db = "postgres"):
        super().__init__()
        self._define_path()

    def _define_path(self):
        self.oracle_path = f"../knowledge_pool/official_documents/oracle"
        self.oracle_file_path = f"../knowledge_pool/official_documents/oracle/Design_Considerations"

#     def get_description_from_gpt(self):


    # read the json content of the overview.json
    def read_overview_json(self):
        overview_json_path = os.path.join(self.oracle_path, "overview.json")
        with open(overview_json_path, 'r') as f:
            data = json.load(f)
        return data

    # read the corresponding text file according to the method value
    def read_method_text_file(self, method):
        text_file_path = os.path.join(self.oracle_file_path, f"{method}.txt")
        if os.path.exists(text_file_path):
            with open(text_file_path, 'r') as f:
                return f.read()
        else:
            return None

    # get GPT response
    def get_summary_from_gpt(self, content):
        prompt=textwrap.dedent(f"""
            <mission>
            Suppose you are an experenced DBA, you are required to provide a summary of the following content.
            1. Summarize the following content.
            2. Meanwhile, you need to return the anwser based on the json format demand as follows:
            
            <content>
            {content}
            
            <demand>
            JSON FORMAT TEMPLATE:
            {{
                "orale_summary": {{summary}}, //fill the 'summary' with the summary of the content
            }}
        
        """)
        answer = self.get_GPT_response(prompt,json_format = True)
        print(f"""
              {answer}
              """)
        self.token += self.calc_token(prompt, answer)
        self.money += self.calc_money(prompt, answer)
        return answer
        # get GPT response
        
    def get_description_from_gpt(self, method, summary):
        prompt=textwrap.dedent(f"""
            <mission>
            Suppose you are an experenced DBA, you are required to provide a detailed description of the following content.
            1. Give the SQL rewrite {method} description accroding to the following summary.
            2. Make sure your description is concise, only use one brief sentence.
            3. Meanwhile, you need to return the anwser based on the json format demand as follows:

            <summary>
            {summary}
            
            <demand>
            JSON FORMAT TEMPLATE:
            {{
                "orale_description": {{description}}, //fill the 'description' with the description of the content
            }}
        
        """)
        answer = self.get_GPT_response(prompt,json_format = True)
        self.token += self.calc_token(prompt, answer)
        self.money += self.calc_money(prompt, answer)
        return answer

    # input summary into json format file
    def write_summary_to_json(self, data):
        overview_json_path = os.path.join(self.oracle_path, "overview.json")
        with open(overview_json_path, 'w') as f:
            json.dump(data, f, indent=4)

    # pipelined function to read, process and write back to json
    def pipeline(self):
        # 1. load the overview json file
        data = self.read_overview_json()
        # 2. iterate the method  value in the overview json file
        for item in data:
            method = item['method']
            method_content = self.read_method_text_file(method)

            if method_content:
                # 3. get gpt response
                summary = self.get_summary_from_gpt(method_content)
                input_summary = summary['orale_summary']
                description = self.get_description_from_gpt(method,summary)
                input_description = description['orale_description']
                print(f"the processing method '{method}' is: {method_content}\n")
                print(f"the summary of the method '{method}' is: {input_summary}")
                print(f"the description of the method '{method}' is: {input_description}\n")
                # 4. update the summary amd the decription value in the overview json file
                item['summary'] = input_summary
                item['description'] = input_description

        # 5. rewrite overview.json file
        self.write_summary_to_json(data)
        # print(f"the total cost of the gpt: {self.money}")
        
# test
# model = Oracle_file_preparation_model()
# model.pipeline()

