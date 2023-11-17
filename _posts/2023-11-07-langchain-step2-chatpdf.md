---
title: LangChain 으로 AI 서비스 만들기 - Step2 LLaMA2 + LangChain 경험하기
date: 2023-11-17 05:30 +09:00
published: true
categories: [AI]
tags: [AI, LangChain, Dev, Python, LLM, LLaMA2, chatPDF, cTransformers]
---

** *본 컨텐츠는 Udemy의 "랭체인으로 AI 웹서비스 만들기 with ChatGPT, LLaMA2" 내용 중 일부를 정리한 글입니다. 문제시 삭제될 수 있습니다.**

## 개요

[Step1 - Init](https://keitechnote.github.io/blog/posts/langchain-step1-init/)를 통해 설치해야 하는 프로그램 목록과 개발환경을 위한 조합을 확인했습니다. 본 Post에서는 그 중 VSCode 와 LangChain, LLaMA2 를 설치하고 chatPDF 를 만들어 보겠습니다. 
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

_VSCode 최초 실행 화면_


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
하지만 LLaMA2 와 같이 PC에 설치하는 LLM 의 경우, 사용시 많은 리소스가 필요하며 이를 위해 하드웨어 업그레이드를 통해 PC 성능을 높여 리소스 사용을 감당하거나 리소스 사용을 줄이도록 경량화하는 버전을 사용하는 방법이 있습니다. 
Meta 에서는 LLaMA2 정식 버전만을 공개하고 있지만, 상업적 목적의 활용까지 허용한 LLaMA2 이기에 수많은 사람들이 LLaMA2 경량화 버전을 제작해 공개하고 있습니다. 다음 사이트도 경량화된 버전의 LLaMA2를 공개하고 있습니다. 

- LLaMA2 경량화 버전 공개 사이트 : https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML

![llama2_light_version_homepage](/assets/images/llama2_light_version_homepage.png)

_LLaMA2 경량화 버전 (출처 : [TheBloke](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML))_

해당 사이트에는 LLaMA2 경령화 버전을 더 가볍게 한 버전(llama-2-7b-chat.ggmlv3.q2_K.bin)부터 경량화 버전 중 가장 무거운 버전(llama-2-7b-chat.ggmlv3.q8_0.bin)까지 [세부적][llama2_light_version_provided_files]으로 나누고 있습니다. 
본 프로젝트에서는 LLaMA2 정식 버전, 경량화 버전중 가장 무거운 버전, 가장 가벼운 버전 총 세가지를 사용할 예정입니다. 이는 서로간에 결과나 처리 시간등을 비교해 보기 위함일 뿐 사용방법은 모두 동일합니다. 

> 경량화 버전의 파일명은 "7Billion 개의 피쳐를 학습한 Chat용 LLaMA2"란 의미로 "llama-2-7b-chat" 이며 ggml은 개발자인 "Georgi Gerganov Machine Learning"의 약자입니다. 뒤의 v3는 버전입니다. 
{: .prompt-info}

원하는 버전의 LLaMA2 를 다운로드 한 후 LLaMA2를 프로젝트 폴더에 옮깁니다. 

### cTransformers 설치하기 

다운로드한 LLaMA2 파일은 확장자 `bin`으로 C언어로 개발되어 빌드된 파일입니다. 파이썬에서 C언어로된 LLM 을 사용하기 위해선 그에 걸맞는 라이브러리인 `cTransformers` 가 필요합니다. cTransformers 도 LLaMA2 경량화 버전 제공한 Georgi Gerganov 가 개발해 제공하고 있습니다.

- 명령어 :  `pip install ctransformers`

![install_ctransformers](/assets/images/install_ctransformers.png)

_cTransformers 설치_


### LLaMA2 + cTransformers 로 LLM 사용해 보기

LLaMA2 에 cTransformers 를 직접 사용해 간단한 Chat 을 작성해 보겠습니다. 

```python
# cTransformers 모듈 사용하기 위해 가져옵니다. 
from ctransformers import AutoModelForCausalLM

# 사용한 LLM 과 LLM 종류를 지정합니다. 
llm = AutoModelForCausalLM.from_pretrained(
    "llama-2-7b-chat.ggmlv3.q2_K.bin", 
    model_type="llama"
)

# 질문하고 그 결과를 출력합니다. 
print(llm("AI is going to"))
```

![llam_sample_question_1](/assets/images/llam_sample_question_1.png)

_샘플코드를 작성해 질문 결과 (1)_


참고로 샘플 코드를 실행했을 때, 어느정도 리소스를 사용하는지 간단하게 윈도우 작업관리자로 CPU, 메모리를 확인해 보았습니다. 

다음은 LLaMA2 경량화 버전 중 가장 가벼운 버전인 `llama-2-7b-chat.ggmlv3.q2_K.bin` 을 사용했을 때 결과입니다. 

![task_manager_result_1](/assets/images/task_manager_result_1.png)

_llama-2-7b-chat.ggmlv3.q2-K.bin 을 사용했을 때, 작업관리자 리소스 화면_


다음은 LLaMA2 경량화 버전 중 가장 무거운 버전인 `llama-2-7b-chat.ggmlv3.q8_0.bin` 을 사용했을 때 결과입니다.

![task_manager_result_2](/assets/images/task_manager_result_2.png)

_llama-2-7b-chat.ggmlv3.q8-0.bin 을 사용했을 때, 작업관리자 리소스 화면_

리소스 사용량이 상대적으로 높긴 하지만 일반 CPU 에서 동작하기에 무리가 없는 수준입니다. 이는 학습을 "시켜" 모델을 "생성"하는 것이 아닌 생성된 모델을 "사용"만 하기 때문입니다. 따라서, 사용자 PC 의 리소스가 반드시 높아야 한다는 부담은 조금 내려놓아도 될 것 같습니다. 


### LLaMA2 + cTransformers + LangChain 으로 LLM 사용해 보기

이제 LLaMA2 와 cTransformers 를 LangChain 을 활용해 실행하겠습니다. 

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

첫번째 LLaMA2 + cTransformers 를 사용한 코드와 크게 다르지 않는다는 것을 알 수 있습니다. 

### Streamlit 설치하기

지금까지 LLaMA2 를 사용해 보았습니다. 하지만 아직 Cli 화면에서 질문했을 때 답변을 받아보았을 뿐 화면에서 질문하고 답변을 받을 수 있도록 간단한 웹 서버와 화면이 필요합니다. 
파이썬의 경우, 로컬 PC 에서 간단히 띄울 수 있는 웹서버들이 존재합니다. 주로 Flask, http.server, FastAPI 등이 있습니다. 
하지만 본 Post 에서는 `Streamlit` 을 사용합니다. Streamlit 은 앞서 언급한 라이브러리들과 같은 웹 서버로 markdown 언어를 지원하고 있습니다. Streamlit 의 자세한 내용은 [홈페이지][streamlit_homepage] 또는 [공식문서][streamlit_docs] 를 참고하기 바랍니다.

- 명령어 : `pip install streamlit`

![install_streamlit](/assets/images/install_streamlit.png)

_streamlit 설치 화면_

설치가 완료되었으면 공식문서의 설명처럼 정상적으로 설치가 되었는지 확인합니다. 

- 명령어 : `streamlit hello`

![check_streamlit_after_install](/assets/images/check_streamlit_after_install.png)

_streamlit 설치 후 테스트_

`hello` 명령을 넣으면 처음 설치한 사용자로 생각해 다양한 정보를 이메일로 받아볼 수 있도록 등록 화면이 나옵니다. 원하지 않는다면 엔터로 넘어가면 됩니다. 

![streamlit_welcome_page](/assets/images/streamlit_welcome_page.png)

_streamlit welcome 페이지_

Streamlit 의 웰컴 페이지와 함께 약간의 샘플 데모를 볼 수 있습니다. 여기까지 잘 나왔다면, 정상적으로 설치가 완료되었습니다. 

ChatPDF 를 만들기 위한 모든 준비가 끝났습니다. 이제 PDF 를 학습시키고, 질의 응답을 할 수 있는 웹 페이지를 작성해 보겠습니다. 




---
### 정리
* LangChaing 은 다양한 언어 모델과 이를 활용할 수 있는 도구들을 연결해 주는 프레임워크입니다. 

---
### 관련 Posts
1. [LangChain 으로 AI 서비스 만들기 - Step 1. Init](https://keitechnote.github.io/blog/posts/langchain-step1-init/)

[VSCode 다운로드]: https://code.visualstudio.com/download
[llama2_homepage]: https://ai.meta.com/llama/
[llama2_light_version]: https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML
[llama2_light_version_provided_files]: https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML#provided-files
[ctransformer_github]: https://github.com/marella/ctransformers
[streamlit_homepage]: https://streamlit.io/
[streamlit_docs]: https://docs.streamlit.io/library/get-started