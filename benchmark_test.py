import psycopg2
import time
import json
import os
import subprocess
from dotenv import load_dotenv

# queries_path ="/home/orderheart/syy/sql_rewriter/query_template/tpchds/test"
queries_path = "./query_template/tpcds/queries.json"
storage_path = "./data/result_tpcds_1.json"
time_out = 100

class Evaluation():
    def __init__(self,evaluation_queries_path,result_storage_path,timeout):
        self.evaluation_queries_path = evaluation_queries_path
        self.result_storage_path = result_storage_path
        self.timeout = timeout
        
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


    # def execute_query(self,conn, cursor, query):
    #     try:
    #         start_time = time.time()
    #         cursor.execute(query)
    #         cursor.fetchall()  # 获取所有结果
    #         conn.commit()  # 提交事务
    #         end_time = time.time()
    #         return end_time - start_time
    #     except psycopg2.Error as e:
    #         conn.rollback()  # 回滚事务
    #         print(f"Error executing query: {e}")

    #         return None
    def execute_query(self, conn, cursor, query, timeout):
        try:
            # 设置 PostgreSQL 的 statement 超时
            # timeout 以毫秒为单位，所以将秒数乘以 1000
            cursor.execute(f"SET statement_timeout = {timeout * 1000};")
            # print(f"query:{query}")
            start_time = time.time()
            cursor.execute(query)
            cursor.fetchall()  # 获取所有结果
            conn.commit()  # 提交事务
            end_time = time.time()

            return end_time - start_time
        except psycopg2.OperationalError as e:
            # 如果超时错误被捕获，回滚事务并返回 -2
            if "canceling statement due to statement timeout" in str(e):
                conn.rollback()
                print(f"Query execution exceeded {timeout} seconds and was terminated.")
                # self.restart_postgresql()
                return -2
            else:
                # 捕获其他数据库错误，回滚事务
                conn.rollback()
                print(f"Error executing query: {e}")
                # self.restart_postgresql()
                return None
        finally:
            # 确保在任何情况下都取消超时设置（可选）
            cursor.execute("SET statement_timeout = 0;")

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
            id_number = query_pair.get('id','')
            print(f"this is the {iteration} times execution: execution {id_number} queries")
            iteration += 1
            time = self.execute_query(conn, cursor,query,self.timeout)    
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

    def restart_postgresql(self):
        # 使用 subprocess.run 来执行命令并等待其完成
        result = subprocess.run(["docker", "exec", "syy_db", "/bin/bash", "service", "postgresql", "restart"], capture_output=True, text=True)
        # 检查命令是否成功执行
        if result.returncode == 0:
            print("PostgreSQL service restarted successfully.")
            # 等待几秒，确保PostgreSQL服务完全启动
            time.sleep(5)  # 等待5秒
        else:
            print(f"Failed to restart PostgreSQL service. Error: {result.stderr}")

    # def evaluate(self):
    #     # 存储执行结果
    #     existing_results = []

    #     # 检查 result.json 是否存在，存在则加载它
    #     if os.path.exists(self.result_storage_path):
    #         with open(self.result_storage_path, 'r') as result_file:
    #             try:
    #                 existing_results = json.load(result_file)
    #                 # 确保 existing_results 是一个列表
    #                 if isinstance(existing_results, dict):
    #                     existing_results = [existing_results]
    #                 elif not isinstance(existing_results, list):
    #                     existing_results = []
    #             except json.JSONDecodeError:
    #                 existing_results = []

    #     # 遍历文件夹中的 .sql 文件
    #     sql_folder_path = self.evaluation_queries_path  # 假设这个变量指向包含 .sql 文件的文件夹路径
    #     iteration = 1
    #     conn = self.connect_to_database()
    #     cursor = conn.cursor()

    #     for filename in os.listdir(sql_folder_path):
    #         if filename.endswith(".sql"):
    #             # 读取 .sql 文件内容
    #             file_path = os.path.join(sql_folder_path, filename)
    #             with open(file_path, 'r') as sql_file:
    #                 query = sql_file.read()
                
    #             # 执行查询
    #             print(f"this is the {iteration} times execution: executing query from {filename}")
    #             iteration += 1
    #             time = self.execute_query(conn, cursor, query, self.timeout)
    #             print(f"time costs: {time}\n")
    #             query_name = os.path.splitext(filename)[0].replace('query', '', 1)  # 去除前缀 'query'  # 使用文件名作为查询名称
    #             # 保存执行结果
    #             result_data = {
    #                 "id": query_name,
    #                 "query": query,
    #                 "execution time": time
    #             }
    #             existing_results.append(result_data)

    #     # 关闭数据库连接
    #     cursor.close()
    #     conn.close()

    #     # 将结果保存回 result.json
    #     with open(self.result_storage_path, 'w') as result_file:
    #         json.dump(existing_results, result_file, indent=4)
        
    #     print(f"Experiment results appended to {self.result_storage_path}")

# test part
model = Evaluation(queries_path,storage_path,time_out)
model.evaluate()
