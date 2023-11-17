---
title: LangChain 으로 AI 서비스 만들기 - Step3 chatPDF
date: 2023-11-17 05:30 +09:00
published: true
categories: [AI]
tags: [AI, LangChain, Dev, Python, LLM, LLaMA2, chatPDF, cTransformers]
---

***본 컨텐츠는 Udemy의 "랭체인으로 AI 웹서비스 만들기 with ChatGPT, LLaMA2" 내용 중 일부를 정리한 글입니다. 문제시 삭제될 수 있습니다.**

## 개요

chatPDF를 만드는 과정은 그게 "PDF를 분석하는 단계" 와 분석된 데이터를 기반으로 "질의/응답하는 단계" 로 나눌 수 있습니다. 
각 단계를 세부적으로 나누면 다음과 같습니다. 

**1단계 : PDF 분석**

1. PDF 를 읽어들인다. 
2. PDF 속 글을 `Embedding` 을 거쳐 `Vector`로 변환합니다. 
3. 변환한 Vector 를 `VectorDB` 에 저장합니다. 


**2단계 : 질의 응답**

1. 질문을 분석해 Vector 로 변환합니다. 
2. Vector 로 DB 를 조회합니다. 
3. 응답합니다. 

**3단계 : 웹 서비스**

1. 웹 페이지을 만듭니다. 
2. 일련의 기능을 연결한다. 
3. 웹 서비스를 구동한다. 


앞으로 위의 단계에 맞춰 진행합니다. 

### 들어가기 앞서...

이전에 보지 못했던 개념들이 등장합니다. `Vector (벡터)` 와 `VectorDB (벡터DB)`, `Embedding (임베딩)` 입니다. 
`Vector` 는 숫자들의 묶음으로 파이썬의 List ([ ]) 형태로 표현됩니다. Vector 의 숫자들은 어떤 값의 위치를 나타내기 위한 좌표입니다. 
예를 들어, 하나의 점을 표현할 때, 2차원의 X, Y 그래프는 \[1,2\] 와 같이 2개 값으로 표현하고, 3차원의 X, Y, Z 그래프에서는 \[1, 2, 3\] 의 3개의 값으로 표현합니다. 이와 유사하게, PDF 와 같은 문자열을 분석하고 개별 위치를 숫자로 변환한 것으로 Vector 라고 합니다. 
`VectorDB` 는 Vector 값을 효율적으로 저장하기 위한 DB 입니다. 저장되는 값이 Vector 라서 Vector DB 라고 일컫지만 MySQL 과 같은 보통 DB 와 크게 다르진 않습니다. 

`Embedding (임베딩)`은 데이터를 Vector로 변환하는 것을 의미합니다. 본 Post 의 chatPDF 에서는 PDF 속의 글들이 데이터가 되고 글들을 분석해 Vector로 변환하는 과정이 Embedding 입니다. 

![mnist_to_vector_2d](/assets/images/mnist_to_vector_2d.png)

_손글씨 이미지(mnist) 를 2차원 벡터로 변환한 모습 (출처 : [colah's blog][colah_blog])_

![mnist_to_vector_3d](/assets/images/mnist_to_vector_3d.png)

_손글씨 이미지(mnist) 를 3차원 벡터로 변환한 모습 (출처 : [colah's blog][colah_blog])_

굳이 Embedding 을 이용해 Vector 로 변환하는 이유는 숫자이므로 연산(덧셈, 뺄셈 등)을 할 수 있고, 여러 Vector 를 모아두면 Vector 간의 연관성도 표출되기 때문입니다. 

![index_data_as_vector](/assets/images/index_data_as_vector.png)

_Vector 로 확인한 데이터간의 연관성 (출처 : [Weaviate][weaviate])_

이러한 데이터간의 연관성을 이용해 재밌는 게임([꼬맨틀][꼬맨틀])도 만들 수 있습니다. 관심있으면 방문해 보기 바랍니다. 


### 1단계 : PDF 분석 - PDF 를 읽어들인다. 

chatPDF 로 분석할 PDF 를 준비합니다. 보안에 관심이 많고 최근 AWS 를 공부하기 시작해서 SK쉴더스에서 제작해 배포한 [2023 클라우드 보안 가이드 - AWS][sk_shieldus_cloud_security_aws] 를 사용하겠습니다. 

> 파일명이 한글이고 너무 길면 번거롭기 떄문에 임의의 영문명으로 변경해 사용합니다. (예 :2023_cloud_security_aws)
{: .prompt-info}

PDF 파일을 읽어들이는 방법은 [LangChain 문서][python_langchain_pdf_load] 에 다양한 방법이 설명되어 있습니다. 그 중 `PyMuPDF` 를 사용하겠습니다. PyMuPDF 를 설치합니다. 

- 명령어 : `pip install pymupdf`

![install_pymypdf](/assets/images/install_pymypdf.png)

_pymupdf 라이브러리 설치_

> 강의에서는 `PyPDF`를 사용했고 한글이 정상적으로 출력되는 것도 확인되었습니다. 하지만 제가 사용중인 노트북에서는 한글이 깨지는 현상이 발생해 `PyMuPDF` 를 사용합니다. 
![error_encoding_korean](/assets/images/error_encoding_korean.png)

_한글 깨짐 화면_

```python
# -*- coding:utf-8 -*-
# Step 1-1. Load PDF
from langchain.document_loaders import PyMuPDFLoader

filename = "2023_cloud_security_aws.pdf"

# PDF 파일 불러오기
loader = PyMuPDFLoader(filename)
pages = loader.load()

# 테스트 코드 - 두번째 페이지 출력하기
print(pages[1])
```

![print_pdf_second_pages](/assets/images/print_pdf_second_pages.png)

_PDF 두번째 페이지 출력하기_

> 읽어들인 PDF 의 첫번째 페이지는 표지로 한글이 많지 않아 두번째 페이지를 출력해 보았습니다. 이 점 참고 바랍니다. 
{: .prompt-info}


### 1단계 : PDF 속 글을 Embedding 을 거쳐 Vector 로 변환합니다. 

Vector는 찾을려는 데이터의 위치라고 말씀드렸습니다. 즉, 정확도를 위해선 Vector 를 많이 만드는 것이 좋지만, 너무 많이 만들면, Vector 크기가 많아지고, 이를 저장한 DB 에서 찾을 때 속도가 느려지는 등의 문제점도 있습니다. 따라서, 적절한 수준으로 나눠서 Vector를 작성해야 합니다. 따라서, Embedding 에 넣는 데이터의 크기에 따라 결과물인 Vector 가 달라집니다. 

현재 PDF로 읽어들인 원본 데이터는 페이지 단위로 나눠져 있습니다. 이를 좀 더 작은 크기로 나눠(split)보겠습니다. 이 또한 [공식문서][text_splitters]에 설명되어 있습니다. 

```python
# Step 1-2. Split PDF
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size = 100,               # 나누는 글자 수 단위, 100글자 단위로 나뉨
    chunk_overlap  = 20,            # 앞뒤 겹치는 글자 수, 앞뒤 20글자를 추가로 가지고 있어 문맥을 유지시킴
    length_function = len,          # 글자 길이는 결정하는 함수명
    is_separator_regex = False,     # 패턴(정규표현식) 기반으로 나눌지 여부, 사용하지 않음(False)
)

texts = text_splitter.split_documents(pages)
print(texts[0])
```

![split_texts](/assets/images/split_texts.png)

_Text Split 결과_
 
이제 Vector 로 만들기 위해 Embedding 합니다. [공식문서][text_embedding_model]에서는 OpenAI를 사용하는 방법만을 설명하고 있지만 첫 문단의 설명처럼  [OpenAI][text_embedding_openai] 이외에 [Cohere][text_embedding_cohere], [HuggingFace][text_embedding_hugging_face]  등도 사용할 수 있습니다. 

> The Embeddings class is a class designed for interfacing with text embedding models. There are lots of embedding model providers (OpenAI, Cohere, Hugging Face, etc) - this class is designed to provide a standard interface for all of them.
(Embedding 클래스는 text embedding model 인터페이스를 위해 설계되었습니다. 이 클래스는 수 많은 embedding model provider 가 있습니다. - 이 클래스는 모든 것을 지원하기 위한 표준 인터페이스를 제공하기 위해 설계되었습니다.)

본 Post 에서는 HuggingFace 를 사용합니다. 

- 명령어 : `pip install sentence_transformers`

![install_huggingface](/assets/images/install_huggingface.png)

_Embedding 을 위한 HuggingFace 라이브러리 설치_

HugginggFace 는 LLM 처럼 다운로드할 수 있는 [다양한 모델][hugging_face_model]을 제공하고 있습니다. 그 중 하나를 선택합니다. 

```python
# Step 1-3. create embedding function to vector
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings

embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L12-v2")
```
모델을 지정하고 실행하면 해당 모델이 PC 에 설치되어 있는지를 살핀 후 없는 경우 자동으로 다운로드 됩니다. 

![download_hugging_face_model](/assets/images/download_hugging_face_model.png)

_HuggingFace 모델 다운로드_

Embedding 모델은 Vector 정보를 얼마나 잘 가져오느냐와 같은 성능에 영향을 미친다. 따라서, HunggingFace 에서 제공하는 모델이외에도 OpenAI 나 Cohere 등 다양한 Embedding 모델로 테스트해 보기 바랍니다. 

추가로 Embedding 을 통해 데이터가 Vector 로 변환될 때, 데이터를 일정 단위로 나누는 작업이 내부적으로 이루어집니다. 이를 토큰화(Tokenization) 라 하고 이렇게 토큰화하는 도구를 토큰나이저 (Tokenizer) 라고 합니다. 
예를 들어, 페이지 단위로 읽어들인 PDF 를 Text Splitter 로 일정 단위로 나누었습니다. (예제 코드에서 chunk_size 를 의미하며, 100 글자 단위로 설정했었습니다.) 여러 단어, 문장 또는 문단을 단위로 나눠졌습니다. 이를 Vector 로 변환될 때, 단어 단위로 나눠서 Vector 로 만드는 경우, 단어 토큰화 (Word Tokenization) 라고 합니다. 
따라서, Embedding 에서 어떤 단위든 토큰화가 이루어져야 Vector 로 생성할 수 있습니다. 이를 위해 토큰나이저 중 하나인 `tiktoken` 을 사용합니다. 

- 명령어 : `pip install tiktoken`

![install_tokenizer_tiktoken](/assets/images/install_tokenizer_tiktoken.png)

_토큰나이저 tiktoken 설치_


### 1단계 : 변환한 Vector 를 VectorDB 에 저장합니다. 

VectorDB 의 종류는 `chroma`, `Pinecone`, `Weaviate` 등이 있습니다. 본 Post 에서는 [chroma][component_vectorstore_chroma] 를 사용합니다. 

- 명령어 : `pip install chromadb`

![install_chromadb](/assets/images/install_chromadb.png)

_VectorDB 로 Chroma 설치_

```python
# Step 1-4. Load it into Chroma
from langchain.vectorstores import Chroma

db = Chroma.from_documents(texts, embedding_function)
```

> Chroma DB 는 기본적으로 메모리에만 존재합니다. 따라서, 코드를 실행할 때마다 PDF 를 읽고, 분석하는 일련의 과정을 반복하는 단점이 있습니다. 이를 해소하려면 데이터를 Chroma DB 파일로 저장하는 옵션을 부여하면 됩니다. 
```python
# 이전 코드 생략
db = Chroma.from_documents(texts, embedding_function, persist_directory=r"<DB 저장위치>")
```
{: .prompt-info}


### 2단계 : 질문을 분석해 응답합니다. 

질의 응답을 위한 LLM을 선택합니다. 로컬 PC 에서 오프라인에서 사용하기 위해 LLaMA2 를 선택하고 질문을 입력하고 그 결과를 확인합니다. 

```python
# Step 2-1. Select LLaMA2 & Question
from langchain.llms import CTransformers

llm = CTransformers(
    model="llama-2-7b-chat.ggmlv3.q8_0.bin", 
    model_type="llama"
)

from langchain.retrievers.multi_query import MultiQueryRetriever

question = "S3 에서 퍼블릭 액세스 차단 관리는 어떻게 해야하지?"
retriever_from_llm = MultiQueryRetriever.from_llm(
    retriever=db.as_retriever(), llm=llm
)

docs = retriever_from_llm.get_relevant_documents(query=question)
print(docs)

```

![return_docs_for_question_1](/assets/images/return_docs_for_question_1.png)

_질의에 대한 PDF 내용 추출_

PDF 의 페이지 데이터가 그대로 추출되는 것을 알 수 있습니다. 이는 질문을 인식하고 유사성을 인식해 가장 가까운 값을 추출해 보여는 것입니다. 하지만 분석된 형태로 출력되므로 사람이 인지하는데는 조금 불편한 부분이 있습니다. 

### 2단계 : Chatbot 처럼 응답합니다. 

```python
from langchain.chains import RetrievalQA

qa_chain = RetrievalQA.from_chain_type(llm, retriever=db.as_retriever())
answer = qa_chain({"query": question})
print(answer)
```

![return_docs_for_question_2](/assets/images/return_docs_for_question_2.png)

_질의에 대한 응답_

질의에 대해 응답했으나 아쉽게도 한글 문서이지만 영문으로 출력되는 것을 볼 수 있습니다. 이는 LLaMA2 의 특성입니다. 즉, 한국어를 입력하면 이해는 하지만 질의에 대한 응답은 영문으로 출력되는 것입니다. 이러한 부분을 해소하려면 LLaMA2 가 아닌 한국어를 지원하는 LLM 을 선택하면 됩니다. 

![korean_llm_awesome_list](/assets/images/korean_llm_awesome_list.png)

_한국어 오픈소스 LLM Awesome List (출처 : [PyTouch 게시판 - 읽을거리 & 정보공유][korean_llm_awesome_list_pytouch])

지금까지 chatPDF 의 핵심기능인 PDF 파일을 읽고, 분석하고 질의/응답하는 기능을 작성해 보았습니다. 
다음 Post 에서 Streamlit 을 이용해 웹 서비스 형태로 작성해 보겠습니다. 

---
### 정리
* 데이터는 토큰화를 거쳐 Vector 형태로 변환되어 연산합니다. 
* chatPDF 에서 PDF 읽기, Embedding, Vector DB, LLM 등 각 단계별 선택할 수 있는 다양한 요소들을 조합해 볼 수 있습니다. 

---
### 참고
* 샘플코드
    - [chatPDF.py](https://github.com/KeiTechNote/blog/tree/main/codes/chatPDF.py)

---
### 관련 Posts
1. [LangChain 으로 AI 서비스 만들기 - Step 1. Init](https://keitechnote.github.io/blog/posts/langchain-step1-init/)
2. [LangChain 으로 AI 서비스 만들기 - Step 2. LLaMA2 + LangChain 경험하기](https://keitechnote.github.io/blog/posts/langchain-step2-chatpdf/)


[colah_blog]: https://colah.github.io/posts/2014-10-Visualizing-MNIST/
[weaviate]: https://weaviate.io/developers/weaviate/concepts/vector-index
[꼬맨틀]: https://semantle-ko.newsjel.ly/
[sk_shieldus_cloud_security_aws]: https://www.skshieldus.com/download/files/download.do?o_fname=2023%20%ED%81%B4%EB%9D%BC%EC%9A%B0%EB%93%9C%20%EB%B3%B4%EC%95%88%20%EA%B0%80%EC%9D%B4%EB%93%9C_%20AWS.pdf&r_fname=20221220170637944.pdf
[python_langchain_pdf_load]: https://python.langchain.com/docs/modules/data_connection/document_loaders/pdf
[text_splitters]: https://python.langchain.com/docs/modules/data_connection/document_transformers/#text-splitters
[text_embedding_model]: https://python.langchain.com/docs/modules/data_connection/text_embedding/
[text_embedding_openai]: https://python.langchain.com/docs/modules/data_connection/text_embedding/#get-started
[text_embedding_cohere]: https://python.langchain.com/docs/integrations/text_embedding/cohere
[text_embedding_hugging_face]: https://python.langchain.com/docs/integrations/text_embedding/huggingfacehub
[hugging_face_model]: https://huggingface.co/models
[component_vectorstore_chroma]: https://python.langchain.com/docs/integrations/vectorstores/chroma
[korean_llm_awesome_list_pytouch]: https://discuss.pytorch.kr/t/gn-awesome-korean-llm-llm-awesome-list/2315