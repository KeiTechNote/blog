---
title: 업그레이드 가능한 스마트 컨트랙트 (6) - Proxies without Storage Collision without common Storage Contracts 
date: 2023-09-05 05:00 +09:00
published: true
categories: [BlockChain]
tags: [BlockChain, Dev, Smart Contract, Proxy, Upgradeable Smart Contract, Solidity, 번역]
---

## EIP-1822 : Proxies without Storage Collision without common Storage Contracts (번역_한글)
- 원문/출처 : https://ethereum-blockchain-developer.com/110-upgrade-smart-contracts/08-eip-1822-uups/

***본 컨텐츠는 원문/출처의 내용을 한글 번역한 내용입니다. 일부 오역이 있을 수 있으며 필요시 삭제될 수 있습니다.**

EIP-1822 는 업그레이드 가능한 표준 프록시 (UUPS)는 컴파일러가 어떤 Storage Slot 을 사용할지 알려주는 Storage 컨트랙트가 필요없는 솔루션입니다. 즉, 메소드들 대신 랜덤 Storage Slot 을 사용해 로직 컨트랙트 주소를 저장합니다. 

예제를 보여드리기 전, 중요한 부분이 있습니다. 

```
sstore(0xc5f16f0fcc639fa48a6947836d9850f504798523bf8c9a3a87d5876cf622bcf7, contractLogic)
let contractLogic := sload(0xc5f16f0fcc639fa48a6947836d9850f504798523bf8c9a3a87d5876cf622bcf7) 
```

어셈블리에서 특정 Storage Slot 에 변수를 저장하면, 다시 사용할 수 있습니다. 이 경우, EIP-1822는 `keccak256("PROXIABLE") = "0xc5f16f0fcc639fa48a6947836d9850f504798523bf8c9a3a87d5876cf622bcf7"`를 사용하여 Storage Slot 을 생성합니다. 100% 완전한 랜덤은 아니지만 정상적인 상황에서는 충돌이 발생하지 않습니다.  
[솔리디티의 스토리지 변수 레이아웃](https://docs.soliditylang.org/en/v0.8.2/internals/layout_in_storage.html#layout-of-state-variables-in-storage) 을 자세히 살펴보면 충돌이 발생할 가능성이 거의 없음을 알 수 있습니다. 

EIP-1822를 사용한 전체 코드는 다음과 같습니다. 
```
//SPDX-License-Identifier: MIT

pragma solidity 0.8.1;

contract Proxy {
    // Code position in storage is keccak256("PROXIABLE") = "0xc5f16f0fcc639fa48a6947836d9850f504798523bf8c9a3a87d5876cf622bcf7"
    constructor(bytes memory constructData, address contractLogic) {
        // save the code address
        assembly { // solium-disable-line
            sstore(0xc5f16f0fcc639fa48a6947836d9850f504798523bf8c9a3a87d5876cf622bcf7, contractLogic)
        }
        (bool success, bytes memory result ) = contractLogic.delegatecall(constructData); // solium-disable-line
        require(success, "Construction failed");
    }

    fallback() external payable {
        assembly { // solium-disable-line
            let contractLogic := sload(0xc5f16f0fcc639fa48a6947836d9850f504798523bf8c9a3a87d5876cf622bcf7)
            calldatacopy(0x0, 0x0, calldatasize())
            let success := delegatecall(sub(gas(), 10000), contractLogic, 0x0, calldatasize(), 0, 0)
            let retSz := returndatasize()
            returndatacopy(0, 0, retSz)
            switch success
            case 0 {
                revert(0, retSz)
            }
            default {
                return(0, retSz)
            }
        }
    }
}

contract Proxiable {
    // Code position in storage is keccak256("PROXIABLE") = "0xc5f16f0fcc639fa48a6947836d9850f504798523bf8c9a3a87d5876cf622bcf7"

    function updateCodeAddress(address newAddress) internal {
        require(
            bytes32(0xc5f16f0fcc639fa48a6947836d9850f504798523bf8c9a3a87d5876cf622bcf7) == Proxiable(newAddress).proxiableUUID(),
            "Not compatible"
        );
        assembly { // solium-disable-line
            sstore(0xc5f16f0fcc639fa48a6947836d9850f504798523bf8c9a3a87d5876cf622bcf7, newAddress)
        }
    }

    function proxiableUUID() public pure returns (bytes32) {
        return 0xc5f16f0fcc639fa48a6947836d9850f504798523bf8c9a3a87d5876cf622bcf7;
    }
} 

contract MyContract {

    address public owner;
    uint public myUint;

    function constructor1() public {
        require(owner == address(0), "Already initalized");
        owner = msg.sender;
    }

    function increment() public {
        //require(msg.sender == owner, "Only the owner can increment"); //someone forget to uncomment this
        myUint++;
    }
}

contract MyFinalContract is MyContract, Proxiable {

    function updateCode(address newCode) onlyOwner public {
        updateCodeAddress(newCode);
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner is allowed to perform this action");
        _;
    }
}
```

실행 순서는 다음과 같습니다. 

1. `MyFinalContract` 컨트랙트를 배포합니다. 
2. Proxy 컨트랙트 배포시 Proxy Constructor 로 contractLogic은 `MyFinalContract` 컨트랙트 주소를, constructData는 `bytes4(keccak256("constructor1()"))`를 전달합니다. 이를 통해 Remix 콘솔에서 `web3.utils.sha3("constructor1()").substring(0, 10)` 를 사용할 수 있습니다. 

![remix_ide_1](/assets/images/6_uups_remix_ide_1.png)
_Proxy 배포_

3. Proxy 컨트랙트 주소에서 MyFinalContract 가 실행중임을 Remix 에 알립니다. 

![remix_ide_2](/assets/images/6_uups_remix_ide_2.png)
_전체 과정_

각 과정을 진행하면, 컨트랙트는 Storage Slot 0에서 시작할 수 있기 때문에 Storage 상속을 무시하고 어떤 컨트랙트도 상속할 수 있습니다. 

> 변수 삭제는 불가능합니다. 
>
> 이전에 정의한 변수를 제거하거나 혼합할 수 없습니다. 변수가 여전히 프록시 컨트랙트의 특정 Storage Slot 에 존재합니다. 만약 변수를 제거하면, 솔리디티 컴파일러는 단순히 다음 변수가 이전 변수의 위치에 있다고 가정해 Storage 가 충돌하게 됩니다. {: .prompt-warning}


여기서 유일한 문제점은 Storage Slot 이 실제로 표준화되어 있지 않다는 것입니다. 즉, 로직 컨트랙트 주소를 저장할 Storage Slot 을 원하는 대로 선택할 수 있습니다. 이는 블록 탐색기의 경우, 사용자에게 정보를 표시하고 조치를 취하기가 매우 어렵게 만듭니다. 


---
### 정리
* Storage Slot 정보를 저장하는 스마트 컨트랙트를 작성하고 이용하는 대신, Storage Slot 위치를 랜덤하게 지정하는 방식을 적용할 수 있다.


---
### 참고
* 샘플코드
    - [uups](https://github.com/KeiTechNote/blog/tree/main/codes/6_uups.sol)

---
### 관련 Posts
1. [First Proxy](https://github.com/KeiTechNote/blog/tree/main/posts/2023-08-28-first-proxy.md) 
2. [Eternal Storage Without Proxy](https://github.com/KeiTechNote/blog/tree/main/posts/2023-08-29-eternal-storage-without-proxy.md)
3. [Storage Collisions](https://github.com/KeiTechNote/blog/tree/main/posts/2023-08-30-storage-collisions.md)
4. [ERC-897 Proxy](https://github.com/KeiTechNote/blog/tree/main/posts/2023-09-05-erc-897-proxy.md)
5. [EIP-897 DelegateProxy](https://github.com/KeiTechNote/blog/tree/main/posts/2023-09-05-eip-897-delegateproxy.md)