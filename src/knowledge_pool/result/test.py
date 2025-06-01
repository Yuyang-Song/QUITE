from openai import OpenAI
import json
import asyncio
import sys
import json
import tiktoken
sys.path.append('../')
sys.path.append('./utils')
sys.path.append('./')
import textwrap



class GPT:
    def __init__(self):
        self.api_key = "sk-8453dce8250848cfbdfed0c638ed6410"
        self.model = "qwen-plus"
        self.base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        self.client = OpenAI(
            api_key= self.api_key,
            base_url = self.base_url
        )

    def get_GPT_response(self, prompt, system_message=None, json_format=False):
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})
        
        if json_format:
            completion = self.client.chat.completions.create(
                temperature=0.6,
                model=self.model,
                response_format={"type": "json_object"},
                messages=messages,
                stream=True
            )
            full_response = ""
            for chunk in completion:
                if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content:
                    chunk_text = chunk.choices[0].delta.content
                    print(chunk_text, end="", flush=True)
                    full_response += chunk_text
            print()
            return json.loads(full_response)
            
        else:
            completion = self.client.chat.completions.create(
                temperature=0.0,
                model=self.model,
                messages=messages,
                stream=True
            )
            full_response = ""
            for chunk in completion:
                if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content:
                    chunk_text = chunk.choices[0].delta.content
                    print(chunk_text, end="", flush=True)
                    full_response += chunk_text
            print()
            return full_response
    
    
# Test with system message
gpt = GPT()

# Example 1: With a system message
# prompt = "What is the capital of France?"
# response = gpt.get_GPT_response(prompt, json_format=False)
# print("This is the response of the assistant:")
# print(response)

with open("result.json", "r") as f:
    data = json.load(f)

ans = []
iteration = 1
for item in data:
    print(f"this is the {iteration}th item / {len(data)}")
    iteration += 1
    group = item["group"] 
    if "query_optimization" not in group:
        ans.append(item)
    else:
        if isinstance(group, str):
            prompt = textwrap.dedent(f"""
            <Mission>
            You are a SQL query optimization expert. And your mission is to classify the group of the SQL query optimization task.
            Each task contains a question description, a question query example, an answer summary, and an answer query example.
            You should classify the group of SQL query optimization tasks into one categories:
            (1) join_optimization
            (2) constant_folding
            (3) predicate_simplification
            (4) other
            
            <content>
            question_description: {item["question_description"]}
            question_query_example: {item["question_query_example"]}
            answer_summary: {item["answer_summary"]}
            answer_query_example: {item["answer_query_example"]}

            
            You should return the group in JSON format as follow:
            {{
                {{analysis}} : ,//Fill in the analysis
                {{group}} : ,//Fill in the group, note that the group should be one of the four categories, including "other"
            }}  
            """)
            response = gpt.get_GPT_response(prompt, json_format=True)
            group = response["group"]
            ans.append(
                {
                    "group": group,
                    "question_description": item["question_description"],
                    "question_query_example": item["question_query_example"],
                    "answer_summary": item["answer_summary"],
                    "answer_query_example": item["answer_query_example"],
                    "id": item["id"]
                }
            )
        elif isinstance(group,list): # len(group) >=2:
            # remove the query_optimization in group list
            group.remove("query_optimization")
            ans.append(
                {
                    "group": group,
                    "question_description": item["question_description"],
                    "question_query_example": item["question_query_example"],
                    "answer_summary": item["answer_summary"],
                    "answer_query_example": item["answer_query_example"],
                    "id": item["id"]
                }
            )


with open("result_fiexed.json", "w") as f:
    json.dump(ans, f, indent=4)