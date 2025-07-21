import sys
import sys
sys.path.append('../')
sys.path.append('../../')
sys.path.append('./')
import asyncio
import json
import os
from dotenv import load_dotenv
import asyncpg
import re
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict,Any, Optional,Tuple
import concurrent.futures
import os
import hashlib
import json
import time
import textwrap
from dotenv import load_dotenv
import re
from typing import List, Dict, Any

# os.environ['HTTP_PROXY'] = 'socks5h://127.0.0.1:1080'
# os.environ['HTTPS_PROXY'] = 'socks5h://127.0.0.1:1080'


class DBMS_PLUS:
    def __init__(self,json_file_path = None):
        # load_dotenv(dotenv_path='../../config_file/.env')  # Load environment variables from .env file
        load_dotenv(dotenv_path="/root/syy/code/Hint_injection/config_file/.env")
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

class DBMS:
    def __init__(self,db_id,json_file_path = None):
        # 初始化数据库配置
        # """异步连接到 PostgreSQL 数据库"""
        # 内部执行，两个../
        # load_dotenv(dotenv_path='../../config_file/.env')  # Load environment variables from .env file
        load_dotenv(dotenv_path="/root/syy/MAReter_2/config_file/.env")
        self.db_name = db_id
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
        
    def execute_query(self, sql: str):
        """执行单个 SQL 语句并返回结果"""
        self.connect()
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            result = None
            try:
                result = self.cursor.fetchall()
            except:
                # 有些语句没有返回结果，比如 SET 语句
                pass
            self.close()
            return result
        except Exception as e:
            self.connection.rollback()
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

    def process_query(self, sql: str, index: int, results: List[Dict]):
        print(f"\nExecuting EXPLAIN (Query {index + 1}): {sql}")
        success, explain_info_or_error = self.execute_explain(sql)

        if success:
            print(f"EXPLAIN result for Query {index + 1} retrieved successfully.")
            results.append({
                "query": sql,
                "explain": explain_info_or_error
            })
        else:
            print(f"Failed to retrieve EXPLAIN result for Query {index + 1}. Error: {explain_info_or_error}")
            results.append({
                "query": sql,
                "explain": None,
                "error": explain_info_or_error
            })

    def get_explain(self, query: str) -> Tuple[bool, Any]:
        """
        Gets the EXPLAIN result for a single SQL query.

        :param query: SQL query to explain.
        :return: Tuple (success: bool, explain result or error message)
        """
        # Connect to the database
        self.connect()

        # Get the EXPLAIN result
        success, explain_info_or_error = self.execute_explain(query)
        # print(f"EXPLAIN result: {explain_info_or_error}")
        # Close the database connection
        self.close()

        return success, explain_info_or_error
    

    def traverse_plan(self, plan: Dict[str, Any], operations: List[Dict[str, Any]]):
        """
        递归遍历执行计划，收集操作节点信息
        """
        if not plan:
            return

        node_info = {
            'Node Type': plan.get('Node Type'),
            'Total Cost': plan.get('Total Cost', 0),
            'Startup Cost': plan.get('Startup Cost', 0),
            'Plan Rows': plan.get('Plan Rows', 0),
            'Actual Rows': plan.get('Actual Rows', 0),
            # 'Relation Name': plan.get('Relation Name', ''),
            'Join Type': plan.get('Join Type', ''),
            'Filter': plan.get('Filter', '') or plan.get('Join Filter', '') or plan.get('Index Cond', '')
            # 'SQL Clause': self.map_operation_to_sql_clause(plan)
        }

        operations.append(node_info)
        for sub_plan in plan.get('Plans', []):
            self.traverse_plan(sub_plan, operations)

    def get_top_k_operations(self,operations: List[Dict[str, Any]], k: int) -> List[Dict[str, Any]]:
        """
        根据多个维度（如 Total Cost, Startup Cost, Plan Rows 等）进行综合排序，获取 Top-K 的操作
        """
        sorted_ops = sorted(operations, key=lambda x: (
            x['Total Cost'], x['Startup Cost'], x['Plan Rows'], x['Actual Rows']), reverse=True)
        return sorted_ops[:k]

    def map_operation_to_sql_clause(self,operation: Dict[str, Any], sql_query: str) -> str:
        """
        Attempts to map the operation node to the specific clause in the SQL query.
        Returns the corresponding SQL clause description.

        Args:
            operation (Dict[str, Any]): Operation node information.
            sql_query (str): Corresponding SQL query.

        Returns:
            str: Mapped SQL clause description.
        """
        node_type = operation['Node Type']
        filter_cond = operation.get('Filter','')
        relation = operation.get('Relation Name','')

        # Simple mapping logic to infer the corresponding SQL clause based on Node Type and other information
        if node_type == 'Aggregate':
            # Find the aggregate function in the SELECT clause
            match = re.search(r'SELECT\s+(.+?)\s+FROM', sql_query, re.IGNORECASE | re.DOTALL)
            if match:
                select_clause = match.group(1).strip()
                return f"Aggregate function in the SELECT clause: {select_clause}"
        elif node_type in ['Nested Loop', 'Hash Join', 'Merge Join']:
            # Find the JOIN condition
            if filter_cond:
                return f"JOIN operation, join condition: {filter_cond}"
            else:
                return "JOIN operation"
        elif node_type in ['Seq Scan', 'Index Scan']:
            # Find the involved table and filter condition
            if filter_cond:
                return f"Table scan in the FROM clause: {relation}, filter condition: {filter_cond}"
            else:
                return f"Table scan in the FROM clause: {relation}"
        elif node_type == 'Filter':
            return f"Filter condition in the WHERE clause: {filter_cond}"
        else:
            return "Other operation"

    def analyze_sql_plans(self,data: Dict[str, Any], top_k: int) -> List[Dict[str, Any]]:
        """
        分析每个 SQL 语句的执行计划，返回总成本和最耗时的 Top-K 操作及其对应的 SQL 子句。
        
        :param data: 包含查询和解释结果的字典
        :param top_k: 获取 Top-K 的数量
        :return: 分析结果列表
        """
        results = []
        query = data['query']
        explain = data['explain']

        # 确保 'explain' 是列表并且包含计划
        if isinstance(explain, list) and len(explain) > 0:
            plan = explain[0]['Plan']
            total_cost = plan['Total Cost']
            operations = []
            self.traverse_plan(plan, operations)
            top_operations = self.get_top_k_operations(operations, top_k)

            # 对每个操作进行映射
            for op in top_operations:
                op['SQL Clause'] = self.map_operation_to_sql_clause(op, query)
            
            results.append({
                'query': query,
                'total_cost': total_cost,
                'top_operations': top_operations
            })
        else:
            results.append({
                'query': query,
                'error': 'Invalid EXPLAIN result'
            })
        
        return results

    def explain_analysis(self, query: str, top_k: int = 5) -> Tuple[bool, Any]:
        """
        Analyzes a single SQL query's execution plan with robust error handling.

        :param query: SQL query to analyze.
        :param top_k: Number of top operations to retrieve.
        :return: Tuple containing the operate flag and either top operations or error message.
        """
        success, explain_info_or_error = self.get_explain(query)

        input_data = {
            "query": query,
            "explain": explain_info_or_error if success else None,
            "operate": success
        }

        if not success:
            input_data["error"] = explain_info_or_error

        if input_data["operate"]:
            # analysis = self.get_explain_top(input_data, top_k)
            analysis = self.analyze_sql_plans(input_data, top_k)
            if analysis and 'top_operations' in analysis[0]:
                return input_data["operate"], analysis[0]['top_operations']
            else:
                # In case analyze_sql_plans didn't return top_operations
                return False, "Failed to analyze EXPLAIN result."
        else:
            return input_data["operate"], input_data.get("error", "Unknown error.")
    