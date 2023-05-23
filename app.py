import os
import openai
from flask import Flask, request, jsonify, render_template, redirect, url_for
import requests
import json 
import threading



app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
def generate_text(prompt, name, result_dict):
    
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature=.5,
    max_tokens=1500,
    messages=[
            {"role": "user", 
            "content": prompt}]

    )
    chatgpt_answer = response['choices'][0]['message']['content']
    webhookhit(result_dict, chatgpt_answer, name)
    result_dict["function1"] = json.dumps(response)

def webhookhit(result_dict, message, name):
 
    headers={'Content-Type': 'application/json'}
    webhook_url = os.getenv("WEBHOOK")

    headers = {
        "Content-Type": "application/json"
    }

    payload = {  
            "message": message,
            "name": name
    }

    requests.post(
        webhook_url,
        headers=headers,
        data=json.dumps(payload)
    )


    
    result_dict["function2"] = {"message":"done", "name": "Joshua Clark"}


@app.route("/", methods=['POST'])
def chat():
    data = request.json
    prompt = data['message']
    name = data['name']
    result_dict = {}
    thread1 = threading.Thread(target=webhookhit, args=(result_dict,"ok","no one"))
    thread2 = threading.Thread(target=generate_text, args=(prompt,name,result_dict,))
    thread1.start()
    thread2.start()

    # Wait for both threads to finish

    return {"message":"complete"}

    


@app.errorhandler(429)
def ratelimit_handler(e):
  return {"message":"You have exceeded your rate-limit",
          "name":"Joshua Clark"}


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')