import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
API_KEY = os.getenv("DUNE_KEY")
API_KEY = 'JYLDIVjVB4qX40CKDGFqead4ZuvDrEav'

def list_bundles(blockMin: int, blockMax: int = 0) -> list:
    blockMax = max(blockMin, blockMax)+1
    query = 3583631
    url = f"https://api.dune.com/api/v1/query/{query}/execute"  # Replace with the actual API URL
    headers = {"X-DUNE-API-KEY": API_KEY}
    result = requests.request("POST", url, headers=headers, params = {'blockMin' : blockMin, 'blockMax' : blockMax}).json()

    execution_id = result['execution_id']
    while True:
        url = f"https://api.dune.com/api/v1/execution/{execution_id}/status"
        headers = {"X-DUNE-API-KEY": API_KEY}
        response = requests.request("GET", url, headers=headers).json()
        if response['is_execution_finished']:
            break

    url = f"https://api.dune.com/api/v1/execution/{execution_id}/results"
    headers = {"X-DUNE-API-KEY": API_KEY}
    result = requests.request("GET", url, headers=headers).json()
    print(result)
    result = result['result']
    return result['rows']
    txs = [[] for i in range(blockMin, blockMax)]
    for i in result['rows']:
        txs[i['blockNumber']-blockMin].append(i['transactions'])
    return txs

