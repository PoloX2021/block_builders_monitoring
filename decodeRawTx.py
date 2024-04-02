from dataclasses import asdict, dataclass
from pprint import pprint
from typing import Optional

import rlp
from eth_typing import HexStr
from eth_utils import keccak, to_bytes
from rlp.sedes import Binary, big_endian_int, binary
from web3 import Web3
from web3.auto import w3
from eth.vm.forks.arrow_glacier.transactions import ArrowGlacierTransactionBuilder as TransactionBuilder
from eth_utils import (
  encode_hex,
  to_bytes,
)
class Transaction(rlp.Serializable):
    fields = [
        ("nonce", big_endian_int),
        ("gas_price", big_endian_int),
        ("gas", big_endian_int),
        ("to", Binary.fixed_length(20, allow_empty=True)),
        ("value", big_endian_int),
        ("data", binary),
        ("v", big_endian_int),
        ("r", big_endian_int),
        ("s", big_endian_int),
    ]


@dataclass
class DecodedTx:
    hash_tx: str
    from_: str
    to: Optional[str]
    nonce: int
    gas: int
    gas_price: int
    value: int
    data: str
    chain_id: int
    r: str
    s: str
    v: int

def hex_to_bytes(data: str) -> bytes:
    return to_bytes(hexstr=HexStr(data))


def decode_raw_tx(raw_tx: str):
    if raw_tx[2:4] =='f8':
        tx = rlp.decode(hex_to_bytes(raw_tx), Transaction)
        hash_tx = Web3.to_hex(keccak(hex_to_bytes(raw_tx)))
        from_ = w3.eth.account.recover_transaction(raw_tx)
        to = w3.to_checksum_address(tx.to) if tx.to else None
        data = w3.to_hex(tx.data)
        r = hex(tx.r)
        s = hex(tx.s)
        chain_id = (tx.v - 35) // 2 if tx.v % 2 else (tx.v - 36) // 2
        return DecodedTx(hash_tx, from_, to, tx.nonce, tx.gas, tx.gas_price, tx.value, data, chain_id, r, s, tx.v)
    
    # 2) convert the hex string to bytes:
    signed_tx_as_bytes = to_bytes(hexstr=raw_tx)

    # 3) deserialize the transaction using the latest transaction builder:
    decoded_tx = TransactionBuilder().decode(signed_tx_as_bytes)
    sender = encode_hex(decoded_tx.sender)
    decoded_tx = decoded_tx.__dict__['_inner'].as_dict()
    decoded_tx['from'] = w3.to_checksum_address(sender)
    decoded_tx['to'] = w3.to_checksum_address(decoded_tx['to']) if decoded_tx['to'] else None
    decoded_tx['data'] = decoded_tx['data'].hex()
    return decoded_tx

