import os
import openai
from flask import Flask, request, jsonify, render_template
import requests
import json 
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
def generate_text(prompt):
    
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature=.5,
    max_tokens=150,
    messages=[
            {"role": "user", 
            "content": prompt}]

    )

    message = response['choices'][0]['message']['content']
    return message



limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["1 per 10 seconds"],
    storage_uri="memory://",
)
@app.route("/", methods=['POST', 'GET'])
@limiter.limit("1 per 10 seconds")
def chat():
    if request.method == "POST":
        print(request.json)
        data = request.json
        prompt = data['message']
        name = data['name']
        response_chatgpt = generate_text(prompt)
        headers={'Content-Type': 'application/json'}
        webhook_url = os.getenv("WEBHOOK")

        headers = {
            "Content-Type": "application/json"
        }

        payload = {  
                "message": response_chatgpt,
                "group": name
        }

        requests.post(
            webhook_url,
            headers=headers,
            data=json.dumps(payload)
        )
        return jsonify({'message': response_chatgpt})
    return render_template('index.html')


@app.errorhandler(429)
def ratelimit_handler(e):
  return "You have exceeded your rate-limit"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')