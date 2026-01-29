from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader
from langchain_chroma import Chroma

# 用Chroma 向量数据库
# 安装langchain-chroma chromadb

vector_store = Chroma(
    collection_name="test_2026_0129",
    embedding_function=DashScopeEmbeddings(),
    persist_directory="./data/chroma_db"

)

loader = CSVLoader(
    file_path="./data/stu_info_exmp.csv",
    encoding = "utf-8",
    source_column = "name"
)

documents = loader.load()

# 文档添加
vector_store.add_documents(
    documents=documents,    # 被添加的文档，类型是list[Document]
    ids=["id" + str(i) for i in range(1, len(documents)+1)]
)

# 删除
vector_store.delete("id5")

# 检索
result = vector_store.similarity_search(
    "蔡柿听",
    k=3, # 检索结果个数
    filter={"gender":"男"}
)

print(result)