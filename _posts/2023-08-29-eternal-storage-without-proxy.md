---
title: 업그레이드 가능한 스마트 컨트랙트 (1) - Eternal Storage without Proxy
date: 2023-08-29 05:30 +09:00
categories: [BlockChain]
tags: [BlockChain, Dev, Smart Contract, Proxy, Upgradeable Smart Contract, Solidity, 번역]
---

## Eternal Storage without Proxy (번역_한글)
- 원문/출처 : https://ethereum-blockchain-developer.com/110-upgrade-smart-contracts/04-eternal-storage/

***본 컨텐츠는 원문/출처의 내용을 한글 번역한 내용입니다. 일부 오역이 있을 수 있으며 필요시 삭제될 수 있습니다.**

(업그레이드 가능한 스마트 컨트랙트를 위해) 가장 먼저 해결해야 할 문제는 재배포 중 데이터 손실입니다. (이를 위해) 가장 먼저 떠오르는 방법은 Logic 과 Storage를 분리하는 것입니다. 어떻게 할 수 있을까요?

![Eternal Storage Idea](/assets/images/eternal_storage_without_proxy_1.png)

Eternal Storage 패턴에서는 setter와 getter가 있는 Storage 를 별도의 스마트 컨트랙트로 옮기고 Logic 스마트 컨트랙트만 읽기/쓰기를 하는 것입니다. 

이는 필요한 변수를 정확히 처리하는 스마트 컨트랙트일 수도 있고, 변수 유형별로 일반화된 스마트 컨트랙트일 수도 있습니다. 예시를 통해 설명하겠습니다. 

간단하게 설명하기 위해 엘레나 디미트로바가 예시에서 사용했던 것을 그대로 사용하겠습니다. 그러나 이는 요약본으로 완전한 스마트 컨트랙트는 아니지만 내부에서 무슨일이 일어나는지 이해하는데 가장 중요한 부분입니다. 

솔리디티 0.8.1 로 포팅했습니다. 

(엘레나 디미트로바가 사용했던 예시는) 간단한 투표 스마트 컨트랙트입니다. `vote()`를 호출하면 숫자가 늘어나는 기본적인 Logic 입니다. 

먼저, Eternal Storage 를 배포합니다. 이 컨트랙트는 변경되지 않습니다. 

![remix_ide_1](/assets/images/2_eternal_storage_remix_ide_1.png)

그 다음 Logic 을 실행하는 라이브러리와 투표 스마트 컨트랙트를 배포합니다. 

![remix_ide_2](/assets/images/2_eternal_storage_remix_ide_2.png)

내부적으로, 투표 컨트랙트의 컨텍스트에서 delegatecall 로 라이브러리 코드를 실행합니다. 만약, 라이브버리에서 msg.sender 를 사용하면, 투표 컨트랙트와 동일한 값입니다. 

몇번 투표를 통해 동작을 테스트해 보겠습니다. 

![remix_ide_3](/assets/images/2_eternal_storage_remix_ide_3.png)

모든 사람들이 원하는 만큼 투표할 수 있는 버그를 발견했다고 가정해 보겠습니다. 
버그를 수정하고 투표 스마트 컨트랙트를 재배포합니다. (이때, 버그가 있는 이전 버전도 여전히 실행중이며, 중지할 방법이 없다는 점은 무시합니다.)

모든 코드는 다음 코드로 교체합니다. 

![compare_code](/assets/images/compare_code.png)

보다시피, 라이브러리만 변경되었습니다. Storage 는 이전과 동일합니다. 
하지만, 업데이터는 어떻게 배포할까요?

투표 컨트랙트를 재배포하고, Storage 스마트 컨트랙트 주소를 제공하면 됩니다. 그게 전부입니다. 

![remix_ide_4](/assets/images/2_eternal_storage_remix_ide_4.png)

Storage 스마트 컨트랙트는 변경하지 않았으므로, 재배포할 필요는 없습니다. 한번 더 투표하면, 화면과 같은 오류(3)이 표시됩니다. 

엘레나의 원본 스마트 컨트랙트는 uint, bool 로 충분하지 않기 때문에, 몇가지 변수 유형이 더 있습니다. 

여기에는 몇가지 장단점이 있습니다. 

### 장점
1. 비교적 이해하기 쉽습니다. 솔리디티 어셈블리를 사용하지 않습니다.
2. (라이브러리가 없어도) Storage 스마트 컨트랙트만으로도 동작합니다.
3. 컨트랙트 업데이트 후 Storage 마이그레이션을 제거합니다. 

### 단점
1. 변수에 접근 과정이 매우 어렵습니다. 
2. 토큰 등과 같은 기존 스마트 컨트랙트에서 바로 사용할 수 없습니다. 

단순하지만, 사용 사례에 따라, 매우 실용적인 솔루션입니다. 특히 스마트 컨트랙트는 단순할 수록 좋습니다. 만약 실사례를 보고 싶다면, 모퍼닷컴(Morpher.com) 스마트 컨트랙트의 모퍼상태(MorpherState) 와 모퍼토큰(MorpherToken) 을 확인하기 바랍니다. 두 스마트 컨트랙트는 단순히 getter 와 setter 로 연결되지만, 효과는 동일합니다. 감사가 쉽고, 검색 측면에서 내부에서 무슨일이 일어나는지 파악하기 쉽습니다. 

---
### 정리
* 업그레이드 가능한 스마트 컨트랙트를 위해 Logic 과 Storage 를 분리한다. 
* 목적은 달성할 수 있으나 사용성이 떨어진다. 

---
### 참고
* 샘플 코드
    - [Eternal Storage 1](/assets/codes/2_eternal_storage_1.sol)
    - [Eternal Storage 2](/assets/codes/2_eternal_storage_2.sol)