import os
import openai
from flask import Flask, request, jsonify
import requests
import json 


openai.api_key = os.getenv("OPENAI_API_KEY")
def generate_text(prompt):
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0,
    max_tokens=60,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)

    message = response.choices[0].text.strip()
    return message


app = Flask(__name__)

@app.route('/', methods=['POST'])
def chat():
    data = request.json
    prompt = data['message']
    response_chatgpt = generate_text(prompt)
    answer = jsonify({'message': response_chatgpt})
    headers={'Content-Type': 'application/json'}
    webhook_url = os.getenv("webhook")

    headers = {
        "Content-Type": "application/json"
    }

    payload = {  
            "message": response_chatgpt
    }

    response = requests.post(
        webhook_url,
        headers=headers,
        data=json.dumps(payload)
    )

    return jsonify({'message': response_chatgpt})






# Set the webhook_url to the one provided by Slack when you create the webhook at https://my.slack.com/services/new/incoming-webhook/


if __name__ == '__main__':
    app.run(debug=True)