import requests
import json
import traceback
### time costs
from functools import wraps
def ISZ_main_exception_report_args(msg):
    def main_exception_report(function):
        @wraps(function)
        def function_main_exception_report(*args, **kwargs):
            try:
                function(*args, **kwargs)
            except Exception as e:
                person_msgreport = ISZMsgReport(webhook="http://192.168.6.241:5008/ding/sendByMembers")
                person_msgreport.chatbot_text(title=f"{msg}",content=f"{msg}:<br>{e}<br><br>{traceback.format_exc()}")
            return None
        return function_main_exception_report
    return main_exception_report

class ISZMsgReport():
    def __init__(self,webhook) -> None:
        self.webhook = webhook
        pass
    def chatbot_text(self, touser:list = ["011222671211-1181533439"], title:str = None, content:str = None):
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            "code": "ipd",
            "userIds": 
                touser
            ,
            "content": content,
            "title": title
        }
        result = requests.post(self.webhook, json=data, headers=headers)
        return result
    
    def send_group_markdown(self,code = "weatherReport", conversation_id = "cidR59tfQt2vstqR25R2nW0PA==", content = None, title = None):
        payload = json.dumps({
            "code": code,
            "conversationId": conversation_id,
            "content": content,
            "title": title
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", self.webhook, headers=headers, data=payload)
        return response
