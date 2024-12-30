from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)



def find_best_match(inputtext:str,keyword:str):
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
        "role": "system",
        "content": [
            {
            "type": "text",
            "text": "you are helpful agent for data scrapping and will help me for so. always return json. need closest match > 90%"
            }
        ]
        },
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": inputtext
            },
            {
            "type": "text",
            "text": keyword
            }

        ]
        },
        
    ],
    response_format={
        "type": "json_object"
    },
    temperature=1,
    max_completion_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    return response.choices[0].message.content