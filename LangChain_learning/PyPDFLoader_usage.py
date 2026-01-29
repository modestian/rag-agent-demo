from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader( # 读取文档型PDF
    file_path="./data/学习.pdf",
    mode = "page" # 默认是page模式，每个页面形成一个Document对象
    # mode = "single" # single模式，不管多少页只返回一个Document对象
    # password = "{your_password}" 输入密码
)

i = 0
for doc in loader.lazy_load():
    i += 1
    print(doc)
    print("="*5 , i)