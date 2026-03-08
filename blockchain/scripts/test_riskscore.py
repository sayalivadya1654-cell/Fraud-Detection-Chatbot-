from scripts import blockchain_utils as utils

w3 = utils.w3
account = w3.eth.accounts[0]

risk_contract = utils.load_contract("artifacts/contract_address_riskscore.txt", "artifacts/contract_abi_riskscore.json")

# Example: set and read a score
tx = risk_contract.functions.setRiskScore(account, 50).transact({"from": account})
w3.eth.wait_for_transaction_receipt(tx)
score = risk_contract.functions.getRiskScore(account).call()
print(f"Risk score for {account}: {score}")