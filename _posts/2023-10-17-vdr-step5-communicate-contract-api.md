---
title: SSI 개발 환경 구성하기 - Step5 Communicating between smart contracts and API
date: 2023-10-16 05:30 +09:00
published: true
categories: [SSI]
tags: [BlockChain, Dev, Smart Contract, Solidity, SSI, DID, Python]
---

지금까지 스마트 컨트랙트를 개발했고 앞으로 스마트 컨트랙트와 사용자를 연결한 API 서버도 만들어보았습니다. 
상호간에 연결하기 위해선 몇가지 단계가 더 필요합니다. 우선 서로간에 연결하기 위해 파이썬 라이브러리가 추가로 필요합니다. 
그 라이브러리가 Web3 입니다. Web3 라이브러리를 설치한 후 Ganache-Cli 와 통신해 보겠습니다. 

### Web3 라이브러리 설치 및 API 함수 개발하기 

- 명령어 : `pip install web3`

![install_web3](/assets/images/install_web3.png)

_Web3 라이브러리 설치_

설치된 Web3 라이브러리는 블록체인 환경에 배포된 스마트 컨트랙트와 통신하기 위한 기능을 제공합니다.
이제 Web3 라이브러리를 활용해 스마트 컨트랙트와 연결할 함수 2개를 작성합니다. 
작성할 함수는 스마트 컨트랙트로 작성했던 `register` 와 `resolve` 입니다. API 서버에서도 동일한 이름으로 작성하겠습니다. 

우선 Web3 라이브러리를 가져옵니다. 

```python
from web3 import Web3, HTTPProvider
import json
```

> 파이썬에서는 라이브러리를 가져오는 방식이 크게 `from & import` 와 `import` 두가지가 있습니다. 
- from & import : web3 라이브러리를 가져오는 것처럼 web3 라이브러리에서 특정 함수, 클래스만을 가져올 때 사용합니다. 
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