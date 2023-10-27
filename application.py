from json import JSONDecodeError
from uu import encode
import os
from flask import Flask, request
from services import claude, openAI
from models.chatResponse import chatResponse
import jsonpickle
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Limit content lenght to 2mb
app.config['MAX_CONTENT_LENGTH'] = 2 * 1000 * 1000
app.config['UPLOAD_FOLDER'] = './files'

# File types that are accepted to use claude with attachment
allowedTypes = {"docx", "txt", "pdf", "csv"}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowedTypes

# Routes
@app.route('/api2/init', methods=['GET'])
def init():
    try:
        return jsonpickle.encode(claude.initNewChat())
    except:
        return jsonpickle.encode(openAI.initNewChat())

@app.route('/api2/chat', methods=['POST'])
def chat():
    try:
        if (request.get_json()['c_id']):
            return jsonpickle.encode(claude.chat(request.get_json()['prompt'], request.get_json()['c_id']))
        elif (request.get_json()['messages']):
            return jsonpickle.encode(openAI.chat(request.get_json()['prompt'], request.get_json()['messages']))
        else :
            return jsonpickle.encode(chatResponse(code = 400, message ="Id and messages are required! Init new chat first",
                                                   c_id= "", messages=[], prompt= "", response= ""))
    except JSONDecodeError:
        return jsonpickle.encode(openAI.chat(request.get_json()['prompt'], openAI.initNewChat()))
    except:
        return jsonpickle.encode(chatResponse(code = 400, message ="Somethings missed or key reached limit", c_id= "",
                                               messages=[], prompt= "", response= ""))

@app.route('/api2/file', methods=['POST'])
def chatWithAttachment(): 
    # try:
        if 'file' in request.files and request.form.get("c_id") and request.form.get("prompt"):
            file = request.files['file']
            if file or file.filename == '':
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    return jsonpickle.encode(claude.chatWithAttachment(request.form.get("prompt"),
                                                os.path.join(app.config['UPLOAD_FOLDER'], filename), request.form.get("c_id")))
                else:
                    return jsonpickle.encode(chatResponse(code = 400, message ="Media file are not supported", c_id= "",
                                                messages=[], prompt= "", response= ""))
                
        return jsonpickle.encode(chatResponse(code = 400, message ="No selected file!", c_id= "",
                                                messages=[], prompt= "", response= ""))
    # except:
    #     return jsonpickle.encode(chatResponse(code = 400, message ="Somethings missed or key reached limit", c_id= "",
    #                                            messages=[], prompt= "", response= ""))

if __name__ == "__main__":
    app.run(host="0.0.0.0")