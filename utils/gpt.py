from openai import OpenAI
from dotenv import load_dotenv
import json
import os
import re
import tiktoken
import json

class GPT:
    # init function to initialize the GPT class using gpt-4o, ignoring the token and money cost termerarily
    def __init__(self):
        load_dotenv(dotenv_path='../config_file/.env')  # Load environment variables from .env file
        self.api_key = os.getenv("OPENAI_API_KEY")  # Get the API key from the environment variable
        self.model = os.getenv("OPENAI_MODEL")
        self.money = 0
        self.token = 0
        self.cur_token = 0
        self.cur_money = 0
        

    def get_GPT_response(self, prompt,json_format = False):
        client = OpenAI(
            # base_url = self.base_url,
            api_key = self.api_key
        )
        if(json_format == True):
            completion = client.chat.completions.create(
            temperature= 0.0,
            model = self.model,
            response_format={"type": "json_object"},
            messages=[
                {"role":"system","content":"You should output JSON."},
                {"role": "user", "content": prompt},
            ]
            )
            answer = json.loads(completion.choices[0].message.content)

        else:
            completion = client.chat.completions.create(
            temperature= 0.0,
            model = self.model,
            messages=[
                {"role": "user", "content": prompt}
            ]
            )
            answer = completion.choices[0].message.content
        return answer

    def calc_token(self, in_text, out_text=""):
        enc = tiktoken.encoding_for_model(self.model)
        return len(enc.encode(str(out_text) + str(in_text)))

    def calc_money(self, in_text, out_text):
        if self.model == "gpt-4o":
            return (self.calc_token(in_text) * 0.005 + self.calc_token(out_text) *  0.015) / 1000
        elif self.model == "gpt-4o-mini":
            return (self.calc_token(in_text) * 0.00015  + self.calc_token(out_text) * 0.0006 ) / 1000
        elif self.model == "gpt-4o-2024-08-06":
            return (self.calc_token(in_text) * 0.0025  + self.calc_token(out_text) * 0.01 ) / 1000 
        elif self.model == "gpt-4":
            return (self.calc_token(in_text) * 0.03 + self.calc_token(out_text) * 0.06) / 1000
        elif self.model == "gpt-3.5-turbo":
            return (self.calc_token(in_text) * 0.0015 + self.calc_token(out_text) * 0.002) / 1000

    def extract_json_from_text(self, text):
        json_pattern = r'\{[^{}]*\}'
        match = re.search(json_pattern, text)
        if match:
            try:
                json_data = json.loads(match.group())
                return json_data
            except json.JSONDecodeError:
                return None
        else:
            return None

# test

# gpt = GPT()
# prompt = "What is the capital of France?"
# response = gpt.get_GPT_response(prompt,json_format=False)
# print(f"{response}")
