import requests
import json
import random

def send_otp(mobile, code):
    url = "https://api.sms.ir/v1/send/verify"
    payload = json.dumps({
        "mobile": mobile,
        "templateId": 886831, # کد قالب تایید که در پنل sms.ir ساختید
        "parameters": [
            {
                "name": "CODE", # نام متغیر در قالب شما
                "value": str(code)
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'text/plain',
        'x-api-key': 'Rwa9Fc0qqhUyGvG1sl6f9h5IcCUOr38B4CJnH64g7SPRi0nd' # کلید اختصاصی شما
    }
    try:
        response = requests.post(url, data=payload, headers=headers)
        return response.status_code == 200
    except:
        return False