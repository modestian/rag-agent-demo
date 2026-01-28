# langchain_ollama
from langchain_ollama import OllamaLLM

model = OllamaLLM(model="deepseek-r1:7b")

# res = model.invoke(input="你是谁呀能做什么?")
# print(res)

res = model.stream("请写一个关于机器学习的段落")
for chunk in res:
    print(chunk, end="", flush=True)