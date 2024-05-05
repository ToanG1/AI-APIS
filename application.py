# from crypt import methods
from json import JSONDecodeError
import os
from flask import Flask, request
from services import openAI, youtube, textModeration, imageModeration, anthropic
from models.chatResponse import chatResponse
import jsonpickle
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
# cors = CORS(app, resources={r"/api2/*": {"origins": ["http://localhost:3000", "http://localhost:5001"]}})
CORS(app)

# Limit content lenght to 2mb
app.config['MAX_CONTENT_LENGTH'] = 2 * 1000 * 1000
app.config['UPLOAD_FOLDER'] = './files'

# File types that are accepted to use claude with attachment
allowedTypes = {"docx", "doc", "txt", "pdf", "csv", "html", "jpg", "jpeg", "png"}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowedTypes

# Routes
@app.route('/api/init', methods=['GET'])
def init():
    return jsonpickle.encode(openAI.initNewChat())

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
            return jsonpickle.encode(anthropic.chat(request.get_json()['prompt'], request.get_json()['messages']))
    except:
        return jsonpickle.encode(chatResponse(code = 400, message ="Somethings missed or key reached limit", c_id= "",
                                               messages=[], prompt= "", response= ""))

@app.route('/api/gen', methods=['POST'])
def genRoadmap(): 
    try:
        return jsonpickle.encode(openAI.genRoadmap(request.get_json()['topic'], request.get_json()['level'], request.get_json()['language']))
    except:
        return jsonpickle.encode(chatResponse(code = 400, message ="Somethings missed or key reached limit", c_id= "",
                                               messages=[], prompt= "", response= ""))

@app.route('/api/suggest', methods=['POST'])
def getSuggestion(): 
    try:
        return jsonpickle.encode(openAI.getSuggestion(request.get_json()['topic'], request.get_json()['content'], request.get_json()['language']))
    except:
        return jsonpickle.encode(chatResponse(code = 400, message ="Somethings missed or key reached limit", c_id= "",
                                               messages=[], prompt= "", response= ""))

@app.route('/api/subtitle', methods=['GET'])
def getSubtitles():
    try:
        return jsonpickle.encode(youtube.getYoutubeSubtitles(request.args.get('videoId')))
    except:
        return jsonpickle.encode(chatResponse(code = 400, message ="Somethings missed or key reached limit", c_id= "",
                                               messages=[], prompt= "", response= ""))

@app.route('/api/summarize', methods=['POST'])
def summarizeDocument():
    try:
        return jsonpickle.encode(openAI.summarize(request.get_json()['document']))
    except:
        return jsonpickle.encode(chatResponse(code = 400, message ="Somethings missed or key reached limit", c_id= "",
                                               messages=[], prompt= "", response= ""))
    
@app.route('/api/check-nsfw', methods=['POST'])
def checkModeration():
    priority = request.args.get('priority')
    type = request.args.get('type')
    if (type == "image"):
        return jsonpickle.encode(
        imageModeration.
        checkImageModeration(request.get_json()['content']))
    
    elif (type == "text"):
        if (priority == "high"):
            return jsonpickle.encode(
                textModeration.
                checkModerationHighPriority(request.get_json()['content']))
        else:
            return jsonpickle.encode(
                textModeration.
                checkModerationLowPriority(request.get_json()['content']))

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5009, threads=1000)