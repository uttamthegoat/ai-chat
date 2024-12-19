import os
import openai
from typing import List
from dotenv import load_dotenv

class AIService:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        
        # Get API key from environment variables
        api_key = os.getenv("SAMBANOVA_API_KEY")
        if not api_key:
            raise ValueError("SAMBANOVA_API_KEY not found in environment variables")
            
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url="https://api.sambanova.ai/v1",
        )

    def get_chat_response(self, messages: List[dict]) -> str:
        try:
            response = self.client.chat.completions.create(
                model='Qwen2.5-72B-Instruct',
                messages=messages,
                temperature=0.1,
                top_p=0.1
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"