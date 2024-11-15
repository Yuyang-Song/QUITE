import psycopg2
import time
import json
import os
import numpy as np
import statistics
import subprocess
from dotenv import load_dotenv
from decimal import Decimal
from datetime import date


# queries_path ="/home/orderheart/syy/sql_rewriter/query_template/imdb/"
queries_path = "/root/syy/queries/tpch/queries.json"
storage_path = "/root/syy/results/tpch/benchmark_test_s1.json"
filtered_path = "/root/syy/results/tpch/filtered_benchmark_test_s1.json"
time_out = 300

class Evaluation():
    def __init__(self,evaluation_queries_path,result_storage_path,filtered_path,timeout):
        self.evaluation_queries_path = evaluation_queries_path
        self.result_storage_path = result_storage_path
        self.filtered_path = filtered_path
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

    # def restart_postgresql(self):
    #     # 使用 subprocess.run 来执行命令并等待其完成
    #     # result = subprocess.run(["brew", "services", "restart", "postgresql@14"], capture_output=True, text=True)
    #     result = subprocess.run(["docker", "exec", "syy_db", "/bin/bash", "service", "postgresql", "restart"], capture_output=True, text=True)
    #     # 检查命令是否成功执行
    #     if result.returncode == 0:
    #         print("PostgreSQL service restarted successfully.")
    #         # 等待几秒，确保PostgreSQL服务完全启动
    #         time.sleep(3)  # 等待5秒
    #     else:
    #         print(f"Failed to restart PostgreSQL service. Error: {result.stderr}")
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

    def execute_query(self, conn, cursor, query, timeout,return_flag=False):
        # try:
        #     # 设置 PostgreSQL 的 statement 超时
        #     # timeout 以毫秒为单位，所以将秒数乘以 1000
        #     cursor.execute(f"SET statement_timeout = {timeout * 1000};")
        #     # print(f"query:{query}")
        #     start_time = time.time()
        #     cursor.execute(query)
        #     cursor.fetchall()  # 获取所有结果
        #     conn.commit()  # 提交事务
        #     end_time = time.time()
        #     return end_time - start_time
        
        try:
            # Set PostgreSQL statement timeout
            cursor.execute(f"SET statement_timeout = {timeout * 1000};")
            start_time = time.time()
            
            # Execute the query
            cursor.execute(query)
            
            # Only fetch results if the query is a SELECT statement
            if query.strip().lower().startswith("select"):
                execution_result = cursor.fetchall()  # Fetch all results
                conn.commit()  # Commit transaction
            else:
                execution_result = None  # No results to fetch for non-SELECT queries
            
            end_time = time.time()

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
                return -2
            else:
                # 捕获其他数据库错误，回滚事务
                conn.rollback()
                print(f"Error exe cuting query: {e}")
                # self.restart_postgresql()
                return None
            
        # Exception 是所有异常的基类
        except Exception as e:
            conn.rollback()  # Rollback transaction in case of error
            raise e



        finally:
            # 确保在任何情况下都取消超时设置（可选）
            cursor.execute("SET statement_timeout = 0;")

    def tranform_file(self):
        result = []
        with open(self.result_storage_path, "r") as file:
            data = json.load(file)

        for info in data:
            id = info.get('id', '')
            query = info.get('query', '')
            time = info.get('execution time', '')
            data = {
                "id": id,
                "query": query,
                "execution_time": time
            }
            result.append(data)

        with open(self.filtered_path, "w") as file:
            result = sorted(result,key = lambda x: int(x["id"]))
            json.dump(result, file, indent=4)
        print("Filted Result Done!") # Debug line to check if the script has finished running
    
    def cal(self):
        with open(self.filtered_path, "r") as file:
            data = json.load(file)
            execution_times = [info['execution_time'] for info in data]
            # 计算平均数
        avg = statistics.mean(execution_times)
        print(f"The average execution time is: {avg}")
        # 计算中位数
        median = statistics.median(execution_times)
        print(f"The median execution time is: {median}")
        # 计算75th百分位数
        percentile_75 = np.percentile(execution_times, 75)
        print(f"The 75th percentile execution time is: {percentile_75}")
        # 计算95th百分位数
        percentile_95 = np.percentile(execution_times, 95)
        print(f"The 95th percentile execution time is: {percentile_95}")
        result = {
            "average": avg,
            "median": median,
            "75th_percentile": percentile_75,
            "95th_percentile": percentile_95
        }
        with open(self.filtered_path, "w") as file:
            data = json.load(file)
            data.insert(0, result)
            json.dump(data, file, indent=4)
        print("Calculate Metrics Done!") # Debug line to check if the script has finished running

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
        iterate_range = 4
        conn = self.connect_to_database()
        cursor = conn.cursor()
        for query_pair in data:
            TIME_OUT = False
            query = query_pair.get('query', '')
            id_number = query_pair.get('id','')
            print(f"this is the {iteration} times execution: execution {id_number} queries")
            iteration += 1
            time = 0
            for i in range(iterate_range):
                if i == 0:
                    iterate_time = self.execute_query(conn, cursor,query,self.timeout)
                    print(f"this is the init execution time:{iterate_time}")
                    if iterate_time == -2:
                        TIME_OUT = True
                        break
                    else:
                        continue
                # iteration_time = self.execute_query(conn, cursor,query,self.timeout)
                iteration_time, result = self.execute_query(conn, cursor, query, self.timeout, return_flag=True)
                print(f"the {i}-th iteration_time:",iteration_time)
                # print(f"the {i}-th result:",result)
                time += iteration_time   
            if TIME_OUT == False: 
                time = time/(iterate_range-1)
            else:
                time = self.timeout
            print(f"time costs: {time}\n")    
            result_data = {
                "id": id_number,
                "query": query,
                "execution time" :time,
                "result": self.convert_to_serializable(result)
            }

            existing_results.append(result_data)
            # # query11.sql ,query4.sql ,query74.sql,query95.sql,query1.sql
            # if(id_number in ["11","4","74","95","1"]):
            #     print(f"this is the {iteration} times execution: execution {id_number} queries")
            #     iteration += 1
            #     time = self.execute_query(conn, cursor,query,self.timeout)    
            #     print(f"time costs: {time}\n")    
            #     result_data = {
            #         "query": query,
            #         "execution time" :time
            #     }

            #     existing_results.append(result_data)

        cursor.close()
        conn.close()
        #  将结果按照 id 升序排序
        existing_results = sorted(existing_results, key=lambda x: x["id"])
        # 将结果写回到 result.json 文件
        with open(self.result_storage_path, 'w') as result_file:
            json.dump(existing_results, result_file, indent=4)

        print(f"Experiment results appended to {self.result_storage_path}")

        self.tranform_file()
        self.cal()


    def restart_postgresql(self):
        # 使用 subprocess.run 来执行命令并等待其完成
        # result = subprocess.run(["brew", "services", "restart", "postgresql@14"], capture_output=True, text=True)
        result = subprocess.run(["docker", "exec", "syy_db", "/bin/bash", "service", "postgresql", "restart"], capture_output=True, text=True)
        # 检查命令是否成功执行
        if result.returncode == 0:
            print("PostgreSQL service restarted successfully.")
            # 等待几秒，确保PostgreSQL服务完全启动
            time.sleep(5)  # 等待5秒
        else:
            print(f"Failed to restart PostgreSQL service. Error: {result.stderr}")
        


# test part
model = Evaluation(queries_path,storage_path,filtered_path,time_out)
model.evaluate()
