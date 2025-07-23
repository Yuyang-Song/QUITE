import sys
sys.path.append('../')
sys.path.append('../../')
sys.path.append('./')

import psycopg2
import concurrent.futures
import os
import hashlib
import json
import pickle
import time
import textwrap
import subprocess
import tempfile
import signal
from pathlib import Path

from dotenv import load_dotenv
from typing import List, Dict,Any, Optional,Tuple
from psycopg2.extras import RealDictCursor
from haystack import Pipeline, Document
from haystack.utils import Secret
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever, InMemoryEmbeddingRetriever
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.components.embedders import SentenceTransformersTextEmbedder, SentenceTransformersDocumentEmbedder
from datetime import datetime
from typing import List, Dict, Any

PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT", Path(__file__).resolve().parents[2]))
LOAD_PATH = PROJECT_ROOT / "config_file" / ".env"
load_dotenv(dotenv_path= LOAD_PATH)


class DBMS:
    def __init__(self,json_file_path = None):
        
        self.db_name = os.getenv("DB_NAME")
        self.db_user= os.getenv("DB_USER")
        self.db_password= os.getenv("DB_PASSWORD")
        self.db_host= os.getenv("DB_HOST")
        self.db_port= os.getenv("DB_PORT")
        self.json_file_path = json_file_path
        self.pool = None
        self.connection = None
        self.cursor = None
    
    def connect(self):
        try:
            # 创建数据库连接
            self.connection = psycopg2.connect(
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port
            )
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            # print("数据库连接成功！")
        except Exception as e:
            print(f"Failed to connect the database system!: {e}")
            raise

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            # print("数据库连接已关闭。")

    def get_pure_plan(self, sql :str):
        self.connect()
        try:
            self.cursor.execute(f"EXPLAIN {sql}")
            result = self.cursor.fetchall()
            
            self.close()
            return result
        except Exception as e:
            
            self.close()
            return str(e)

    def execute_explain(self, sql: str) -> Tuple[bool, Any]:
        """
        Executes an EXPLAIN statement and returns a tuple indicating success and the result or error.

        :param sql: SQL query to explain.
        :return: Tuple (success: bool, data: explain result or error message)
        """
        try:
            self.cursor.execute(f"EXPLAIN (FORMAT JSON) {sql}")
            result = self.cursor.fetchone()
            explain_result = result['QUERY PLAN'] if result else None

            # Check if explain_result is a string or list and parse accordingly
            if isinstance(explain_result, str):
                return True, json.loads(explain_result)
            elif isinstance(explain_result, list):
                return True, explain_result  # Return list directly
            else:
                return False, "Unexpected EXPLAIN result format."
        except Exception as e:
            error_message = str(e)
            print(f"Error executing EXPLAIN: {error_message}")
            return False, error_message
    
    def execute_ddl(self, sql: str) -> Tuple[bool, Any]:
        """执行DDL语句（CREATE/ALTER/DROP VIEW）"""
        try:
            self.connect()
            self.cursor.execute(sql)
            self.connection.commit()  # DDL需要显式提交
            return True, None
        except Exception as e:
            self.connection.rollback()
            return False, str(e)
        finally:
            self.close()

    def execute_view_queries(self, queries: List[str]) -> Dict:
        results = {}
        try:
            self.connect()
            # 自动清理残留视图
            self.connection.set_session(autocommit=False)  # 启用事务
            for i, query in enumerate(queries):
                clean_query = query.strip().lower()
                # 自动添加IF EXISTS判断
                if clean_query.startswith("create view"):
                    view_name = clean_query.split()[2]
                    self.cursor.execute(f"DROP VIEW IF EXISTS {view_name} CASCADE")
                
                self.cursor.execute(query)
                
                if "create view" in clean_query:
                    results[f'view_{i}'] = 'created'
                else:
                    self.cursor.execute(f"EXPLAIN (FORMAT JSON) {query}")
                    results[f'query_{i}'] = self.cursor.fetchall()
            
            self.connection.commit()
            return {'success': True, 'data': results}
        except Exception as e:
            self.connection.rollback()
            return {'success': False, 'error': str(e)}
        finally:
            self.close()

    def read_sql_from_json(self, json_file_path):
        """
        从 JSON 文件读取多个 SQL 查询
        :param json_file_path: JSON 文件路径
        :return: SQL 查询列表
        """
        try:
            with open(json_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return [item['query'] for item in data]
        except Exception as e:
            print(f"读取 JSON 文件时出错: {e}")
            return []

    def execute_statement(self, sql: str):
        """执行单个 SQL 语句（非 EXPLAIN）"""
        self.connect()
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            self.close()
        except Exception as e:
            self.close()
            print(f"Error executing statement: {e}")
            raise

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


# tool_1
async def DBMS_EXPLAIN_Tool(dbms: DBMS, input_sql: str) -> str:
    print("DBMS_EXPLAIN_Tool starts...")
    
    # 按分号拆分 SQL 脚本为单个语句
    statements = [stmt.strip() for stmt in input_sql.split(';') if stmt.strip()]
    
    query_plans = []
    
    try:
        # 遍历每个语句
        for stmt in statements:
            # 如果是 CREATE VIEW，先执行它
            if stmt.upper().startswith("CREATE VIEW"):
                dbms.execute_statement(stmt)
            
            # 如果是 SELECT 或其他需要 EXPLAIN 的语句，获取其执行计划
            if not stmt.upper().startswith("CREATE VIEW") and not stmt.upper().startswith("DROP VIEW"):
                result = dbms.get_pure_plan(stmt)
                if isinstance(result, list):
                    query_plans.extend([item['QUERY PLAN'] for item in result])
                else:
                    query_plans.append(f"Error: {result}")
            
            # 如果是 DROP VIEW，先执行它
            if stmt.upper().startswith("DROP VIEW"):
                dbms.execute_statement(stmt)
    
    except Exception as e:
        print(f"Error processing statements: {e}")
    
    print(query_plans)
    print("DBMS_EXPLAIN_Tool ends...")
    return query_plans


# tool_2
async def Knowledge_Base_Tool(input_sql: str, origin_suggestion_list: str) -> str:
    print("Knowledge_Pool_Tool starts...")
    # 指定文件夹路径
    folder_path = PROJECT_ROOT / "src" / "Rewrite_Middleware" / "Structured_Knowledge_Base" / "storage"
    json_file_path = PROJECT_ROOT / "src" / "Rewrite_Middleware" / "Structured_Knowledge_Base" / "documents.json"
    document_path = PROJECT_ROOT / "src" / "Rewrite_Middleware" / "Structured_Knowledge_Base" / "documents_document_store.pkl"
    rag = Structured_Knowledge_Base(folder_path, json_file_path,document_path)

    start = time.time()

    def retrieve_for_bottleneck(bn_item: Dict[str, Any]) -> str:
        """
        封装对 rag.retrieval 的调用，使其只负责当前bottleneck的检索并返回结果。
        :param bn_item: 字典形式的瓶颈信息
        :return: 针对该瓶颈的检索结果字符串
        """
        return rag.retrieval(input_sql, bn_item)

    # 使用线程池并发执行检索操作
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers = 8) as executor:
        future_to_bottleneck = {
            executor.submit(retrieve_for_bottleneck, bn): bn
            for bn in origin_suggestion_list
        }

        # 收集每个任务的执行结果，并按照完成顺序拼接/合并
        for future in concurrent.futures.as_completed(future_to_bottleneck):
            bn_item = future_to_bottleneck[future]
            try:
                suggestion = future.result()
                formatted_suggestion = rag.format_suggestion(suggestion)
                results.append({
                    "group": bn_item["group"],
                    "origin_suggestion": bn_item["origin_suggestion"],
                    "retrieval_suggestion": formatted_suggestion
                })
            except Exception as exc:
                print(f"Error in retrieval for origin_suggestion {bn_item}: {exc}")

    end = time.time()
    retrieval_time = end - start
    print(f"Retrieval time: {retrieval_time:.2f} seconds.")

    # 根据需求对结果做进一步处理或组合
    final_output = json.dumps(results, indent=2, ensure_ascii=False)
    print("Knowledge Pool ends! Retrieved Knowledge:",final_output)
    return final_output



# tool_3
async def DBMS_Syntax_Tool(dbms: DBMS, test_sql: str) -> Dict[str, Any]:
    print("DBMS_syntax_Tool starts...")

    # 初始化数据库连接
    dbms.connect()

    # 调用 execute_explain 来测试 SQL 语法
    success, explain_result_or_error = dbms.execute_explain(test_sql)

    if success:
        result = {"flag": True, "error": None}
    else:
        result = {"flag": False, "error": explain_result_or_error}

    dbms.close()
    print(result)
    print("DBMS_syntax_Tool ends...")
    return result



## tool_5
async def Equivalence_Check_Tool(sql1_query, sql2_query, schema_file_path, timeout=10, verbose=False):
    """
    调用sqlsolver.jar并返回结果，如果超时则终止进程并返回UNKNOWN
    
    参数:
        sql1_query (str): 第一个SQL查询的内容
        sql2_query (str): 第二个SQL查询的内容
        schema_file_path (str): schema文件的路径
        jar_path (str, optional): jar包路径
        timeout (int): 超时时间（秒）
        verbose (bool): 是否打印详细信息
    
    返回:
        str: jar包执行的输出结果，如果超时则返回"UNKNOWN_TIMEOUT"
    """
    jar_path = PROJECT_ROOT / "src" / "Rewrite_Middleware" / "Hybrid_SQL_Corrector" / "sqlsolver-v1.1.0.jar"
    
    sql1_query = sql1_query.replace('\n', ' ')
    sql1_query = sql1_query.replace('\"', '')
    sql2_query = sql2_query.replace('\n', ' ')
    sql2_query = sql2_query.replace('\"', '')

    # print(f"This is the original query: {sql1_query}")
    # print(f"This is the rewritten query: {sql2_query}")

    # 创建临时文件保存SQL查询
    with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', delete=False) as sql1_file:
        sql1_file.write(sql1_query)
        sql1_path = sql1_file.name
        
    with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', delete=False) as sql2_file:
        sql2_file.write(sql2_query)
        sql2_path = sql2_file.name
    
    # 创建临时文件用于输出
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as output_file:
        output_path = output_file.name
    
    process = None
    try:
        if jar_path is None:
            jar_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sqlsolver.jar")
        
        command = [
            "java", "-jar", jar_path,
            f"-sql1={sql1_path}",
            f"-sql2={sql2_path}",
            f"-schema={schema_file_path}",
            f"-output={output_path}"
        ]
        
        if verbose:
            print(f"Executing command: {' '.join(command)}")
            print(f"Setting timeout: {timeout} seconds")
        
        # 启动进程
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        try:
            # 使用超时参数执行命令
            stdout, stderr = process.communicate(timeout=timeout)
            
            if process.returncode != 0:
                if verbose:
                    print(f"Command failed with exit code {process.returncode}")
                    print(f"Error: {stderr}")
                return None
            
            # 读取输出文件
            with open(output_path, 'r') as f:
                result = f.read()
                
            if verbose:
                print(f"Command output: {stdout}")
                print(f"Result: {result}")
                
            return result
            
        except subprocess.TimeoutExpired:
            # 超时处理
            if verbose:
                print(f"Process timed out after {timeout} seconds")
            
            # 强制终止进程
            process.kill()
            try:
                process.wait(timeout=2)  # 给进程一点时间完成终止
            except subprocess.TimeoutExpired:
                if verbose:
                    print("Process still alive after kill, force terminating")
                os.kill(process.pid, signal.SIGKILL)
            
            # 返回UNKNOWN结果
            return "UNKNOWN_TIMEOUT"
    
    finally:
        # 确保进程已经终止
        if process and process.poll() is None:
            try:
                process.kill()
            except:
                pass
        
        # 清理临时文件
        for file_path in [sql1_path, sql2_path, output_path]:
            try:
                os.unlink(file_path)
            except Exception as e:
                if verbose:
                    print(f"Error removing temporary file {file_path}: {e}")


# os.environ['LD_LIBRARY_PATH'] = str(PROJECT_ROOT / "src" / "Rewrite_Middleware" / "Hybrid_SQL_Corrector" )

# SCHEMA_PATH = PROJECT_ROOT / "dataset" / "schemas" / "calcite.sql"
# with open(SCHEMA_PATH, 'r') as f:
#     schema_content = f.read()
#     print(f"Schema content loaded from {SCHEMA_PATH}")

# original_sql = "SELECT * FROM (VALUES (1,2)) WHERE FALSE"
# rewritten_sql = "SELECT * FROM (SELECT NULL AS EXPR$0, NULL AS EXPR$1) AS t WHERE 1 = 0"


# # original_sql = "SELECT i, j FROM a"
# # rewritten_sql = "SELECT T.COL1, T.COL2 FROM (SELECT i AS COL1, j AS COL2 FROM a) AS T"
# # rewritten_sql = "SELECT i, j FROM a"
# import asyncio

# async def main():
#     result = await Equivalence_Check_Tool(original_sql, rewritten_sql, SCHEMA_PATH)
#     print(result)

# asyncio.run(main())

