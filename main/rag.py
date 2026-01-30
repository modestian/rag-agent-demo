from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatTongyi
from langchain_core.runnables import RunnablePassthrough
from main.vector_stores import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config

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
                ("human", "{input}"),
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

        chain = (
            {
                "input":RunnablePassthrough(),
                "context": retriever | format_document
            } | self.prompt_template | self.chat_model | StrOutputParser()
        )

        return chain

if __name__ == "__main__":
    rag_service = RagService()
    res = rag_service.chain.invoke("我体重180斤，怎么穿衣服")
    print(res)