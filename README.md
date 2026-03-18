# RAG-AI-Agent 项目技术总结

## 项目概述

**RAG-AI-Agent** 是一个基于检索增强生成（RAG）技术的智能问答系统，能够根据用户问题从知识库中检索相关信息，并结合大语言模型生成准确、专业的回答。项目支持多轮对话、流式输出，并提供友好的Web交互界面。

---

## 技术栈

### 核心框架
| 技术 | 版本/模型 | 用途 |
|------|----------|------|
| **Python** | 3.13 | 编程语言 |
| **LangChain** | - | RAG应用开发框架 |
| **Streamlit** | - | Web界面框架 |

### 向量数据库与嵌入模型
| 技术 | 版本/模型 | 用途 |
|------|----------|------|
| **Chroma DB** | - | 向量数据库，存储文档嵌入 |
| **DashScopeEmbeddings** | text-embedding-v4 | 阿里云文本嵌入模型 |

### 大语言模型
| 技术 | 版本/模型 | 用途 |
|------|----------|------|
| **ChatTongyi** | qwen3-max | 阿里云通义千问大语言模型 |

### LangChain 组件
| 组件 | 用途 |
|------|------|
| `langchain_chroma` | Chroma向量数据库集成 |
| `langchain_community` | 社区组件（ChatTongyi, DashScopeEmbeddings） |
| `langchain_core` | 核心组件（Runnable, Prompt, OutputParser） |
| `langchain_text_splitters` | 文本分割器 |

### 其他技术
| 技术 | 用途 |
|------|------|
| `hashlib` | MD5计算，实现内容去重 |
| `json` | 会话历史数据序列化 |
| `os` | 文件系统操作 |

---

## 项目架构

```
main/
├── config_data.py          # 配置文件（模型参数、提示词模板）
├── knowledge_base.py       # 知识库服务（文件上传、向量化存储）
├── vector_stores.py        # 向量存储服务（检索功能）
├── rag.py                  # RAG服务（核心问答链）
├── file_history_store.py   # 会话历史管理
├── app_file_uploader.py    # 文件上传Web界面
├── app_qa.py               # 问答Web界面
├── data/                   # 知识库数据文件
├── chroma_db/              # 向量数据库存储
└── chat_history/           # 会话历史记录
```

---

## 核心功能模块

### 1. 知识库管理 (`knowledge_base.py`)
- 支持txt文件上传
- 自动文本分割（RecursiveCharacterTextSplitter）
- 基于MD5的内容去重机制
- 元数据管理（来源、时间、操作者）

### 2. 向量检索 (`vector_stores.py`)
- Chroma向量数据库集成
- 基于相似度的文档检索
- 可配置检索参数（k值）

### 3. RAG问答 (`rag.py`)
- LangChain链式调用
- 提示词模板管理
- 多轮对话支持
- 流式输出

### 4. 会话管理 (`file_history_store.py`)
- 基于文件的会话历史存储
- 支持多用户会话隔离
- JSON格式序列化

### 5. Web界面
- **文件上传** (`app_file_uploader.py`): 知识库文件管理
- **智能问答** (`app_qa.py`): 多轮对话交互界面

---

## 项目优势特点

### 1. 模块化设计
- 清晰的组件分离，各模块职责单一
- 易于维护和扩展
- 支持独立测试和调试

### 2. 智能去重机制
- 基于MD5哈希的内容去重
- 避免重复数据存储
- 节省存储空间和计算资源

### 3. 多轮对话支持
- 会话历史持久化存储
- 支持上下文理解
- 提供连贯的对话体验

### 4. 流式输出
- 实时返回生成内容
- 提升用户体验
- 减少等待时间

### 5. 智能文本分割
- 支持中英文分隔符
- 可配置chunk大小和重叠
- 保留语义完整性

### 6. 友好的Web界面
- 基于Streamlit快速构建
- 实时状态反馈
- 简洁直观的操作流程

### 7. 高效向量检索
- Chroma向量数据库
- 基于语义相似度的检索
- 支持大规模文档处理

### 8. 可扩展性强
- 支持多种嵌入模型
- 可替换不同LLM
- 易于添加新功能模块

---

## 配置参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `chunk_size` | 1000 | 文本分割块大小 |
| `chunk_overlap` | 100 | 分割块重叠长度 |
| `similarity_threshold` | 2 | 检索返回文档数量 |
| `embedding_model` | text-embedding-v4 | 嵌入模型 |
| `chat_model` | qwen3-max | 对话模型 |

---

## 应用场景

- **穿衣搭配推荐**: 基于用户体型提供个性化建议
- **知识库问答**: 企业内部知识管理
- **智能客服**: 基于文档的自动问答
- **文档检索**: 快速定位相关信息

---

## 运行方式

### 文件上传服务
```bash
streamlit run main/app_file_uploader.py
```

### 智能问答服务
```bash
streamlit run main/app_qa.py
```

### 命令行测试
```bash
python main/rag.py
python main/vector_stores.py
```

---

## 技术亮点

1. **RAG架构**: 结合检索与生成，确保回答准确性
2. **会话管理**: 完整的多轮对话支持
3. **流式处理**: 实时响应，提升交互体验
4. **去重机制**: 高效的内容管理
5. **模块解耦**: 高内聚低耦合的设计原则

---

## 未来扩展方向

- [ ] 支持更多文档格式（PDF、Word、Markdown）
- [ ] 集成更多LLM模型
- [ ] 添加用户认证系统
- [ ] 实现知识库版本管理
- [ ] 支持多语言处理
- [ ] 添加评估指标和监控
