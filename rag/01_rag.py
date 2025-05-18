import os
from typing import List
from langchain.docstore.document import Document
from langchain_community.document_loaders import (
    PyPDFLoader, 
    TextLoader, 
    Docx2txtLoader, 
    UnstructuredPowerPointLoader, 
    CSVLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain.chains import RetrievalQA
import warnings

# 忽略PDF解析警告
warnings.filterwarnings("ignore", message="Ignoring wrong pointing object")

class DocumentProcessor:
    """文档处理工具类"""
    
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
        """根据文件扩展名加载文档"""
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
        """从目录加载所有支持的文档"""
        all_docs = []
        supported_exts = set(cls.SUPPORTED_EXTS.keys())
        
        for root, _, files in os.walk(directory):
            for file in files:
                if any(file.lower().endswith(ext) for ext in supported_exts):
                    file_path = os.path.join(root, file)
                    try:
                        print(f"正在加载: {file_path}")
                        docs = cls.load_document(file_path)
                        all_docs.extend(docs)
                        print(f"✅ 成功加载 {len(docs)} 页内容")
                    except Exception as e:
                        print(f"❌ 加载失败: {str(e)}")
        
        return all_docs

class RAGEngine:
    """检索增强生成引擎"""
    
    def __init__(self, embedding_model="nomic-embed-text", llm_model="deepseek-r1:7b"):
        self.embedding_model = embedding_model
        self.llm_model = llm_model
        self.vectorstore = None
        
    def process_documents(self, documents: List[Document]):
        """处理文档并创建向量存储"""
        if not documents:
            raise ValueError("没有可处理的文档")
            
        print("\n正在分割文档...")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        texts = text_splitter.split_documents(documents)
        
        print(f"共生成 {len(texts)} 个文本块，正在创建向量存储...")
        embeddings = OllamaEmbeddings(
            # base_url="http://localhost:11434", # windows要加这个选项，mac不加
            model=self.embedding_model)
        self.vectorstore = Chroma.from_documents(texts, embeddings)
        
        print("✅ 向量存储创建完成")
        
    def create_qa_chain(self):
        """创建问答链"""
        if self.vectorstore is None:
            raise RuntimeError("向量存储未初始化")
            
        llm = OllamaLLM(
            # base_url="http://localhost:11434", # windows要加这个选项，mac不加
            model=self.llm_model)
        return RetrievalQA.from_chain_type( # 使用旧接口
            llm,
            retriever=self.vectorstore.as_retriever(),
            chain_type="stuff"
        )

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
    processor = DocumentProcessor()
    try:
        if os.path.isfile(path):
            print(f"正在加载单个文档: {path}")
            documents = processor.load_document(path)
        else:
            print(f"正在加载目录下的所有文档: {path}")
            documents = processor.load_documents_from_dir(path)
            
        if not documents:
            print("❌ 未找到任何支持的文档")
            return
            
        print(f"\n总共加载了 {len(documents)} 页内容")
        
    except Exception as e:
        print(f"❌ 文档加载失败: {str(e)}")
        return
    
    # 初始化RAG引擎
    engine = RAGEngine()
    
    try:
        engine.process_documents(documents)
        qa_chain = engine.create_qa_chain()
    except Exception as e:
        print(f"❌ 系统初始化失败: {str(e)}")
        return
    
    # 交互式问答
    print("\n===== 开始交互式问答 =====")
    print("输入问题进行查询，输入 'q' 退出")
    
    try:
        while True:
            query = input("\n问题: ").strip()
            if query.lower() == 'q':
                break
                
            if not query:
                continue
                
            try:
                result = qa_chain.invoke({"query": query})
                print("\n回答:")
                print(result['result'])
                if result.get("source_documents"):
                    print("\n📚 参考文档:")
                    for i, doc in enumerate(result["source_documents"], 1):
                        print(f"{i}. {os.path.basename(doc.metadata.get('source', '未知文档'))}")

            except Exception as e:
                print(f"❌ 查询失败: {str(e)}")
    except KeyboardInterrupt:
        pass
    finally:
        print("\n感谢使用文档智能问答系统！")

if __name__ == "__main__":
    main()
