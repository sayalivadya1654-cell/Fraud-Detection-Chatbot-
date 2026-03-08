from web3 import Web3
from solcx import compile_standard, install_solc, set_solc_version
import json
import os

# Install and set Solidity compiler version
install_solc("0.8.0")
set_solc_version("0.8.0")

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
account = w3.eth.accounts[0]

# Get absolute project root path
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
contract_path = os.path.join(base_dir, "contracts", "FraudDetection.sol")

with open(contract_path, "r") as f:
    source = f.read()

compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {"FraudDetection.sol": {"content": source}},
    "settings": {
        "outputSelection": {
            "*": {
                "*": ["abi", "evm.bytecode.object"]
            }
        }
    }
})

abi = compiled_sol["contracts"]["FraudDetection.sol"]["FraudDetection"]["abi"]
bytecode = compiled_sol["contracts"]["FraudDetection.sol"]["FraudDetection"]["evm"]["bytecode"]["object"]

# Create artifacts folder
artifacts_path = os.path.join(base_dir, "artifacts")
os.makedirs(artifacts_path, exist_ok=True)

# Save ABI
with open(os.path.join(artifacts_path, "contract_abi.json"), "w") as f:
    json.dump(abi, f)

# Deploy contract
FraudDetection = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = FraudDetection.constructor().transact({"from": account})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# Save contract address
with open(os.path.join(artifacts_path, "contract_address.txt"), "w") as f:
    f.write(tx_receipt.contractAddress)

print("✅ FraudDetection deployed at:", tx_receipt.contractAddress)