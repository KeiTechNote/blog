---
title: 업그레이드 가능한 스마트 컨트랙트 (8) - EIP-2535 Diamond Standard
date: 2023-09-10 00:30 +09:00
published: true
categories: [BlockChain]
tags: [BlockChain, Dev, Smart Contract, Proxy, Upgradeable Smart Contract, Solidity, 번역]
---

## EIP-2535 : Diamond Standard (번역_한글)
- 원문/출처 : https://ethereum-blockchain-developer.com/110-upgrade-smart-contracts/11-eip-2535-diamond-standard/

***본 컨텐츠는 원문/출처의 내용을 한글 번역한 내용입니다. 일부 오역이 있을 수 있으며 필요시 삭제될 수 있습니다.**


Diamond Standard 는 EIP-1538 을 개선한 것입니다. 전체 컨트랙트를 Proxy 하는 대신, delegatecall 을 위한 주소만을 매핑하는 기존의 아이디어와 동일합니다. 

Diamond Standard 의 중요한 부분은 Storage 동작입니다. Openzeppelin 이 사용하는 비정형화된 Storage 패턴과는 달리, Diamond Standard 의 Storage 는 특정 Storage Slot 에 하나의 `구조체`를 저장합디ㅏ. 

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

이렇게 하면, 전체 `구조`때문에, 분리된 Storage Slot 에 있는 LibXYZ, FacetXYZ 를 원하는 만큼 가질 수 있습니다. 즉, Facet 컨트랙트가 아닌 delegatecall 을 호출하는 Proxy 컨트랙트에 저장됩니다. 

그렇기 때문에, 다른 Facet 간에 Storage 를 공유할 수 있습니다. 모든 Storage Slot 은 수동으로 정의합니다. (`keccak256("diamond.storage.LibXYZ")`)

### Proxy 컨트랙트




### 사용해 보기
먼저, 다음 Repository 를 가져옵니다. 

> git clone https://github.com/mudgen/diamond-1.git

![git_clone](/assets/images/7_1_clone_diamond.png)
_git clone 실행화면_

그리고 나서, ganache-cli 을 터미널로 실행합니다.

> ganache-cli 가 없다면 `npm install -g ganache-cli`로 설치합니다. 설치과정에서 Permission Deny 오류가 발생하는 경우, 관리자 권한으로 설치하기 바랍니다.
{: .prompt-info}


> ganache-cli

![start_ganachi_cli](/assets/images/7_3_start_ganache_cli.png)
_ganache-cli 실행화면_

테스트를 실행해 다음과 같이 출력되는지 확인합니다. 

> truffle test 는 Repository 에서 가져온 소스코드가 있는 위치로 이동해서 실행한다. 본 Post의 경우 `~/Desktop/Dev/edu/diamond-1` 에 위치한다. 
{: .prompt-info}

> truffle test

![truffle_test_1](/assets/images/7_4_truffle_test_1.png)
_truffle 테스트 실행 후 truffle 화면_

![truffle_test_2](/assets/images/7_4_truffle_test_2.png)
_truffle 테스트 실행 후 ganache-cli 화면_

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

마이그레이션 파일을 추가합니다. 

**/migration/03_faceta.js**

```javascript
const FacetA = artifacts.require('Test2Facet')

module.exports = function (deployer, network, accounts) {
    deployer.deploy(FacetA)
}
```

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

`truffle test test/facetA.test.js` 를 실행하면, FacetA.sol 에서 Diamond로 함수가 추가됐음을 알 수 있습니다. 다음 테스트 케이스에서, 저장되고, 다시 반환합니다. 

![truffle_facetA_test_1](/assets/images/7_5_truffle_facetA_test_1.png)
_truffle unittest 실행 후 truffle 화면_

![truffle_facetA_test_2](/assets/images/7_5_truffle_facetA_test_2.png)
_truffle unittest 실행 후 ganache-cli 화면_


### 장단점




---
### 정리
* 


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