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
        self.api_key = "sk-HWmTLFjVk6bOVaMw3993Bd491fE8494b939bB94b080e7545"
        self.base_url = "https://aihubmix.com/v1"
        self.model = "claude-3-7-sonnet-20250219"
        self.client = OpenAI(
            api_key= self.api_key,
            base_url = self.base_url
        )
        self.log_file = "model_output.txt"
        # 在每次程序启动时清空日志文件
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write("--- LLM Interaction Log ---\n\n")

    def _log_interaction(self, model_name, response):
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write("="*80 + "\n")
                f.write(f"MODEL: {model_name}\n")
                f.write("-" * 34 + " RESPONSE " + "-" * 34 + "\n")
                
                # 如果响应是字典或列表（来自JSON模式），则格式化输出
                if isinstance(response, (dict, list)):
                    f.write(json.dumps(response, indent=2, ensure_ascii=False))
                else:
                    f.write(str(response))
                
                f.write("\n" + "="*80 + "\n\n")
        except Exception as e:
            print(f"\n[Logging Error] Failed to write to log file: {e}\n")

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
            self._log_interaction(self.model, full_response)
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
            self._log_interaction(self.model, full_response)
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

        print(answer)
        self._log_interaction(self.model, answer)
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

