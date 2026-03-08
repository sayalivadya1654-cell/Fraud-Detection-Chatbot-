from web3 import Web3
import json
import os

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
account = w3.eth.accounts[0]

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
artifacts_path = os.path.join(base_dir, "artifacts")

with open(os.path.join(artifacts_path, "contract_abi.json"), "r") as f:
    abi = json.load(f)

with open(os.path.join(artifacts_path, "contract_address.txt"), "r") as f:
    address = f.read().strip()

contract = w3.eth.contract(address=address, abi=abi)

# ✅ Store fraud result (2 string parameters)
tx_hash = contract.functions.storeResult(
    "TXN12345",     # transaction ID
    "Fraud - Risk Score: 87"   # result string
).transact({"from": account})

receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("✅ Result stored on blockchain")

# Check count
count = contract.functions.getResultCount().call()
print("Total stored results:", count)

# Retrieve latest result
result = contract.functions.getResultAt(count - 1).call()
print("Stored Result:", result)