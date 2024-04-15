import requests
import json
import os
from dotenv import load_dotenv
from pprint import pprint
from llmmodule import ARTICLE, EMAIL_EXAMPLE, TRAINING_EXAMPLE

load_dotenv()

key = os.environ['OPEN_ROUTERS_KEY']

def getPromptResponse(prompt):
    response = requests.post(
        url='https://openrouter.ai/api/v1/chat/completions',
        headers={
            "Authorization": f"Bearer {key}",
        },
        data=json.dumps({
            "model":"nousresearch/nous-capybara-7b:free",
            "messages":[
                {"role": "user", "content": f"{prompt}"},
            ],
            "temperature":0.5,
        })
    )

    jsonData = json.loads(response.text)

    pprint(jsonData)

    return jsonData

def fetchRateLimits():
    response = requests.get(f"https://openrouter.ai/api/v1/auth/key", headers={
        "Authorization": f"Bearer {key}",
    })

    jsonData = json.loads(response.text)

    pprint(jsonData)
    
    return jsonData

def fetchPerRequestLimits():
    response = requests.get(f"https://openrouter.ai/api/v1/models", headers={
        "Authorization": f"Bearer {key}",
    })

    jsonData = json.loads(response.text)

    pprint(jsonData)
    
    return jsonData

if __name__ == '__main__':
    EXAMPLE_PROMPT=f"""You must respond using JSON format.
Extract details of an event from given body of text
EXAMPLES
--------
{TRAINING_EXAMPLE}

BEGIN! Extract event data
--------
Mail: {EMAIL_EXAMPLE}
Data:"""

    if input('Run json ?') == 'y': getPromptResponse(EXAMPLE_PROMPT)
    if input('Run summarize ?') == 'y': getPromptResponse(f"Summarize in less than 50 words: {ARTICLE}")
    if input('Run response ?') == 'y': getPromptResponse(f"Respond to the mail: {EMAIL_EXAMPLE}")
    fetchRateLimits()