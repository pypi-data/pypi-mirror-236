import openai
import json
import random as r
import markdown as mk
import tiktoken

keyList = json.load(open("data/models.json"))

def getKey(number: int = 1):
    return r.choices(keyList, k=number)


class ChatGPT:
    def __init__(self):
        self.key = getKey()
        self.openai = openai
        self.openai.api_key = self.key
        self.openai.api_base = "https://openkey.cloud/v1"
        self.messages = []
        self.model = "gpt-3.5-turbo"

    def get_response(self, message: str, role: str = "user", **kwargs):
        self.messages.append({'role': role, 'content': message})
        resp = self.openai.ChatCompletion.create(
            model=self.model, messages=self.messages, **kwargs)
        return resp

    def retHTML(self, **kwargs):
        retMk = self.get_response(**kwargs).choices[0].text
        return mk.markdown(retMk, unsafe_allow_html=True)

    def getToken(self):
        encodeing = tiktoken.encoding_for_model(self.model)
        allToken = 0
        for i in self.messages:
            allToken += len(encodeing.encode(i['content']))
        return allToken
