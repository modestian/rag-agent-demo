from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models import ChatTongyi
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda
from vector_stores import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config
from file_history_store import get_history

def print_prompt(prompt):
    print(prompt.to_string())
    return prompt

class RagService(object):
    def __init__(self):

        self.vector_store_service = VectorStoreService(
            embedding=DashScopeEmbeddings(model=config.embedding_model)
        )

        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", config.system_prompt),
                ("system","我提供的用户对话记录为:"),
                MessagesPlaceholder("history"),
                ("human", "{input}")
            ]
        )

        self.chat_model = ChatTongyi(model=config.chat_model)

        self.chain = self.__getchain()

    def __getchain(self):
        """获取最终的执行链"""
        retriever = self.vector_store_service.get_retriever()

        def format_document(documents: list[Document]):
            if not documents:
                return "无相关参考资料"

            formatted_str = ""
            for doc in documents:
                formatted_str += f"文档片段:{doc.page_content}\n文档元数据:{doc.metadata}"
            return formatted_str

        def formate_to_retriever(value: dict) -> str:
            return value["input"]

        def format_to_prompt_template(value):
            new_value = {}
            new_value["input"] = value["input"]["input"]
            new_value["context"] = value["context"]
            new_value["history"] = value["input"]["history"]
            return new_value

        chain = (
            {
                "input":RunnablePassthrough(),
                "context": RunnableLambda(formate_to_retriever) | retriever | format_document
            } | RunnableLambda(format_to_prompt_template) | self.prompt_template | self.chat_model | StrOutputParser()
        )

        conversation_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history"
        )
        return conversation_chain

if __name__ == "__main__":
    session_config = {
        "configurable":{
            "session_id": "user_20260130_1121"
        }
    }

    rag_service = RagService()
    res = rag_service.chain.invoke({"input":"刚刚我询问的是哪两个体重？"},session_config)
    print(res)