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

@app.route("/", methods=['POST', 'GET'])

def chat():
    if request.method == "POST":
        print(request.json)
        data = request.json
        prompt = data['message']
        response_chatgpt = generate_text(prompt)
        answer = jsonify({'message': response_chatgpt})
        headers={'Content-Type': 'application/json'}
        webhook_url = os.getenv("WEBHOOK")

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
        print(jsonify({'message': response_chatgpt}))
        return "Posted Woo"
    return "Hello World!"
    

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)