import anthropic
import os
from dotenv import load_dotenv
from models.chatResponse import chatResponse

load_dotenv()

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key=os.getenv('ANTHROPIC_KEY'),
)

def chat(prompt, messages):
    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        messages = appendMessage(messages, "user", prompt)
    )
    return chatResponse(code = 200, message ="Chat request are served successfully", c_id = "",
                        messages = appendMessage(messages, response.role, response.content[0].text), 
                        prompt = prompt, response = response.content[0].text)

def appendMessage(messages, role, content):
    message = {"role": role, "content": content}
    messages.append(message)
    return messages