from scripts import blockchain_utils as utils

w3 = utils.w3
account = w3.eth.accounts[0]

fraud_contract = utils.load_contract("artifacts/contract_address.txt", "artifacts/contract_abi.json")
risk_contract = utils.load_contract("artifacts/contract_address_riskscore.txt", "artifacts/contract_abi_riskscore.json")

tx_count = fraud_contract.functions.getTransactionCount().call()

for i in range(tx_count):
    user, amount, flagged = fraud_contract.functions.getTransaction(i).call()
    score = 100 if flagged else 10
    tx = risk_contract.functions.setRiskScore(user, score).transact({"from": account})
    w3.eth.wait_for_transaction_receipt(tx)
    print(f"Risk score {score} set for {user}")