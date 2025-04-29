from flask import Flask, jsonify, request
from openai import OpenAI
from flask_cors import CORS


app = Flask(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
max_tokens = 20000

#Save all the conversations so that the AI has context
system_behaviour = "Always answer in two to three sentences. Only change this behaviour if a message starts with system:"
conversation = [{"role": "user", "content":system_behaviour}]

@app.route("/", methods = ['POST'])
def chatWithBot():
    response = {}
    message = request.get_json()['message']
    print(client.models.list().data[0].id)

    conversation.append({"role": "user", "content":system_behaviour + "\n" + message})

    print(conversation)
    completion = client.chat.completions.create(
        model=client.models.list().data[0].id,
        messages=conversation,
        temperature = 0.7,
        max_completion_tokens = 1000
      )
    response['message'] = completion.choices[0].message.content
    tokens = completion.usage.total_tokens
    conversation.append({"role": "assistant", "content": response['message']})    
    return response