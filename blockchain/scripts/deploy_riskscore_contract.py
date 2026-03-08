from web3 import Web3
from solcx import compile_standard, install_solc
import json
import os

install_solc("0.8.20")

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
account = w3.eth.accounts[0]

with open("contracts/RiskScore.sol", "r") as f:
    source = f.read()

compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {"RiskScore.sol": {"content": source}},
    "settings": {"outputSelection": {"*": {"*": ["abi","evm.bytecode.object"]}}}
})

abi = compiled_sol["contracts"]["RiskScore.sol"]["RiskScore"]["abi"]
bytecode = compiled_sol["contracts"]["RiskScore.sol"]["RiskScore"]["evm"]["bytecode"]["object"]

# Save ABI separately
os.makedirs("artifacts", exist_ok=True)
with open("artifacts/contract_abi_riskscore.json", "w") as f:
    json.dump(abi, f)

RiskScore = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = RiskScore.constructor().transact({"from": account})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

with open("artifacts/contract_address_riskscore.txt", "w") as f:
    f.write(tx_receipt.contractAddress)

print(f"RiskScore deployed at {tx_receipt.contractAddress}")