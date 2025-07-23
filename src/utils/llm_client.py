"""
Author: Yuyang Song
Created: 2024-10-13
Last Modified: 2025-07-22

Module: llm_client.py

A lightweight wrapper around OpenAI's synchronous and asynchronous Chat Completion APIs.
Provides methods for streaming and non-streaming responses, decision-style JSON outputs,
token counting, and cost estimation for different GPT models.

Usage:
    from llm_client import GPT
    gpt = GPT(api_key="YOUR_KEY", model="gpt-4o", base_url="https://api.openai.com")
    response = gpt.get_LLM_response("Hello, world!", system_message="You are a helpful assistant.")
"""

from openai import OpenAI, AsyncOpenAI
import json
import asyncio
import sys
import json
import tiktoken

# Add parent directories to Python path for relative imports
sys.path.append('../')
sys.path.append('./utils')
sys.path.append('./')



class GPT:
    def __init__(self, api_key, model, base_url):
        """
        Initialize the GPT client.
        
        Args:
            api_key (str): Your OpenAI API key
            model (str): The GPT model to use (e.g., 'gpt-4o', 'gpt-3.5-turbo')
            base_url (str): The base URL for the OpenAI API
        """
        self.api_key = api_key  
        self.model = model
        self.base_url = base_url

        # Initialize synchronous client
        self.client = OpenAI(
            api_key= self.api_key,
            base_url = self.base_url
        )

        # Initialize asynchronous client
        self.async_client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

    def get_LLM_response(self, prompt, system_message=None, json_format=False) -> str:
        """
        Get a streaming response from GPT.
        
        Args:
            prompt (str): The user prompt to send to GPT
            system_message (str, optional): System message to set context. Defaults to None.
            json_format (bool, optional): Whether to request JSON formatted response. Defaults to False.
            
        Returns:
            str: The complete response from GPT
        """
        # Prepare messages array
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})
        
        if json_format:
            # Request JSON formatted response
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
            return full_response
            
        else:
            # Request regular text response
            completion = self.client.chat.completions.create(
                temperature=0.0,
                model=self.model,
                messages=messages,
                stream=True
            )

            # Process streaming response
            full_response = ""
            for chunk in completion:
                if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content:
                    chunk_text = chunk.choices[0].delta.content
                    print(chunk_text, end="", flush=True)
                    full_response += chunk_text
            print() # New line after response
            return full_response
    
    async def get_LLM_response_async(self, prompt, system_message=None, json_format=False) -> str:
            """
            Get an asynchronous streaming response from GPT.
            
            Args:
                prompt (str): The user prompt to send to GPT
                system_message (str, optional): System message to set context. Defaults to None.
                json_format (bool, optional): Whether to request JSON formatted response. Defaults to False.
                
            Returns:
                str: The complete response from GPT
            """
            # Prepare messages array
            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": prompt})
            
            if json_format:
                # Request JSON formatted response
                completion = await self.async_client.chat.completions.create(
                    temperature=0.0,
                    model=self.model,
                    response_format={"type": "json_object"},
                    messages=messages,
                    stream=True
                )
                full_response = ""
                async for chunk in completion:
                    if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content:
                        chunk_text = chunk.choices[0].delta.content
                        print(chunk_text, end="", flush=True)
                        full_response += chunk_text
                print()
                return full_response
            else:
                # Request regular text response
                completion = await self.async_client.chat.completions.create(
                    temperature=0.0,
                    model=self.model,
                    messages=messages,
                    stream=True
                )

                # Process streaming response asynchronously
                full_response = ""
                async for chunk in completion:
                    if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content:
                        chunk_text = chunk.choices[0].delta.content
                        print(chunk_text, end="", flush=True)
                        full_response += chunk_text
                print() # New line after response
                return full_response
    

    
    def calc_token(self, in_text, out_text="") -> int:
        """
        Calculate the number of tokens for given text using the model's tokenizer.
        
        Args:
            in_text (str): Input text to tokenize
            out_text (str, optional): Output text to tokenize. Defaults to "".
            
        Returns:
            int: Total number of tokens
        """
        enc = tiktoken.encoding_for_model(self.model)
        return len(enc.encode(str(out_text) + str(in_text)))

    def calc_money(self, in_text, out_text) -> float:
        """
        Calculate the estimated cost for API usage based on token count.
        
        Args:
            in_text (str): Input text
            out_text (str): Output text
            
        Returns:
            float: Estimated cost in USD
            
        Note:
            Pricing is based on OpenAI's pricing as of the implementation date.
            Actual costs may vary. Please refer to OpenAI's current pricing.
        """
        if self.model == "gpt-4o":
            return (self.calc_token(in_text) * 0.005 + self.calc_token(out_text) * 0.015) / 1000
        elif self.model == "gpt-4o-mini":
            return (self.calc_token(in_text) * 0.00015 + self.calc_token(out_text) * 0.0006) / 1000
        elif self.model == "gpt-4o-2024-08-06":
            return (self.calc_token(in_text) * 0.0025 + self.calc_token(out_text) * 0.01) / 1000
        elif self.model == "gpt-4":
            return (self.calc_token(in_text) * 0.03 + self.calc_token(out_text) * 0.06) / 1000
        elif self.model == "gpt-3.5-turbo":
            return (self.calc_token(in_text) * 0.0015 + self.calc_token(out_text) * 0.002) / 1000



# # Test with system message
# gpt = GPT()

# # Example 1: With a system message
# system_message = "You are a helpful assistant that provides factual answers to general knowledge questions."
# prompt = "What is the capital of France?"
# response = gpt.get_LLM_response(prompt, system_message=system_message, json_format=False)
# print(response)

# # Example 2: Without system message
# response_no_system = gpt.get_LLM_response(prompt, system_message=None, json_format=False)
# print(f"Response without system message: {response_no_system}")



