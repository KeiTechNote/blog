---
title: 업그레이드 가능한 스마트 컨트랙트 (8) - EIP-2535 Diamond Standard
date: 2023-09-19 05:30 +09:00
published: true
categories: [BlockChain]
tags: [BlockChain, Dev, Smart Contract, Proxy, Upgradeable Smart Contract, Solidity, 번역]
---

## EIP-2535 : Diamond Standard (번역_한글)
- 원문/출처 : https://ethereum-blockchain-developer.com/110-upgrade-smart-contracts/11-eip-2535-diamond-standard/

***본 컨텐츠는 원문/출처의 내용을 한글 번역한 내용입니다. 일부 오역이 있을 수 있으며 필요시 삭제될 수 있습니다.**


Diamond Standard 는 EIP-1538 을 개선한 것입니다. 전체 컨트랙트를 Proxy 하는 대신, delegatecall 을 위한 주소만을 매핑하는 기존의 아이디어와 동일합니다. 

Diamond Standard 의 중요한 부분은 Storage 동작입니다. Openzeppelin 이 사용하는 비정형화된 Storage 패턴과는 달리, Diamond Standard 의 Storage 는 특정 Storage Slot 에 하나의 `구조체`를 저장합니다. 


> 앞으로 나오는 코드들은 최신 버전이 아니며 다수의 버그를 포함하고 있다. 따라서, 본문 내 코드는 작성일을 기준으로 설명하기 위한 간략한 버전으로 참고하고 실습은 github 에서 가져온 최신 버전으로 진행한다. 
{: .prompt-warning}


EIP 페이지 내 코드는 다음과 같습니다. 
```
// A contract that implements diamond storage.
library LibA {

  // This struct contains state variables we care about.
  struct DiamondStorage {
    address owner;
    bytes32 dataA;
  }

  // Returns the struct from a specified position in contract storage
  // ds is short for DiamondStorage
  function diamondStorage() internal pure returns(DiamondStorage storage ds) {
    // Specifies a random position from a hash of a string
    bytes32 storagePosition = keccak256("diamond.storage.LibA")
    // Set the position of our struct in contract storage
    assembly {ds.slot := storagePosition}
  }
}

// Our facet uses the diamond storage defined above.
contract FaucetA {

  function setDataA(bytes32 _dataA) external {
    LibA.DiamondStorage storage ds = LibA.diamondStorage();
    require(ds.owner == msg.sender, "Must be owner.");
    ds.dataA = _dataA
  }

  function getDataA() external view returns (bytes32) {
    return LibDiamond.diamondStorage().dataA
  }
}
```
{: .nolineno }

이렇게 하면, 전체 `구조`때문에, 분리된 Storage Slot 에 있는 LibXYZ, FacetXYZ 를 원하는 만큼 가질 수 있습니다. 즉, Facet 컨트랙트가 아닌 delegatecall 을 호출하는 Proxy 컨트랙트에 저장됩니다. 

그렇기 때문에, 다른 Facet 간에 Storage 를 공유할 수 있습니다. 모든 Storage Slot 은 수동으로 정의합니다. (`keccak256("diamond.storage.LibXYZ")`)


### Proxy 컨트랙트

Diamond Standard 에서 모든 것은 Diamond 를 중심으로 동작합니다. 이 아이디어는 Diamond를 잘라 함수를 추가합니다. (또는 주소를 함수에 매핑하거나 그 반대의 경우도 마찬가지 입니다.)
Facet과 함수를 추가하는 기능을 "diamondCut"라고 합니다. 그리고 Facet에 어떤 함수가 있는지 확인하는 기능을 루페("Loupe")라고 합니다. : 이 함수는 함수 시그니처(역: 함수명)과 주소, Facet에 대해 알고 싶은 모든 것을 반환합니다. 이 기능을 구현하는 방법은 다양합니다. Nick은 레퍼런스로 구현할 수 있는 세가지 방식을 보여주며, [Nick의 Repository][Nick_Repository]에서 확인할 수 있습니다. 

먼저, migration 파일에서 스마트 컨트랙트가 어떻게 배포되었는지 확인합니다. 이를 통해 Diamond 컨트랙트를 배포할 때, DiamondCutFacet 과 DiamondLoupeFacet 의 주소와 함수 셀렉터가 제공된다는 것을 알 수 있습니다. 기본적으로 Diamond Proxy 의 일부가 됩니다. 

테스트 파일을 확인해보면, 첫 번째 테스트 케이스는 주소와 함수명 매핑을 가져오고, Diamond Proxy 로 설정되었는지 확인합니다. 121줄은 Test1Facet 과 Test2Facet 함수가 추가되었습니다. 

> 최신버전의 Nick Repository를 살펴보면 번역에서 언급한 내용과 다름을 알 수 있습니다. 그 동안 스마트 컨트랙트 기술이 발전했고, 관련내용을 적용해 Diamond-1, Diamond-2, Diamond-3 으로 구분해 개별 Repository로 작성해 두었습니다. 원본 문서는 Diamond-1 을 기준으로 했으나 그 또한 원본 글이 작성된 시기와 다른 코드이므로 이 점을 감안하기 바란다. 
{: .prompt-info}


### 사용해 보기
먼저, 다음 Repository 를 가져옵니다. 

- 명령어 : ```git clone https://github.com/mudgen/diamond-1.git```

![git_clone](/assets/images/7_1_clone_diamond.png){: .shadow }
_git clone 실행화면_

그리고 나서, ganache-cli 을 터미널로 실행합니다.

> ganache-cli 가 없다면 `npm install -g ganache-cli`로 설치합니다. 설치과정에서 Permission Deny 오류가 발생하는 경우, 관리자 권한으로 설치하기 바랍니다.
{: .prompt-info}


- 명령어 : ```ganache-cli```

![start_ganachi_cli](/assets/images/7_3_start_ganache_cli.png){: .shadow }
_ganache-cli 실행화면_

테스트를 실행해 다음과 같이 출력되는지 확인합니다. 

> truffle test 는 Repository 에서 가져온 소스코드가 있는 위치로 이동해서 실행한다. 본 Post의 경우 `~/Desktop/Dev/edu/diamond-1` 에 위치한다. 
{: .prompt-info}

- 명령어 : ```truffle test```

![truffle_test_1](/assets/images/7_4_truffle_test_1.png){: .shadow }


![truffle_test_2](/assets/images/7_4_truffle_test_2.png){: .shadow }


diamondCut 인터페이스는 라이브러리를 통해서만 이용할 수 있고, 생성자의 Diamond 컨트랙트에서 호출됩니다. 만약, 업데이트 기능을 제거하려면, diamondCut 함수를 제거하면 됩니다. 

contracts/facets 폴더에 "Facet.sol" 파일을 추가하겠습니다. 그리고 "Facet.sol"에 간단한 변수를 추가하고 테스트 케이스를 추가해 보겠습니다. 

**/contracts/facets/FacetA.sol**

```
// SPDX-License-Identifier: MIT
pragma solidity ^0.7.6;

library LibA {

    // This struct contains state variables we care about.
    struct DiamondStorage {
        address owner;
        bytes32 dataA;
    }

    // Returns the struct from a specified position in contract storage
    // ds is short for DiamondStorage
    function diamondStorage() internal pure returns(DiamondStorage storage ds) {
        // Specifies a random position from a hash of a string
        bytes32 storagePosition = keccak256("diamond.storage.LibA");
        // Set the position of our struct in contract storage
        assembly {
        ds.slot := storagePosition
        }
    }
    }

    // Our facet uses the diamond storage defined above.
    contract FacetA {

    function setDataA(bytes32 _dataA) external {
        LibA.DiamondStorage storage ds = LibA.diamondStorage();
        ds.dataA = _dataA;
    }

    function getDataA() external view returns (bytes32) {
        return LibA.diamondStorage().dataA;
    }
}
```
{: .nolineno }

마이그레이션 파일을 추가합니다. 

**/migration/03_faceta.js**

```javascript
const FacetA = artifacts.require('Test2Facet')

module.exports = function (deployer, network, accounts) {
    deployer.deploy(FacetA)
}
```
{: .nolineno }

keccak256("diamond.storage.LibA") 는 누구든지 검색해 Storage Slot 을 덮어쓸 수 있기 때문에 안전하지 않다는 것을 알 수 있습니다. 

다음 unittest를 추가합니다. 

**/test/facetA.test.js**

```javascript
/* eslint-disable prefer-const */
/* global contract artifacts web3 before it assert */

const Diamond = artifacts.require('Diamond')
const DiamondCutFacet = artifacts.require('DiamondCutFacet')
const DiamondLoupeFacet = artifacts.require('DiamondLoupeFacet')
const OwnershipFacet = artifacts.require('OwnershipFacet')
const FacetA = artifacts.require('FacetA')
const FacetCutAction = {
    Add: 0,
    Replace: 1,
    Remove: 2
}

const zeroAddress = '0x0000000000000000000000000000000000000000';

function getSelectors (contract) {
    const selectors = contract.abi.reduce((acc, val) => {
        if (val.type === 'function') {
        acc.push(val.signature)
        return acc
        } else {
        return acc
        }
    }, [])
    return selectors
}

contract('FacetA Test', async (accounts) => {

    it('should add FacetA functions', async () => {
        let facetA = await FacetA.deployed();
        let selectors = getSelectors(facetA);
        let addresses = [];
        addresses.push(facetA.address);
        let diamond  = await Diamond.deployed();
        let diamondCutFacet = await DiamondCutFacet.at(diamond.address);
        await diamondCutFacet.diamondCut([[facetA.address, FacetCutAction.Add, selectors]], zeroAddress, '0x');

        let diamondLoupeFacet = await DiamondLoupeFacet.at(diamond.address);
        result = await diamondLoupeFacet.facetFunctionSelectors(addresses[0]);
        assert.sameMembers(result, selectors)
    })

    it('should test function call', async () => {
        let diamond  = await Diamond.deployed();
        let facetAViaDiamond = await FacetA.at(diamond.address);
        const dataToStore = '0xabcdef';
        await facetAViaDiamond.setDataA(dataToStore);
        let dataA = await facetAViaDiamond.getDataA();
        assert.equal(dataA,web3.eth.abi.encodeParameter('bytes32', dataToStore));
    })

})
```
{: .nolineno }

`truffle test test/facetA.test.js` 를 실행하면, FacetA.sol 에서 Diamond로 함수가 추가됐음을 알 수 있습니다. 다음 테스트 케이스에서, 저장되고, 다시 반환합니다. 

- 명령어 : ```truffle test test/facetA.test.js```

> 최신 버전에서 테스트시 ```truffle test test/diamondTest.js``` 로 합니다. 

![truffle_facetA_test_1](/assets/images/7_5_truffle_facetA_test_1.png){: .shadow }
_truffle unittest 실행 후 truffle 화면_


### 장단점

장점은 매우 큰 스마트 컨트랙트의 한계점을 우회하고 점진적으로 컨트랙트를 업데이트할 수 있다는 점입니다. 아직 초기 단계이므로 더 많은 연구가 필요합니다. 
스마트 컨트랙트를 작은 단위로 나누고 개별적으로 배포하고 업데이트할 수 있는 프레임워크가 되었으면 좋겠습니다. 어떻게든 할 수 있겠지만, 여전히 Facet은 모든 내부 함수와 함수명이 필요하기 때문에 완전하진 않습니다. 

전반적으로, Nick은 더 나은 방향으로 나아가고 있다고 생각합니다. 하지만, 몇가지 주요 단점이 있어 아직 사용할 수는 없는 상태입니다. 

- Proxy 는 스마트 컨트랙트 생태계로 진입하기 위한 시작점이 될 수 있습니다. 대규모 시스템의 경우, 상속을 사용하므로 Diamond Proxy 에 함수를 추가할 때, 주의해야 합니다. 또한 같은 이름을 가진 시스템의 서로 다른 두 부분에 함수명이 쉽게 충돌할 수 있습니다. 

- 만약 비정형 Storage를 사용하는 단일 Facet을 사용하지 않는다면, 시스템상의 모든 스마트 컨트랙트는 Diamond Storage를 사용해야 합니다. 단순히, OpenZeppelin ERC20 이나 ERC777 토큰을 사용하는 것은 Diamond Storage Slot 0 에 쓰기 때문에 권장하지 않습니다. 

- Facet 간 Storage 를 공유하는 것은 위험합니다. 관리자에게 많은 책임을 지우게 됩니다. 

- diamondCut 으로 Diamond 에 함수를 추가하는 것은 매우 번거롭습니다. 또한 이 [블로그][Blog] 내용처럼, Facet 설정을 가져오는 다른 기법도 있습니다. 

- diamondCut 으로 Diamond 에 함수를 추가하는 것은 상당히 많은 Gas 를 소모합니다. FacetA 컨트랙트 두 함수를 추가하는데 109316 Gas 가 듭니다. 20달러 이상입니다. 



---
### 정리

- Diamond Standard 는 특정 Storage Slot 에 구조체를 저장하고 등록 후 사용하는 방식이다. 
- 꾸준히 발전 중인 방식이며 비용, 충돌 가능성등의 문제로 사용성은 떨어진다. 


---
### 참고
* 샘플코드
    - Facet 컨트랙트 : [FacetA.sol](https://github.com/KeiTechNote/blog/tree/main/codes/7_FacetA.sol)
    - Facet 마이그레이션 파일 : [03_faceta.js](https://github.com/KeiTechNote/blog/tree/main/codes/7_03_faceta.js)
    - Facet Unittest 파일 : [facetA.test.js](https://github.com/KeiTechNote/blog/tree/main/codes/7_facetA.test.js) 


---
### 관련 Posts
1. [Eternal Storage Without Proxy](https://keitechnote.github.io/blog/posts/eternal-storage-without-proxy/)
2. [First Proxy](https://keitechnote.github.io/blog/posts/first-proxy/) 
3. [Storage Collisions](https://keitechnote.github.io/blog/posts/storage-collisions/)
4. [ERC-897 Proxy](https://keitechnote.github.io/blog/posts/erc-897-proxy/)
5. [EIP-897 DelegateProxy](https://keitechnote.github.io/blog/posts/eip-897-delegateproxy/)
6. [Proxies Without Storage Collisions Without Common Storage Contracts](https://keitechnote.github.io/blog/posts/proxies-without-storage-collisions-without-common-storage-contracts/)
7. [EIP-1967 Standard Proxy Storage Slot](https://keitechnote.github.io/blog/posts/eip-1967-standard-proxy-storage-slot/)


[Nick_Repository]: https://github.com/mudgen/Diamond
[Blog]: https://hiddentao.com/archives/2020/05/28/upgradeable-smart-contracts-using-diamond-standard