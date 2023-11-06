---
title: LangChain 으로 AI 서비스 만들기 - Step1 Init
date: 2023-10-30 05:30 +09:00
published: true
categories: [AI]
tags: [AI, LangChain, Dev, Python, LLM, LLaMA2, chatPDF]
---

***본 컨텐츠는 Udemy의 "랭체인으로 AI 웹서비스 만들기 with ChatGPT, LLaMA2" 내용을 정리한 글입니다. 문제시 삭제될 수 있습니다.**

### 들어가기 앞서...

2022년 11월 chatGPT-3 (정확하게는 chatGPT-3.5) AI 챗봇이 공개되었고 이듬해인 2023년 3월 chatGPT-4가 공개되었습니다. 
chatGPT-3 가 공개되었을 때, 추상적으로 느껴지던 AI 시대가 도래됐음을 피부로 느끼게 되었습니다. 이를 반영하듯 수많은 기업들이 chatGPT에서 사용하는 것과 유사한 (또는 더 뛰어나다고 말하는) 언어 모델을 적용해 AI 챗봇을 경쟁하듯 공개하기 시작했습니다.

![llm_timeline](/assets/images/llm_timeline.png)

_언어모델 공개 타임라인 (출처 : [브런치 - 거대언어모델(LLM)의 현주소][brunch_brunchgpjz])

이때 언어 모델의 성능을 비교할 수 있는 지표로 언어 모델을 생성할 때 사용한 데이터의 양을 비교했습니다. 

![ai_model_data_size](/assets/images/ai_model_data_size.jpg)

_언어모델별 데이터 크기 비교 (출처 : [Life Architect][life_architect])_

chatGPT-3가 1750억개, 구글이 공개한 PaLM은 5400억개, 메타가 공개한 LLaMA는 최소 70억개에서 많게는 650억개를 사용하는 등 기존과 다른 엄청난 수의 데이터를 사용했습니다. chatGPT 이전 논의되던 데이터 크기보다 압도적으로 많은 데이터를 사용한 언어 모델이 사용되었으므로 이를 `거대 언어 모델 (Large Language Model, 이하 LLM)`이라 합니다. 

이렇게 만들어진 언어 모델을 활용한 각종 AI 챗봇은 글을 쓰거나 사람을 대신해 검색해 결과를 정리해 보여주고, VSCode 와 같은 IDE 의 플러그인으로 동작해 개발을 도와주는 등의 텍스트 방식으로 활용했다면 지금은 그림을 그려주고, 동영상을 제작/편집하는 등 활용 방식이 다양해졌습니다. 

다양한 활용은 다양한 기능을의 결합으로 해석될 수 있습니다. 랭체인(LangChain)은 다양한 기능을 제공하기 위해 필요한 도구들을 모아둔 프레임워크입니다. 

![langchain_tools](/assets/images/langchain_tools.png)

_랭체인 제공 도구 (출처 : [LangChain 홈페이지][langchain_homepage])

앞으로 "LangChain 으로 AI 서비스 만들기" 에서는 랭체인 프레임워크를 활용해 chatPDF 를 만들어 보겠습니다. 
이때, chatGPT, Bard 사용시 가장 큰 우려사항인 데이터 유출 부분을 해소하기 위해 오프라인 LLM 인 LLaMA2를 활용하겠습니다. 

> chatGPT, Bard 사용시 발생하는 데이터 유출은 이와 같은 서비스를 사용하는 사용자에 의한 부분입니다. 즉, chatGPT, Bard 가 스스로 중요정보를 찾아내 사용하는 것이 아니라 사용자가 질문을 만들 때, 입력하는 글에 중요 정보를 포함하는 경우에 발생할 수 있습니다. 데이터 유출 과정은 다음과 같습니다. 
사용자가 중요정보가 포함된 질문을 작성합니다. 입력된 질문을 처리하고 결과를 보여줍니다. 이때 질문은 chatGPT, Bard 학습 데이터로 재활용됩니다. 다른 사용자가 유사한 질문 또는 유사한 영역의 질문을 작성합니다. 학습된 AI 가 이전 질문의 내용을 활용해 결과를 보여줍니다. 
따라서, 수많은 기업들이 데이터 유출 방지의 목적으로 chatGPT와 같은 AI 서비스 사용을 막는 이유는 이를 사용하는 사용자가 성숙되지 않았기 때문입니다. 이 점 주의하기 바랍니다. 
{: .prompt-warning}

앞으로 게시되는 "LangChain 으로 AI 서비스 만들기"에서는 다음과 같은 환경을 기준으로 설명합니다 .

### 기술 스택

- OS : Windows11
- OS 언어 : 한글
- IDE : VSCode([다운로드][VSCode 다운로드])
- 개발언어
    - 파이썬 3.10 이상([다운로드][Python 다운로드]) or 파이썬 플랫폼 Anaconda ([다운로드][Anaconda 다운로드])
- 필수 프로그램
    - LLaMA2
- 인프라
    - 화면(Front-End) : [Streamlit][Streamlit_site]
    - 저장소(DataBase) : [chroma][chroma_site]


VSCode 와 파이썬 설치만 완료한 상태에서 진행되며 LLaMA2, Streamlit, chroma 등이 필요한 시점에 설치와 함께 활용해 보겠습니다. 


---
### 정리
* 많은 데이터를 기반으로 생성된 언어 모델을 거대 언어 모델(Large Language Model), LLM 이라고 합니다. 

---
### 참고
* [LangChain 홈페이지](https://www.langchain.com/)
* [LangChain 개발문서](https://python.langchain.com/docs/get_started/introduction)
* [OpenAI](https://platform.openai.com)

[life_architect]: https://lifearchitect.ai/
[brunch_brunchgpjz]: https://brunch.co.kr/@brunchgpjz/49
[langchain_homepage]: https://www.langchain.com/
[Streamlit_site]: https://streamlit.io/
[chroma_site]: https://www.trychroma.com/