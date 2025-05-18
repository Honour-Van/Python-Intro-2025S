import os
import warnings
from typing import List

from langchain.docstore.document import Document
from langchain_community.document_loaders import (
    PyPDFLoader, TextLoader, Docx2txtLoader, 
    UnstructuredPowerPointLoader, CSVLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import RegexParser
from langchain.schema.runnable import RunnableLambda


# 忽略警告
warnings.filterwarnings("ignore", message="Ignoring wrong pointing object")
# warnings.filterwarnings("ignore", category=DeprecationWarning, module="langchain")

class DocumentProcessor:
    SUPPORTED_EXTS = {
        '.pdf': PyPDFLoader,
        '.txt': lambda p: TextLoader(p, encoding='utf-8'),
        '.docx': Docx2txtLoader,
        '.doc': Docx2txtLoader,
        '.pptx': UnstructuredPowerPointLoader,
        '.csv': CSVLoader
    }

    @classmethod
    def load_document(cls, file_path: str) -> List[Document]:
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in cls.SUPPORTED_EXTS:
            raise ValueError(f"不支持的文件格式: {ext}")
        try:
            loader = cls.SUPPORTED_EXTS[ext](file_path)
            return loader.load()
        except Exception as e:
            raise RuntimeError(f"加载文件失败: {file_path}") from e

    @classmethod
    def load_documents_from_dir(cls, directory: str) -> List[Document]:
        all_docs = []
        for root, _, files in os.walk(directory):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in cls.SUPPORTED_EXTS:
                    file_path = os.path.join(root, file)
                    try:
                        print(f"正在加载: {file_path}")
                        docs = cls.load_document(file_path)
                        all_docs.extend(docs)
                        print(f"✅ 成功加载 {len(docs)} 页")
                    except Exception as e:
                        print(f"❌ 加载失败: {e}")
        return all_docs


class RAGEngine:
    DEFAULT_PROMPT = """
你是一个智能助手，擅长回答各种问题。
你需要依据以下提供的上下文信息回答用户的问题。
如果上下文信息不足，返回“未找到参考文档”。

上下文信息:
{context}

用户问题:
{input}

回答:
"""

    FALLBACK_PROMPT = """
你是一个智能助手，擅长回答各种问题。
目前没有找到与用户问题相关的具体信息，请基于你的知识进行回答。

用户问题:
{question}

回答:
"""

    def __init__(self, embedding_model="nomic-embed-text", llm_model="deepseek-r1:7b"):
        self.embedding_model = embedding_model
        self.llm_model = llm_model
        self.vectorstore = None
        self.qa_chain = None
        self.fallback_chain = None
        self.parser = None

    def process_documents(self, documents: List[Document]):
        if not documents:
            raise ValueError("文档为空，无法处理")

        print("\n📖 正在分割文档...")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        texts = text_splitter.split_documents(documents)

        print(f"🔢 共生成 {len(texts)} 个文本块，开始构建向量索引...")
        embeddings = OllamaEmbeddings(
            # base_url="http://localhost:11434", # windows要加这个选项，mac不加
            model=self.embedding_model)
        self.vectorstore = Chroma.from_documents(texts, embeddings)
        print("✅ 向量存储创建完成")

    def init_output_parser(self):
        # 定义正则表达式解析器，提取冒号后的内容
        # 为什么不对？pattern = r"<think>(.*?)</think>\s*(.*)" # 默认不开DOTALL
        deepseek_pattern = r"<think>([\s\S]*?)</think>\s*([\s\S]*)"
        output_keys = ["thought", "answer"]

        self.parser = RegexParser(
            regex=deepseek_pattern,
            output_keys=output_keys,
            default_output_key="answer",
        )


    def create_qa_chain(self):
        if self.vectorstore is None:
            raise RuntimeError("请先调用 process_documents 初始化向量存储")

        llm = OllamaLLM(
            # base_url="http://localhost:11434", # windows要加这个选项，mac不加
            model=self.llm_model)

        retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": 3}
        )

        # 新版Prompt + LLM检索链
        primary_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", self.DEFAULT_PROMPT),
                    ("human", "{input}"),
                ]
            )
        document_chain = create_stuff_documents_chain(llm, primary_prompt)
        self.qa_chain = create_retrieval_chain(retriever, document_chain).pick("answer") | self.parser

        fallback_prompt = PromptTemplate(
            template=self.FALLBACK_PROMPT,
            input_variables=["question"]
        )
        self.fallback_chain = fallback_prompt | llm

    def ask(self, question: str) -> str:
        if self.qa_chain is None or self.fallback_chain is None:
            raise RuntimeError("请先调用 create_qa_chain() 初始化问答链")

        try:
            result = self.qa_chain.invoke({"input": question})
            # print(result) # 不知道调用输入输出结构，就打印，像做题一样
            answer = result['answer']
            if not answer.strip():
                raise ValueError("答案为空")
            if result.get("context"):
                print("\n📚 参考文档:")
                for i, doc in enumerate(result["context"]):
                    print(f"{i}. {os.path.basename(doc.metadata.get('source', '未知文档'))}")

            if "未找到参考文档" in answer:
                raise ValueError("未找到参考文档，调用fallback链")
            return answer
        except Exception as e:
            print(f"⚠️ 检索失败或无结果，使用 fallback: {e}")
            # return self.fallback_chain.invoke({"question": question})

def main():
    """主函数"""
    print("\n===== 文档智能问答系统 =====")
    
    # 获取文档路径
    while True:
        path = input("\n请输入文档路径或目录 (例如: ./docs): ").strip()
        if not path:
            print("路径不能为空，请重新输入")
            continue
            
        if os.path.isfile(path) or os.path.isdir(path):
            break
        else:
            print("路径不存在，请重新输入")
    
    # 加载文档
    docs = DocumentProcessor.load_documents_from_dir(path)
    
    # 初始化RAG引擎
    engine = RAGEngine()
    
    try:
        if docs:  # 只有当有文档时才处理
            engine.process_documents(docs)
        engine.init_output_parser()
        engine.create_qa_chain()
    except Exception as e:
        print(f"❌ 系统初始化失败: {str(e)}")
        return
    
    # 交互式问答
    print("\n===== 开始交互式问答 =====")
    print("输入问题进行查询，输入 'q' 退出")
    
    try:
        while True:
            query = input("\n❓ 请输入问题（或输入 'exit' 退出）：\n> ").strip()
            if query.strip().lower() == "exit":
                break
            if not query:
                continue
                
            try:
                answer = engine.ask(query)
                print(answer)
            except Exception as e:
                print(f"❌ 查询失败: {str(e)}")
    except KeyboardInterrupt:
        print("")
    finally:
        print("\n感谢使用文档智能问答系统！")


if __name__ == "__main__":
    main()
