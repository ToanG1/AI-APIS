import os
from dotenv import load_dotenv
import openai
from models.chatResponse import chatResponse

openai.api_key = os.getenv('GPTKEY')

def initNewChat():
    messages = [ {"role": "system", "content": 
              "You are a intelligent assistant."} ]
    return chatResponse(code = 200, message ="Initialize new chat with ChatGPT successfully", c_id = "",
                         messages = messages, prompt = "", response = "")

def chat(prompt, messages):
    message = "User : " + prompt
    if message:
        messages.append(
            {"role": "user", "content": message},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
    reply = chat.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    return chatResponse(code = 200, message ="Chat request are served successfully", c_id = "",
                         messages = messages, prompt = prompt, response = reply)