from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = TextLoader("./data/Python基础语法.txt",encoding="utf-8")

docs = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, # 分块大小
    chunk_overlap=50, # 分块重叠
    length_function=len,
    separators=["\n\n", "\n", " ", "", "。", "？", "！", "，", "；", "："]
)

split_docs = splitter.split_documents(docs)

print(split_docs)
print(len(split_docs))

for doc in split_docs:
    print("="*5)
    print(doc)
    print("=" * 5)