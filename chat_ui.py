import streamlit as st
import requests

API_STREAM_URL = "http://localhost:8000/stream"

st.set_page_config(page_title="Zunneko LLM Router", layout="wide")

st.title("🤖 Zunneko AI Router Chat")

# -------- Session Memory --------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------- Display Chat History --------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------- User Input --------
prompt = st.chat_input("Ask something...")

if prompt:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # -------- Assistant Streaming --------
    with st.chat_message("assistant"):

        response_placeholder = st.empty()
        full_response = ""

        try:
            with requests.get(
                API_STREAM_URL,
                params={"prompt": prompt},
                stream=True
            ) as r:

                for chunk in r.iter_content(chunk_size=1):
                    if chunk:
                        token = chunk.decode("utf-8",errors="ignore")
                        full_response += token
                        response_placeholder.markdown(full_response)

        except Exception as e:
            full_response = f"❌ Error: {e}"
            response_placeholder.markdown(full_response)

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response
    })
