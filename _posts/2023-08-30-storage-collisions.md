---
title: 업그레이드 가능한 스마트 컨트랙트 (3) - Storage Collisions
date: 2023-08-30 05:30 +09:00
categories: [BlockChain]
tags: [BlockChain, Dev, Smart Contract, Proxy, Upgradeable Smart Contract, Solidity, 번역]
---

## Understanding Storage and Storage Collisions (번역_한글)
- 원문/출처 : https://ethereum-blockchain-developer.com/110-upgrade-smart-contracts/06-storage-collisions/

***본 컨텐츠는 원문/출처의 내용을 한글 번역한 내용입니다. 일부 오역이 있을 수 있으며 필요시 삭제될 수 있습니다.**

프록시를 사용하는 두개의 스마트 컨트랙트를 사용해 프록시에서 저장소와 첫번째 변수와 어떻게 충돌이 발생하는지 확인해 보겠습니다. 

이 [storage collisions 코드](https://github.com/KeiTechNote/blog/tree/main/codes/4_storage_collisions.sol) 를 Remix IDE 에 붙여넣습니다. 

```
// SPDX-License-Identifier: MIT
pragma solidity 0.8.1;

contract LostStorage {
    address public myAddress;
    uint public myUint;

    function setAddress(address _address) public {
        myAddress = _address;
    }

    function setMyUint(uint _uint) public {
        myUint = _uint;
    }
}

contract ProxyClash {
    address public otherContractAddress;

    constructor(address _otherContract) {
        otherContractAddress = _otherContract;
    }

    function setOtherAddress(address _otherContract) public {
        otherContractAddress = _otherContract;
    }

    fallback() external {
        address _impl = otherContractAddress;

        assembly {
            let ptr := mload(0x40)
            calldatacopy(ptr, 0, calldatasize())
            let result := delegatecall(gas(), _impl, ptr, calldatasize(), 0, 0)
            let size := returndatasize()
            returndatacopy(ptr, 0, size)

            switch result
            case 0 { revert(ptr, size) }
            default { return(ptr, size) }
        }
    }
}
```

이 Fallback 함수는 약간 복잡해 보이지만, 본질적으로는 이전 함수들과 동일한 기능을 수행합니다. 여기서도 값을 반환하고, 대상 컨트랙트에 예외가 있는 경우 예외를 발생시킬 수 있습니다. 

한 가지 큰 차이점은 LostStorage 컨트랙트가 Proxy를 상속하지 않는다는 점입니다. 따라서, 내부적으로 Storage Layout 이 분리되어 있고, 둘 다 Storage Slot 0 에서 시작합니다. 

실행순서는 다음과 같습니다. 

1. LostStorage 컨트랙트를 배포합니다. 
2. ProxyCrash 컨트랙트를 배포하고, Constructor 로 LostStorage 컨트랙트 주소를 설정합니다.
3. LostStorage 컨트랙트가 ProxyCrash 컨트랙트 주소에서 실행중이라고 Remix IDE 에 알립니다. 
4. LostStorage 컨트랙트의 myAddress() 를 호출합니다. 놀랍게도, 0 이 아닌 주소가 반환됩니다. 충돌이 발생합니다. 

![remix_ide_1](/assets/images/4_storage_collisions_1.png){: .shadow }
_Storage Collisions 확인_

이것이 솔리디티 컴파일러가 Storage Slot 이 어디에 사용되는지 알 수 있도록, Storage 컨트랙트로 상속을 수행하는 이유입니다. 그리고 나중에 이에 대한 해결책이 있다는 것을 알게 될 것 입니다. 

---
### 정리
* DelegateCall 을 통해 호출되는 스마트 컨트랙트의 주소는 Proxy 스마트 컨트랙트의 Storage Slot 0 에 저장됩니다. 
* 외부 호출되는 스마트 컨트랙트의 첫번째 변수는 Proxy 스마트 컨트랙트의 Storage Slot 0 에 저장됩니다. 
* 두 스마트 컨트랙트의 Storage Slot 0 에 서로 다른 목적의 값이 저장되므로 Storage Collisions (충돌) 이 발생합니다. 


---
### 참고
* 샘플코드
    - [Storage Collisions](https://github.com/KeiTechNote/blog/tree/main/codes/4_storage_collisions.sol)

---
### 관련 Posts
1. [First Proxy](https://github.com/KeiTechNote/blog/tree/main/posts/2023-08-28-first-proxy.md) 
2. [Eternal Storage Without Proxy](https://github.com/KeiTechNote/blog/tree/main/posts/2023-08-29-eternal-storage-without-proxy.md)