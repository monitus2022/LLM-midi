from openai import OpenAI
from dotenv import load_dotenv
import os
import json

from ollama import chat, ChatResponse

load_dotenv()


class OpenrouterLlm:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
        )

        self.model = "x-ai/grok-4-fast"

    def prompt_llm(self, user_message: str, system_message: str = None, **kwargs) -> list:
        """
        Prompts the LLM with any message and returns the response.
        Args:
            user_message (str): The message to send to the LLM.
        Returns:
            list: Parsed JSON response from the LLM.
        """
        if not system_message:
            system_message = "You are a helpful assistant."
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            **kwargs
            # response_format={"type": "json_object"}
        )
        response_text = response.choices[0].message.content
        return response_text
    
    def json_response(self, response_text: str) -> list:
        """
        Parses the LLM response text as JSON.
        Args:
            response_text (str): The raw response text from the LLM.
        Returns:
            list: Parsed JSON object.
        """
        return json.loads(response_text)


class OllamaLlm:
    def __init__(self):
        self.model = "gemma3:4b"

    def prompt_llm(self, user_message: str, system_message: str = None,
                   temperature: float = 0.8, max_tokens: int = 2500) -> list:
        """
        Prompts the LLM with any message and returns the response.
        Args:
            user_message (str): The message to send to the LLM.
        Returns:
            list: Parsed JSON response from the LLM.
        """
        if not system_message:
            system_message = "You are a helpful assistant."

        response: ChatResponse = chat(model='gemma3', messages=[
            {
                'role': 'user',
                'content': user_message,
            },
            {
                'role': 'system',
                'content': system_message,
            }
        ],
            options = {
                "temperature": temperature,
                "max_tokens": max_tokens,
            }
        )

        response_text = response.message.content
        return response_text
