# -*- coding:utf-8 -*-
from web3 import Web3, HTTPProvider
import json

# Ganache 연결
ganache_address = "http://127.0.0.1:9545"
web3 = Web3(HTTPProvider(ganache_address))
print(f"[*] Connect Ganache : {web3.is_connected()}")


# 배포된 스마트 컨트랙트 정보 수집 (abi, bytecode)
compiled_sol = r"c:\Users\amana\OneDrive\바탕 화면\Dev\client\src\contracts\simpleVDR.json"
with open(compiled_sol, "r", encoding="UTF-8") as file:
    compiled_data = json.load(file)
    abi = compiled_data["abi"]
    bytecode = compiled_data["bytecode"]

# 받는 사람
contract_addr = "0xAb3604c16ea9Bd01edcd44707930eDf756154B29"

# 보내는 사람
deployer_addr = "0xe974d84295a8fd6fbd2fc368329d6baebae9ad00"
# or
# deployer_addr = web3.eth.accounts[0]
deployer_privatekey = "b7ce7e89e213c2f60acf743a8a02ece3220bb7dee784da12c6fee77e980ac28d"

# register 트랜잭션 
contract = web3.eth.contract(address=contract_addr, abi=abi)
tx = contract.functions.register("dkei2", "dkei_did_document").build_transaction({
    "from" : deployer_addr,
    'gas': 200000,
    'gasPrice': web3.eth.gas_price,
    'nonce': web3.eth.get_transaction_count(deployer_addr)
})
print(f"[*] Tx : {tx}")

# register 트랜잭션 서명
signed_tx = web3.eth.account.sign_transaction(tx, deployer_privatekey)
print(f"[*] Signed Tx : {signed_tx}")

# 트랜잭션 전송
tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
print(f"[*] Transaction Hash : {tx_hash}")

# 트랜잭션 전송 후 처리 결과 
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
print(f"[*] {tx_receipt}")