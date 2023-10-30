---
title: SSI 개발 환경 구성하기 - Step5 Communicating between smart contracts and API
date: 2023-10-16 05:30 +09:00
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

Truffle 환경의 Ganache 주소는 `http://127.0.0.1:9545` 임을 확인했습니다. 
Ganache 환경에 접속 후 정상 접속을 확인하기 위해 Ganache 가 제공하는 기본 계정 중 첫번째 계정 주소를 출력해 보겠습니다. 

```python
from web3 import Web3, HTTPProvider

ganache_address = "http://127.0.0.1:9545
web3 = Web3(HTTPProvider(ganache_address))
print(web3.eth.accounts[0])
```

![truffle_ganache_connect](/assets/images/truffle_ganache_connect.png)

_truffle 환경의 Ganache 접속_

계정 주소를 출력하는 것이외에 이더리움 노드가 제공하는 대부분의 기능을 Web3 라이브러리가 제공하고 있으므로 자세한 내용은 [공식문서][web3py_document]를 참고하기 바랍니다. 


### API 함수 작성










- import : json 라이브러리를 가져오는 것처럼 json 라이브러리를 모두 가져올 때 사용합니다. 



먼저 register 함수를 작성해 본 후 정상적으로 동작한다면, resolve 함수를 작성하겠습니다. 

```python
...생략



```









---
### 정리
* 

---
### 참고
* [Step0 - Prolog](https://keitechnote.github.io/blog/posts/vdr-step0-prolog/)
* [Step1 - Init (VSCode + TruffleSuite + Ganache-cli)](https://keitechnote.github.io/blog/posts/vdr-step1-init/)
* [Step2 - First Contract](https://keitechnote.github.io/blog/posts/vdr-step2-first-contract/)
* [Step3 - Deploy Smart Contract on Ganache-Cli](https://keitechnote.github.io/blog/posts/vdr-step3-deploy-ganache/)
* [Step4 - Configuring the FastAPI environment for API development](https://keitechnote.github.io/blog/posts/vdr-step4-config-fastapi-env-for-api-dev/)


[web3py_document]: https://web3py.readthedocs.io/en/stable/web3.main.html