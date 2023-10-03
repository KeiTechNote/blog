---
title: SSI 개발 환경 구성하기 - Step3 Deploy Smart Contract on Ganache-Cli
date: 2023-10-03 05:30 +09:00
published: true
categories: [SSI]
tags: [BlockChain, Dev, Smart Contract, Solidity, SSI, DID, Python]
---

## 개요

[Step2 First Contract][step2_first_contract] 에서 가장 단순한 형태로 데이터를 저장하는 스마트 컨트랙트를 만들어보고, Remix IDE 에서 빌드 및 배포를 진행해 보았습니다. Remix IDE 는 컨트랙트를 개발하고 동작 테스트를 하기에는 적합하지만 제품 수준의 스마트 컨트랙트를 개발하기에는 부족한 부분이 있습니다. 특히, 개발된 코드가 우리가 원하는 동작을 정상적으로 수행하는지 테스트하는 `단위 테스트 (unittest)`가 이에 해당합니다. 따라서, 제품 개발에 좀 더 맞는 개발 환경을 구성할 필요가 있습니다. 

### Truffle 기반 개발환경 구성하기 

개발환경을 구성할 기본 디렉토리(`.\OneDrive\바탕 화면\Dev`) 를 만듭니다. 

> 본 Post 를 포함해 앞으로 개발환경의 기본 디렉토리는 `.\OneDrive\바탕 화면\Dev` 으로 진행됩니다.
{: .prompt-info}

기본 디렉토리에서 터미널을 생성해 Truffle 기반 템플릿을 설치합니다. 

> NodeJS 와 TruffleSuite 가 설치되지 않았다면, [Step1 Init (VSCode + TruffleSuite + Ganache-cli)][step1_init] 의 `설치 방법 - NodeJS + TruffleSuite` 을 참고하시 바랍니다.
{: .prompt-info}

- 명령어 : `truffle unbox react`

![truffle_unbox_react_1](/assets/images/vdr_step3_truffle_unbox_react_1.png){: .shadow}

_Truffle React 설치_

> Truffle 은 스마트 컨트랙트를 개발할 때 필요한 라이브러리, 도구를 묶은 Box 를 제공합니다. 그 중 react 는 스마트 컨트랙트 개발, 컴파일, 테스트, 배포에 필요한 도구를 모아놓았습니다. 따라서, truffle unbox react 를 통해 truffle 이 제공하는 react box 를 unbox 함으로써 설치하는 방식입니다. react 외에 [다양한 Box][truffle_boxes] 를 제공하니 참고하기 바랍니다. 
{: .prompt-info}

기본 디렉토리를 VSCode로 열어보면 다음과 같은 구조를 볼 수 있습니다. 

![truffle_unbox_react_2](/assets/images/vdr_step3_truffle_unbox_react_2.png){: .shadow}

_React Box 구조_

앞으로 주로 다룰 폴더 및 파일은 다음과 같습니다. 

- truffle/contracts : 개발된 스마트 컨트랙트가 위치할 폴더입니다. 
- truffle/migrations : 스마트 컨트랙트를 배포할 때, 배포 스크립트(JavaScript)가 위치할 폴더입니다. 
- truffle/test : 개발된 스마트 컨트랙트의 기능 테스트에 필요한 스크립트가 위치할 폴더입니다. 
- package.json : 사용되는 라이브러리 종류나 단축명령어를 스크립트로 지정하는 파일입니다. 
- truffle-config.js : 컴파일 프로그램 버전이나 배포되는 블록체인 네트워크 등을 지정하는 파일입니다. 

### simple_vdr 스마트 컨트랙트 생성하기 

[Step2 First Contract][step2_first_contract] 에서 개발한 simpleVDR 을 Truffle 기반 개발환경으로 이관하겠습니다. 
Remix IDE 에서 작성했던 simple_vdr.sol 파일을 복사하거나, truffle/contracts 폴더에 simple_vdr.sol 파일을 생성 후 코드를 복사/붙여넣기해 simple_vdr.sol 파일을 만듭니다.

- 위치 : truffle/contracts/simple_vdr.sol

![simple_vdr_1](/assets/images/vdr_step3_simple_vdr_1.png){: .shadow}

_simple\_vdr 파일 생성_

### simple_vdr 빌드/배포 스크립트 작성하기

스마트 컨트랙트를 빌드/배포시 컨트랙트 간 의존성 등의 이유로 배포되는 순서가 중요합니다. 그로인해 truffle/migrations 폴더에 스크립트를 작성할 때, 파일명에 처리 진행 순서를 명시적으로 기입하고 있습니다. 즉, truffle/migrations/1_deploy_simple_storage.js 처럼 1_~ 로 시작하고 있습니다. 따라서, 본 Post 에서는 1_deploy_simple_storage.js 다음으로 배포되도록 2_deploy_simple_vdr.js 로 작성합니다. 

- 위치 : truffle/migrations/2_deploy_simple_vdr.js

```javascript
const SimpleVDR = artifacts.require("simpleVDR");

module.exports = function (deployer) {
  deployer.deploy(SimpleVDR);
};
```
`artifacts.require("simpleVDR")` 에서 require는 라이브러리 등 파일을 읽어들이는 JavaScript 문법입니다. 여기서는 simple_vdr.sol 파일 내 simpleVDR 컨트랙트를 읽어들일 수 있도록 simpleVDR 컨트랙트명을 지정합니다. 읽어들인 컨트랙트는 SimpleVDR 변수에 저장됩니다. 
저장된 SimpleVDR 정보는 `deployer.deploy(SimpleVDR)`을 통해 배포(deploy)됩니다. 

> 배포를 위한 정보는 있지만 컴파일을 위한 정보를 별도로 작성하지 않았습니다. 하지만 truffle-config.json 파일에서 보듯 컴파일을 위한 기본정보는 설정되어 있으므로 별도 설정하지 않습니다. ![simple_vdr_2](/assets/images/vdr_step3_simple_vdr_2.png){: .shadow}
{: .prompt-warning}

다음 명령어를 통해 컴파일/배포를 위해 truffle 개발 환경에 접속합니다. 

- 명령어 : `truffle develop`

![simple_vdr_3](/assets/images/vdr_step3_simple_vdr_3.png){: .shadow}

_truffle 개발 환경 접속_

Ganache-Cli 를 실행했을 때와 같은 화면을 볼 수 있습니다. truffle develop 명령어는 PC 에 구성된 개발환경으로 접속하는 명령어입니다. 
현재 개발환경을 VSCode + TruffleSuite + Ganache-Cli 로 작성했으므로 Ganache-Cli 로 접속됩니다. 

![simple_vdr_4](/assets/images/vdr_step3_simple_vdr_4.png){: .shadow}

_truffle 지원 명령어_

배포를 시작합니다. truffle/migrations 디렉토리에 1_deploy_simple_storage 와 2_deploy_simple_vdr 두개가 있으므로 배포시 두개가 배포 대상이 됩니다. 따라서, 컴파일링 파일이 2개가 표기됩니다. (1_deploy_simple_storage 는 관심대상이 아니므로 표기에서 제외했습니다. )
컴파일이 완료되면 `.\Dev\client\src\contracts` 에 컨트랙트명과 동일한 이름의 json 파일이 생성되며 Remix IDE 에서 확인했던 ABI 정보를 저장합니다. 

![simple_vdr_5](/assets/images/vdr_step3_simple_vdr_5.png){: .shadow}

_컴파일 화면(1)_

2_deploy_simple_vdr 을 통해 simple_vdr.sol 컨트랙트가 배포된 후 배포된 컨트랙트 주소나 소모된 Gas 비용등이 표기됩니다. 

![simple_vdr_6](/assets/images/vdr_step3_simple_vdr_6.png){: .shadow}

_컴파일 화면(2)_

앞으로 사용할 VSCode + TruffleSuite + Ganache-Cli 개발 환경으로 simpleVDR 컨트랙트를 이관했습니다. 
다음 Post 에서는 simpleVDR 의 register, resolve 함수를 외부에서 실행할 수 있도록 API 를 작성해 보겠습니다. 

---
### 정리
* 개발된 스마트 컨트랙트는 truffle/contracts 에, 컴파일/배포 스크립트는 truffle/migrations 에 위치합니다. 

---
### 참고
* [Step0 - Prolog](https://keitechnote.github.io/blog/posts/vdr-step0-prolog/)
* [Step1 - Init (VSCode + TruffleSuite + Ganache-cli)](https://keitechnote.github.io/blog/posts/vdr-step1-init/)
* [Step2 - First Contract](https://keitechnote.github.io/blog/posts/vdr-step2-first-contract/)

[step1_init]: https://keitechnote.github.io/blog/posts/vdr-step1-init/
[step2_first_contract]: https://keitechnote.github.io/blog/posts/vdr-step2-first-contract/
[truffle_boxes]: https://trufflesuite.com/boxes/