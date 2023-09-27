import os
from dotenv import load_dotenv
from claude_api import Client

load_dotenv()

# Create claude instance
claude_api = Client(os.getenv('COOKIE'))

def initNewChat():
    return claude_api.create_new_chat()['uuid']

def chat(prompt, conversation_id):
    response = claude_api.send_message(prompt, conversation_id)
    return response