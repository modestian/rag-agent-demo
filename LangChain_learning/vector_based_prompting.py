"""
提示词：用户的提问 + 向量库中检索到的参考资料
"""
from langchain_community.chat_models import ChatTongyi
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

# 检索向量库
result = vector_store.similarity_search(input_text, k=2)
reference = "["
for document in result:
    reference += document.page_content
reference += "]"

def print_prompt(prompt):
    print(prompt.to_string())
    return prompt

# chain
chain = prompt | print_prompt | model | StrOutputParser()

res = chain.invoke({"input": input_text, "context": reference})
print(res)
