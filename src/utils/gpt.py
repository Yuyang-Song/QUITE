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
            return full_response
            
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
prompt = "What is the capital of France?"
response = gpt.get_GPT_response(prompt, json_format=False)
print("This is the response of the assistant:")
print(response)


# Example 2: Without system message
question = "What is the capital of France?"

prompt = textwrap.dedent(f"""
<Mission>
You are a helpful assistant that provides factual answers to general knowledge questions.

<Question>
{question}

You must return the answer in JSON format as follow:
{{
    {{analysis}} : ,//Fill in the analysis
    {{answer}} : ,//Fill in the answer
}}
""")

response = gpt.get_GPT_response(prompt,json_format=True)
print("This is the response of the assistant:")
print(response)



