from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_community.llms.tongyi import Tongyi

example_template = PromptTemplate.from_template("单词:{word},反义词:{antonym}")

example_data = [
    {"word": "好", "antonym": "坏"},
    {"word": "大", "antonym": "小"},
    {"word": "高", "antonym": "低"},
    {"word": "强", "antonym": "弱"},
    {"word": "上", "antonym": "下"},
    {"word": "早", "antonym": "晚"}
]

few_shot_prompt = FewShotPromptTemplate(
    example_prompt=example_template,
    examples=example_data,
    prefix="请给出一个单词和它的反义词，有如下示例:",
    suffix="单词:{input},请告诉我它的反义词",
    input_variables=['input']
)

# 获得最终提示词
prompt_text = few_shot_prompt.invoke({"input": "左"}).to_string()

# 调用大模型
model = Tongyi(model = "qwen-max")
print(model.invoke(prompt_text))