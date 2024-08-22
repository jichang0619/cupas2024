# https://github.com/openai/openai-python

import os
from openai import OpenAI



client = OpenAI(api_key=Project_API_KEY)

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


prompt = "한국의 쿠팡쇼핑몰 물 2리터에 대한 글을 사진과 고객 후기등을 담아서 블로그 형식으로 써줘"
text = chat_with_gpt(prompt)


print(text)

