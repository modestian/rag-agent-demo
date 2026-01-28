from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder

chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你一个唐诗作者"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ]
)

history_data = [
    ("human", "写一首唐诗"),
    ("ai","床前明月光，疑是地上霜。举头望明月，低头思故乡。"),
    ("human", "请继续"),
    ("ai", "锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦？")
]

model = ChatTongyi(model = "qwen-max")

# 组成链
chain = chat_prompt_template | model

# 通过链调用invoke或者stream
# invoke
# res = chain.invoke({"input": "请继续", "history": history_data})
# print(res.content, type(res))
# stream
for chunk in chain.stream({"input": "请继续", "history": history_data}):
    print(chunk.content, end="", flush=True)
