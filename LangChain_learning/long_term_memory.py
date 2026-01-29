import os,json
from typing import Sequence

from langchain_community.chat_models import ChatTongyi
# messgae_to_dict单个消息对象转换字典 , messages_from_dict [字典,字典...] -> [消息,消息...]
from langchain_core.messages import message_to_dict, messages_from_dict, BaseMessage
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory


class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id: str, storage_path: str):
        self.session_id = session_id # 会话id
        self.storage_path = storage_path # 不同会话id的存储文件所在的路径

        # 完整的文件路径
        self.file_path = os.path.join(self.storage_path, self.session_id)

        # 确保文件夹存在
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        # Seq序列 类似list和tuple
        all_messages = list(self.messages) # 已有的消息列表
        all_messages.extend(messages) # 新的和已有的合成一个列表

        # 将数据同步到本地文件中

        # 类对象写入文件 -> 二进制

        # 将BaseMessage对象转换成字典，借助json模块以json字符串写入
        # new_messages = []
        # for message in all_messages:
        #     d = message_to_dict(message)
        #     new_messages.append(d)

        new_messages = [message_to_dict(message) for message in all_messages]

        # 数据写入
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(new_messages,f)

    @property # 装饰器将方法变成属性
    def messages(self) -> list[BaseMessage]:
        try:
            # 目前文件内全是list[字典]
            with open(self.file_path, "r", encoding="utf-8") as f:
                messages_data = json.load(f)
                return messages_from_dict(messages_data)
        except FileNotFoundError:
            return []


    def clear(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)



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
    return FileChatMessageHistory(session_id, "./chat_history")

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
    # res = conversation_chain.invoke({"input": "小明有2只猫"},session_config)
    # print("第一次执行:",res)
    #
    # res = conversation_chain.invoke({"input": "小刚有6只狗"}, session_config)
    # print("第二次执行:", res)

    res = conversation_chain.invoke({"input": "总共几个宠物？总共有几只鸡？"}, session_config)
    print("第三次执行:", res)
