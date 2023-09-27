from flask import Flask
from flask import request
from services import chat

app = Flask(__name__)
# Routes
@app.route('/init', methods=['GET'])
def initClaude():
    return chat.initNewChat()

@app.route('/chat', methods=['POST'])
def chatWithClaude():
    return chat.chat('hello', request.get_json()['id'])

if __name__ == '__main__':
    print (app.url_map)
    app.run(debug=True)