import psycopg2
import time
import subprocess
import json
import os
from dotenv import load_dotenv

# queries_path = "./data/result_lr_excusion_s1.json"
queries_path = "/home/orderheart/syy/sql_rewriter/query_template/case/case_2.json"
storage_path = "./data/mac/case_2_study.json"

class Evaluation():
    def __init__(self,evaluation_queries_path,result_storage_path):
        self.evaluation_queries_path = evaluation_queries_path
        self.result_storage_path = result_storage_path
    def connect_to_database(self, retries=5, wait_time=5):
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
        
        # 尝试多次连接数据库
        for attempt in range(retries):
            try:
                conn = psycopg2.connect(**conn_params)
                print("Database connection successful")
                return conn
            except psycopg2.Error as e:
                print(f"Database connection failed (attempt {attempt+1}/{retries}): {e}")
                if attempt < retries - 1:
                    time.sleep(wait_time)  # 等待一段时间再重试
                else:
                    print("Max retries reached. Exiting.")
                    return None
    # def connect_to_database(self):
    #         # 设置连接参数
    #     load_dotenv(dotenv_path='./config_file/.env')  # Load environment variables from .env file
    #     db_name = os.getenv("DB_NAME")
    #     db_user= os.getenv("DB_USER")
    #     db_password= os.getenv("DB_PASSWORD")
    #     db_host= os.getenv("DB_HOST")
    #     db_port= os.getenv("DB_PORT")
    #     conn_params = {
    #         'dbname': db_name,
    #         'user': db_user,
    #         'password': db_password,
    #         'host': db_host,
    #         'port': db_port
    #     }
    #     try:
    #         conn = psycopg2.connect(**conn_params)
    #         print("Database connection successful")
    #         return conn
    #     except psycopg2.Error as e:
    #         print(f"Database connection failed: {e}")
    #         return None
        
    # def restart_postgresql(self):
    #     # os.system("sudo service postgresql restart")
    #     os.system("brew services restart postgresql@14")
    #     print("PostgreSQL service restarted.")
    
    def restart_postgresql(self):
        # 使用 subprocess.run 来执行命令并等待其完成
        # result = subprocess.run(["brew", "services", "restart", "postgresql@14"], capture_output=True, text=True)
        result = subprocess.run(["docker", "exec", "syy_db", "/bin/bash", "service", "postgresql", "restart"], capture_output=True, text=True)
        # 检查命令是否成功执行
        if result.returncode == 0:
            print("PostgreSQL service restarted successfully.")
            # 等待几秒，确保PostgreSQL服务完全启动
            time.sleep(3)  # 等待5秒
        else:
            print(f"Failed to restart PostgreSQL service. Error: {result.stderr}")

    def execute_query(self, conn, cursor, query):
        db_name = os.getenv("DB_NAME")
        clr_q = "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE pid <> pg_backend_pid() AND datname = '" + db_name + "';"
        try:
            cursor.execute(clr_q)
            cursor.execute("SET enable_seqscan = off;")
            cursor.execute("SET enable_indexscan = off;")
            
            start_time = time.time()
            cursor.execute(query)
            cursor.fetchall()  # 获取所有结果
            conn.commit()  # 提交事务
            end_time = time.time()
            return end_time - start_time
        except psycopg2.Error as e:
            conn.rollback()  # 回滚事务
            print(f"Error executing query: {e}")
            return -1  # 如果执行失败，返回 -1

    def compare_rewritten(self,original_query,rewritten_query,iteration  = 2):
        conn = self.connect_to_database()
        cursor = conn.cursor()
        total_original_time = 0.0
        total_rewrite_time = 0.0
        # 执行原始查询并记录时间
        cursor.execute("SELECT pg_stat_reset()")
        for i in range(iteration + 1):
            # 重启PostgreSQL服务
            self.restart_postgresql()
            
            # 重新连接数据库
            conn = self.connect_to_database()
            if conn is None:
                return -1, -1, -1, -1  # 无法连接时返回 -1
            cursor = conn.cursor()
            
            if i == 0:
                original_time = self.execute_query(conn, cursor, original_query)
                cursor.execute("SELECT pg_stat_reset()")
                print(f"this is the init: original query excute time: {original_time}")
                continue
            original_time = self.execute_query(conn, cursor, original_query)
            print(f"the {i}-th{iteration} iteration original query excute time: {original_time}")
            cursor.execute("SELECT pg_stat_reset()")
            total_original_time += original_time
            
        total_original_time = total_original_time / iteration 

        if total_original_time == -1:
            print("Original Query Execution Failed")
            return -1, -1, -1, -1  # 如果原始查询失败，返回 -1
        
        if total_original_time is not None:
            print(f"Original Query Execution Time: {total_original_time:.6f} seconds")
        else:
            print("Original Query Execution Failed")

        for i in range(iteration + 1):
             # 重启PostgreSQL服务
            self.restart_postgresql()
            if conn is None:
                return -1, -1, -1, -1  # 无法连接时返回 -1
            # 重新连接数据库
            conn = self.connect_to_database()
            cursor = conn.cursor()
            
            if i == 0:
                rewritten_time = self.execute_query(conn, cursor, rewritten_query)
                if rewritten_time == -1:  # 如果执行失败，返回 -1
                    return -1, -1, -1, -1
                cursor.execute("SELECT pg_stat_reset()")
                print(f"this is the init: rewrite query excute time: {rewritten_time}")
                continue
            rewritten_time = self.execute_query(conn, cursor, rewritten_query)
            cursor.execute("SELECT pg_stat_reset()")
            print(f"the {i}th{iteration} iteration rewrite query excute time: {rewritten_time}")
            total_rewrite_time += rewritten_time
            
        total_rewrite_time = total_rewrite_time / iteration
        if total_rewrite_time is not None:
            print(f"Rewritten Query Execution Time: {total_rewrite_time:.6f} seconds")
        else:
            print("Rewritten Query Execution Failed")
        # total_rewrite_time = total_rewrite_time / iteration if iteration > 0 else -1

        if total_rewrite_time == -1:
            print("Rewritten Query Execution Failed")
            return -1, -1, -1, -1  # 如果重写查询失败，返回 -1
        
        if total_original_time is not None and total_rewrite_time is not None:
            speed_up = (total_original_time - total_rewrite_time) / total_original_time
            times_up = total_original_time / total_rewrite_time
            print(f"speed_up : {speed_up}")
            print(f"times up: {times_up}x")
        
        # cursor.close()
        # conn.close()

        return total_original_time,total_rewrite_time,speed_up,times_up
            

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
        for query_pair in data:
            original_query = query_pair.get('original_sql', '')
            rewritten_query = query_pair.get('rewritten_sql', '')
            
            if original_query and rewritten_query:
                print(f"Running queries for pair: {original_query[:30]}... and rewritten query.")
                
                original_execution_time, rewrite_execution_time, speed_up, times_up = self.compare_rewritten(
                    original_query, rewritten_query, iteration=3
                )

                result_data = {
                    "original_query": original_query,
                    "rewritten_query": rewritten_query,
                    "original_execution_time": original_execution_time,
                    "rewrite_execution_time": rewrite_execution_time,
                    "speed_up": speed_up,
                    "times_up": times_up
                }

                existing_results.append(result_data)

        # 将结果写回到 result.json 文件
        with open(self.result_storage_path, 'w') as result_file:
            json.dump(existing_results, result_file, indent=4)

        print(f"Experiment results appended to {self.result_storage_path}")


# test part
model = Evaluation(queries_path,storage_path)
# model.evaluate()
# 加载 JSON 数据
with open(queries_path, 'r') as file:
    json_content = file.read()
data = json.loads(json_content)

print(data)
result = []
# 遍历 JSON 中的每个项目
for i, query_info in enumerate(data, start=0):
    # 获取 original_query 和 rewritten_query
    original_query = query_info.get("original_query", "No original query found")
    rewritten_query = query_info.get("rewritten_query", "No rewritten query found")
    # 输出结果
    print(f"Original Query: {original_query}")
    print(f"Rewritten Query: {rewritten_query}")
    total_original_time,total_rewrite_time,speed_up,times_up = model.compare_rewritten(original_query,rewritten_query)
    result_data = {
        "original_query": original_query,
        "rewritten_query": rewritten_query,
        "original_execution_time": total_original_time,
        "rewrite_execution_time": total_rewrite_time,
        "speed_up": speed_up,
        "times_up": times_up
    }
    result.append(result_data)
    
# 将结果写回到 result.json 文件
with open(storage_path, 'w') as result_file:
    json.dump(result, result_file, indent=4)
# 提取 original_query 和 rewritten_query
# original_query = data["original_query"]
# rewritten_query = data["rewritten_query"]


# model.compare_rewritten()