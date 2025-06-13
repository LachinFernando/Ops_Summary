from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
import os
import streamlit as st

import prompts as pm


# environment variables
os.environ["LANGCHAIN_TRACING_V2"] = st.secrets["llm"]["LANGCHAIN_TRACING_V2"]
os.environ["LANGCHAIN_API_KEY"] = st.secrets["llm"]["LANGCHAIN_API_KEY"]
os.environ["LANGCHAIN_ENDPOINT"] = st.secrets["llm"]["LANGCHAIN_ENDPOINT"]
os.environ["LANGCHAIN_PROJECT"] = st.secrets["llm"]["LANGCHAIN_PROJECT"]
os.environ["OPENAI_API_KEY"] = st.secrets["llm"]["OPENAI_API_KEY"]


# constants
MODEL = "gpt-4o-mini"

# set the openai model
llm = ChatOpenAI(model=MODEL, temperature=0)


# this is be default has the messages and add_messages reducers
class BotState(MessagesState):
    full_script: str
    ten_minute_script: str
    topics: str
    review: str
    directions: str
    homework: str
    code_error: str
    technical_issue: str
    email_info: str


def get_important_topic(state: BotState):
    # get full script
    full_session_script = state["full_script"]

    # invoke the llm
    message_input = [SystemMessage(pm.IMPORTANT_TOPICS_PROMPT.format(transcript = full_session_script))]
    topic_invoke = llm.invoke(message_input)

    return {
        "topics": topic_invoke.content
    }


def get_homework_feedback(state: BotState):
    ten_minutes_script = state["ten_minute_script"]

    # invoke structured output llm
    homework_input = [SystemMessage(pm.HOMEWORK_CHECK_PROMPT.format(transcript = ten_minutes_script))]

    homework_invoke = llm.invoke(homework_input)

    return {
        "review": homework_invoke.content
    }


def get_future_topics(state: BotState):
    full_script = state["full_script"]

    # invoke the llm
    message_ft_input = [SystemMessage(pm.FUTURE_TOPICS_PROMPT.format(transcript = full_script))]
    future_topic_invoke = llm.invoke(message_ft_input)

    return {
        "directions": future_topic_invoke.content
    }


def extract_next_week_homework(state: BotState):
    full_script = state["full_script"]

    # create homework extraction
    homework_input = [SystemMessage(pm.GIVEN_HOMEWORK_PROMPT.format(transcript = full_script))]
    homework_invoke = llm.invoke(homework_input)

    return {
        "homework": homework_invoke.content
    }


def extract_code_errors(state: BotState):
    full_script = state["full_script"]

    # create code error ouput
    code_error_output = [SystemMessage(pm.ERROR_CHECKS.format(transcript = full_script))]
    code_error_invoke = llm.invoke(code_error_output)

    return {
        "code_error": code_error_invoke.content
    }


def extract_technical_issues(state: BotState):
    full_script = state["full_script"]

    # technical issue idenitfier
    technical_issue = [SystemMessage(pm.TECHNICAL_ISSUE.format(transcript = full_script))]
    technical_issue_invoke = llm.invoke(technical_issue)

    return {
        "technical_issue": technical_issue_invoke.content
    }


def extract_sending_emails(state: BotState):
    full_script = state["full_script"]
    print(full_script)

    # technical issue idenitfier
    email_sending = [SystemMessage(pm.SEND_EMAIL_PROMPT.format(transcript = full_script))]
    email_sending_invoke = llm.invoke(email_sending)

    return {
        "email_info": email_sending_invoke.content
    }


# add nodes and edges
helper_builder = StateGraph(BotState)
helper_builder.add_node("main_topics", get_important_topic)
helper_builder.add_node("homework_review", get_homework_feedback)
helper_builder.add_node("future_topics", get_future_topics)
helper_builder.add_node("homework_extraction", extract_next_week_homework)
helper_builder.add_node("extract_code_errors", extract_code_errors)
helper_builder.add_node("extract_technical_issues", extract_technical_issues)
helper_builder.add_node("extract_sending_emails", extract_sending_emails)

# build graph
helper_builder.add_edge(START, "main_topics")
helper_builder.add_edge(START, "homework_review")
helper_builder.add_edge(START, "future_topics")
helper_builder.add_edge(START, "homework_extraction")
helper_builder.add_edge(START, "extract_code_errors")
helper_builder.add_edge(START, "extract_technical_issues")
helper_builder.add_edge(START, "extract_sending_emails")
helper_builder.add_edge(["main_topics", "homework_review", "future_topics", "homework_extraction", "extract_code_errors", "extract_technical_issues", "extract_sending_emails"], END)

# compile the graph
memory = MemorySaver()
helper_graph = helper_builder.compile()