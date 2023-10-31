---
title: SSI 개발 환경 구성하기 - Step5 Communicating between smart contracts and API
date: 2023-10-31 05:30 +09:00
published: true
categories: [SSI]
tags: [BlockChain, Dev, Smart Contract, Solidity, SSI, DID, Python]
---

### 들어가기 앞서...

지금까지 스마트 컨트랙트를 개발했고 앞으로 스마트 컨트랙트와 사용자를 연결한 API 서버도 만들어보았습니다. 
이 시점에 한가지 고려할 부분이 있습니다. Truffle 환경에서 개발된 스마트 컨트랙트를 배포할 때, Truffle 환경의 Ganache 는 개발할 때는 용이하지만, 앞으로 VDR 컨트랙트를 Ganache 에 배포해서 운영하진 않을 것입니다. 이더리움 개발 또는 테스트 노드에 배포하거나 Private 이더리움 노드에 배포하거나 스마트 컨트랙트가 호환되는 제 3의 블록체인 네트워크에 배포할 수 도 있습니다. 
따라서, 운영환경에서 배포는 어떤 방식으로 할지 생각해야 합니다. 

굳이 이 시점에 고민하는 이유는 여러사람이 함께 개발하는 프로젝트라면 각각의 영역을 담당하면 되지만 본 프로젝트는 한명이 서로 다른 두 환경의 개발 환경에서 개발해야 합니다. 즉, 서로 다른 개발 환경을 한 명이 오가며 개발해야 한다면 개발은 각각 환경에서 하지만 배포는 일관되게 할지, 개발, 배포를 각 개발환경에 따라 다르게 가져갈지를 결정해야 하기 때문입니다. 
그리고 또 다른 이유는 회귀 본능 때문입니다. 스마트 컨트랙트 개발이 익숙하지 않고 Truffle 을 처음 사용해 본다면 익숙한 언어로 회귀하고 싶습니다. 개발 효율이 훨씬 뛰어나고 오류가 발생해도 빠르게 이해하고 조치할 수 있는 등 경험치가 다름에 오는 부분이 분명 있기 때문입니다. 

이 부분은 개인 성향에 따라 다를 것이고, 두 가지 모두 가능한 방법이기에 고민이 발생합니다. 즉,

1. 스마트 컨트랙트 개발, 운영과 API 서버 개발 운영을 완전 분리한다. 
2. 스마트 컨트랙트, API 서버 개발은 각각의 환경에서 진행하되, 배포는 한 환경(여기서는 API 서버를 개발하는 파이썬) 으로 통인한다. 

1번 방식은 Truffle-config.js 파일에 배포할 네트워크 정보를 기입하고 `truffle migrate --network <기입한 네트워크 이름>` 로 배포할 수 있습니다. 
2번 방식은 Truffle 환경에서 스마트 컨트랙트를 개발/테스트를 완료하고 API 서버를 재시작할 때, 스마트 컨트랙트를 원하는 네트워크에 배포할 수 있습니다. 

본 프로젝트는 1번 방식으로 진행하지만 2번 방식을 사용해도 차이가 전혀 없습니다. 이 점 참고 바랍니다. 

### Web3 라이브러리 설치 및 테스트 코드 작성하기 

각각 구성된 스마트 컨트랙트와 API 서버를 연결할 차례입니다. 즉, 현재 개발 프로젝트 상에서는 배포된 스마트 컨트랙트는 Ganache 에 있으므로, Ganache 와 API 서버간에 연결해야 합니다. 

파이썬에서는 이더리움 네트워크와 연결하기 위해 Web3 라이브러리를 사용합니다.
Web3 라이브러리를 설치하고 개발된 스마트 컨트랙트를 배포했던 Truffle 의 Ganache 와 연결하고 스마트 컨트랙트에서 작성한 `register` 와 `resolve`를 호출하는 API 를 만들겠습니다. 

다만, 그 전에 Web3 라이브러리를 처음 사용해 보기 때문에 Ganache 계정 주소를 출력하는 간단한 테스트 코드를 작성해 보겠습니다. 

Web3 라이브러리를 설치합니다. 

- 명령어 : `pip install web3`

![install_web3](/assets/images/install_web3.png)

_Web3 라이브러리 설치_

설치한 Web3 라이브러리를 가져옵니다. 

```python
from web3 import Web3, HTTPProvider
```

> 파이썬에서는 라이브러리를 가져오는 방식이 크게 `from & import` 와 `import` 두가지가 있습니다. 
- from & import : web3 라이브러리를 가져오는 것처럼 web3 라이브러리에서 특정 함수, 클래스만을 가져올 때 사용합니다.
{: .prompt-info}

Web3 라이브러리로 Truffle 환경의 Ganache 로 접속하기 위해서 Ganache 주소를 사용합니다. 
Truffle 환경의 Ganache 주소는 `truffle develop` 명령어로 Ganache 환경에 들어가면 확인할 수 있습니다. 

![truffle_ganache_addr_1](/assets/images/truffle_ganache_addr_1.png)

_truffle develop 명령어로 확인하는 Ganache 주소_

또는 스마트 컨트랙트가 배포되는 블록체인 네트워크 정보를 저장하고 있는 `truffle-config.js` 에서도 확인할 수 있습니다. 

![truffle_ganache_addr_2](/assets/images/truffle_ganache_addr_2.png)

_truffle-config.js 설정 파일로 확인하는 Ganache 주소_

Truffle 환경의 Ganache 주소는 `http://127.0.0.1:9545` 임을 확인했습니다. Ganache 환경에 접속해 보겠습니다. 


```python
from web3 import Web3, HTTPProvider

ganache_address = "http://127.0.0.1:9545
web3 = Web3(HTTPProvider(ganache_address))
print(web3.is_connected())
```

![truffle_ganache_connect](/assets/images/truffle_ganache_connect.png)

_truffle 환경의 Ganache 접속_

Web3 라이브러리는 이더리움 노드의 모든 기능을 제공하고 있으므로 자세한 사용법은 [공식문서][web3py_document]를 참고하기 바랍니다. 

### 스마트 컨트랙트 함수 호출하기

Truffle 환경의 Ganache 와 연결이 확인되었으므로 작성한 스마트 컨트랙트를 Ganache 에 배포(`migrate`명령어 사용)한 후 배포된 스마트 컨트랙트의 함수를 호출해 보겠습니다. 

블록체인에서는 블록체인 네트워크와 상호작용하기 위해 서로 주고받는 데이터를 `트랜잭션 (Transaction)`이라 합니다. 트랜잭션은 이메일(더욱 직관적으로는 편지)을 발송하는 것과 같습니다.  즉, 보내는 사람, 받는 사람, 주고받을 정보 그리고 약간의 수수료로 구성되어 있습니다. 
우선 본 Post에서 받는 사람은 배포된 스마트 컨트랙트이므로 필요한 세부 정보는 다음과 같습니다. 

- 배포된 스마트 컨트랙트 주소 
- 배포된 스마트 컨트랙트 컴파일 정보 (ABI, ByteCode)

이는 이메일을 보낼 때 받는 사람의 주소를 알아야 하고, 받는 사람의 주소 기입 방식을 아는 것과 같은 이치입니다. 
컨트랙트 주소는 Ganache 에 배포가 완료되면 화면에서 확인할 수 있습니다. 

![deployed_contract_address](/assets/images/deployed_contract_address.png)

_Ganache 에 배포된 컨트랙트 주소_

컨트랙트 컴파일 정보는 다음의 경로에 저장되어 있습니다. 

- 컴파일된 Truffle 데이터 : `~\Dev\client\src\contracts\simpleVDR.json`

컴파일된 스마트 컨트랙트는 인터페이스 정보를 관리하는 ABI 와 블록체인 네트워크상에 배포, 저장될 ByteCode 로 구분되며, 컴파일된 솔리디티 데이터인 SimpleVDR.json 파일에 관련 정보가 보관되어 있습니다. ABI 와 ByteCode 정보를 가져옵니다. 

```python
import json

compiled_sol = r"c:\Users\amana\OneDrive\바탕 화면\Dev\client\src\contracts\simpleVDR.json"
with open(compiled_sol, "r", encoding="UTF-8") as file:
    compiled_data = json.load(file)
    abi = compiled_data["abi"]
    bytecode = compiled_data["bytecode"]
```

simpleVDR.json 파일은 json 파일형식으로 저장되어 있으므로 json 라이브러리를 가져와 읽어들입니다. 이때, json 파일내 데이터 인코딩 형식을 지정해 주어야 이후 활용시 `UnicodeDecodeError` 와 같은 오류가 발생하지 않습니다. 

> 읽어들인 데이터(`compiled_data`)는 파이썬의 Dict 자료형이므로 `compiled_data["abi"]` 와 같이 직접 가져오거나 `compiled_data.get("abi", "")` 와 같이 get 메소드를 활용해 가져올 수 있습니다. 직관적으로 이해할 수 있도록 직접 접근하는 코드를 작성했지만, 잘못된 json 파일을 가져오거나, json 파일에 오류가 있는 등의 문제를 사전에 알 수 있도록 get 메소드를 활용하는 것을 권장합니다. 
{: .prompt-info}

보내는 사람은 배포자, 즉 Ganache 계정으며 필요한 정보는 다음과 같습니다. 

- 배포자 주소
- 배포자 개인키

배포자 주소 및 개인키는 `truffle develop` 명령어로 Ganache 에 들어가면 바로 확인할 수 있습니다 .

![deploy_address_privatekey](/assets/images/deploy_address_privatekey.png)

_Ganache 에서 배포자 주소 및 개인키 확인_

Ganache 실행시 기본 제공되는 10개의 계정과 개인키 쌍을 볼 수 있습니다. 각 계정과 개인키는 순서대로 매핑되므로 원하는 계정과 개인키를 선택해 사용하면 됩니다. 본 Post 에서는 첫번째 (0번) 계정과 개인키를 사용합니다. 

```python
deployer_addr = "0xe974d84295a8fd6fbd2fc368329d6baebae9ad00"
deployer_privatekey = "b7ce7e89e213c2f60acf743a8a02ece3220bb7dee784da12c6fee77e980ac28d"
```

계정 정보 중 개인키를 함께 수집하고 있습니다. 보내는 사람의 정보를 알고 있지만 개인키를 추가로 수집하는 이유는 개인키로 암호화하는 디지털 서명을 통해 `부인방지` 를 하기 위함입니다. 

> 암호화 또는 복호화할 때 사용하는 키가 동일한 하나의 키만을 사용한다면 이를 `대칭키 (Symmetric Key)`, 서로 다른 2개의 키를 사용한다면 `비대칭키(Asymmetric Key)`라고 합니다. 그 중 2개의 키로 구성된 비대칭키는 키 중 하나를 외부에 노출할 수 있 수 있기 때문에 비대칭키 암호화를 `공개키 암호화`라고 부릅니다. 대표적인 공개키 암호화 활용예는 공인인증서가 있습니다. 공인인증서와 같이 공개키 암호화를 사용할 수 있도록 구성되어 있는 환경을 `공개키 기반 구조 (Public Key Infrastructure, PKI)` 라고 합니다. 공개키 암호화는 노출된 공개키로 암호화하는 방법과 노출되지 않은 개인키로 암호화하는 방법이 있으며 각각 `데이터 암호화`와 `디지털 서명` 기능을 제공합니다. 블록체인에서는 공개키 암호화의 디지털 서명 기능을 활용해 서명한 사람을 특정할 수 있는 `부안빙지` 기능을 사용합니다. 
{: .prompt-info}

보내는 사람과 받는 사람 정보를 모두 확인했습니다. 이러한 정보를 종합해 simpleVDR 컨트랙트의 `register` 함수를 호출하는 트랜잭션을 작성합니다.

```python
# -*- coding:utf-8 -*-
from web3 import Web3, HTTPProvider
import json

# Ganache 연결
ganache_address = "http://127.0.0.1:9545
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
```
Truffle 환경의 Ganache 가 실행된 상태에서 파이썬 코드를 실행하면 다음과 같은 결과를 확인할 수 있습니다. 

![contract_register_run_result](/assets/images/contract_register_run_result.png)

_simpleVDR의 register 호출 결과_












먼저 register 함수를 작성해 본 후 정상적으로 동작한다면, resolve 함수를 작성하겠습니다. 

```python
...생략



```









---
### 정리
* 
  
---
### 참고
* 샘플코드
    - [simple_vdr_register.py](https://github.com/KeiTechNote/blog/tree/main/codes/simple_vdr_register.py)


[web3py_document]: https://web3py.readthedocs.io/en/stable/web3.main.html