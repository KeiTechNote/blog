---
title: SSI 개발 환경 구성하기 - Step1 Init (VSCode + TruffleSuite)
date: 2023-09-18 05:30 +09:00
published: true
categories: [SSI]
tags: [BlockChain, Dev, Smart Contract, Solidity, SSI, DID, Python]
---

## 개요

[Step0 - Prolog](https://keitechnote.github.io/blog/posts/vdr-step0-prolog/)를 통해 설치해야 하는 프로그램 목록과 개발환경을 위한 조합을 확인했습니다. 그 중 본 Post에서는 VSCode 와 TruffleSuite 를 조합한 개발환경을 구성해 보겠습니다. 

- 구성환경 : VSCode + TruffleSuite + Ganache-Cli

### 설치 방법 - VSCode

VSCode 는 Microsoft에서 제공하는 개발 IDE 입니다. 무료로 공개되어 있어 누구든지 설치할 수 있으며 확장 프로그램을 통해 다양한 기능을 자유롭게 추가할 수 있는 장점이 있어 (저를 포함한) 많은 개발자들이 사용하고 있습니다. 

- VSCode [다운로드][VSCode_Download]

![VSCode 다운로드](/assets/images/VSCode_Download.png){: .shadow }
_OS별 VSCode 다운로드 페이지_

붉은 색 박스로 표시해 둔 윈도우용 VSCode 를 클릭하면 VSCode 설치파일이 다운로드됩니다. 다운로드가 완료되면 이를 실행하고 "다음" 버튼만 눌러서 설치하면 됩니다. 별도 선택할 부분은 없습니다. 

설치가 완료되면 실행합니다. 다음과 같은 화면이 나온다면, 정상 설치가 완료되었습니다. 

![VSCode_실행](/assets/images/VSCode_Init.png){: .shadow }


### 설치 방법 - NodeJS + TruffleSuite

TruffleSuite 를 설치하기 위해서는 `npm`명령어를 사용합니다. npm 은 NodeJS 에서 제공하는 *N*ode *P*ackage *M*anager입니다. 
따라서, NodeJS 를 먼저 설치합니다. 만약 NodeJS 를 설치했다면 다음 단계로 넘어갑니다. 


#### 1. NodeJS

- NodeJS [다운로드][Node_Download]

![NodeJS 다운로드](/assets/images/NodeJS_Download.png){: .shadow }
_OS별 NodeJS 다운로드 페이지_

VSCode와 같이 붉은 색 박스로 표시해 둔 윈도우용 NodeJS 를 클릭하면 설치파일이 다운되며, 완료시 설치하면 됩니다. 

설치가 완료되면 버전 정보 출력을 통해 정상 실행여부를 확인합니다. 터미널을 실행한 후 다음의 명령어를 실행합니다. 
명령어를 실행하는 위치는 어디든 상관없습니다. 

```node --version```

![NodeJS 버전](/assets/images/NodeJS_Version.png){: .shadow }
_NodeJS 버전 확인_


#### 2. TruffleSuite

이전에도 언급했듯 TruffleSuite 설치는 `npm`명령어를 사용합니다. 터미널에서 다음의 명령어를 실행합니다. 

```npm install -g truffle```

![Truffle 설치](/assets/images/truffle_install.png){: .shadow }
_터미널 환경에서 TruffleSuite 설치_

> TruffleSuite 설치 명령어 중 `-g` 옵션은 `global` 의 약자입니다. npm 을 통해 설치하는 프로그램, 라이브러리들은 npm 명령어를 실행한 폴더에서만 사용하는 방식과 어디서든 사용할 수 있는 방식 두가지로 나뉜니다. truffle 의 경우 -g 옵셥을 통해 어디서든 사용할 수 있도록 했습니다. Prolog 에서 설명한 충돌 가능성에 대한 부분과 일맥상통하며 이는 Truffle을 사용하는 다양한 개발 환경을 어디서든 구성하고 사용할 수 있음을 의미합니다. 
{: .prompt-info}

설치가 정상적으로 완료되었다면, 버전 정보 출력을 통해 정상 실행여부를 확인합니다. 

```truffle version```

![Truffle 버전](/assets/images/truffle_version.png){: .shadow }
_TruffleSuite 버전 확인_

참고로 버전확인시 TruffleSuite는 Truffle 버전과 함께 Ganach, Solidity, Web3 가 함께 설치됐음을 알 수 있습니다. 


### 설치 방법 - Ganache-cli

Ganache 는 쉽게 Ethereum 환경을 만들 수 있도록 TruffleSuite 측에서 제공하는 프로그램입니다.
GUI 버전과 CLI 버전을 모두 지원하고 있으며 개발환경에서는 GUI 보단 CLI 가 편리하다고 판단되어 CLI 버전을 기준으로 설명합니다. 
Ganache-CLI 를 설치하는 방식은 TruffleSuite 와 같이 터미널에서 npm 명령어를 사용하면 됩니다.

```npm install -g ganache```

![Ganache-Cli 설치](/assets/images/ganache_cli_install.png){: .shadow }
_Ganache-Cli 설치_

설치가 정상적으로 완료되었다면, 실행합니다. 다음과 같은 화면이 나온다면, 정상 설치가 완료되었습니다. 

```ganache-cli```

![Ganache-Cli 실행](/assets/images/ganache_cli.png){: .shadow }
_Ganache-Cli 실행_

> 공식 ReadMe 파일을 살펴보면, `ganache` 명령어로 실행하도록 되어 있으나 ganache 는 GUI 버전 실행 명령어이므로 CLI 버전은 `ganache-cli`명령어로 실행해야합니다.  
{: .prompt-info}

지금까지 `VSCode + TruffleSuite + Ganache-Cli`의 개발환경을 구성해 보았습니다. 

---
### 참고
* [Step0 - Prolog](https://keitechnote.github.io/blog/posts/vdr-step0-prolog/)
* [(Official) TruffleSuite 설치방법](https://trufflesuite.com/docs/truffle/how-to/install/)
* [(Official) Ganache-Cli 설치방법](https://github.com/trufflesuite/ganache#readme)


[Prolog]: https://keitechnote.github.io/blog/posts/vdr-step0-prolog
[VSCode_Download]: https://code.visualstudio.com/download
[Node_Download]: https://nodejs.org/ko/download