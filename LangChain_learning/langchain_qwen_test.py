# langchain_community
from langchain_community.llms.tongyi import Tongyi

# 不用qwen3-max，因为qwen3-max是聊天模型，qwen-max是LLM
model = Tongyi(model = "qwen-max")

# # 调用invoke向模型提问
# res = model.invoke("请写一个关于机器学习的段落")
# print(res)

res = model.stream("请写一个关于机器学习的段落")
for chunk in res:
    print(chunk, end="", flush=True)