import psycopg2
import time
import json
import os
from dotenv import load_dotenv

evaluation_queries_path = "./queries/llmr2_result_tpch.json"
result_storage_path = "../data/result_llmr2.json"

def connect_to_database():
        # 设置连接参数
    load_dotenv(dotenv_path='../config_file/.env')  # Load environment variables from .env file
    conn_params = {
        'dbname': os.getenv("DBNAME")  ,
        'user': os.getenv("USER"),
        'password': os.getenv("PASSWORD"),
        'host': os.getenv("HOST"),
        'port': os.getenv("PORT")
    }
    try:
        conn = psycopg2.connect(**conn_params)
        print("Database connection successful")
        return conn
    except psycopg2.Error as e:
        print(f"Database connection failed: {e}")
        return None


def execute_query(conn, cursor, query):
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

def compare_rewritten(original_query,rewritten_query,iteration  = 3):
    conn = connect_to_database()
    cursor = conn.cursor()
    total_original_time = 0.0
    total_rewrite_time = 0.0
    # 执行原始查询并记录时间
    cursor.execute("SELECT pg_stat_reset()")
    for i in range(iteration + 1):
        if i == 0:
            rewritten_time = execute_query(conn, cursor, rewritten_query)
            cursor.execute("SELECT pg_stat_reset()")
            print(f"this is the init: rewrite query excute time: {rewritten_time}")
            continue
        original_time = execute_query(conn, cursor, original_query)
        print(f"the {i}-th\{iteration} iteration original query excute time: {original_time}")
        cursor.execute("SELECT pg_stat_reset()")
        total_original_time += original_time
        
    total_original_time = total_original_time / iteration
    if total_original_time is not None:
        print(f"Original Query Execution Time: {total_original_time:.6f} seconds")
    else:
        print("Original Query Execution Failed")

    for i in range(iteration):
        rewritten_time = execute_query(conn, cursor, rewritten_query)
        cursor.execute("SELECT pg_stat_reset()")
        print(f"the {i}th\{iteration} iteration rewrite query excute time: {rewritten_time}")
        total_rewrite_time += rewritten_time
        
    total_rewrite_time = total_rewrite_time / iteration
    if total_rewrite_time is not None:
        print(f"Rewritten Query Execution Time: {total_rewrite_time:.6f} seconds")
    else:
        print("Rewritten Query Execution Failed")

    if total_original_time is not None and total_rewrite_time is not None:
        speed_up = (total_original_time - total_rewrite_time) / total_original_time
        times_up = total_original_time / total_rewrite_time
        print(f"speed_up : {speed_up}")
        print(f"times up: {times_up}x")
        
    return total_original_time,total_rewrite_time,speed_up,times_up
        
    cursor.close()
    conn.close()


if __name__ == "__main__":
# 打开并读取JSON文件
    with open(evaluation_queries_path, 'r') as file:
        data = json.load(file)

    existing_results = []

    # 检查 result.json 是否存在，存在则加载它
    if os.path.exists(result_storage_path):
        with open(result_storage_path, 'r') as result_file:
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
            
            original_execution_time, rewrite_execution_time, speed_up, times_up = compare_rewritten(
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
    with open(result_storage_path, 'w') as result_file:
        json.dump(existing_results, result_file, indent=4)

    print(f"Experiment results appended to {result_storage_path}")