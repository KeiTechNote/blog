---
title: 업그레이드 가능한 스마트 컨트랙트 (10) - Metamorphosis Smart Contracts using CREATE2
date: 2023-09-10 00:30 +09:00
published: true
categories: [BlockChain]
tags: [BlockChain, Dev, Smart Contract, Proxy, Upgradeable Smart Contract, Solidity, 번역]
---

## Metamorphosis Smart Contracts using CREATE2 (번역_한글)
- 원문/출처 : https://ethereum-blockchain-developer.com/110-upgrade-smart-contracts/12-metamorphosis-create2/

***본 컨텐츠는 원문/출처의 내용을 한글 번역한 내용입니다. 일부 오역이 있을 수 있으며 필요시 삭제될 수 있습니다.**

모든 스마트 컨트랙트는 `DelegateCall`을 통해 Proxy를 다른 스마트 컨트랙트에 연결합니다. 따라서, Proxy 주소는 일정하게 유지되고 모든 호출은 Proxy 에서 시작되거나 Proxy 엥서 실행됩니다. 

스마트 컨트랙트를 완전히 대체할 수 있는 방법이 있으며 "Metamorphosis Smart Contact"라고 하며 다음 그림과 비슷한 느낌입니다. 

![image1](/assets/images/2021-03-19-09-49-03.webp)
{: .shadow }


이 솔루션으로 자신의 바이트코드를 다른 스마트 컨트랙트로 바꾸는 스마트 컨트랙트를 배포하는 스마트 컨트랙트를 배포할 수 있습니다. 어떨게 동작하는지 살펴 봅시다. 

> Very Low Level
지금부터는 매우 Low Level 내용입니다. 매우 진보된 내용이기 때문에 우리가 여기서 세부사항을 완전히 파악하는데 시간이 걸릴 수 있습니다. 밑바탕이되는 아키텍처에 대해 최대한 자세히 설명하겠습니다. 
{: .prompt-warning}

### CREATE2 동작 - 입문
CREATE2 작동 방식에 대한 설명 부분입니다. CREATE2는 솔리디틱가 특정 주소에 스마트 컨트랙트를 생성하기 위한 어셈블리 Op-Code 입니다. 
CREATE2 의 가장 큰 장점은 이 주소가 미리 알려져 있다는 점입니다. 
보통 스마트 컨트랙트 주소는 배포자 주소와 nonce 로 생성됩니다. nonce 는 계속 증가하므로, CREATE2 는 nonce 대신 salt 를 사용합니다. salt 는 사용자가 지정할 수 있습니다. 그래서, 스마트 컨트랙트 주소를 알 수 있는 장점을 갖게 됩니다. 

> 주소가 미리 알려져 있다는 점은 고정된 주소이거나 필수값만 알고 있다면 계산으로 알 수 있다는 의미이므로 nonce 와 같이 값이 변경하면 계산할 수 없기 때문에 고정된 값인 salt 를 사용한다. 
{: .prompt-info}


CREATE2 는 다음과 같이 정의됩니다. :
`keccak256(0xff ++ deployerAddr ++ salt ++ keccak256(bytecode))[12:]`

1. 0xff : 상수
2. deployerAddr : 배포자 주소로 CREATE2 를 전송한 스마트 컨트랙트 주소
3. salt: 랜덤 salt
4. 특정 주소로 배포될 해시 바이트코드

이렇게 하면, 새로운 스마트 컨트랙트가 배포될 주소가 됩니다. 

먼저, 컨트랙트를 배포하는 Factory 컨트랙트가 필요합니다. 

```
//SPDX-License-Identifier: MIT

pragma solidity 0.8.1;

contract Factory {
  event Deployed(address _addr);
  function deploy(uint salt, bytes calldata bytecode) public {
    bytes memory implInitCode = bytecode;
    address addr;
    assembly {
        let encoded_data := add(0x20, implInitCode) // load initialization code.
        let encoded_size := mload(implInitCode)     // load init code's length.
        addr := create2(0, encoded_data, encoded_size, salt)
    }
    emit Deployed(addr);
  }
}
```
새로운 컨트랙트가 배포되면 주소를 이벤트로 전송합니다. 이를 이용해 다른 스마트 컨트랙트를 배포할 수 있습니다. 스마트 컨트랙트가 배포되는 주소는 결정되어 있습니다. 다음은 EIP-1014 (에서 스마트 컨트랙트 주소를 결정하는) 내용입니다.

```
keccak256(0xff ++ address ++ salt ++ keccak256(init_code))[12:]
```

미구엘 모타는 CREATE2 주소를 연산하는 단일 함수를 작성했습니다. 그러나, 우린 이 함수를 사용하지 않고 한단계씩 진행하겠습니다. 

먼저, Factory 컨트랙트를 이용해 다음 스마트 컨트랙트를 배포합니다. (Factory 컨트랙트 파일에) 다음 코드를 추가합니다. 

```
contract NoConstructor {
    uint public myUint = 5;
}
```

솔리디티 컨파일러로 이동해, Web3-Create 에서 바이트코드를 복사합니다. 

![remix_ide_1]()

![remix_ide_2]()

'배포' 탭에서, Factory 컨트랙트를 먼저 배포한 다음, 바이트코드를 사용해 CREATE2 로 NoConstructor 컨트랙트를 배포합니다. 

![remix_ide_3]()

'salt' 는 숫자로, 1을 설정했습니다. salt 는 컨트랙트 주소를 결정할 때 사용됩니다. 'bytecode' 는 이전에 복사한 바이트코드입니다. 'transact' 를 누른 후 세부 트랙잭션을 확인합니다. Factory 컨트랙트를 통해 새롭게 배포된 NoConstructor 컨트랙트 주소를 확인할 수 있습니다. 

![remix_ide_4]()

이 주소를 계산하는 방법이 특별한가요? 매우 쉽습니다. Remix 콘솔에서 직접 계산할 수도 있습니다. 

```
factoryAddress = "ENTER_FACTORY_ADDRESS"

bytecode = "0x6080604052600560005534801561001557600080fd5b5060b3806100246000396000f3fe6080604052348015600f57600080fd5b506004361060285760003560e01c806306540f7e14602d575b600080fd5b60336047565b604051603e9190605a565b60405180910390f35b60005481565b6054816073565b82525050565b6000602082019050606d6000830184604d565b92915050565b600081905091905056fea264697066735822122019e87f67a50e9a888075265bb077e909763324a0aae35530f1359e047b40e06064736f6c63430008010033"

salt = 1;

"0x" + web3.utils.sha3('0xff' + factoryAddress.slice(2) + web3.eth.abi.encodeParameter('uint256',salt).slice(2).toString() + web3.utils.sha3(bytecode).slice(2).toString()).slice(-40);
```

![remix_ide_5]()

Factory 컨트랙트로 배포한 주소와 같다는 것을 확인할 수 있습니다. 

![remix_ide_6]()


### Constructor 매개변수를 갖는 CREATE2

Constructor 가 있다면 어떻게 동작할까요? 조금 다릅니다. 
기본적으로 Constructor 가 매개변수로 받는 데이터는 초기 바이트코드에 포함되어야 합니다. 

(이전에 배포한 스마트 컨트랙트 파일에) 다음 코드를 추가합니다. 

```
contract WithConstructor {
  address public owner;

  constructor(address _owner) {
    owner = _owner;
  }
}
```

(WithConstructor) 컨트랙트를 배포하려면 스마트 컨트랙트 끝에 인코딩된 주소를 추가해야 합니다. 주소를 인코딩하는 방법은 무엇일까요?

먼저, 'Account' 에서 주소를 복사합니다. 그리고 나서 Remix 콘솔에 `web3.eth.abi.encodeParameter('address', '<복사한 Account 주소>')` 를 입력합니다. 

![remix_ide_7]()

앞 "0x"를 제외한 값을 복사해 바이트코드(끝)에 추가한 후 Factory 컨트랙트로 배포합니다. 

바이트코드 + 주소는 다음과 같습니다. 

```
0x608060405234801561001057600080fd5b506040516102043803806102048339818101604052810190610032919061008d565b806000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550506100ff565b600081519050610087816100e8565b92915050565b60006020828403121561009f57600080fd5b60006100ad84828501610078565b91505092915050565b60006100c1826100c8565b9050919050565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b6100f1816100b6565b81146100fc57600080fd5b50565b60f78061010d6000396000f3fe6080604052348015600f57600080fd5b506004361060285760003560e01c80638da5cb5b14602d575b600080fd5b60336047565b604051603e91906078565b60405180910390f35b60008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b6072816091565b82525050565b6000602082019050608b6000830184606b565b92915050565b6000609a8260a1565b9050919050565b600073ffffffffffffffffffffffffffffffffffffffff8216905091905056fea26469706673582212207debf1ceacd0990dc89fd5c4d429bcd8cddbc1899ed06c9d40d571067827229764736f6c634300080100330000000000000000000000005b38da6a701c568545dcfcb03fcb875f56beddc4
```

(배포된) 컨트랙트를 살펴봅시다.

![remix_ide_8]()

Constructor 로 전달했던 주소일 것입니다. CREATE2 Op-Code 를 이용해 스마트 컨트랙트를 배포하는 방법에 대해 살펴봤습니다. 
문제는, 새로운 스마트 컨트랙트를 생성할 때 바이트코드 해시를 사용했기 때문에, 변경할 수 없다는 것입니다. 맞나요?

틀렸습니다. (방법이 있습니다.)


### 스마트 컨트랙트 덮어쓰기

> SELFDESTRUCT 제거
덮어쓰는 함수는 동작을 위해 스마트 컨트랙트의 selfdestruct 가 필요합니다. 이는 제거될 예정입니다.
{: .prompt-warning}

이 아이디어는 배포시, 자신의 바이트코드를 다른 바이트코드로 바꾸는 스마트 컨트랙트를 배포하는 것입니다. 따라서, CREATE2 를 통해 실행되는 바이트코드는 항상 동일하며, 배포 중 Factory 를 재호출하여 스스로를 바꿉니다. 


#### 위험

한번 시도해 보겠습니다. 

전체 코드는 [여기][Metamorphic]를 참고하시기 바랍니다. 내부에서 어떤일이 일어나는지 이해할 수 있는 가장 작은 크기의 예제입니다.

Remix IDE 에 새 파일을 만들고, 다음의 코드를 추가합니다.

```
//SPDX-License-Identifier: MIT

pragma solidity 0.8.1;

contract Factory {
    mapping (address => address) _implementations;

    event Deployed(address _addr);

    function deploy(uint salt, bytes calldata bytecode) public {

        bytes memory implInitCode = bytecode;

          // assign the initialization code for the metamorphic contract.
        bytes memory metamorphicCode  = (
          hex"5860208158601c335a63aaf10f428752fa158151803b80938091923cf3"
        );

         // determine the address of the metamorphic contract.
        address metamorphicContractAddress = _getMetamorphicContractAddress(salt, metamorphicCode);

        // declare a variable for the address of the implementation contract.
        address implementationContract;

        // load implementation init code and length, then deploy via CREATE.
        /* solhint-disable no-inline-assembly */
        assembly {
          let encoded_data := add(0x20, implInitCode) // load initialization code.
          let encoded_size := mload(implInitCode)     // load init code's length.
          implementationContract := create(       // call CREATE with 3 arguments.
            0,                                    // do not forward any endowment.
            encoded_data,                         // pass in initialization code.
            encoded_size                          // pass in init code's length.
          )
        } /* solhint-enable no-inline-assembly */

        //first we deploy the code we want to deploy on a separate address
        // store the implementation to be retrieved by the metamorphic contract.
        _implementations[metamorphicContractAddress] = implementationContract;



        address addr;
        assembly {
            let encoded_data := add(0x20, metamorphicCode) // load initialization code.
            let encoded_size := mload(metamorphicCode)     // load init code's length.
            addr := create2(0, encoded_data, encoded_size, salt)
        }

         require(
          addr == metamorphicContractAddress,
          "Failed to deploy the new metamorphic contract."
        );
        emit Deployed(addr);
    }

    /**
    * @dev Internal view function for calculating a metamorphic contract address
    * given a particular salt.
    */
    function _getMetamorphicContractAddress(
        uint256 salt,
        bytes memory metamorphicCode
        ) internal view returns (address) {

        // determine the address of the metamorphic contract.
        return address(
          uint160(                      // downcast to match the address type.
            uint256(                    // convert to uint to truncate upper digits.
              keccak256(                // compute the CREATE2 hash using 4 inputs.
                abi.encodePacked(       // pack all inputs to the hash together.
                  hex"ff",              // start with 0xff to distinguish from RLP.
                  address(this),        // this contract will be the caller.
                  salt,                 // pass in the supplied salt value.
                  keccak256(
                      abi.encodePacked(
                        metamorphicCode
                      )
                    )     // the init code hash.
                )
              )
            )
          )
        );
    }

    //those two functions are getting called by the metamorphic Contract
    function getImplementation() external view returns (address implementation) {
        return _implementations[msg.sender];
    }

}

contract Test1 {
    uint public myUint;

    function setUint(uint _myUint) public {
        myUint = _myUint;
    }

    function killme() public {
        selfdestruct(payable(msg.sender));
    }
}

contract Test2 {
    uint public myUint;

    function setUint(uint _myUint) public {
        myUint = 2*_myUint;
    }

    function killme() public {
        selfdestruct(payable(msg.sender));
    }

}
```

두가지 동작을 하는 컨트랙트를 배포합니다. 

1. msg.sender 를 호출해 주소를 확인합니다. 
2. 해당 주소에서 동작중인 바이트코드를 자신의 바이트코드로 덮어 씌웁니다. 

어떻게 사용하나요?

1. Factory 컨트랙트를 배포합니다. 
2. salt = 1 인 Test1 바이트코드를 사용해 Test1 컨트랙트를 배포합니다. 
3. Test1 컨트랙트가 Metamorphic 컨트랙트에서 실행된다는 것을 Remix IDE 에 알립니다. 
4. "myUint" 를 원하는 값으로 설정합니다. 
5. Test1 컨트랙트를 삭제합니다. 
6. salt = 1 인 Test2 바이트코드를 배포합니다. 
7. 주소는 같지만 다른 바이트코드가 배포될 것입니다. 
8. setUint 함수는 입력값을 2배로 늘립니다. 
9. 안전하게 사용할 수 있다고 생각했던 Token 컨트랙트가 어떻게 될지 상상해 봅니다. 

![remix_ide_9]()

Token 컨트랙트나 DeFi 프로젝트라고 가정해 봅시다. 사람들이 투자를 시작하고 갑자기 Logic 컨트랙트가 바뀐다고 상상해 봅시다. 블록체인에 대한 모든 신뢰가 사라지게 됩니다. 

스캠(사기)를 피하려면 어떻게 해야할까요? 먼저, selfdestruct 기능이 있는지 확인합니다. 만약 있다면, 전체 배포자 체인을 따라가 CREATE2 Op-Code 를 사용했는지 확인합니다. 만약, CREATE2 Op-Code를 사용했다면, 무엇을 배포했는지 조사합니다. 만약 Metamorphic 컨트랙트라면, 뭔가 수상한 일이 벌어지고 있다는 것을 알 수 있습니다. 



---
### 정리
* 


---
### 참고
* 

---
### 관련 Posts
1. [Eternal Storage Without Proxy](https://keitechnote.github.io/blog/posts/eternal-storage-without-proxy/)
2. [First Proxy](https://keitechnote.github.io/blog/posts/first-proxy/) 
3. [Storage Collisions](https://keitechnote.github.io/blog/posts/storage-collisions/)
4. [ERC-897 : Proxy](https://keitechnote.github.io/blog/posts/erc-897-proxy/)
5. [EIP-897 : DelegateProxy](https://keitechnote.github.io/blog/posts/eip-897-delegateproxy/)
6. [Proxies Without Storage Collisions Without Common Storage Contracts](https://keitechnote.github.io/blog/posts/proxies-without-storage-collisions-without-common-storage-contracts/)
7. [EIP-1967 : Standard Proxy Storage Slot](https://keitechnote.github.io/blog/posts/eip-1967-standard-proxy-storage-slot/)
8. [EIP-1538: Transparent Contract Standard]()
9. [EIP-2535: Diamond Standard]()


[Metamorphic]: https://github.com/0age/metamorphic