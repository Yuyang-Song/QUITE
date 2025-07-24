from haystack import Pipeline, Document
from haystack.utils import Secret
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever, InMemoryEmbeddingRetriever
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.components.embedders import SentenceTransformersTextEmbedder, SentenceTransformersDocumentEmbedder
from datetime import datetime
import os
import json
import hashlib
from pathlib import Path
import pickle
import time
import textwrap
from typing import List, Dict
from dotenv import load_dotenv

PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT", Path(__file__).resolve().parents[3]))
LOAD_PATH = PROJECT_ROOT / "config_file" / ".env"
load_dotenv(dotenv_path= LOAD_PATH)

class Structured_Knowledge_Base:
    def __init__(self, folder_path, json_file_path, document_store_path=None):
        self.open_api_key = Secret.from_token(os.getenv("ASSISTANT_MODEL_API_KEY"))  # Get the API key from the environment variable
        self.model = os.getenv("ASSISTANT_MODEL")
        self.api_base_url = os.getenv("ASSISTANT_MODEL_URL")
        self.folder_path = folder_path
        self.json_file_path = json_file_path

        # 设置document_store缓存路径
        if document_store_path is None:
            base_dir = os.path.dirname(json_file_path)
            base_name = os.path.basename(json_file_path).split('.')[0]
            self.document_store_path = os.path.join(base_dir, f"{base_name}_document_store.pkl")
        else:
            self.document_store_path = document_store_path
        
        # 尝试从缓存加载document_store
        if not self.load_document_store_from_cache():
            print("Building new document store...")
            # 如果缓存加载失败，执行原始的加载和索引构建流程
            self.document_store = InMemoryDocumentStore()
            documents = self.load_documents_from_file()
            self.document_store.write_documents(documents)
            # 保存构建好的document_store到缓存
            self.save_document_store_to_cache()

    def _compute_json_file_hash(self):
        """计算JSON文件的哈希值，用于检测文件是否被修改"""
        if not os.path.exists(self.json_file_path):
            return None
            
        try:
            with open(self.json_file_path, 'rb') as f:
                file_content = f.read()
            return hashlib.md5(file_content).hexdigest()
        except Exception as e:
            print(f"Error computing JSON file hash: {e}")
            return None
    
    def save_document_store_to_cache(self):
        """将document_store保存到缓存文件"""
        try:
            # 创建一个包含文档内容哈希值的元数据
            json_hash = self._compute_json_file_hash()
            cache_data = {
                "document_store": self.document_store,
                "metadata": {
                    "json_hash": json_hash,
                    "created_at": datetime.now().isoformat(),
                    "document_count": len(self.document_store.filter_documents())
                }
            }
            
            # 保存到文件
            with open(self.document_store_path, 'wb') as f:
                pickle.dump(cache_data, f)
                
            print(f"Saved document store to {self.document_store_path}")
            print(f"Document count: {len(self.document_store.filter_documents())}")
            return True
        except Exception as e:
            print(f"Error saving document store: {e}")
            return False
    
    def load_document_store_from_cache(self):
        """从缓存文件加载document_store"""
        if not os.path.exists(self.document_store_path):
            print(f"Document store cache file not found: {self.document_store_path}")
            return False
            
        try:
            # 加载缓存数据
            with open(self.document_store_path, 'rb') as f:
                cache_data = pickle.load(f)
            
            document_store = cache_data["document_store"]
            metadata = cache_data["metadata"]
            
            # 验证JSON文件哈希值是否匹配
            current_json_hash = self._compute_json_file_hash()
            if current_json_hash != metadata["json_hash"]:
                print("JSON file has changed since document store was cached. Rebuilding store.")
                return False
                
            # 设置文档存储
            self.document_store = document_store
            
            print(f"Loaded document store from cache with {metadata['document_count']} documents.")
            print(f"Cache created at: {metadata['created_at']}")
            return True
            
        except Exception as e:
            print(f"Error loading document store from cache: {e}")
            return False
            
    def refresh_document_store(self):
        """强制重新构建document_store"""
        print("Refreshing document store...")
        self.document_store = InMemoryDocumentStore()
        documents = self.load_documents_from_file()
        self.document_store.write_documents(documents)
        self.save_document_store_to_cache()
        print("Document store refreshed")

    # 将文档保存到本地 JSON 文件
    def save_documents_to_file(self, documents):
        documents_data = [{"id": doc.id, "content": doc.content} for doc in documents]
        with open(self.json_file_path, 'w', encoding='utf-8') as file:
            json.dump(documents_data, file, ensure_ascii=False, indent=4)
            
    # 从本地 JSON 文件加载文档
    def load_documents_from_file(self):
        print("Loading documents from file...")
        documents = []
        if os.path.exists(self.json_file_path):
            with open(self.json_file_path, 'r', encoding='utf-8') as file:
                documents_data = json.load(file)
                for doc_data in documents_data:
                    documents.append(Document(id=doc_data["id"], content=doc_data["content"]))

        return documents

    # 读取文件夹中的所有 json 文件
    def read_json_files_from_folder(self):
        start_time = time.time()
        documents = []
        existing_ids = set()

        if not os.path.exists(self.folder_path):
            print(f"Error: The folder '{self.folder_path}' does not exist.")
            return []

        for filename in os.listdir(self.folder_path):
            if filename.endswith(".json"):
                file_path = os.path.join(self.folder_path, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)

                    # 若为数组，则逐个处理
                    if isinstance(data, list):
                        for item in data:
                            if 'id' not in item or not item['id']:
                                generated_id = hashlib.sha256(json.dumps(item, ensure_ascii=False).encode('utf-8')).hexdigest()
                                item['id'] = generated_id
                            item_id = item['id']

                            # 将该对象保存为独立 Document
                            doc_json_str = json.dumps(item, ensure_ascii=False)
                            doc_hash_id = hashlib.sha256(doc_json_str.encode('utf-8')).hexdigest()
                            if doc_hash_id not in existing_ids:
                                documents.append(Document(content=doc_json_str, id=item_id))
                                existing_ids.add(doc_hash_id)
                    # 若为单个对象
                    elif isinstance(data, dict):
                        if 'id' not in data or not data['id']:
                            generated_id = hashlib.sha256(json.dumps(data, ensure_ascii=False).encode('utf-8')).hexdigest()
                            data['id'] = generated_id
                        item_id = data['id']

                        doc_json_str = json.dumps(data, ensure_ascii=False)
                        doc_hash_id = hashlib.sha256(doc_json_str.encode('utf-8')).hexdigest()
                        if doc_hash_id not in existing_ids:
                            documents.append(Document(content=doc_json_str, id=item_id))
                            existing_ids.add(doc_hash_id)

                    # 将处理过的文件重新写回，确保都有 id
                    with open(file_path, 'w', encoding='utf-8') as file:
                        json.dump(data, file, ensure_ascii=False, indent=4)

                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")

        end_time = time.time()
        print(f"Read {len(documents)} documents in {(end_time - start_time):.2f} seconds.")
        return documents

    def format_suggestion(self, suggestion) -> List[Dict[str, str]]:
        """
        格式化 suggestion 字段，将其解析为结构化 JSON 格式并去除不需要的符号。
        :param suggestion: 需要格式化的原始 suggestion（可能是字符串、列表或其他类型）
        :return: 格式化后的 suggestion 字段（作为 JSON 对象列表）
        """
        import re
        
        try:
            # 处理空值
            if not suggestion:
                return [{"suggestion": "No suggestion available"}]
            
            # 统一转换为字符串
            if isinstance(suggestion, list):
                text = ''.join(str(item) for item in suggestion)
            else:
                text = str(suggestion)
            
            if not text.strip():
                return [{"suggestion": "No suggestion content"}]
            
            # 提取JSON内容 - 使用正则表达式简化
            text = text.strip()
            
            # 尝试提取```json...```或```...```包围的内容
            json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', text, re.DOTALL)
            if json_match:
                json_content = json_match.group(1).strip()
            else:
                # 尝试提取从第一个{或[开始的JSON
                brace_match = re.search(r'[{\[].*[}\]]', text, re.DOTALL)
                if brace_match:
                    json_content = brace_match.group(0)
                else:
                    json_content = text
            
            # 尝试解析JSON
            try:
                parsed = json.loads(json_content)
                if isinstance(parsed, list):
                    return parsed
                elif isinstance(parsed, dict):
                    return [parsed]
                else:
                    return [{"suggestion": str(parsed)}]
            except json.JSONDecodeError:
                # JSON解析失败，尝试提取suggestion字段
                suggestions = re.findall(r'"suggestion"\s*:\s*"([^"]*)"', json_content)
                if suggestions:
                    return [{"suggestion": s} for s in suggestions]
                
                # 最后备选：返回清理后的文本
                return [{"suggestion": json_content}]
                
        except Exception as e:
            print(f"Error in format_suggestion: {e}")
            return [{"suggestion": str(suggestion)}]


    def retrieval(self,input_sql, suggestion_tuple):
        # 建立RAG pipeline
        question = textwrap.dedent(f"""
        find the potential rewrite strageties for the sql query: {input_sql} and its suggestions are: {suggestion_tuple["origin_suggestion"]}.
        Please notice that the suggestion group reffered to the rewritten strataegie classification: {suggestion_tuple["group"]}.
        """)

        prompt_template = textwrap.dedent("""
        You are an experienced DBA and specialized in Query rewrite process of query optimization. 
        You have been given a SQL query to optimize from Question part.
        Note that you shouldn't have to directly rewrite the original sql, but to find and summarize the potential rewrite strageties for the sql query and its suggestion, make the strageties clear and simple.
                        
        Your work is to retrieval and summarize the documents related to its suggestion to find the rewrite optimization stratages.
        Note that you should summarize and return the most relevant and efficient stratages no more than two in the answer. Make your explain clear and simple.

                   
        # Documents:
        # {% for doc in documents %}
        #     {{ doc.content }}
        # {% endfor %}
        # Question: {{question}}

        Answer:
        You must return the answer in the following json format:
        # {
        #         "suggestion": //   
        # },
        #     ... //If more suggestions are needed, add more objects in the json array.          
        """)

        retriever = InMemoryBM25Retriever(document_store=self.document_store)
        # retriever = InMemoryEmbeddingRetriever(document_store=self.document_store)
        prompt_builder = PromptBuilder(template=prompt_template)
        llm = OpenAIGenerator(api_key = self.open_api_key, model = self.model, api_base_url = self.api_base_url)

        rag_pipeline = Pipeline()
        rag_pipeline.add_component("retriever", retriever)
        rag_pipeline.add_component("prompt_builder", prompt_builder)
        rag_pipeline.add_component("llm", llm)
        rag_pipeline.connect("retriever", "prompt_builder.documents")
        rag_pipeline.connect("prompt_builder", "llm")

        results = rag_pipeline.run(
            {
                "retriever": {"query": question},
                "prompt_builder": {"question": question},
            }
        )
        return results["llm"]["replies"]
