---
title: LangChain 으로 AI 서비스 만들기 - Step2 chatPDF
date: 2023-11-07 05:30 +09:00
published: true
categories: [AI]
tags: [AI, LangChain, Dev, Python, LLM, LLaMA2, chatPDF, cTransformers]
---

***본 컨텐츠는 Udemy의 "랭체인으로 AI 웹서비스 만들기 with ChatGPT, LLaMA2" 내용 중 일부를 정리한 글입니다. 문제시 삭제될 수 있습니다.**

## 개요

[Step1 - Init](https://keitechnote.github.io/blog/posts/langchain-step1-init/)를 통해 설치해야 하는 프로그램 목록과 개발환경을 위한 조합을 확인했습니다. 그 중 본 Post에서는 VSCode 와 LangChain, LLaMA2 를 설치하고 chatPDF 를 만들어 보겠습니다. 
그리고 본 프로젝트와 관련된 코드는 다음의 경로를 기준으로 작성됩니다. 

- 프로젝트 경로 : C:\Users\amana\OneDrive\바탕 화면\AI
- 구성 환경 : VSCode + LangChain + LLaMA2

### VSCode 설치하기

VSCode 는 Microsoft에서 제공하는 개발 IDE 입니다. 무료로 공개되어 있어 누구든지 설치할 수 있으며 확장 프로그램을 통해 다양한 기능을 자유롭게 추가할 수 있는 장점이 있어 (저를 포함한) 많은 개발자들이 사용하고 있습니다. 

- VSCode [다운로드][VSCode_Download]

![VSCode 다운로드](/assets/images/VSCode_Download.png){: .shadow }
_OS별 VSCode 다운로드 페이지_

붉은 색 박스로 표시해 둔 윈도우용 VSCode 를 클릭하면 VSCode 설치파일이 다운로드됩니다. 다운로드가 완료되면 이를 실행하고 "다음" 버튼만 눌러서 설치하면 됩니다. 별도 선택할 부분은 없습니다. 

설치가 완료되면 실행합니다. 다음과 같은 화면이 나온다면, 정상 설치가 완료되었습니다. 

![VSCode_실행](/assets/images/VSCode_Init.png){: .shadow }


### LangChain 설치하기 

LangChain 은 파이썬에서 라이브러리로 제공하고 있습니다. PIP 로 설치합니다. 

- 명령어 : `pip install langchain`

![install_langchain](/assets/images/install_langchain.png)

_LangChain 설치_

### LLaMA2 설치하기

LLaMA2 는 (페이스북을 서비스하는) Meta 에서 개발한 LLM 으로 홈페이지 첫 화면에 표기된 것처럼 상업적 목적 ("Commercial use") 으로도 사용할 수 있도록 오픈소스로 공개되어 있습니다. 

![llama2_homepage](/assets/images/llama2_homepage.png)

_LLaMA2 홈페이지 첫화면_

LLM 은 수많은 데이터를 학습해 만들어진 모델인 만큼 사용시 CPU나 메모리와 같은 PC 의 많은 리소스를 사용합니다. 이러한 이유로 LLM 기반 서비스는 대부분 온라인으로 공개되어 웹, API 형태로 기능을 제공하고 있습니다. 
하지만 LLaMA2 와 같이 PC에 설치해서 사용하는 경우, 많은 리소스 사용 문제를 해소하는 방법은 PC 성능을 높여 사용 리소스를 감당하거나 리소스 사용을 줄이도록 경량화하는 방법이 있습니다. 
Meta 에서는 LLaMA2 정식 버전만을 공개하고 있지만, 상업적 목적의 활용까지 허용한 LLaMA2 이기에 수많은 사람들이 LLaMA2 경량화 버전을 제작해 공개하고 있습니다. 

- LLaMA2 경량화 버전 공개 사이트 : https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML

![llama2_light_version_homepage](/assets/images/llama2_light_version_homepage.png)

_LLaMA2 경량화 버전 (출처 : [TheBloke](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML))_

경령화 버전도 가장 가벼운 버전(llama-2-7b-chat.ggmlv3.q2_K.bin)부터 가장 무거운 버전(llama-2-7b-chat.ggmlv3.q8_0.bin)까지 [세부적][llama2_light_version_provided_files]으로 나누고 있습니다. 
본 프로젝트에서는 LLaMA2 정식 버전, 경량화 버전중 가장 무거운 버전, 가장 가벼운 버전 총 세가지를 사용할 예정입니다. 이는 서로간에 결과나 처리 시간등을 비교해 보기 위함일 뿐 사용방법은 모두 동일합니다. 

> 경량화 버전의 파일명은 "7Billion 개의 피쳐를 학습한 개발된 Chat용 LLaMA2"란 의미로 "llama-2-7b-chat" 이며 ggml은 개발자인 "Georgi Gerganov Machine Learning"의 약자입니다. 뒤의 v3는 버전입니다. 
{: .prompt-info}

LLaMA2를 다운로드했으면 LLaMA2를 프로젝트 폴더에 옮깁니다. 

### cTransformers 설치하기 

다운로드한 LLaMA2 파일은 확장자 `bin`으로 C언어로 개발되어 빌드된 파일입니다. 파이썬에서 C언어로된 LLM 을 사용하기 위해선 그에 걸맞는 라이브러리인 `cTransformers` 가 필요합니다. cTransformers 는 또한 LLaMA2 경량화 버전 제공한 Georgi Gerganov 가 개발해 제공하고 있습니다.

- 명령어 :  `pip install ctransformers`

![install_ctransformers](/assets/images/install_ctransformers.png)

_cTransformers 설치_


### LLaMA2 + cTransformers 로 LLM 사용해 보기

```python
# cTransformers 모듈 가져오기
from ctransformers import AutoModelForCausalLM

# 사용한 LLM 과 LLM 종류를 지정 
llm = AutoModelForCausalLM.from_pretrained(
    "llama-2-7b-chat.ggmlv3.q2_K.bin", 
    model_type="llama"
)

# 질문하기
print(llm("AI is going to"))
```

![llam_sample_question_1](/assets/images/llam_sample_question_1.png)

_샘플코드를 작성해 질문 결과 (1)_


### LLaMA2 + cTransformers + LangChain 으로 LLM 사용해 보기

```python
# LangChain 모듈에서 CTransformers 가져오기
from langchain.llms import CTransformers

# 사용한 LLM 과 LLM 종류를 지정 
llm = CTransformers(
    model="llama-2-7b-chat.ggmlv3.q2_K.bin", 
    model_type="llama"
)

# 질문하기
print(llm("AI is going to"))
```

![llam_sample_question_2](/assets/images/llam_sample_question_2.png)

_샘플코드를 작성해 질문 결과 (2)_


### Streamlit 설치하기

- 명령어 : `pip install streamlit`

![install_streamlit](/assets/images/install_streamlit.png)





---
### 정리
* 

---
### 참고
* 

[llama2_homepage]: https://ai.meta.com/llama/
[llama2_light_version]: https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML
[llama2_light_version_provided_files]: https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML#provided-files
[ctransformer_github]: https://github.com/marella/ctransformers