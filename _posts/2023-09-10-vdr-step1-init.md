---
title: SSI 개발 환경 구성하기 - Step1 Init
date: 2023-09-07 05:30 +09:00
published: true
categories: [SSI]
tags: [BlockChain, Dev, Smart Contract, Solidity, SSI, DID, Python]
---

[Prolog][Prolog]를 통해 SSI 개발 환경 구성을 위한 기본 프로그램을 알아봤으며 설치까지 완료했습니다. 
개발환경 초기 세팅을 하기에 앞서 우리가 앞으로 어떤 구성을 만들지, 그리고 어디부터 만들어 갈지를 고민해 보겠습니다. 

### Verifiable Credentials LifeCycle

![LifeCycle](/assets/images/verifiable_credentials_lifecycle.jpg)
_Verifiable Credentials LifeCycle (출처 : [Verifiable Credentials LifeCycle 1.0][LifeCycle_Draft])_

> Verifiable Credentials LifeCycle 은 본적있으며 구성원의 기본 역할은 알고 있음을 가정하고 설명됩니다. 

(현재 Unofficial Draft로 분류된) Verifiable Credentials LifeCycle 입니다. 
LifeCycle 을 구성하는 각 구성원은 Issuer, Holder, Verifier, Registry 이며 어떤 역할을 하는 구성원이든 처음 Ecosystem 에 들어오면 Registry 에 등록하는 절차부터 시작합니다. 이때, Registry 는 Credential 을 저장하고 요청시 전달하는 단순 DataBase 기능에 블록체인이 갖는 데이터 무결성까지 함께 제공해야 합니다.  
이로 인해, SSI Ecosystem 에서 Registry 를 단순 저장 공간이 아닌 `Verifiable Data Registry (VDR)` 로 표현합니다.   
따라서, Issuer, Holder, Verifier 를 구성하기 이전 `Registry` 부터 준비한 후 개별 구성원을 추가하겠습니다. 

### Verifiable Data Registry (VDR)

앞서 설명한 것처럼 VDR은 "DataBase 의 기능 + 블록체인의 무결성" 이 결합된 형태입니다. 따라서, 블록체인의 무결성은 이더리움으로, DataBase의 기능은 스마트 컨트랙트와 스마트 컨트랙트에 접근할 API 서버로 대체합니다. 

이더리움 네트워크는 Mainnet과 테스트넷(Goerli, Sepolia, Rinkeby 등) 으로 구성되어 있습니다. Mainnet 이나 테스트넷 중 하나를 선택해 사용할 수 있지만, 초기 개발단계에서 테스트를 좀 더 용이하게 하기 위해 로컬 PC 에 Ganache-Cli 를 Docker 로 구성해 사용합니다. 

> Ganache-Cli 는 PoA 방식의 이더리움 프라이빗 네트워크로 테스트 계정 10개를 제공하며, 스마트 컨트랙트를 쉽게 배포해 동작을 확인할 수 있습니다. 

![LifeCycle_Detail](/assets/images/LifeCycle_Details.svg)
_Verifiable Credentials LifeCycle Details (출처 : [LifeCycle Details][LifeCycle_Details])

(Ecosystem 이 구성됐다고 가정했을 때) Registry 는 Issuer 가 발급한 Credential 의 검증 정보를 `저장`하고 Verifier 가 검증 정보를 `조회`하고 시간이 지나 더 이상 유효하지 않을 때, `삭제` 합니다. 








---
### 정리
* 

---
### 참고
* [(PDF) Self-Sovereign Identity as a Service : Architecture in Practice](https://arxiv.org/pdf/2205.08314.pdf)
* [(Youtube) Verifiable Credentials 101 for SSI with Tyler Ruff](https://youtu.be/6O_iJnhIh5o?si=fmru4N7QEwIuCwqz)


[Prolog]: https://keitechnote.github.io/blog/posts/vdr-step0-prolog
[LifeCycle_Draft]: https://w3c-ccg.github.io/vc-lifecycle/
[LifeCycle_Details]: https://www.w3.org/TR/vc-data-model/#lifecycle-details

