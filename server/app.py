from flask import Flask, jsonify, request
from openai import OpenAI
from flask_cors import CORS


app = Flask(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

completion = client.chat.completions.create(
  model="model-identifier",
  messages=[
    {"role": "system", "content": "Always answer in two to three sentences."},
  ],
  temperature=0.7,
)

@app.route("/", methods = ['GET', 'POST'])
def chatWithBot():
    response = {}
    if request.method == 'POST':
      message = request.get_json()['message']
      print(message)

      completion = client.chat.completions.create(
        model="model-identifier",
        messages=[
           {"role": "system", "content": "Always answer in two to three sentences."},
          {"role": "user", "content": message}
        ],
      )
      response['message'] = completion.choices[0].message.content
      return response