
import os
import openai
import requests
import json 
from io import BytesIO
from PIL import Image

openai.api_key = os.getenv("OPENAI_API_KEY")
def alter():
    # Read the image file from disk and resize it
    image = Image.open("KID_2.png")
    width, height = 1024, 1024
    image = image.resize((width, height))

    # Convert the image to a BytesIO object
    byte_stream = BytesIO()
    image.save(byte_stream, format='PNG')
    byte_array = byte_stream.getvalue()
    response_chatgpt = openai.Image.create_variation(
    image=byte_array,
    n=1,
    size="1024x1024"
    )

    print(response_chatgpt)
