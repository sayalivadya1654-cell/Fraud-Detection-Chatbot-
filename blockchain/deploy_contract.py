import json
import os
from solcx import compile_standard, install_solc
from web3 import Web3

# Install Solidity compiler
install_solc("0.8.0")

# Read Solidity file
with open("blockchain/FraudDetection.sol", "r") as file:
    contract_source_code = file.read()

# Compile contract
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"FraudDetection.sol": {"content": contract_source_code}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.0",
)

# Save ABI directly in blockchain/
abi = compiled_sol["contracts"]["FraudDetection.sol"]["FraudDetection"]["abi"]
with open("blockchain/contract_abi.json", "w") as abi_file:
    json.dump(abi, abi_file)

# Get bytecode
bytecode = compiled_sol["contracts"]["FraudDetection.sol"]["FraudDetection"]["evm"]["bytecode"]["object"]

# Connect to Ganache
ganache_url = "HTTP://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_url))

account_address = "0xCa4c8B135A5FEB1F6086A905a8F517Cd07B0016A"
private_key = "0xcf8c0e4bb203d56b5f0b76b5436420a550e1323275b7fbce4f664d1c0018370d"

# Deploy contract
FraudDetection = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.get_transaction_count(account_address)
transaction = FraudDetection.constructor().build_transaction({
    "chainId": 1337,
    "gas": 3000000,
    "gasPrice": w3.to_wei("20", "gwei"),
    "nonce": nonce
})

# Sign & send
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

# Wait for receipt
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Contract deployed at address: {tx_receipt.contractAddress}")

# Save contract address in blockchain/
with open("blockchain/contract_address.txt", "w") as addr_file:
    addr_file.write(tx_receipt.contractAddress)
