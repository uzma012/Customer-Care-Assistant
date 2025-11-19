import google.generativeai as genai
from .prompts import prompt_text
import os
import json
import dotenv
dotenv.load_dotenv()

def extract_text(file_content: str) -> str:
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    prompt = prompt_text(file_content=file_content)
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    text  = remove_json_header(response.text)
    print(text) 
    return text


def remove_json_header(text: str) -> str:
    json_str = text.strip()
    if json_str.startswith("```json"):
        json_str = json_str[len("```json"):].strip()
    if json_str.endswith("```"):
        json_str = json_str[:-3].strip()
    return json_str