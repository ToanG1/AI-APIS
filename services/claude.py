import os
from dotenv import load_dotenv
from package.claude_api import Client
from models.chatResponse import chatResponse

load_dotenv()

# Create claude instance
claude_api = Client(os.getenv('COOKIE'))

def initNewChat():
    conversation_id = claude_api.create_new_chat()['uuid']
    return chatResponse(code = 200, message ="Initialize new chat with Claude successfully", c_id = conversation_id,
                         messages = [], prompt = "", response = "")

def chat(prompt, conversation_id):
    response = claude_api.send_message(prompt, conversation_id)
    return chatResponse(code = 200, message ="Chat request are served successfully", c_id = conversation_id,
                         messages = [], prompt = prompt, response = response)

# Accept only txt file
def chatWithAttachment(prompt, file, conversation_id):
    response = claude_api.send_message(prompt, conversation_id, attachment= file, timeout=600)
    print(response)
    return chatResponse(code = 200, message ="Chat request are served successfully", c_id = conversation_id,
                         messages = [], prompt = prompt, response = response)