import streamlit as st
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
import time
import pandas as pd

load_dotenv()

model = ChatAnthropic(model="claude-3-5-sonnet-20240620")

prompt = st.chat_input("Say something")

uploaded_files = st.file_uploader("Upload files", type=["pdf", "docx", "txt", "csv"], accept_multiple_files=True)

file_contents = ""
if uploaded_files:
    for uploaded_file in uploaded_files:
        # Read the file contents
        if uploaded_file.type == "text/plain":
            file_contents += uploaded_file.read().decode("utf-8") + "\n"
        elif uploaded_file.type == "text/csv":
            df = pd.read_csv(uploaded_file)
            file_contents += df.to_string(index=False) + "\n"
        # Add more conditions for other file types if needed

if prompt or file_contents:
    # Ensure prompt is a string
    context = (prompt or "") + "\n" + file_contents

    # Call the LLM with streaming
    config = {"configurable": {"thread_id": "abc789"}}
    input_messages = [HumanMessage(content=context)]
    
    def stream_response():
        for chunk in model.stream(
            input_messages,
            config=config,
        ):
            if isinstance(chunk, AIMessage):
                yield chunk.content + " "
                time.sleep(0.02)

    st.write_stream(stream_response)
