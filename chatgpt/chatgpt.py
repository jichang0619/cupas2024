# https://github.com/openai/openai-python

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')

client = OpenAI(api_key=API_KEY)

def chat_with_gpt(prompt, model="gpt-4o", temperature=0.7, max_tokens=150):
    response = client.chat.completions.create(
    model = model,
    #response_format = {"type" : "json_object"},
    messages= [
        {"role" : "system", "content" : "You are a helpful assistant"},
        {"role" : "user", "content" : prompt},
    ]
    )
    return response.choices[0].message.content


prompt = "한국의 오이슬에 대해 알려줘"
text = chat_with_gpt(prompt)


print(text)

