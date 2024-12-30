import requests
import json

def create_chat_completion(messages):
    url = "http://localhost:11434/api/chat"
    
    payload = {
        "model": "llama2:3.1",
        "messages": [
            {
                "role": "system",
                "content": "you are helpful agent for data scrapping and will help me for so"
            },
            {
                "role": "user",
                "content": messages 
            }
        ],
        "format": "json",
        "options": {
            "temperature": 1,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0
        }
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None

