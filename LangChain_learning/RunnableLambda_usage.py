from langchain_core.output_parsers import  StrOutputParser
from langchain_core.output_parsers import  JsonOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

str_parser = StrOutputParser()
json_parser = JsonOutputParser()

model = ChatTongyi(model = "qwen-max")

first_prompt = PromptTemplate.from_template(
    "我的邻居姓{lastname}，刚生了一个{gender}，帮我起一个名字，并封装到JSON格式返回给我:"
    "要求key是name，value就是起的名字，请严格遵守格式要求"
)

second_prompt = PromptTemplate.from_template(
    "姓名{name}，请帮我介绍下这个名字的含义，简单回答"
)

# 函数的参数变化: AIMessage -> dict
my_func = RunnableLambda(lambda ai_msg: {"name": ai_msg.content})

# 底下这个是langchain自动生成Callable实例
# chain = first_prompt | model | (lambda ai_msg: {"name": ai_msg.content}) | second_prompt | model | str_parser
chain = first_prompt | model | my_func | second_prompt | model | str_parser
for chunk in chain.stream({"lastname": "张", "gender": "女儿"}):
    print(chunk, end="", flush=True)