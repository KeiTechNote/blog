---
title: SSI 개발 환경 구성하기 - Prolog
date: 2023-09-09 23:30 +09:00
published: true
categories: [SSI]
tags: [BlockChain, Dev, Smart Contract, Solidity, SSI, DID, Python]
---

SSI 개발환경을 구성하는 다양한 방식이 있습니다. 
주로 개발 언어에 따라, 개발 목적에 따라, 개발 환경에 따라 입맛에 맞는 환경을 구성합니다. 

이번 Post에서는 다음의 요건을 고려해 개발환경을 선택했습니다. 

1. 충돌 가능성

    개발 특성상 다양한 3rd Party 라이브러리를 설치하고, 변경하며, 테스트합니다. 
    이때, 라이브러리간 의존성이나 버전 문제로 환경 구성이 용이하지 않을 수 있습니다. 
    예를 덜어, 개발 프로젝트1은 ZIP 라이브러리 버전 1.0 을 쓰는데 개발 프로젝트2는 ZIP 라이브러리 버전 2.0 을 쓴다고 가정했을 때, 서로 다른 버전을 같은 환경에 설치할 경우, 설치시 또는 실행시 이전에 없던 오류가 발생할 수 있습니다. 


2. 변화 관리의 용이성

    개발이란 한번에 완료되는 형태가 아닌 지속적인 변화가 발생하는 생명체와 같습니다. 계속 진화하려고 노력합니다. 
    예를 들면, SSI 개발 프로젝트에서는 스마트 컨트랙트 개발이 포함되어 있습니다. 이때 개발된 스마트 컨트랙트를 블록체인 네트워크 상에 배포할 때, truffle 을 사용한다고 가정해 봅시다. 최초 구축시에는 truffle에 만족했지만, 이후 Hardhat 이 개선되면서 편의성 기능이 추가된다면, 배포 환경을 truffle 에서 Hardhat 으로 변경해야 할 수도 있습니다. 또는 Hardhat 적용 후 다양한 이유로 truffle 로 롤백해야 할 수도 있습니다. 
    이러한 과정은 솔리디티 버전을 변경하는 과정에서도, 블록체인 네트워크를 변경하는 과정(예: 이더리움 -> 폴리곤)에서도 발생할 수 있습니다. 


3. 익숙한 개발 언어 사용

    처음 스마트 컨트랙트를 개발하고 SSI 환경을 구축한다면, 익숙한 언어를 사용하길 권장합니다. 물론 다양한 언어를 공부한 경험도 있고, 충분한 개발 경험이 있어 앞으로 발생하는 다양한 오류들을 스스로 해결해 나갈 수 있다면 전혀 문제되진 않습니다. 하지만, 대다수는 그렇지 않을 것입니다. 스마트 컨트랙트 개발 또한 처음이라면 더욱 그렇습니다. 사전에 발생할 수 있는 문제를 해소하고 시작한다면, 새로운 것을 익히는 과정에서 발생하는 오류들에 집중할 수 있기 때문에 앞으로 나아가는데 좀 더 쉬울 것 입니다. 


이러한 조건들을 고려해 나에게 맞는 개발환경을 구축하면 됩니다. 
앞으로 게시되는 SSI 개발 프로젝트는 위의 조건에 충족하는, 다음과 같은 나만의 환경을 기준으로 설명합니다. 

- OS : Windows11
- OS 언어 : 한글
- IDE : VSCode([다운로드][VSCode 다운로드]), Remix IDE([사이트][Remix IDE 사이트])
- 개발언어
    - 파이썬 3.10 이상([다운로드][Python 다운로드]) or 파이썬 플랫폼 Anaconda ([다운로드][Anaconda 다운로드])
    - 솔리디티 0.8.0 이상
- 필수 프로그램
    - NodeJS 18.17.0 이상 ([다운로드][NodeJS 다운로드])
    - TruffleSuite ([다운로드][TruffleSuite 다운로드]) or Hardhat ([다운로드][Hardhat 다운로드])
- 인프라 
    - Docker ([다운로드][Docker 다운로드])
    - Ganache-cli ([도커 이미지 다운로드][Ganache-cli 도커 이미지 다운로드])
- 기타 (Optional)
    - Git ([다운로드][Git 다운로드])

Remix IDE는 Browser에서 동작하는 Online IDE 입니다. 물론 Remix IDE도 설치형이 있지만 Remix IDE는 즉시 확인할 수 있는 테스트 형태의 코드를 작성할 뿐 실제 개발은 VSCode에서 진행되므로 설치형은 사용하지 않아도 됩니다. 이와 함께 솔리디티 또한 TruffleSuite 설치시 함께 설치되므로 별도 설치 링크는 첨부하지 않았습니다. 

일부 프로그램은 설치 순서가 있습니다. 
TruffleSuite 와 HardHat 은 설치시 터미널 환경에서 NodeJS 의 `npm` 을 사용합니다. 따라서, NodeJS를 먼저 설치한 후 설치를 진행하기 바랍니다.
인프라 부분에서 Ganache-cli는 도커 이미지를 사용하기 때문에, 도커를 먼저 설치해야 다운로드 할 수 있습니다. 


> Remix IDE, 솔리디티, TruffleSuite, Hardhat, Docker, Ganache-cli, Git 등 용어가 생소한 분들도 있습니다. 우리가 목표로 하는 SSI 를 개발하기 위한 도구이므로 필요할 때 어떻게 활용하는지만 알고 있으면 되고 이후 Post 에서 필요할 때 관련 설명을 첨부할 예정입니다. 
{: .prompt-info}


SSI 개발환경 구성은 다양한 조합이 가능합니다. 그 중 가장 기본이 되는 조합은 빌드 환경과 개발 IDE 입니다. 
필수 프로그램으로 언급했던 TruffleSuite 와 Hardhat 은 가장 대표적인 스마트 컨트랙트 빌드 환경을 제공하는 프레임워크입니다. 

> 빌드란 개발된 프로그램을 실행할 환경에 맞게 변환하는 것을 의미합니다. 즉, 스마트 컨트랙트(sol 파일)을 이더리움 환경에서 동작하는 바이트코드로 변환하는 것을 의미합니다. 
{: .prompt-info}

따라서, 개발환경 구성을 위해선 TruffleSuite 와 Hardhat 중 하나만 선택해 설치하면 됩니다. 
즉, 조합하면 다음과 같이 세가지 방식이 나올 수 있습니다. 

- VSCode + TruffleSuite
- VSCode + Hardhat
- VSCode + TruffleSuite (VSCode Extension)

> TruffleSuite 에서 VSCode용 확장 프로그램 형태로 TruffleSuite 를 제공하고 있습니다. 
{: .prompt-info}


---
### 정리
* 자신에게 맞는 개발환경을 구축한다. 

---
### 참고
- [Docker Cli Command](https://docs.docker.com/engine/reference/run/)
- [Git의 기초](https://git-scm.com/book/ko/v2)
- [Truffle for VSCode](https://trufflesuite.com/docs/vscode-ext/)



[VSCode 다운로드]: https://code.visualstudio.com/download
[Remix IDE 사이트]: https://remix.ethereum.org/
[Python 다운로드]: https://www.python.org/downloads/
[Anaconda 다운로드]: https://www.anaconda.com/
[NodeJS 다운로드]: https://nodejs.org/ko/download
[TruffleSuite 다운로드]: https://trufflesuite.com/docs/truffle/how-to/install/#install-truffle
[Hardhat 다운로드]: https://hardhat.org/hardhat-runner/docs/getting-started#installation
[Docker 다운로드]: https://www.docker.com/products/docker-desktop/
[Ganache-cli 도커 이미지 다운로드]: https://hub.docker.com/r/trufflesuite/ganache-cli
[Git 다운로드]: https://git-scm.com/downloads

