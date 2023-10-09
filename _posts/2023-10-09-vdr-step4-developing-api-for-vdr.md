---
title: SSI 개발 환경 구성하기 - Step4 Developing APIs for VDRs
date: 2023-10-09 05:30 +09:00
published: true
categories: [SSI]
tags: [BlockChain, Dev, Smart Contract, Solidity, SSI, DID, Python]
---

## 개요

[Step2 First Contract][step2_first_contract] 에서 개발한 VDR 스마트 컨트랙트를 [Deploy Smart Contract on Ganache-Cli][step3_Deploy_Contract] 
에서 로컬 개발 환경인 Ganache-Cli 에 배포해 보았습니다. 이제 배포된 스마트 컨트랙트의 Register 와 Resolve 함수를 호출하력고 합니다. 
배포된 스마트 컨트랙트의 함수에 접근하기 위해선 스마트 컨트랙트 주소로 접속하고 함수를 호출하는 과정이 필요합니다. 하지만 빈번하게 발생하는 동작이 복잡하면 사용하기 불편하고, 스마트 컨트랙트 주소가 변경되면 이를 사용하는 모든 사용자가 주소를 알아야 한다는 문제가 있습니다. 
만약, 작성된 스마트 컨트랙트를 100명이 사용하고 있다면, 스마트 컨트랙트가 업그레이드되거나 문제를 수정해 다시 배포하면 주소가 변경되기 때문에 사용자 100명에게 변경된 주소를 알려줘야 하는 문제가 있습니다. 
따라서, 사용자는 스마트 컨트랙트에 직접 접속하지 않지만 스마트 컨트랙트의 함수 호출을 보장해 줄 수 있는 별도의 프로그램을 만들면 이러한 문제의 상당 부분을 해소할 수 있습니다. 본 Post 에서는 이러한 부분을 해결해 줄 API 를 만듭니다. 이 API 는 스마트 컨트랙트에 대신 접속하고 사용자가 호출한 함수를 대신 호출해 주고 결과를 전달해 주는 역할을 하게 됩니다. 

> API 는 *A*pplication *P*rogramming *I*nterface 의 첫 머리글자를 딴 약자입니다. 어플리케이션(또는 프로그램, 서비스) 간 연결해 주는 것을 의미합니다. 본 Post 에서는 사용자와 VDR 스마트 컨트랙트간을 연결해 주는 것을 의미합니다.
{: .prompt-info}

> 앞서 언급한 API 는 "사용자 - API - 스마트 컨트랙트" 간 연결로 발생할 수 있는 문제를 해소하고 있습니다. 하지만 사용자와 스마트 컨트랙트 간의 문제는 해소되지만 이는 사용자가 갖는 불편함을 API 가 대신 감내하는 것입니다. 즉, API 와 스마트 컨트랙트 간의 문제는 동일한 문제가 여전히 존재합니다. 이 점은 스마트 컨트랙트가 처음 공개되었을 때 부터 재기되어 왔던 문제점이며 최근에는 프록시를 통해 해소하려고 노력하고 있습니다. 본 블로그의 [블록체인 카테고리][BlockChain_Category] 를 참고하기 바랍니다. 
{: .prompt-warning}

### API 개발하기 앞서...

API 를 개발하는 방식은 다양합니다. 본 Post 는 [Prolog][step0-prolog] 에서 정의한 것처럼 개발언어로 파이썬을 활용해 API 를 개발합니다. 
구글에서 "파이썬 API 만들기" 로 검색하면 "Flask", "FastAPI", "Django" 외 여러가지 방법이 있음을 알 수 있습니다. 물론 모두 좋은 방법이고 개발된 철학에 맞는 장점을 품고 있지만, 본 Post 에서는 그 중 "FastAPI" 를 사용합니다. 

[FastAPI 홈페이지][fastapi_homepage] 를 보면 다양한 장점들을 설명하고 있지만 "빠름", "짧음", "견고함"과 같은 용어들은 다양한 형태로 API 를 작성해 보지 않은 사용자라면 와닿지 않습니다. 다만, 개인적으로 사용하기 쉽다라는 장점도 있지만, 가장 큰 장점이라면 "개발 문서를 기본 제공하는 것"입니다. 
어떤 것이든 문서를 작성하고 그 문서를 다른 사람들과 함께 공유해 본 사람이라면, 가장 골치 아픈 부분이 항상 최신버전을 유지하는 부분일 것입니다. 앞으로 만들 API 는 다른 사용자가 스마트 컨트랙트의 기능을 사용할 수 있도록 기능을 제공하지만, 완성된 상태가 아닌, 꾸준히 수정, 개발되어야 하기 때문에 빈번히 변경이 발생합니다. 이 모든 것을 매번 문서로 작성하고 공유하는 것은 개발자에게 있어 매우 고된 작업입니다. 하지만, FastAPI 는 Swagger UI 나 ReDoc 두가지 형태로 문서를 자동 생성하므로 개발자는 개발에만 집중할 수 있습니다. 


### FastAPI 설치하기

FastAPI 는 파이썬용 웹 프레임워크입니다. 앞서 설명한 Swagger UI 나 ReDoc 외에 다양한 기능을 활용하기 위해선 FastAPI 프레임워크를 설치해야 합니다. 

- 명령어 : `pip install fastapi`











---
### 정리
* 

---
### 참고
* [Step0 - Prolog](https://keitechnote.github.io/blog/posts/vdr-step0-prolog/)
* [Step1 - Init (VSCode + TruffleSuite + Ganache-cli)](https://keitechnote.github.io/blog/posts/vdr-step1-init/)
* [Step2 - First Contract](https://keitechnote.github.io/blog/posts/vdr-step2-first-contract/)
* [Step3 - Deploy Smart Contract on Ganache-Cli](https://keitechnote.github.io/blog/posts/vdr-step3-deploy-ganache/)

[step0-prolog]: https://keitechnote.github.io/blog/posts/vdr-step0-prolog/
[step2_first_contract]: https://keitechnote.github.io/blog/posts/vdr-step2-first-contract/
[step3_Deploy_Contract]: https://keitechnote.github.io/blog/posts/vdr-step3-deploy-ganache/
[BlockChain_Category]: https://keitechnote.github.io/blog/categories/blockchain/
[fastapi_homepage]: https://fastapi.tiangolo.com/ko/