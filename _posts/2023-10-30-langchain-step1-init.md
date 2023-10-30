---
title: LangChain 으로 AI 서비스 만들기 - Step1 Init
date: 2023-10-30 05:30 +09:00
published: true
categories: [AI]
tags: [AI, LangChain, Dev, Python]
---

***본 컨텐츠는 Udemy의 "랭체인으로 AI 웹서비스 만들기 with ChatGPT, LLaMA2" 내용을 정리한 글입니다. 문제시 삭제될 수 있습니다.**

### 들어가기 앞서...

2022년 11월 chatGPT-3 (정확하게는 chatGPT-3.5) AI 챗봇이 공개되었고 이듬해인 2023년 3월 chatGPT-4가 공개되었습니다. 
chatGPT-3 가 공개되었을 때, 추상적으로 느껴지던 AI 시대가 도래됐음을 피부로 느끼게 되었습니다. 이를 반영하듯 수많은 기업들이 chatGPT에서 사용하는 것과 유사한 (또는 더 뛰어나다고 말하는) 언어 모델을 적용한 AI 챗봇을 경쟁하듯 공개하기 시작했습니다.

![llm_timeline](/assets/images/llm_timeline.jpg)

_언어모델 공개 타임라인 (출처 : [브런치 - 거대언어모델(LLM)의 현주소][brunch_brunchgpjz])

이때 언어 모델의 성능을 비교할 수 있는 지표로 언어 모델을 생성할 때 사용한 데이터의 양을 비교했습니다. 

![ai_model_data_size](/assets/images/ai_model_data_size.jpg)

_언어모델 데이터 크기 비교 (출처 : [Life Architect][life_architect])_

chatGPT-3가 1750억개, 구글이 공개한 PaLM은 5400억개, 메타가 공개한 LLaMA는 최소 70억개에서 많게는 650억개를 사용하는 등 기존과 다른 엄청난 수의 데이터를 사용했습니다. chatGPT 이전 논의되던 데이터 크기보다 압도적으로 많은 데이터를 사용한 언어 모델이 사용되었으므로 이를 `거대 언어 모델 (Large Language Model, 이하 LLM)`이라 합니다. 

이렇게 만들어진 언어 모델을 활용한 각종 AI 챗봇은 글을 쓰거나 사람을 대신해 검색해 결과를 정리해 보여주고, VSCode 와 같은 IDE 의 플러그인으로 동작해 개발을 도와주는 등의 텍스트 방식의 활용에서 그림을 그려주고, 동영상을 제작/편집하는 등 수많은 곳에서 활용하고 있습니다. 

랭체인(LangChain) 은 이러한 LLM을 기반으로 이를 활용하기 위해 필요한 도구들을 모아둔 프레임워크입니다.

![langchain_tools](/assets/images/langchain_tools.jpg)

_랭체인 제공 도구 (출처 : [LangChain 홈페이지][langchain_homepage])

앞으로 "LangChain 으로 AI 서비스 만들기" 에서는 랭체인 프레임워크를 활용해 chatPDF 를 만들어보고, 이때 데이터 유출을 방지하기 위해 오프라인 LLM 인 LLaMA2 를 활용해 보겠습니다. 


### 기술 스택

- OS : Windows11
- OS 언어 : 한글
- IDE : VSCode([다운로드][VSCode 다운로드])
- 개발언어
    - 파이썬 3.10 이상([다운로드][Python 다운로드]) or 파이썬 플랫폼 Anaconda ([다운로드][Anaconda 다운로드])
- 필수 프로그램
    - LangChain
    - chroma
    - OpenAI API Key 
- 인프라
    - 화면(Front-End) : Streamlit
    - 저장소(DataBase) : chrome


### OpenAI API Key 발급받기










---
### 정리
* 

---
### 참고
* [LangChain 홈페이지](https://www.langchain.com/)
* [LangChain 개발문서](https://python.langchain.com/docs/get_started/introduction)
* [OpenAI](https://platform.openai.com)

[life_architect]: https://lifearchitect.ai/
[brunch_brunchgpjz]: https://brunch.co.kr/@brunchgpjz/49
[langchain_homepage]: https://www.langchain.com/