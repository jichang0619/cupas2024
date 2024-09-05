import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
API_KEY = os.getenv('API_KEY')

client = OpenAI(api_key=API_KEY)


def chat_with_gpt(text, max_tokens=300, system_role='You are a helpful assistant.'):
    print('-----\nREQUEST :: chatGPT api')
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_role},
            {"role": "user", "content": f"모든 답변은 한국어로 해줘.\n\n {text}"}
        ],
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].message.content


def create_image(text):
    print('-----\nREQUEST :: dall-e api')
    response = client.images.generate(
        model="dall-e-3",
        prompt=text,
        n=1,
        size="1024x1024"
    )
    return response.data
