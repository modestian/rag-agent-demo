from langchain_classic.chains.question_answering.map_reduce_prompt import messages
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import convert_to_messages

# 得到模型对象，qwen3-max是聊天模型
model = ChatTongyi(model = "qwen3-max")

# 准备消息列表：改为元组格式

# 支持变量注入
messages = [
    ("system", "你是一个唐代边塞诗人"),
    ("human", "写一首五言唐诗"),
    ("ai", "锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦？"),
    ("human", "请继续")
]


messages = convert_to_messages(messages)
res = model.stream(messages)

# for循环迭代打印输出，通过.content来获取内容
for chunk in res:
    print(chunk.content, end="", flush=True)