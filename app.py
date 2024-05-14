import os
import tempfile
import streamlit as st
from streamlit_chat import message
from urlbot import Chatbot
from dotenv import load_dotenv


st.set_page_config(page_title="Website to Chatbot")

def display_messages():
    st.subheader("Chat")
    for i, (msg, is_user) in enumerate(st.session_state["messages"]):
        message(msg, is_user=is_user, key=str(i))
    st.session_state["thinking_spinner"] = st.empty()

def process_input():
    if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
        user_text = st.session_state["user_input"].strip()
        with st.session_state["thinking_spinner"], st.spinner(f"Thinking"):
            query_text = st.session_state["urlbot"].ask(user_text)

        st.session_state["messages"].append((user_text, True))
        st.session_state["messages"].append((query_text, False))

def ingest_input():
    if st.session_state["input_url"] and len(st.session_state["input_url"].strip()) > 0:
        url = st.session_state["input_url"].strip()
        with st.session_state["thinking_spinner"], st.spinner(f"Ingesting {url}"):
            ingest_text = st.session_state["urlbot"].ingest(url)


def display_mesaage():
    if st.session_state["input_url"] and len(st.session_state["input_url"].strip())>0:
        url = st.seesion_state["input_url"].strip()
        with st.session_state["thinking_sprinner"], st.spinner(f"Thinking"):
            query_text=st.session_state["url_bot"].ask(user_text)
    
    st.session_state["message"].append((user_text ,True))
    st.session_state["message"].append((query_text, False))


def ingest_input():
    if st.session_state["input_url"] and len(st.session_state["user_input"].strip()) >0:
        user_text = st.session_state["user_input"].strip()
        with st.session_state["thinking_sprinner"], st.spinner(f"thinking"):
            query_text=st.session_state["urlbot"].ask(user_text)
        

        st.session_state["message"].append((user_text, True))
        st.session_state["message"].append((query_text, False))




def main():
    load_dotenv()
    openai_api_key = os.getenv("openai_api_key")
    urls = ['https://www.javatpoint.com/what-is-computer']

    # # Initialize Chatbot with urls and openai_api_key
    chatbot = Chatbot(urls=urls, openai_api_key=openai_api_key)

    if len(st.session_state) == 0:
        st.session_state["messages"] = []
        st.session_state["url"] = ""
        st.session_state["urlbot"] = chatbot  

    st.header("Website to Chatbot")

    st.subheader("Add a URL")
    st.text_input("Input URL", value=st.session_state["url"], key="input_url", on_change=ingest_input)

    st.session_state["ingestion_spinner"] = st.empty()

    display_messages()
    st.text_input("Message", key="user_input", on_change=process_input)

    st.divider()
    

if __name__ == "__main__":
    main()
