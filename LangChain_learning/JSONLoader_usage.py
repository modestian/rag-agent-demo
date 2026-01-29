from langchain_community.document_loaders import JSONLoader

# loader = JSONLoader(
#     file_path="./data/stu_info.json",
#     jq_schema=".",
#     text_content=False
# )

# loader = JSONLoader(
#     file_path="./data/stus_info.json",
#     jq_schema=".[]",
#     text_content=False
# )

loader = JSONLoader(
    file_path="./data/stus_info_lines.json",
    jq_schema=".name",
    text_content=False,
    json_lines=True
)

document = loader.load()
print( document)