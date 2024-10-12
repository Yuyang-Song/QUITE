import psycopg2
import time
import json
import os
from dotenv import load_dotenv

queries_path = "./query_template/tpch/tpch_queries.json"
storage_path = "./data/result_tpch_1.json"

class Evaluation():
    def __init__(self,evaluation_queries_path,result_storage_path):
        self.evaluation_queries_path = evaluation_queries_path
        self.result_storage_path = result_storage_path
        
    def connect_to_database(self):
        # 设置连接参数
        load_dotenv(dotenv_path='./config_file/.env')  # Load environment variables from .env file
        db_name = os.getenv("DB_NAME")
        db_user= os.getenv("DB_USER")
        db_password= os.getenv("DB_PASSWORD")
        db_host= os.getenv("DB_HOST")
        db_port= os.getenv("DB_PORT")
        conn_params = {
            'dbname': db_name,
            'user': db_user,
            'password': db_password,
            'host': db_host,
            'port': db_port
        }
        try:
            conn = psycopg2.connect(**conn_params)
            print("Database connection successful")
            return conn
        except psycopg2.Error as e:
            print(f"Database connection failed: {e}")
            return None


    def execute_query(self,conn, cursor, query):
        try:
            start_time = time.time()
            cursor.execute(query)
            cursor.fetchall()  # 获取所有结果
            conn.commit()  # 提交事务
            end_time = time.time()
            return end_time - start_time
        except psycopg2.Error as e:
            conn.rollback()  # 回滚事务
            print(f"Error executing query: {e}")

            return None
            


    def evaluate(self):
        # 打开并读取JSON文件
        with open(self.evaluation_queries_path, 'r') as file:
            data = json.load(file)

        existing_results = []

        # 检查 result.json 是否存在，存在则加载它
        if os.path.exists(self.result_storage_path):
            with open(self.result_storage_path, 'r') as result_file:
                try:
                    existing_results = json.load(result_file)
                    # 确保 existing_results 是一个列表
                    if isinstance(existing_results, dict):
                        existing_results = [existing_results]
                    elif not isinstance(existing_results, list):
                        existing_results = []
                except json.JSONDecodeError:
                    existing_results = []

        # 遍历 JSON 数据中的所有 SQL 对
        iteration = 1
        conn = self.connect_to_database()
        cursor = conn.cursor()
        for query_pair in data:

            query = query_pair.get('query', '')
            print(f"this is the {iteration} times execution:")
            iteration += 1
            time = self.execute_query(conn, cursor,query)    
            print(f"time costs: {time}\n")    
            result_data = {
                "query": query,
                "execution time" :time
            }

            existing_results.append(result_data)

        cursor.close()
        conn.close()
        # 将结果写回到 result.json 文件
        with open(self.result_storage_path, 'w') as result_file:
            json.dump(existing_results, result_file, indent=4)

        print(f"Experiment results appended to {self.result_storage_path}")


# test part
model = Evaluation(queries_path,storage_path)
model.evaluate()
