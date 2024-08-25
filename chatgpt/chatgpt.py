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


prompt = "https://www.coupang.com/vp/products/7892877637?itemId=21613410154&src=1139000&spec=10799999&addtag=400&ctag=7892877637&lptag=AF7815336&itime=20240825165045&pageType=PRODUCT&pageValue=7892877637&wPcid=17241594878083356812166&wRef=redcloudimo.tistory.com&wTime=20240825165045&redirect=landing&traceid=V0-101-973afdc8f0a52673&mcid=79f48ab7062a43419317bdf02813aeaf&placementid=&clickBeacon=&campaignid=&puidType=&contentcategory=&imgsize=&tsource=&pageid=&deviceid=&token=&contenttype=&subid=&impressionid=&campaigntype=&puid=&requestid=&contentkeyword=&subparam= 이 페이지에 대해 요약해줘"
text = chat_with_gpt(prompt)


print(text)

