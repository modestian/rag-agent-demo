from langchain_core.messages import AIMessage
from langchain_core.output_parsers import  StrOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate

parser = StrOutputParser()
model = ChatTongyi(model = "qwen3-max")
prompt = PromptTemplate.from_template("我的邻居姓{lastname}，刚生了一个{gender}，帮我起一个名字，简单回答")

chain = prompt | model | parser | model | parser
res= chain.invoke({"lastname": "张", "gender": "女儿"})
print(res)