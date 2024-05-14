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
    def __init__(self, urls, openai_api_key):
        self.urls = urls
        self.openai_api_key = openai_api_key
        self.vector_store = None
        self.llm = None
        self.chain = None

    
    def ingest(self, url):
        loaders = UnstructuredURLLoader(urls=[url])
        data = loaders.load()

        text_splitter = CharacterTextSplitter(separator='\n',
                                          chunk_size=10000,
                                          chunk_overlap=200)

        docs = text_splitter.split_documents(data)
        embeddings = OpenAIEmbeddings()

        vectorStore_openAI=FAISS.from_documents(docs,embbedings)
        with open("faiss_store_openai.pkl","wb") as f:
         pickle.dump(vectorStore_openAI,f)

        with open("faiss_store_openai.pkl","rb") as f:
         vectorestore=pickle.load(f)


    def initialize_llm(self):
        self.llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')

    def initialize_chain(self):
        self.chain = RetrievalQAWithSourcesChain.from_llm(llm=self.llm, retriever=self.vector_store.as_retriever())

    def ask(self, question: str) -> str:
        self.llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')
        self.chain = RetrievalQAWithSourcesChain.from_llm(llm=self.llm, retriever=self.vector_store.as_retriever())
        if self.chain is None:
            response = "Please, add a url."
        else:
            docs = self.db.get_relevant_documents(question)
            response = self.chain.run(input_documents=docs, question=question)
        return response

if __name__ == "__main__":
    load_dotenv()
    openai_api_key = os.getenv("openai_api_key")
    urls = ['https://www.javatpoint.com/what-is-computer']

    chatbot = Chatbot(urls=urls, openai_api_key=openai_api_key)
    chatbot.load_data()
    chatbot.initialize_llm()
    chatbot.initialize_chain()

    question = "what is computer"
    response = chatbot.ask(question)
    print(response)
