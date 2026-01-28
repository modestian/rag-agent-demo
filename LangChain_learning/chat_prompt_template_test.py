from langchain_community.chat_models import ChatTongyi
from langchain_community.llms.tongyi import Tongyi
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

prompt_value = chat_prompt_template.invoke({"input": "请继续", "history": history_data})

model = ChatTongyi(model = "qwen-max")
res = model.invoke(prompt_value)
print(res.content, type(res))
