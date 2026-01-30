"""
基于Streamlit完成Web网页上传服务

streamlit当Web页面元素发生变化，则代码重新执行一遍
"""
import time
import streamlit as st

from knowledge_base import KnowledgeBaseService

# 添加网页标题
st.title("知识库更新服务")

# 添加文件上传组件
uploaded_file = st.file_uploader(
    "请上传.txt格式的文件",
    type = ['txt'],
    accept_multiple_files = False
)

if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()

if uploaded_file:
    # 提取文件信息
    file_name = uploaded_file.name
    file_type = uploaded_file.type
    file_size = uploaded_file.size / 1024 # KB

    st.subheader(f"文件名：{file_name}")
    st.write(f"文件类型：{file_type} | 文件大小：{file_size:.2f}KB")

    # 获取文件内容
    file_text = uploaded_file.getvalue().decode("utf-8")

    with st.spinner("上传中..."):
        time.sleep(1)
        # 上传文件
        result = st.session_state["service"].upload_by_str(file_text, file_name)
        st.write(result)