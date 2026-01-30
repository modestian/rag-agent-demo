import json
import os
from typing import Sequence

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict


def get_history(session_id: str):
    return FileChatMessageHistory(session_id, "./chat_history")

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