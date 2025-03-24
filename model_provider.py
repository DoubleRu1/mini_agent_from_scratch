import os 
import json
from openai import OpenAI
from prompt import user_prompt

class ModelProvider(object):
    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        self.model = os.getenv("MODEL_NAME")
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=os.getenv("BASE_URL"),
    )

    def chat(self, prompt, chat_history):
        messages = [
            {'role': 'system', 'content': prompt}
        ]
        
        for his in chat_history:
            messages.append({'role': 'user', 'content': his[0]})
            messages.append({'role': 'assistant', 'content': his[1]})
        
        messages.append({'role': 'user', 'content': user_prompt})
        
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        response = json.loads(completion.choices[0].message.content)
        return response