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

Transaction1559Index = ['chain_id', 'nonce', 'max_fee_per_gas', 'gas', 'to', 'value', 'data', 'access_list', 'v', 'r', 's']
Transactions2930Index = ['chain_id', 'nonce', 'max_priority_fee_per_gas', 'max_fee_per_gas', 'gas', 'to', 'payload', 'access_list', 'v', 'r', 's']
TransactionsIndex = ['nonce', 'gas_price', 'gas_limit', 'to', 'value', 'payload', 'v', 'r', 's']

def decode_raw_tx(raw_tx: str):
    if raw_tx[:2]=='0x':
        raw_tx = raw_tx[2:]

    command = '"C:\\Users\\Paul CoW\\.cargo\\bin\\cast.exe" from-rlp '

    if raw_tx[:2] =='02' or raw_tx[:2] =='01':
        command = command + raw_tx[2:]
    else : 
        command = command + raw_tx

    # Exécuter la commande
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Obtenir la sortie standard et les erreurs
    stdout, stderr = process.communicate()

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

raw_tx = "0x02f9019701822a47850f08c9003a8513e3166a298302caf3946f1cdbbb4d53d226cf4b917bf768b94acbab616882306cb90124ceb5748e0000000000000000000000004e68ccd3e89f51c3074ca5072bbac773960dfa36000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2000000000000000000000000dac17f958d2ee523a2206206994597c13d831ec70000000000000000000000000000000000000000000000000000000000000bb80000000000000000000000000000000000000000000000019220a7391bab29b20000000000000000000000000000000000000000000000000000001731fd259800000000000000000000000000000000000000000003d9160fac5329e0000000000000000000000000000000000000000000000000000000000000000129b76d0000000000000000000000000000000000000000000000000000000000000000c001a090dd675315e19c1f5e8a155abcd6853cd21d5ac2b53cccedb16877051c416843a0255b78e3759da4ea9d187df49323a16bbdc9feea53e265d8d3c91d8c0ef846ee"
print(decode_raw_tx(raw_tx))