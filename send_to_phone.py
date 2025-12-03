import requests
import os

FEISHU_API = os.getenv("FEISHU_API")

def send_message(msg):
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "msg_type":"text",
        "content":
            {
                "text":f"{msg}"
            }
        }
    try:
        response = requests.post(url=FEISHU_API,headers=headers,json=data)
        print(response)
    except Exception as e:
        print(e)
