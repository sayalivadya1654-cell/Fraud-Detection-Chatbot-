from web3 import Web3
import json
import os
import hashlib

ganache_url = "HTTP://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
chain_id = 1337

# Load credentials
private_key = os.getenv("GANACHE_PRIVATE_KEY")
my_address = os.getenv("GANACHE_ACCOUNT")

# Load compiled contract ABI
build_path = os.path.join(os.path.dirname(__file__), "build.json")
with open(build_path, "r") as build_file:
    compiled_sol = json.load(build_file)

abi = compiled_sol["contracts"]["contract.sol"]["FraudDetection"]["abi"]

# Load deployed contract address
addr_path = os.path.join(os.path.dirname(__file__), "contract_address.txt")
with open(addr_path, "r") as addr_file:
    contract_address = addr_file.read().strip()

contract = web3.eth.contract(address=contract_address, abi=abi)

def add_record_onchain(txnId, payload, status):
    """Store ML fraud detection result on blockchain"""
    data_json = json.dumps(payload, sort_keys=True)
    data_hash = hashlib.sha256(data_json.encode()).hexdigest()

    nonce = web3.eth.getTransactionCount(my_address)
    txn = contract.functions.addRecord(txnId, data_hash, status).build_transaction({
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
        "gasPrice": web3.eth.gas_price
    })

    signed_txn = web3.eth.account.sign_transaction(txn, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    return tx_hash.hex(), receipt
