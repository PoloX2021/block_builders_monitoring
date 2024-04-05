from decodeRawTx import decode_raw_tx
import requests
import re
import json

def simulate_block(block, decode = True):
    url = "http://localhost:8080/api/v1/simulate-bundle"
    headers = {"Content-Type": "application/json"}
    
    data = []
    for i in block['transactions']:
        if decode :
            tx = decode_raw_tx(i)
        else:
            tx = i
        data.append({
            "chainId": 1,
            "from": tx['from'],
            "to":   tx['to'],
            "data": tx['data'],
            "gasLimit": int(tx['gasLimit'],16),
            "value": str(tx['value']),
            "blockNumber": int(block['block_number'])-1, # Previous bloc
            "formatTrace": True,
        })

    response = requests.post(url, headers = headers, json=data).json()
    try :
        code = response['code']
        return None
    except:
        return response

""" the answer is built as follows :
an array of answer per simulation,
'gasUsed'
'blockNumber'
'success' : bool
'logs'
'trace'
'exitReason'
'returnData'
"""
"""
input_file_path = "c:/Users/Paul CoW/Documents/MEVBlocker/Agnostic_relay/block19511148.txt"
with open(input_file_path, "r") as input_file:
    i=0
    for line in input_file.readlines():
        a = re.split(' |\t', line.strip())
        simulate_block(json.loads(a[7])['ExecutionPayload'])
        print(i)
        i+=1
"""