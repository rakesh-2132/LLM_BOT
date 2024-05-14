import os
import pickle
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv

class Chatbot:
    def __init__(self, urls):
        self.urls = urls
        self.vector_store = None
        self.llm = None
        self.chain = None

    def ingest(self):
        loaders = UnstructuredURLLoader(urls=self.urls)
        data = loaders.load()

        text_splitter = CharacterTextSplitter(separator='\n',
                                              chunk_size=10000,
                                              chunk_overlap=1000)

        docs = text_splitter.split_documents(data)
        embeddings = OpenAIEmbeddings()

        self.vector_store = FAISS.from_documents(docs, embeddings)

    def initialize_llm(self):
        self.llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')

    def initialize_chain(self):
        self.chain = RetrievalQAWithSourcesChain.from_llm(llm=self.llm, retriever=self.vector_store.as_retriever())

    def ask_question(self, question):
        return self.chain({"question": question}, return_only_outputs=True)


# import streamlit as st
# from langchain.document_loaders import UnstructuredURLLoader
# from langchain.text_splitter import CharacterTextSplitter
# from langchain.vectorstores.faiss import FAISS
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.chains import RetrievalQAWithSourcesChain
# from langchain.chat_models import ChatOpenAI
# from dotenv import load_dotenv

# class Chatbot:
#     def __init__(self, urls):
#         self.urls = urls
#         self.vector_store = None
#         self.llm = None
#         self.chain = None

#     def ingest(self):
#         loaders = UnstructuredURLLoader(urls=self.urls)
#         data = loaders.load()

#         text_splitter = CharacterTextSplitter(separator='\n',
#                                               chunk_size=10000,
#                                               chunk_overlap=200)

#         docs = text_splitter.split_documents(data)
#         embeddings = OpenAIEmbeddings()

#         self.vector_store = FAISS.from_documents(docs, embeddings)

#     def initialize_llm(self):
#         self.llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')

#     def initialize_chain(self):
#         if self.llm and self.vector_store:
#             self.chain = RetrievalQAWithSourcesChain.from_llm(llm=self.llm, retriever=self.vector_store.as_retriever())
#         else:
#             st.error("LLM and vector store must be initialized before initializing the chain.")

#     def ask_question(self, question):
#         if self.chain:
#             return self.chain({"question": question}, return_only_outputs=True)
#         else:
#             st.error("Chain must be initialized before asking a question.")

# # Rest of the Streamlit app code remains the same
