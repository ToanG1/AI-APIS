from email import message
import os
import string
from dotenv import load_dotenv
import openai
from models.chatResponse import chatResponse
from services.constantObject import roadmapObject

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

def genRoadmap(topic, level, language):
    message = string.Template("Give me a roadmap to study ${topic} at ${level} level, response all content by ${language} language. Return in type of json object follow this ${roadmapObject}")
    values = {"topic": topic, "roadmapObject": roadmapObject, "level": level, "language": language}
    message = message.substitute(values)

    messages =[]
    if message:
        messages.append(
            {"role": "user", "content": message},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
    reply = chat.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    return chatResponse(code = 200, message ="Roadmap generated successfully", c_id = "",
                         messages = "", prompt = message, response = reply)

def getSuggestion(topic, content, language):
    message = string.Template("Suggest some resource to learn about this topic ${content} which is belong to ${topic}. Resource should contain youtube video link or documention link. Response by ${language} language")
    values = {"topic": topic, "content": content, "language": language}
    message = message.substitute(values)

    messages =[]
    if message:
        messages.append(
            {"role": "user", "content": message},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
    reply = chat.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    return chatResponse(code = 200, message ="Roadmap generated successfully", c_id = "",
                         messages = "", prompt = message, response = reply)

