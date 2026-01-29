from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(
    file_path="./data/stu_info_exmp.csv",
    csv_args={
        "delimiter": ",", # 指定分隔符
        "quotechar": '"', # 指定引号
        "fieldnames": ["name", "age", "gender"] # 指定列名（无列名时）
    },
    encoding = "utf-8"
)

# 批量加载 .loader -> [Document, Document, ...]
# documents = loader.load()
#
# print(documents)
#
# for doc in documents:
#     print(doc.page_content)

for document in loader.lazy_load():
    print(document.page_content)