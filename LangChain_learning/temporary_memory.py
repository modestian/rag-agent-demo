from langchain_core.output_parsers import  StrOutputParser
from langchain_core.output_parsers import  JsonOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

model = ChatTongyi(model = "qwen-max")
# prompt = PromptTemplate.from_template(
#     "你需要根据会话历史记忆回应用户问题，对话历史为：{chat_history}，用户提问为：{input}，请回答"
# )
chat_prompt_template = ChatPromptTemplate.from_messages([
    ("system", "你需要根据会话历史记忆回应用户问题"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

str_parser = StrOutputParser()

base_chain = chat_prompt_template | model | str_parser

# 通过会话ID获取InMemoryChatMessageHistory类的对象
history_dict = {}
def get_history(session_id: str):
    if session_id not in history_dict:
        history_dict[session_id] = InMemoryChatMessageHistory()

    return history_dict[session_id]

# 创建一个新链增强原有链功能，添加历史消息
conversation_chain = RunnableWithMessageHistory(
    base_chain,# 被增强的基础链
    get_history,# 通过会话ID获取InMemoryChatMessageHistory类的对象
    input_messages_key="input",# 输入消息的key
    history_messages_key="chat_history",# 历史消息的key
)

if __name__ == "__main__":
    session_config = {
        "configurable":{
            "session_id": "user_zhang01"
        }
    }
    res = conversation_chain.invoke({"input": "小明有2只猫"},session_config)
    print("第一次执行:",res)

    res = conversation_chain.invoke({"input": "小刚有6只狗"}, session_config)
    print("第二次执行:", res)

    res = conversation_chain.invoke({"input": "总共几个宠物？总共有几只鸡？"}, session_config)
    print("第三次执行:", res)