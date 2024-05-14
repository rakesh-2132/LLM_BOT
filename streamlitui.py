import streamlit as st
from web import Chatbot

def main():
    st.title("Chatbot")

  
    url_input = st.text_input("Enter URL for data ingestion:")
    question_input = st.text_input("Ask a question:")

    
    if url_input:
        chatbot = Chatbot(urls=[url_input])

      
        with st.spinner("Ingesting data..."):
            chatbot.ingest()
        st.success("Data ingested successfully!")

        
        with st.spinner("Initializing retrieval chain..."):
            chatbot.initialize_llm()
            chatbot.initialize_chain()
        st.success("Retrieval chain initialized successfully!")

       
        if question_input:
            with st.spinner("Thinking..."):
                response = chatbot.ask_question(question_input)
            st.write("Response:", response)

if __name__ == "__main__":
    main()

