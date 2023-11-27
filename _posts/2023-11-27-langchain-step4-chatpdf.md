---
title: LangChain 으로 AI 서비스 만들기 - Step4 chatPDF advanced
date: 2023-11-27 05:30 +09:00
published: true
categories: [AI]
tags: [AI, LangChain, Dev, Python, LLM, LLaMA2, chatPDF, cTransformers]
---

***본 컨텐츠는 Udemy의 "랭체인으로 AI 웹서비스 만들기 with ChatGPT, LLaMA2" 내용 중 일부를 정리한 글입니다. 문제시 삭제될 수 있습니다.**

## 개요

본 Post 에서는 지금까지 작성된 chatPDF 를 Streamlit 을 활용해 웹 서비스 형태로 작성하겠습니다.

### Streamlit 으로 웹서비스 구성하기

Streamlit 으로 웹 서비스를 구성할 때, 서비스에 접근해 첨부하는 파일에 따라 다른 학습이 가능하도록 파일 업로드 기능을 추가합니다. 
또한 편의를 위해 질문 작성 후 "질문하기" 버튼 등 웹 서비스로써의 동작을 위한 코드를 일부 추가합니다. 
(전체 코드는 함께 [첨부된 파이썬 파일][chatPDF_with_streamlit]을 참고하시기 바랍니다.)

```python
import streamlit as st

# 제목
st.title("chatPDF")
st.write("---")

# 파일 업로드 
import tempfile
import os

uploaded_file = st.file_uploader("Choose a file")
# 파일 업로드 후 동작하는 코드
if uploaded_file is not None:
    tmp_dir = tempfile.TemporaryDirectory()
    tmp_filepath = os.path.join(tmp_dir.name, uploaded_file.name)
    with open(tmp_filepath, "wb") as fp:
        fp.write(uploaded_file.getvalue())
    
    # PDF 파일 Loader 코드를 삽입
    # 생략

# 중간코드 생략

# Chroma DB 생성 후 질문 입력 부분
st.header("PDF 에 질문하세요")
question = st.text_input("질문을 입력하세요")
if st.button("질문하기"):
    # 질문이후 코드 삽입
    # ...
    # 질문에 대한 결과 출력 부분
    st.write(answer)
```

> 만약, 매번 파일을 업로드해 학습하지 않고 정해진 학습을 유지한 채 지속적으로 사용하고 싶다면, Chroma 의 옵션을 추가하면 됩니다. 해당 내용은 [이전 Post][step3_chatpdf_chroma_option] 에 포함되어 있으니 참고하기 바랍니다. 
{: .prompt-info}

Streamlit 로 웹 서비스를 실행합니다. 

- 명령어 : `streamlit run chatPDF_with_streamlit.py`

![streamlit_run_1](/assets/images/streamlit_run_1.png)

_streamlit 실행화면(1)_

정상적으로 실행이 됐다면, 다음과 같이 웹 화면을 볼 수 있습니다. 

![streamlit_run_2](/assets/images/streamlit_run_2.png)

_streamlit 실행화면(2)_

이제 파일을 업로드 후 질문을 하면 답변을 받을 수 있습니다. 






---
### 정리
* 

---
### 참고
* Streamlit 파일업로드 참고 [소스코드](https://github.com/langchain-ai/streamlit-agent/blob/main/streamlit_agent/chat_with_documents.py)
* 샘플코드
    - [chatPDF_with_streamlit.py](https://github.com/KeiTechNote/blog/tree/main/codes/chatPDF_with_streamlit.py)

---
### 관련 Posts
1. [LangChain 으로 AI 서비스 만들기 - Step 1. Init](https://keitechnote.github.io/blog/posts/langchain-step1-init/)
2. [LangChain 으로 AI 서비스 만들기 - Step 2. LLaMA2 + LangChain 경험하기](https://keitechnote.github.io/blog/posts/langchain-step2-chatpdf/)
3. [LangChain 으로 AI 서비스 만들기 - Step 3. chatPDf](https://keitechnote.github.io/blog/posts/langchain-step3-chatpdf/)


[step3_chatpdf_chroma_option]: https://keitechnote.github.io/blog/posts/langchain-step3-chatpdf/#1%EB%8B%A8%EA%B3%84--%EB%B3%80%ED%99%98%ED%95%9C-vector-%EB%A5%BC-vectordb-%EC%97%90-%EC%A0%80%EC%9E%A5%ED%95%A9%EB%8B%88%EB%8B%A4
[chatPDF_with_streamlit]: https://github.com/KeiTechNote/blog/tree/main/codes/chatPDF_with_streamlit.py