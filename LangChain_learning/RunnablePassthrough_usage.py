"""
提示词：用户的提问 + 向量库中检索到的参考资料
"""
from langchain_community.chat_models import ChatTongyi
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

model = ChatTongyi(model = "qwen3-max")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "以我提供的已知参考资料为主，简洁和专业地回答用户的问题，参考资料为{context}。"),
        ("human", "问题：{input}")

    ]
)

vector_store = InMemoryVectorStore(
   embedding=DashScopeEmbeddings(model="text-embedding-v4")
)

# 准备资料，即向量库
vector_store.add_texts(
    texts=[
        "减肥就是要吃得少，锻炼很多",
        "减脂期间吃东西很重要，要多吃清淡的食物，减少热量摄入，增加运动量",
        "跑步是非常适合减肥的运动"
    ]
)

input_text = "怎么减肥？"

# langchain中下那个可以用as_retriever()，可以返回Runnable接口的子类实例对象
retriever = vector_store.as_retriever(search_kwargs={"k": 2})

def format_func(docs: list[Document]):
    if not docs:
        return "无相关参考资料"

    formatted_str = "["
    for doc in docs:
        formatted_str += doc.page_content
    formatted_str += "]"

    return formatted_str


# 构建chain
# chain = retriever | prompt | model | StrOutputParser()

chain = (
    # 本身invoke中的参数会传给链起步，但是RunnablePassthrough也会分流拿到参数
    {"input":RunnablePassthrough(), "context": retriever | format_func } | prompt | model | StrOutputParser()
)

res = chain.invoke(input_text)
print(res)

"""
retrier:
输入：用户的提问 str
输出：向量库的检索结果 list[Document]
prompt
输入：用户提问 + 向量结果 dict (直接对接有问题，首先是上一个输出和此输入类型不同，其次用户提问丢失)
输出：完整输出结果 PromptValue
"""