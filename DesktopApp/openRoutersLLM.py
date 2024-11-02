import requests
import json
import os
from dotenv import load_dotenv, dotenv_values
from pprint import pprint
import boto3
import json

config = dict(dotenv_values())

key = config['OPEN_ROUTERS_KEY']

def getPromptResponse(prompt):
    

    prompt_data = prompt

    bedrock = boto3.client(service_name="bedrock-runtime", region_name="ap-south-1")

    payload = {
        "prompt": "[INST]"+prompt_data + "[INST]",
        "max_tokens": 512,
        "temperature": 0.5,
        "top_p":0.9
    }
    body = json.dumps(payload)

    response = bedrock.invoke_model(
        body = body,
        modelId = "mistral.mistral-7b-instruct-v0:2",
        accept = "application/json",
        contentType = "application/json"
    )

    return (json.loads(response.get("body").read())['outputs'][0]['text'])

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
    from llmmodule import ARTICLE, EMAIL_EXAMPLE, TRAINING_EXAMPLE
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