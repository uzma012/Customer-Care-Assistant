from openai import OpenAI
from groq import Groq
import os

class CustomerCareLLM:
    def __init__(self):
        llm_type = os.getenv("LLM_TYPE")

        if llm_type == "OPENAI":
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model = os.getenv("LLM_MODEL_GPT")

        else :
            self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            self.model = os.getenv("LLM_MODEL_GROQ")

    def call_llm(self, prompt: str, max_tokens=256, temperature=0.3):
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
            {"role": "system", "content": "You are a helpful assistant that answers questions using provided context."},
            {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature,
            
            )
        return resp.choices[0].message.content
    


    # def call_openai(self, prompt: str, max_tokens=256, temperature=0.3):        
    #     response = self.client.chat.completions.create(
    #         model=self.model,
    #         messages=[
    #             {"role": "system", "content": "You are a helpful assistant that answers questions using provided context."},
    #             {"role": "user", "content": prompt}
    #         ],
    #         max_tokens=max_tokens,
    #         temperature=temperature,
    #     )
        
    #     return response.choices[0].message.content