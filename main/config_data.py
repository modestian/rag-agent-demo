# md5
md5_path = './md5.txt'

# Chroma
collection_name = "rags"
persist_directory = "./chroma_db"

# spliter
chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n", "\n", " ", "","!", "?",",", ".","，", "。","！","？"]
max_split_char_number = 1000

# vector_similarity_search
similarity_threshold = 2

# model_name
embedding_model = "text-embedding-v4"
chat_model = "qwen3-max"

# 提示词模版
system_prompt = "以我提供的参考资料为主，简洁专业地回答用户的问题，参考资料:{context}。"