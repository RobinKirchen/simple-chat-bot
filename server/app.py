from flask import Flask, jsonify, request
from openai import OpenAI
from flask_cors import CORS


app = Flask(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")


conversation = [{"role": "system", "content": "Always answer in two to three sentences."}]

@app.route("/", methods = ['GET', 'POST'])
def chatWithBot():
    response = {}
    if request.method == 'POST':
      message = request.get_json()['message']
      print(message)

      conversation.append({"role": "user", "content": message})

      completion = client.chat.completions.create(
        model="model-identifier",
        messages=conversation
        ,
        temperature=0.7
      )
      response['message'] = completion.choices[0].message.content
      conversation.append({"role": "assistant", "content": completion.choices[0].message.content})
      return response