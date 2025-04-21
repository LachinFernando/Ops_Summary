import streamlit as st
from openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
import os

from prompts import COMMON_TEMPLATE


QA_MODEL = "gpt-4o-mini"

# state handling for the chat app
if 'transcript' not in st.session_state:
    st.session_state['transcript'] = None

if not st.session_state["transcript"]:
    st.error("Please Generate a Transcript from App Page!")
    st.stop()


def get_model():
    model = ChatOpenAI(model=QA_MODEL, api_key=os.environ["OPENAI_API_KEY"])
    return model


def streaming_question_answering(query_question: str, context_text: str,  template: str = COMMON_TEMPLATE):
    prompt = ChatPromptTemplate.from_template(template)
    model = get_model()
    output_parser = StrOutputParser()

    # create the chain
    chain = prompt | model | output_parser

    # get the answer
    return chain.stream({"context": context_text, "question": query_question})


# web application
st.title("Chat With Transcript")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.write_stream(streaming_question_answering(prompt, st.session_state["transcript"]))
    st.session_state.messages.append({"role": "assistant", "content": response})