"""
Il y 3 types de transaction : https://eips.ethereum.org/EIPS/eip-1559#specification
 - legacy
 - EIP1559 : payload précédé de 0x02
 - EIP2930 : payload précédé de 0x01
"""

import subprocess
import json
from hash import keccak256
from web3.auto import w3
import tempfile
import os

Transaction1559Index = ['chain_id', 'nonce', 'max_priority_fee_per_gas','max_fee_per_gas', 'gas', 'to', 'value', 'data', 'access_list', 'v', 'r', 's']
Transactions2930Index = ['chain_id', 'nonce', 'max_priority_fee_per_gas', 'max_fee_per_gas', 'gas', 'to', 'data', 'access_list', 'v', 'r', 's']
TransactionsIndex = ['nonce', 'gas_price', 'gas', 'to', 'value', 'data', 'v', 'r', 's']

def decode_raw_tx(raw_tx: str):
    if raw_tx[:2]=='0x':
        raw_tx = raw_tx[2:]

    command = f'"C:\\Users\\Paul CoW\\.cargo\\bin\\cast.exe" from-rlp'
    
    if raw_tx[:2] =='02' or raw_tx[:2] =='01':
        input = raw_tx[2:].encode()
    else : 
        input = raw_tx.encode()

    # Exécuter la commande
    process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Obtenir la sortie standard et les erreurs
    stdout, stderr = process.communicate(input=input)

    # Afficher la sortie standard
    if stdout:
        tx = json.loads(stdout.decode())
        if raw_tx[:2]=='02':
             tx = dict(zip(Transaction1559Index, tx))
        elif raw_tx[:2]=='01':
            tx = dict(zip(Transactions2930Index, tx))
        else:
            tx = dict(zip(TransactionsIndex, tx))
        tx["hash"] = keccak256(raw_tx)
        tx['from_'] = w3.eth.account.recover_transaction(raw_tx)
        return tx

    # Afficher les erreurs
    if stderr:
        print("Error:")
        print(stderr.decode())

