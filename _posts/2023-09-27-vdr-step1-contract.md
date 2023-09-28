---
title: SSI 개발 환경 구성하기 - Step2 First Contract
date: 2023-09-27 05:30 +09:00
published: true
categories: [SSI]
tags: [BlockChain, Dev, Smart Contract, Solidity, SSI, DID, Python]
---

## 개요

[Step1 Init (VSCode + TruffleSuite + Ganache-cli)][step1_init] 을 통해 SSI를 개발할 수 있는 환경을 모두 마련했습니다. 
이제 개발 순서를 정하고 개발을 진행하면 됩니다. 개발 순서를 정하기 위해선 개발해야 하는 대상이 무엇인지 정확히 인지해야 할 필요가 있습니다. 따라서, SSI Architecture 를 살펴보겠습니다. 

### SSI 생태계
![SSI 생태계](/assets/images/roles_information_flow.png){: .shadow }
_SSI 생태계 구성요소의 기본 역할과 정보 흐름도 (출처 : W3C)_

SSI 생태계는 4가지 기본 구성요소 ( `holder`, `issuer`, `verifier`, `verifiable data registry` ) 로 이루어져 있으며,
W3C에서는 각각의 역할을 다음과 같이 정의하고 있습니다. 

- `holder` : 하나의 이상의 (확인 가능한) 자격증명을 보유하고 있고, 보유하고 있는 자격증명을 통해 (확인 가능한) 프레젠테이션을 생성하는 엔티티 (예: 학생, 직원, 고객 등)
- `issuer` : (확인 가능한) 자격증명을 생성하고, 요청한 `holder`에게 자격증명을 전송하는 엔티티 (예: 개인, 기업, 단체, 협회, 정부 등)
- `verifier` : (확인 가능한) 자격증명을 수신하고, 검증하는 엔티티 (예: 고용주, 웹사이트, 은행 등)
- `verifiable data registry` : 자격증명을 검증하는데 필요한 데이터를 중개하는 엔티티 (예: 분산원장, 정부 데이터베이스 등)

> 엔티티(Entity)를 번역하면 '개체'로, SSI 생태계를 구성하고 있는 구성요소 각각의 역할을 하는 대상을 지칭하는 단어입니다.
{: .prompt-info} 

용어와 그림을 보면 굉장히 낯설고 어렵게 느껴집니다. 
하지만 앞으로 내용을 살펴보면, 일반화된 용어를 정의하고 관계도를 그려보지 않았을 뿐 이미 일상생활에서 사용하고 있는 것임을 알 수 있습니다. 

예를 들어보겠습니다. 

```
이름이 "디케이" 인 "나"가 있습니다. 나는 18살 생일이 지나 성인이 되었고, 주민센터에서 주민등록증을 발급받았습니다. 
신기한 마음에 주민등록증을 써보고 싶어 가까운 편의점에서 맥주를 골랐습니다. 
편의점 점원은 성인인지 확인하기 위해 주민등록증을 보여달라고 합니다. 
지갑에 넣어두었던 주민등록증을 점원에게 보여주고 맥주를 계산하고 편의점을 나섰습니다. 
```

위 이야기에는 `holder`, `issuer`, `verifier` 가 모두 나옵니다. holder 는 '디케이'이고, issuer 는 '주민센터(정부)', verifier 는 '편의점 점원'입니다. 

이러한 내용의 이야기는 무한히 작성할 수 있습니다. 예를 하나 더 들어보겠습니다. 

```
오늘 오전 09:00. ABC 병원에서 아내가 첫째 아이를 출산했습니다. 
너무 기쁜 나머지 출산과 동시에 병원에서 출생증명서를 발급받고 전자가족관계등록 시스템을 통해 출생신고를 마쳤습니다. 
```

위 이야기에서는 holder 는 '아빠' 또는 '아이' 입니다. issuer 는 'ABC 병원', verifier 는 '전자가족관계등록시스템(정부)' 가 됩니다. 

> 그림에는 표기되지 않았지만, `자격증명의 대상` 은 `subject` (주체) 로 사람, 동물, 사물 등 어떠한 대상이 될 수 있습니다. 보통 `subject` 와 `holder` 는 동일시되나 위의 이야기처럼 간록 "부모-자료", "소유주-애완동물"과 같이 서로 다른 경우도 있습니다. 
{: .prompt-warning}

그림에서 볼 수 있듯 issuer, holder, verifier 는 DID를 발급하고, 보유하고, 전달하고, 검증하는 `역할`을 의미하며 시나리오에 따라 맡는 역할이 달라질 수 있습니다. 즉, issuer가 ABC 병원이지만, 때에 따라 주민센터(정부)나 사람이 될 수도 있습니다. 
위 이야기 중 병원에서 출생증명서를 발급하는 단계를 나눠보면 다음과 같습니다. 

1. '나'는 'ABC 병원'에 출생증명서 발급을 요청합니다.
2. 'ABC 병원'은 '나'가 출생증명서를 발급 대상인지 확인을 위한 서류를 요청합니다. 
3. '나'는 서류를 제출합니다. 
4. 'ABC 병원'은 서류를 검토합니다. 
5. (서류가 합당하면) 출생증명서를 발급합니다. 
6. '나'는 발급된 출생증명서가 올바른지 검토합니다. 

 









---
### 참고
* [Step0 - Prolog](https://keitechnote.github.io/blog/posts/vdr-step0-prolog/)
* [Step1 - Init](https://keitechnote.github.io/blog/posts/vdr-step1-init/)
* [W3C VC-DATA-MODEL](https://www.w3.org/TR/vc-data-model-2.0/)


[step1_init]: https://keitechnote.github.io/blog/posts/vdr-step1-init/
[VC-DATA-MODEL]: https://www.w3.org/TR/vc-data-model-2.0/
