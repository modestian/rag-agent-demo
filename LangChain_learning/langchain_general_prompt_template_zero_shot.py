from langchain_core.prompts import PromptTemplate
from langchain_community.llms.tongyi import Tongyi

# 这里如果用字符串也可以，但是后续无法加入到Runnable中，所以建议用PromptTemplate(是链式)
prompt_template = PromptTemplate.from_template(
    "我的邻居姓{lastname}，刚生了一个{gender}，帮我起一个名字，简单回答"
)

# # 调用.format方法注入信息
# prompt_text = prompt_template.format(lastname="王", gender="女儿")
#
# model = Tongyi(model = "qwen-max")
# model.stream(prompt_text)
# for chunk in model.stream(prompt_text):
#     print(chunk, end="", flush=True)

# 构建执行链条
model = Tongyi(model = "qwen-max")
chain = prompt_template | model
res = chain.invoke({"lastname": "王", "gender": "女儿"}) # 需要传入字典
print(res)