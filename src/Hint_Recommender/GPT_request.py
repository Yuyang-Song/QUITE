from openai import OpenAI
import textwrap
import json

class GPT():
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
system_message = "You are a helpful assistant that provides factual answers to general knowledge questions."
prompt = "What is the capital of France?"
response = gpt.get_GPT_response(prompt, system_message=system_message, json_format=False)
print(response)


# # Example 2: Without system message
prompt = textwrap.dedent(f"""
<Mission> You are an expert in the field of 
""")
response_no_system = gpt.get_GPT_response(prompt, system_message=None, json_format=False)
print(f"Response without system message: {response_no_system}")