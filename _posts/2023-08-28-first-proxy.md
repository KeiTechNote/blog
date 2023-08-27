---
title: 업그레이드 가능한 스마트 컨트랙트 (1) - First Proxy
date: 2023-08-28 05:30 +09:00
categories: [BlockChain]
tags: [BlockChain, Dev, Smart Contract, Proxy, Upgradeable Smart Contract]
---

## First Proxy (번역_한글)
- 원문/출처 : https://ethereum-blockchain-developer.com/110-upgrade-smart-contracts/05-proxy-nick-johnson/

***본 컨텐츠는 원문/출처의 내용을 한글 번역한 내용입니다. 일부 오역이 있을 수 있으며 필요시 삭제될 수 있습니다.**

(제가 알기로는) 최초로 제안된 프록시는 닉 존슨이 제안했습니다. 잘 모르시는 분들을 위해 소개하자면, 그는 이더리움 네임 서비스 (ENS) 의 창립자이자 수석 개발자이고,
트위터를 확인해보면, 꽤 활발하게 활동하고 있습니다. 항상 한발 앞서 있으며, 뉴질랜드 출신입니다.

프록시는 솔리디티 버전의 경우 함수 가시성 지정자와 실제 프래그마라인이 필요하기 때문에, 솔리디티 0.4.0 (또는 유사 버전)으로 작성되었습니다. 따라서, 아래의 코드는 동일한 스마트 컨트랙트를 솔리디티 0.8.1 버전으로 포팅하고 주석과 대체 메서드를 제거해 실제 스마트 컨트랙트를 대체할 수 있도록 공개한 버전입니다. 이는 거버넌스나 제어 기능이 없는 단순화된 버전의 업그레이드 아키텍처를 보여줄 뿐입니다. ([코드](https://github.com/KeiTechNote/blog/blob/main/_posts/_codes/3_first_proxy_1.sol))

```solidity
//SPDX-License-Identifier: No-Idea!
pragma solidity 0.8.1;

// filename : 3_first_proxy_1.sol
//
// Usage
// 1. deploy Example contract.
// 2. deploy Dispatcher contract using the Example contract address.
// 3. Tell Remix that the Example Contract is now running on the Dispatcher address.


abstract contract Upgradeable {
    mapping(bytes4 => uint32) _sizes;
    address _dest;

    function initialize() virtual public ;

    function replace(address target) public {
        _dest = target;
        // Ignore warnings "Unused local variable". 
        (bool bRet, bytes memory data) = target.delegatecall(abi.encodeWithSelector(bytes4(keccak256("initialize()"))));
    }
}

contract Dispatcher is Upgradeable {
    constructor(address target) {
        replace(target);
    }

    function initialize() override public pure {
        // Should only be called by on target contracts, not on the dispatcher
        assert(false);
    }

    fallback() external {
        bytes4 sig;
        assembly { sig := calldataload(0) }
        uint len = _sizes[sig];
        address target = _dest;

        assembly {
            // return _dest.delegatecall(msg.data)
            calldatacopy(0x0, 0x0, calldatasize())
            let result := delegatecall(sub(gas(), 10000), target, 0x0, calldatasize(), 0, len)
            return(0, len) //we throw away any return data
        }
    }
}

contract Example is Upgradeable {
    uint _value;

    function initialize() override public {
        _sizes[bytes4(keccak256("getUint()"))] = 32;
    }

    function getUint() public view returns (uint) {
        return _value;
    }

    function setUint(uint value) public {
        _value = value;
    }
}
```
그럼 여기서 무슨일이 일어나고 있을까요? 컨트랙트를 시도하기 전에 fallback 함수의 어셈블리에 대해 간단히 설명하겠습니다. 

기본적으로 `delegatecall`이 일어납니다. 

```
솔리디티 문서 내 DelegateCall 

메시지 호출의 특별 버전인 delegatecall 은 대상 주소의 코드가 호출한 컨트랙트 컨텍스트에서 실행되고 msg.sender 와 msg.value 가 변경되지 않는다는 점을 제외하면 메시지 호출과 동일하다. 
```

즉, 대상 컨트랙트 주소에서 대상 컨트랙트의 코드를 실행하는 대신, 대상을 호출한 컨트랙트에서 대상 컨트랙트의 코드를 실행합니다. 실제 코드를 Remix IDE 에서 실행해서 그 과정을 살펴보면 알 수 있을 것입니다. 

1. Example 컨트랙트를 배포합니다. 
![remix_ide_1](https://github.com/KeiTechNote/blog/blob/main/_images/3_first_proxy_remix_ide_1.png)

2. Example 컨트랙트 주소로 Dispatcher 컨트랙트를 배포합니다. 
![remix_ide_2](https://github.com/KeiTechNote/blog/blob/main/_images/3_first_proxy_remix_ide_2.png)

3. Example 컨트랙트가 이제 Dispatcher 주소에서 실행중이라고 Remix에 알립니다. 

```
스토리지 위치

(주의) 업그레이드 가능한 컨트랙트의 대상 주소가 Storage Slot0 에 있기 때문에 이 구현만 작동합니다. 다른 구현이 왜 mload(0x40) 을 사용하는지, 여기서 Storage Pointer 에 어떤 일이 일어나는지 궁긍하다면, OpenZeppelin 의 [가이드 문서](https://blog.openzeppelin.com/proxy-patterns) 를 확인하기 바랍니다. 
```

Example-Dispatcher 컨트랙트에서, Uint를 설정하고, Uint를 받습니다. 변수가 정확하게 저장되지만, Dispatcher는 setUint, getUint 함수를 알지 못합니다. 또한, Example 에서 상송하지도 않습니다. 

![remix_ide_4](https://github.com/KeiTechNote/blog/blob/main/_images/3_first_proxy_remix_ide_4.png)

이는 기본적으로 Dispacher를 Storage처럼 사용하지만, Example 컨트랙트에 저장된 로직을 사용하여 일어나는 일을 제외합니다. Dispatcher가 Example 컨트랙트와 "대화"하는 대신, Example 컨트랙트 코드가 Dispatcher 범위로 이동해 실행하고, Dispatcher Storage를 변경합니다. 이는 이전의 Eternal Storage 패턴과의 큰 차이점입니다. 

![action_flow](https://github.com/KeiTechNote/blog/blob/main/_images/first_proxy_1.png)

`delegatecall` op-code는 Example 컨트랙트를 Dispatcher로 이동하고, Dispatcher Storage를 사용합니다. getUint() 에서 uint * 2 결과를 반환하는 스마트 컨트랙트로 업그레이드 하고 싶다고 가정해 보겠습니다. ([코드](https://github.com/KeiTechNote/blog/blob/main/_codes/3_first_proxy_2.sol))

```solidity
//SPDX-License-Identifier: No-Idea!
pragma solidity 0.8.1;

// filename : 3_first_proxy_2.sol
//
// Usage
// 1. deploy Example contract.
// 2. deploy Dispatcher contract using the Example contract address.
// 3. Tell Remix that the Example Contract is now running on the Dispatcher address.


abstract contract Upgradeable {
    mapping(bytes4 => uint32) _sizes;
    address _dest;

    function initialize() virtual public ;

    function replace(address target) public {
        _dest = target;
        // Ignore warnings "Unused local variable". 
        (bool bRet, bytes memory data) = target.delegatecall(abi.encodeWithSelector(bytes4(keccak256("initialize()"))));
    }
}

contract Dispatcher is Upgradeable {
    constructor(address target) {
        replace(target);
    }

    function initialize() override public pure {
        // Should only be called by on target contracts, not on the dispatcher
        assert(false);
    }

    fallback() external {
        bytes4 sig;
        assembly { sig := calldataload(0) }
        uint len = _sizes[sig];
        address target = _dest;

        assembly {
            // return _dest.delegatecall(msg.data)
            calldatacopy(0x0, 0x0, calldatasize())
            let result := delegatecall(sub(gas(), 10000), target, 0x0, calldatasize(), 0, len)
            return(0, len) //we throw away any return data
        }
    }
}

contract Example is Upgradeable {
    uint _value;

    function initialize() override public {
        _sizes[bytes4(keccak256("getUint()"))] = 32;
    }

    function getUint() public view returns (uint) {
        return _value*2;
    }

    function setUint(uint value) public {
        _value = value;
    }
}
```

`replace` 메소드를 사용해 로직 컨트랙트를 업그레이드하는 방법입니다.

1. getUint() 가 value * 2 를 반환하도록 Example 컨트랙트를 업데이트합니다. 

2. Example 컨트랙트를 배포합니다. 
[!remix_ide_5](https://github.com/KeiTechNote/blog/blob/main/_images/3_first_proxy_remix_ide_5.png)

3. 배포된 Example 컨트랙트 주소를 복사합니다. 

4. 새로운 Example 컨트랙트 주소로 Dispatcher 의 `replace`를 호출합니다. 
[!remix_ide_6](https://github.com/KeiTechNote/blog/blob/main/_images/3_first_proxy_remix_ide_6.png)
[!remix_ide_7](https://github.com/KeiTechNote/blog/blob/main/_images/3_first_proxy_remix_ide_7.png)

내부적으로는 많은 일들이 일어나며 Proxy 가 동작하는 방식입니다. 하지만 Dispatcher 를 사용하는 모든 컨트랙트의 업그레이드 가능한 스마트 컨트랙트에서 확장해야 하며, 그렇지 않으면 Storage Collisions 이 발생할 수 있다는 단점이 있습니다. 
