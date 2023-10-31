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
result = contract.functions.resolve("dkei2").call()
print(f"[*] Return : {result}")    #