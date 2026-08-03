# UI Based interface for ChatWithPDF

import uuid
import streamlit as st
from datetime import datetime
from htmlTemplates import css, bot_template, user_template
from langchain_app import (
    get_pdf_text,
    get_text_chunks,
    get_vectorstore,
    get_conversation_chain,
)

def handle_userinput(user_question):
    time_str = datetime.now().strftime('%H:%M')

    # Build the message history expected by create_agent-based graphs.
    messages = [
        {"role": msg["role"], "content": msg["content"]}
        for msg in st.session_state.chat_history
    ]
    messages.append({"role": "user", "content": user_question})

    result = st.session_state.conversation.invoke(
        {"messages": messages},
        {"configurable": {"thread_id": st.session_state.thread_id}},
    )

    raw_content = result["messages"][-1].content
    final_answer = raw_content if isinstance(raw_content, str) else "".join(
        block.get("text", "") if isinstance(block, dict) else str(block)
        for block in raw_content
    )

    st.session_state.chat_history.append({
        "role": "user", "content": user_question, "time": time_str
    })
    st.session_state.chat_history.append({
        "role": "bot", "content": final_answer, "time": time_str
    })

def render_chat():
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.write(
                user_template.replace("{{MSG}}", msg["content"]).replace("{{TIME}}", msg["time"]),
                unsafe_allow_html=True,
            )
        else:
            st.write(
                bot_template.replace("{{MSG}}", msg["content"]).replace("{{TIME}}", msg["time"]),
                unsafe_allow_html=True,
            )

def new_session():
    st.session_state.chat_history = []
    st.session_state.thread_id = str(uuid.uuid4())
    # rebuild conversation chain with same vectorstore so memory resets
    if st.session_state.vectorstore is not None:
        st.session_state.conversation = get_conversation_chain(st.session_state.vectorstore)

def main():
    st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(uuid.uuid4())
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None

    col1, col2 = st.columns([5, 1])
    with col1:
        st.header("Chat with multiple PDFs :books:")
    with col2:
        st.write("")
        st.write("")
        if st.button("New Session", type="secondary"):
            new_session()

    render_chat()

    user_question = st.chat_input("Ask a question about your documents:")
    if user_question and st.session_state.conversation:
        handle_userinput(user_question)
        st.rerun()

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                vectorstore = get_vectorstore(text_chunks)
                st.session_state.vectorstore = vectorstore
                st.session_state.conversation = get_conversation_chain(vectorstore)
                st.session_state.chat_history = []
                st.session_state.thread_id = str(uuid.uuid4())
                st.success("Processed successfully")

if __name__ == '__main__':
    main()
