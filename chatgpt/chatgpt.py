# https://github.com/openai/openai-python

import os
from openai import OpenAI
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()
API_KEY = os.getenv('API_KEY')

client = OpenAI(api_key=API_KEY)
html_url = '../samples/product-info.html'

def chat_with_gpt(prompt, model="gpt-4o", temperature=0.7, max_tokens=150):
    response = client.chat.completions.create(
    model = model,
    #response_format = {"type" : "json_object"},
    messages= [
        {"role" : "system", "content" : "You are a helpful assistant"},
        {"role" : "user", "content" : '모든 답변은 한국어로 해줘. '+ prompt},
    ]
    )
    return response.choices[0].message.content

def summarize_html_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # BeautifulSoup으로 HTML 파싱
        soup = BeautifulSoup(html_content, 'html.parser')

        # HTML에서 텍스트 추출
        text_content = soup.get_text(separator="\n", strip=True)

        # 추출된 텍스트 요약
        summary_prompt = f"아래 HTML 내용을 요약해줘 :\n\n{text_content}"
        summary = chat_with_gpt(summary_prompt)

        return summary

    except Exception as e:
        return f"An error occurred while summarizing the HTML file: {e}"


def main():
    file_path = html_url

    summary = summarize_html_file(file_path)
    print(summary)


if __name__ == "__main__":
    main()
