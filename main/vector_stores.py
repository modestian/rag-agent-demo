"""
向量存储服务
"""
from langchain_chroma import Chroma
from ollama import embeddings

import config_data as config
from langchain_community.embeddings import DashScopeEmbeddings

class VectorStoreService:
    def __init__(self,embedding):
        self.embedding = embedding
        self.vector_store = Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embedding,
            persist_directory=config.persist_directory,
        )

    def get_retriever(self):
        """
        获取向量检索结果
        """
        return self.vector_store.as_retriever(search_kwargs={"k": config.similarity_threshold})


if __name__ == "__main__":
    vector_store = VectorStoreService(DashScopeEmbeddings(model="text-embedding-v4"))
    retriever = vector_store.get_retriever()

    res = retriever.invoke("我体重180斤，怎么穿衣服")
    print(res)