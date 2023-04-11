import os
import openai
from flask import Flask, request, jsonify, render_template
import requests
import json 

openai.api_key = os.getenv("OPENAI_API_KEY")
def generate_text(prompt):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "user", "content": prompt},
        ]
    )

    message = response['choices'][0]['message']['content']
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
        return jsonify({'message': response_chatgpt})
    return render_template('index.html')
    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')