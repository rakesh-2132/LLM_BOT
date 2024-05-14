import streamlit as st
from web import Chatbot

def main():
    st.set_page_config(page_title="Chatbot Demo", layout="wide")

    st.title("Chatbot")

    # Sidebar for data ingestion
    st.sidebar.header("Data Ingestion")
    url_input = st.sidebar.text_input("Enter URL for data ingestion:")
    ingest_button = st.sidebar.button("Ingest Data")

    # Create an instance of Chatbot if URL is provided and data is ingested
    chatbot = None
    if url_input and ingest_button:
        chatbot = Chatbot(urls=[url_input])
        with st.spinner("Ingesting data..."):
            chatbot.ingest()
        st.success("Data ingested successfully!")

    # Sidebar for initializing language model and retrieval chain
    if chatbot:
        st.sidebar.header("Initialization")
        initialize_llm = st.sidebar.button("Initialize Language Model")
        initialize_chain = st.sidebar.button("Initialize Retrieval Chain")

        # Initialize language model
        if initialize_llm:
            with st.spinner("Initializing language model..."):
                chatbot.initialize_llm()
            st.success("Language model initialized successfully!")

        # Initialize retrieval chain
        if initialize_chain:
            with st.spinner("Initializing retrieval chain..."):
                chatbot.initialize_chain()
            st.success("Retrieval chain initialized successfully!")

    # Main content area for asking questions
    st.subheader("Ask a Question")
    question_input = st.text_area("Enter your question here:", height=100)
    if question_input:
        if st.button("Ask"):
            if chatbot:
                with st.spinner("Thinking..."):
                    response = chatbot.ask_question(question_input)
                st.write("Response:", response)

if __name__ == "__main__":
    main()
