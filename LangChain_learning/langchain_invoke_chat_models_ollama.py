from langchain_ollama import ChatOllama
from langchain_core.messages import  HumanMessage, AIMessage, SystemMessage

model = ChatOllama(model = "deepseek-r1:7b",temperature=0.3)

# 准备消息列表
messages = [
    SystemMessage(content="你是一个唐代诗人"),
    HumanMessage(content="写一首五言唐诗"),
    AIMessage(content="锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦？"),
    HumanMessage(content="请按照上述格式再写一首唐诗")
]

# 调用stream流式输出
res = model.stream(messages)

# for循环迭代打印输出，通过.content来获取内容
for chunk in res:
    print(chunk.content, end="", flush=True)