import psycopg2
import time
import subprocess
import json
import os
import numpy as np
import statistics
from dotenv import load_dotenv
from decimal import Decimal
from datetime import date
import argparse
from pathlib import Path

PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT", Path(__file__).resolve().parents[2]))
LOAD_PATH = PROJECT_ROOT / "config_file" / ".env"
load_dotenv(dotenv_path=LOAD_PATH)


class Evaluation():
    def __init__(self,evaluation_queries_path,result_storage_path,filtered_path,dbname,timeout = 300):
        self.evaluation_queries_path = evaluation_queries_path
        self.result_storage_path = result_storage_path
        self.filtered_path = filtered_path
        self.timeout = timeout
        self.dbname = dbname

    def connect_to_database(self, retries=5, wait_time=5):
        db_name = self.dbname
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
        print("Connecting to database... DB_NAME: {}, DB_USER: {}, DB_HOST: {}, DB_PORT: {}".format(db_name, db_user, db_host, db_port))
        for attempt in range(retries):
            try:
                conn = psycopg2.connect(**conn_params)
                print("Database connection successful")
                return conn
            except psycopg2.Error as e:
                print(f"Database connection failed (attempt {attempt+1}/{retries}): {e}")
                if attempt < retries - 1:
                    time.sleep(wait_time)  
                else:
                    print("Max retries reached. Exiting.")
                    return None

    def convert_to_serializable(self,obj):
        """将数据结构中不可序列化的 Decimal 和 date 转换为可序列化的类型。"""
        if isinstance(obj, Decimal):
            return float(obj)  # 或者使用 str(obj) 转换为字符串
        elif isinstance(obj, date):
            return obj.isoformat()  # 将 date 对象转换为 YYYY-MM-DD 格式的字符串
        elif isinstance(obj, list):
            return [self.convert_to_serializable(item) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(self.convert_to_serializable(item) for item in obj)
        elif isinstance(obj, set):
            return [self.convert_to_serializable(item) for item in obj]  # 转为列表以序列化
        elif isinstance(obj, dict):
            return {key: self.convert_to_serializable(value) for key, value in obj.items()}
        return obj
    
    def restart_postgresql(self):
        # 使用 subprocess.run 来执行命令并等待其完成
        # result = subprocess.run(["brew", "services", "restart", "postgresql@14"], capture_output=True, text=True)
        result = subprocess.run(["service", "postgresql", "restart"], capture_output=True, text=True)
        # 检查命令是否成功执行
        if result.returncode == 0:
            print("PostgreSQL service restarted successfully.")
            # 等待几秒，确保PostgreSQL服务完全启动
            time.sleep(3)  # 等待5秒
        else:
            print(f"Failed to restart PostgreSQL service. Error: {result.stderr}")
        
    def execute_query(self, conn, cursor, query, timeout,return_flag=False):
        try:
            # Set PostgreSQL statement timeout
            cursor.execute(f"SET statement_timeout = {timeout * 1000};")
            start_time = time.time()
            
            # Execute the query
            cursor.execute(query)
            end_time = time.time()

            execution_result = None
            try:
                execution_result = cursor.fetchall()  # Fetch all results
            except psycopg2.ProgrammingError as e:
                # 如果查询没有返回结果，则忽略异常
                pass            
            # # Only fetch results if the query is a SELECT statement
            # if query.strip().lower().startswith("select"):
            #     execution_result = cursor.fetchall()  # Fetch all results
            #     conn.commit()  # Commit transaction
            # else:
            #     execution_result = None  # No results to fetch for non-SELECT queries 

            if return_flag == False:
                return end_time - start_time
            else:
                return end_time - start_time, execution_result
        
        except psycopg2.OperationalError as e:
            # 如果超时错误被捕获，回滚事务并返回 -2
            if "canceling statement due to statement timeout" in str(e):
                conn.rollback()
                print(f"Query execution exceeded {timeout} seconds and was terminated.")
                # self.restart_postgresql()
                return -2, -2
            else:
                # 捕获其他数据库错误，回滚事务
                conn.rollback()
                print(f"Error exe cuting query: {e}")
                # self.restart_postgresql()
                return None
        
        except psycopg2.Error as e:
            conn.rollback()  # 回滚事务
            print(f"Error executing query: {e}")
            if return_flag == False:
                return -1  # 如果执行失败，返回 -1
            else:
                return None
            
        # Exception 是所有异常的基类
        except Exception as e:
            conn.rollback()  # Rollback transaction in case of error
            raise e
        
        finally:
            # 确保在任何情况下都取消超时设置（可选）
            cursor.execute("SET statement_timeout = 0;")

    def compare_rewritten(self,original_query,rewritten_query,iteration=1):
        conn = self.connect_to_database()
        cursor = conn.cursor()
        timeout = self.timeout
        total_original_time = 0.0
        total_rewrite_time = 0.0
        original_result = None
        rewritten_result = None
        
        # 执行原始查询并记录时间
        for i in range(iteration + 1):
            ORIGINAL_TIME_OUT = False
            if conn is None:
                return None, None, None, None, None, None  # 无法连接时返回 -1
            
            if i == 0:
                print("start init hot database execution")
                original_time,original_result = self.execute_query(conn, cursor, original_query,timeout, return_flag = True)
                print(f"this is the init: original query excute time: {original_time}")
                if original_time == -2:
                    ORIGINAL_TIME_OUT = True
                    break
                elif original_time == -1:
                    break
                else:
                    continue
            # original_time = self.execute_query(conn, cursor, original_query)
            original_time= self.execute_query(conn, cursor, original_query,timeout)
            print(f"the {i}-th/{iteration} iteration original query excute time: {original_time}")
            total_original_time += original_time
        
        if ORIGINAL_TIME_OUT == False:
            total_original_time = total_original_time / iteration 
        else:
            total_original_time = timeout

        if total_original_time == -1:
            print("Original Query Execution Failed")
            return None, None, None, None, None, None  # 如果原始查询失败，返回 -1
        
        if total_original_time is not None:
            print(f"Original Query Execution Time: {total_original_time:.6f} seconds")
        else:
            print("Original Query Execution Failed")

        self.restart_postgresql()
        if conn is None:
            return None, None, None, None, None, None  # 无法连接时返回 -1
        # 重新连接数据库
        conn = self.connect_to_database()
        cursor = conn.cursor()

        try:
            for i in range(iteration + 1):
                REWRITTEN_TIME_OUT = False 
                if conn is None:
                    return None, None, None, None, None, None  # 无法连接时返回 -1
                
                if i == 0:
                    print("start init hot database execution")
                    rewritten_time,rewritten_result = self.execute_query(conn, cursor, rewritten_query,timeout, return_flag = True)
                    print(f"this is the init: rewrite query excute time: {rewritten_time}")
                    if rewritten_time == -2:
                        REWRITTEN_TIME_OUT = True
                        break
                    elif rewritten_time == -1:
                        break
                    else:
                        continue
                rewritten_time = self.execute_query(conn, cursor, rewritten_query,timeout)
                print(f"the {i}-th/{iteration} iteration rewrite query excute time: {rewritten_time}")
                total_rewrite_time += rewritten_time

            if total_rewrite_time == -1:
                print("Rewritten Query Execution Failed")
                return total_original_time, None, None, None, original_result, None  # 如果重写查询失败，返回 -1
            
            if REWRITTEN_TIME_OUT == False:
                total_rewrite_time = total_rewrite_time / iteration
            if REWRITTEN_TIME_OUT == True and total_rewrite_time == -1:

                return total_original_time, None, None, None, original_result, None
            
            if REWRITTEN_TIME_OUT == True and total_rewrite_time != -1:
                total_rewrite_time = timeout
                print(f"Rewritten Query Execution Time: {total_rewrite_time:.6f} seconds")
            # total_rewrite_time = total_rewrite_time / iteration if iteration > 0 else -1

        except psycopg2.errors.SyntaxError as e:
            print(f"Rewritten query execution failed due to syntax error: {e}")
            # 设置重写查询的返回值为错误标记值，继续执行下一个查询对
            return total_original_time, None, None, None, original_result, None
        except Exception as e:
            print(f"Rewritten query execution failed due to unexpected error: {e}")
            # 设置重写查询的返回值为错误标记值，继续执行下一个查询对
            return total_original_time, None, None, None, original_result, None

        
        if total_original_time is not None and total_rewrite_time is not None:
            speed_up = (total_original_time - total_rewrite_time) / total_original_time
            times_up = total_original_time / total_rewrite_time
            print(f"speed_up : {speed_up}")
            print(f"times up: {times_up}x")
            equivalance = (original_result == rewritten_result)
            print("equivalance: ",equivalance)
        
        # cursor.close()
        # conn.close()
        # equivalance = (original_result == rewritten_result)
        # print(f"Equivalence: {equivalance}")
        return total_original_time,total_rewrite_time,speed_up,times_up,original_result,rewritten_result
            

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
            query_id = query_pair.get('id', '')
            original_query = query_pair.get('original_sql', '')
            rewritten_query = query_pair.get('rewritten_sql', '')
            
            if original_query and rewritten_query:
                print(f"Running queries for pair: {original_query[:30]}... and rewritten query.")
                
                original_execution_time, rewrite_execution_time, speed_up, times_up,original_result,rewritten_result = self.compare_rewritten(
                    original_query, rewritten_query, iteration= 2
                )
                if original_result != None and rewritten_result != None and original_execution_time != self.timeout and rewrite_execution_time != self.timeout:
                    equivalance = (original_result == rewritten_result)
                else:
                    equivalance = False
                result_data = {
                    "id": query_id,
                    "equivalence": equivalance,
                    "original_query": original_query,
                    "rewritten_query": rewritten_query,
                    "original_execution_time": original_execution_time,
                    "rewrite_execution_time": rewrite_execution_time,
                    "speed_up": speed_up,
                    "times_up": times_up,
                    "original_result": model.convert_to_serializable(original_result),
                    "rewritten_result": model.convert_to_serializable(rewritten_result)                   
                }

                existing_results.append(result_data)


        existing_results = sorted(existing_results, key=lambda x: int(x.get("id", 0)))  # 按照 id 排序
        # 将结果写回到 result.json 文件
        with open(self.result_storage_path, 'w') as result_file:
            json.dump(existing_results, result_file, indent=4)

        print(f"Experiment results appended to {self.result_storage_path}")
    
    def cal(self):
        Metric = []
        result_data = []
        original_execution_times = []
        rewritten_execution_times = []
        with open(self.result_storage_path, "r") as file:
            data = json.load(file)
            for info in data:
                if(info['original_execution_time'] != -1 and info['original_execution_time'] != None and info['rewrite_execution_time'] != -1 and info['rewrite_execution_time'] != None):
                    original_execution_times.append(info['original_execution_time'])
                    rewritten_execution_times.append(info['rewrite_execution_time'])
                    insert_data = {
                        "id": info["id"],
                        "equivalence": info["equivalence"],
                        "original_query": info["original_query"],
                        "rewritten_query": info["rewritten_query"],
                        "original_execution_time": info["original_execution_time"],
                        "rewrite_execution_time": info["rewrite_execution_time"],
                        "speed_up": info["speed_up"],
                        "times_up": info["times_up"]
                    }
                    result_data.append(insert_data)



            # 计算平均数
        ori_avg = statistics.mean(original_execution_times)
        print(f"The average execution time is: {ori_avg}")
        # 计算中位数
        ori_median = statistics.median(original_execution_times)
        print(f"The median execution time is: {ori_median}")
        # 计算75th百分位数
        ori_percentile_75 = np.percentile(original_execution_times, 75)
        print(f"The 75th percentile execution time is: {ori_percentile_75}")
        # 计算95th百分位数
        ori_percentile_95 = np.percentile(original_execution_times, 95)
        print(f"The 95th percentile execution time is: {ori_percentile_95}")

        re_avg = statistics.mean(rewritten_execution_times)
        print(f"The average execution time is: {re_avg}")
        # 计算中位数
        re_median = statistics.median(rewritten_execution_times)
        print(f"The median execution time is: {re_median}")
        # 计算75th百分位数
        re_percentile_75 = np.percentile(rewritten_execution_times, 75)
        print(f"The 75th percentile execution time is: {re_percentile_75}")
        # 计算95th百分位数
        re_percentile_95 = np.percentile(rewritten_execution_times, 95)
        print(f"The 95th percentile execution time is: {re_percentile_95}")
        ori_result = {
            "original_average": ori_avg,
            "original_median": ori_median,
            "original_75th_percentile": ori_percentile_75,
            "original_95th_percentile": ori_percentile_95
        }
        re_result = {
            "rewritten_average": re_avg,
            "rewritten_median": re_median,
            "rewritten_75th_percentile": re_percentile_75,
            "rewritten_95th_percentile": re_percentile_95
        }
        Metric.append(ori_result)
        Metric.append(re_result)
        
        result_data.insert(0, Metric)
        with open(self.filtered_path,"w") as file:
            json.dump(result_data, file, indent=4)
        print("Calculate Metrics Done!") # Debug line to check if the script has finished running

def ensure_file_exists(path):
    if not os.path.exists(path):
        with open(path, 'w') as f:
            json.dump([], f)  # Create an empty JSON array if the file does not exist

def parse_arguments():
    parser = argparse.ArgumentParser(description="filter Script")
    parser.add_argument("-q", "--queries_path", type=str, required=True, help="Path to the queries SQL file (JSON format)")
    parser.add_argument("-s", "--storage_path", type=str, required=True, help="Path to the storage SQL file (JSON format)")
    parser.add_argument("-f", "--filtered_path", type=str, required=True, help="Path to the filtered SQL file (JSON format)")
    parser.add_argument("-d", "--dbname", type=str, required=True, help="database name")
    parser.add_argument("-t", "--time_out", type=int, required=True, help="timeout")
    return parser.parse_args()     

if __name__ == "__main__":
    args = parse_arguments()
    queries_path = args.queries_path
    storage_path = args.storage_path
    filtered_path = args.filtered_path
    time_out = args.time_out
    dbname = args.dbname

    ensure_file_exists(storage_path)
    ensure_file_exists(filtered_path)
    # test part
    model = Evaluation(queries_path,storage_path,filtered_path,dbname,time_out)
    # model.evaluate()
    # 加载 JSON 数据

    with open(queries_path, 'r') as file:
        json_content = file.read()
    data = json.loads(json_content)
    print("data load sucessfully!")
    # print(data)
    result = []
    # 遍历 JSON 中的每个项目
    iteration = 0
    equiv_number = 0
    sucess_run_number = 0
    for i, query_info in enumerate(data, start=0):
        query_id = query_info.get("id","")
        # query_id = query_info["id"]
        # 获取 original_query 和 rewritten_query
        iteration += 1
        print("this is the {}-th iteration".format(iteration))
        original_query = query_info.get("original_query", "No original query found")
        rewritten_query = query_info.get("rewritten_query", "No rewritten query found")
        # 输出结果
        print(f"Original Query: {original_query}")
        print(f"Rewritten Query: {rewritten_query}")
        total_original_time,total_rewrite_time,speed_up,times_up,original_result,rewritten_result = model.compare_rewritten(original_query,rewritten_query)
        
        equivalance = False
        if total_original_time != None and total_rewrite_time != None and original_result != -1 and rewritten_result != -1:
            sucess_run_number += 1
        
        if original_result != None and rewritten_result != None and original_result != -1 and rewritten_result != -1 and total_original_time != time_out and total_rewrite_time != time_out:
            equivalance = (original_result == rewritten_result)
            

        if equivalance:
            equiv_number += 1
        result_data = {
            "id": query_id,
            "equivalence": equivalance,
            "original_query": original_query,
            "rewritten_query": rewritten_query,
            "original_execution_time": total_original_time,
            "rewrite_execution_time": total_rewrite_time,
            "speed_up": speed_up,
            "times_up": times_up,
            "original_result": original_result,
            "rewritten_result": rewritten_result            
        }
        result.append(result_data)


    # 将结果写回到 result.json 文件
    with open(storage_path, 'w') as result_file:
        # json.dump(result, result_file, indent=4)
        json.dump([model.convert_to_serializable(item) for item in result], result_file, indent=4)
        print(f"Experiment results appended to {storage_path}")
        print(f"the number of equivalent query is {equiv_number}")
        print(f"the number of sucess run query is {sucess_run_number}/ {iteration}")

    model.cal()
