from openai import OpenAI,APITimeoutError 

from dotenv import load_dotenv
import json
import os
import re
import tiktoken
import asyncio
import httpx

class GPT:
    def __init__(self):
        # load_dotenv(dotenv_path='../config_file/.env') 
        self.api_key = "sk-RIjSVmomD7UfMDx181B3F6F4A9E34bDcA6F386Cd72Ba016f"
        self.base_url = "https://aihubmix.com/v1"
        # self.model = "gpt-4o-2024-11-20"
        self.model = "claude-3-7-sonnet-20250219"
        # self.api_key = "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",
        # self.base_url = "https://api.openai.com/v1",
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
                temperature=0.0,
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
        
    def get_decision_GPT_response(self, prompt, system_message=None, json_format=False):
    
        # If system_message is provided, include it in the messages list
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})
        
        if json_format:
            completion = self.client.chat.completions.create(
                temperature=0.0,
                model=self.model,
                response_format={"type": "json_object"},
                messages=messages
            )
            answer = json.loads(completion.choices[0].message.content)
        else:
            completion = self.client.chat.completions.create(
                temperature=0.0,
                model=self.model,
                messages=messages
            )
            answer = completion.choices[0].message.content

        return answer
    
    async def get_decision_GPT_response_async(self, prompt, system_message=None, json_format=False):
        loop = asyncio.get_running_loop()
        
        # 将同步请求封装成异步调用，使用 run_in_executor 来运行同步代码
        return await loop.run_in_executor(None, self.get_decision_GPT_response, prompt, system_message, json_format)

    
    async def get_GPT_response_async(self, prompt, system_message=None, json_format=False):
        loop = asyncio.get_running_loop()
        
        # 将同步请求封装成异步调用，使用 run_in_executor 来运行同步代码
        return await loop.run_in_executor(None, self.get_GPT_response, prompt, system_message, json_format)
    
    def calc_token(self, in_text, out_text=""):
        enc = tiktoken.encoding_for_model(self.model)
        return len(enc.encode(str(out_text) + str(in_text)))

    def calc_money(self, in_text, out_text):
        if self.model == "gpt-4o-2024-11-20":
            return (self.calc_token(in_text) * 0.005 + self.calc_token(out_text) * 0.015) / 1000
        elif self.model == "gpt-4o-mini":
            return (self.calc_token(in_text) * 0.00015 + self.calc_token(out_text) * 0.0006) / 1000
        elif self.model == "gpt-4o-2024-08-06":
            return (self.calc_token(in_text) * 0.0025 + self.calc_token(out_text) * 0.01) / 1000
        elif self.model == "gpt-4":
            return (self.calc_token(in_text) * 0.03 + self.calc_token(out_text) * 0.06) / 1000
        elif self.model == "gpt-3.5-turbo":
            return (self.calc_token(in_text) * 0.0015 + self.calc_token(out_text) * 0.002) / 1000


        
# Test with system message
# gpt = GPT()

# # Example 1: With a system message
# system_message = "You are a helpful assistant that provides factual answers to general knowledge questions."
# prompt = "What is the capital of France?"
# response = gpt.get_GPT_response(prompt, system_message=system_message, json_format=False)
# print(response)
# token = gpt.calc_token(prompt, response)
# print(f"Token cost: {token}")

# # Example 2: Without system message
# response_no_system = gpt.get_GPT_response(prompt, system_message=None, json_format=False)
# print(f"Response without system message: {response_no_system}")
