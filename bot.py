import os 
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import CharacterTextSplitter
import pickle
import faiss
# from langchain.vectorstores import faiss
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
os.getenv("openai_api_key")
# os.environ["OPENAI_API_KEY"]="OPENAI_API_KEY"
urls=['https://www.javatpoint.com/what-is-computer']
# urls=['https://www.techtarget.com/searchwindowsserver/definition/computer']



loaders=UnstructuredURLLoader(urls=urls)
data=loaders.load()

text_splitter=CharacterTextSplitter(separator='\n',
                                    chunk_size=10000,
                                    chunk_overlap=200)

docs=text_splitter.split_documents(data)
embbedings=OpenAIEmbeddings()

vectorStore_openAI=FAISS.from_documents(docs,embbedings)
with open("faiss_store_openai.pkl","wb") as f:
     pickle.dump(vectorStore_openAI,f)

with open("faiss_store_openai.pkl","rb") as f:
     vectorestore=pickle.load(f)

llm=ChatOpenAI(temperature=0,model_name='gpt-3.5-turbo')

chain= RetrievalQAWithSourcesChain.from_llm(llm=llm,retriever=vectorestore.as_retriever())

print(chain({"question":"what is computer"},return_only_outputs=True))



