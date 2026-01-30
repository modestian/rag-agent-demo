import time
from rag import RagService
import streamlit as st
import config_data as config

# title
st.title("穿衣助手")
st.divider()

# rag service
if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

# message
if "message" not in st.session_state:
    st.session_state["message"] = [{"role": "assistant", "content": "欢迎来到穿衣助手，请输入你的问题"}]

# load the page
for message in st.session_state["message"]:
        st.chat_message(message["role"]).write(message["content"])

# prompt input
prompt = st.chat_input("请输入你的问题")
if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})

    ai_res_list = []
    with st.spinner("正在全力准备您的回答..."):
        res_stream = st.session_state["rag"].chain.stream({"input": prompt}, config.session_config)
        # yield
        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                yield chunk

        st.chat_message("assistant").write_stream(capture(res_stream, ai_res_list))
        st.session_state["message"].append({"role": "assistant", "content": "".join(ai_res_list)})
