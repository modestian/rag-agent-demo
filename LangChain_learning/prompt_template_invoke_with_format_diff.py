from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import FewShotPromptTemplate
from langchain_core.prompts import ChatPromptTemplate

'''
PromptTemplate -> StringPromptTemplate -> BasePromptTemplate -> RunnableSerializable -> Serializable
FewShotPromptTemplate -> StringPromptTemplate -> BasePromptTemplate -> RunnableSerializable -> Serializable
ChatPromptTemplate -> BaseChatPromptTemplate -> BasePromptTemplate -> RunnableSerializable -> Serializable
'''

template = PromptTemplate.from_template("我的邻居是:{name}")

res1 = template.format(name="王")
print(res1,type(res1))

res2 = template.invoke({"name": "王"})
print(res2,type(res2))

# format输出是:我的邻居是:王 <class 'str'>
# invoke输出是:text='我的邻居是:王' <class 'langchain_core.prompt_values.StringPromptValue'>

