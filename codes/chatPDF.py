# -*- coding:utf-8 -*-
# Step 1-1. Load PDF
from langchain.document_loaders import PyMuPDFLoader

filename = "2023_cloud_security_aws.pdf"

# PDF 파일 불러오기
loader = PyMuPDFLoader(filename)
pages = loader.load()

# 테스트 코드 - 두번째 페이지 출력하기
# print(pages[1])

# Step 1-2. Split PDF
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size = 300,
    chunk_overlap  = 20,
    length_function = len,
    is_separator_regex = False,
)

texts = text_splitter.split_documents(pages)
# print(texts[0])

# Step 1-3. create embedding function to vector
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L12-v2")

# Step 1-4. Load it into Chroma
from langchain.vectorstores import Chroma

db = Chroma.from_documents(texts, embedding_function, persist_directory=r".\security\aws.db")

# Step 2-1. Select LLaMA2 & Question
from langchain.llms import CTransformers

llm = CTransformers(
    model="llama-2-7b-chat.ggmlv3.q8_0.bin", 
    model_type="llama"
)

question = "S3 에서 퍼블릭 액세스 차단 관리는 어떻게 해야하지?"

from langchain.retrievers.multi_query import MultiQueryRetriever

retriever_from_llm = MultiQueryRetriever.from_llm(
    retriever=db.as_retriever(), llm=llm
)
docs = retriever_from_llm.get_relevant_documents(query=question)
print(docs)

# Step 2-2. RetrievalQA
from langchain.chains import RetrievalQA

qa_chain = RetrievalQA.from_chain_type(llm, retriever=db.as_retriever())
answer = qa_chain({"query": question})
print(answer)










# # # Step 1-3. create embedding function to vector
# # from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings

# # embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L12-v2")

# # # Step 1-4. Load it into Chroma
# # from langchain.vectorstores import Chroma

# # def get_embeddings(texts):
# #     embeddings = []
# #     for text in texts:
# #         embeddings.append(embedding_model.predict(text))
# #     return embeddings

# # db = Chroma.from_documents(texts,  get_embeddings)


# # embedding_function
# ['aembed_documents', 'aembed_query', 'cache_folder', 'client', 'construct', 'copy', 'dict', 'embed_documents', 'embed_query', 'encode_kwargs', 'from_orm', 'json', 'model_kwargs', 'model_name', 'multi_process', 'parse_file', 'parse_obj', 'parse_raw', 'schema', 'schema_json', 'update_forward_refs', 'validate']

# # Chroma
# ['aadd_documents', 'aadd_texts', 'add_documents', 'add_texts', 'adelete', 'afrom_documents', 'afrom_texts', 'amax_marginal_relevance_search', 'amax_marginal_relevance_search_by_vector', 'as_retriever', 'asearch', 'asimilarity_search', 'asimilarity_search_by_vector', 'asimilarity_search_with_relevance_scores', 'asimilarity_search_with_score', 'delete', 'delete_collection', 'embeddings', 'from_documents', 'from_texts', 'get', 'max_marginal_relevance_search', 'max_marginal_relevance_search_by_vector', 'persist', 'search', 'similarity_search', 'similarity_search_by_vector', 'similarity_search_by_vector_with_relevance_scores', 'similarity_search_with_relevance_scores', 'similarity_search_with_score', 'update_document', 'update_documents']