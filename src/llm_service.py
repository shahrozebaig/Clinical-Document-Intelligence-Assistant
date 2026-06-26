import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client=Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_response(messages,temperature=0.2):
    response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=temperature,
        response_format={"type":"json_object"}
    )
    return response.choices[0].message.content

def generate_text_response(messages,temperature=0.2):
    response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message.content