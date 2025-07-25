import psycopg2
import time
import subprocess
import json
import numpy as np
import statistics
import sys
import os
from pathlib import Path
sys.path.append('../')
sys.path.append('./')

from dotenv import load_dotenv
from decimal import Decimal
from datetime import date
import argparse
from pathlib import Path

PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT", Path(__file__).resolve().parents[2]))
LOAD_PATH = PROJECT_ROOT / "config_file" / ".env"
load_dotenv(dotenv_path= LOAD_PATH)   

class Evaluation():
    def __init__(self,evaluation_queries_path,result_storage_path,filtered_path,timeout = 300):
        self.evaluation_queries_path = evaluation_queries_path
        self.result_storage_path = result_storage_path
        self.filtered_path = filtered_path
        self.timeout = timeout

    def connect_to_database(self, retries=5, wait_time=5):
        db_name = os.getenv("DB_NAME")
        db_user= os.getenv("DB_USER")
        db_password= os.getenv("DB_PASSWORD")
        db_host= os.getenv("DB_HOST")
        db_port= os.getenv("DB_PORT")
        print("Connecting to database with the following parameters:")
        print(f"DB_NAME: {db_name}, DB_USER: {db_user}, DB_HOST: {db_host}, DB_PORT: {db_port}")
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
        """Convert non-serializable Decimal and date types in the data structure to serializable types."""
        if isinstance(obj, Decimal):
            return float(obj)  # Or use str(obj) to convert to string
        elif isinstance(obj, date):
            return obj.isoformat()  # Convert date object to string in YYYY-MM-DD format
        elif isinstance(obj, list):
            return [self.convert_to_serializable(item) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(self.convert_to_serializable(item) for item in obj)
        elif isinstance(obj, set):
            return [self.convert_to_serializable(item) for item in obj]  # Convert to list for serialization
        elif isinstance(obj, dict):
            return {key: self.convert_to_serializable(value) for key, value in obj.items()}
        return obj
    
    def restart_postgresql(self):
        # Use subprocess.run to execute the command and wait for it to complete
        # result = subprocess.run(["brew", "services", "restart", "postgresql@14"], capture_output=True, text=True)
        result = subprocess.run(["service", "postgresql", "restart"], capture_output=True, text=True)
        # Check if the command was successful
        if result.returncode == 0:
            print("PostgreSQL service restarted successfully.")
            # Wait a few seconds to ensure PostgreSQL service is fully started
            time.sleep(3)  # Wait for 3 seconds
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
                # If the query returns no results, ignore the exception
                pass            

            if return_flag == False:
                return end_time - start_time
            else:
                return end_time - start_time, execution_result
        
        except psycopg2.OperationalError as e:
            # If a timeout error is caught, roll back the transaction and return -2
            if "canceling statement due to statement timeout" in str(e):
                conn.rollback()
                print(f"Query execution exceeded {timeout} seconds and was terminated.")
                # self.restart_postgresql()
                return -2
            else:
                # Catch other database errors, roll back the transaction
                conn.rollback()
                print(f"Error executing query: {e}")
                # self.restart_postgresql()
                return None
        
        except psycopg2.Error as e:
            conn.rollback()  # Rollback transaction in case of error
            print(f"Error executing query: {e}")
            if return_flag == False:
                return -1  # If execution fails, return -1
            else:
                return None

        # Exception is the base class for all exceptions
        except Exception as e:
            conn.rollback()  # Rollback transaction in case of error
            raise e
        
        finally:
            # Ensure statement timeout is canceled in all cases (optional)
            cursor.execute("SET statement_timeout = 0;")

    def compare_rewritten(self,original_query,rewritten_query,iteration=1):
        conn = self.connect_to_database()
        cursor = conn.cursor()
        timeout = self.timeout
        total_original_time = 0.0
        total_rewrite_time = 0.0
        original_result = None
        rewritten_result = None

        # Execute original query and record time
        for i in range(iteration + 1):
            ORIGINAL_TIME_OUT = False
            if conn is None:
                return None, None, None, None, None, None  # Return -1 if unable to connect

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
            return None, None, None, None, None, None  # Return -1 if original query fails

        if total_original_time is not None:
            print(f"Original Query Execution Time: {total_original_time:.6f} seconds")
        else:
            print("Original Query Execution Failed")

        self.restart_postgresql()
        if conn is None:
            return None, None, None, None, None, None  # Return -1 if unable to connect
        # Reconnect to the database
        conn = self.connect_to_database()
        cursor = conn.cursor()

        try:
            for i in range(iteration + 1):
                REWRITTEN_TIME_OUT = False 
                if conn is None:
                    return None, None, None, None, None, None  # Return -1 if unable to connect

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
                return total_original_time, None, None, None, original_result, None  # Return -1 if rewritten query fails

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
            # Set the return value of the rewritten query to the error marker value and continue to the next query pair
            return total_original_time, None, None, None, original_result, None
        except Exception as e:
            print(f"Rewritten query execution failed due to unexpected error: {e}")
            # Set the return value of the rewritten query to the error marker value and continue to the next query pair
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
        # Open and read JSON file
        with open(self.evaluation_queries_path, 'r') as file:
            data = json.load(file)

        existing_results = []

        # Check if result.json exists, if so, load it
        if os.path.exists(self.result_storage_path):
            with open(self.result_storage_path, 'r') as result_file:
                try:
                    existing_results = json.load(result_file)
                    # Ensure existing_results is a list
                    if isinstance(existing_results, dict):
                        existing_results = [existing_results]
                    elif not isinstance(existing_results, list):
                        existing_results = []
                except json.JSONDecodeError:
                    existing_results = []

        # Iterate over all SQL pairs in the JSON data
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


        existing_results = sorted(existing_results, key=lambda x: int(x.get("id", 0)))  # Sort by id
        # Write results back to result.json file
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



            # Calculate average
        ori_avg = statistics.mean(original_execution_times)
        print(f"The average execution time is: {ori_avg}")
        # Calculate median
        ori_median = statistics.median(original_execution_times)
        print(f"The median execution time is: {ori_median}")
        # Calculate 75th percentile
        ori_percentile_75 = np.percentile(original_execution_times, 75)
        print(f"The 75th percentile execution time is: {ori_percentile_75}")
        # Calculate 95th percentile
        ori_percentile_95 = np.percentile(original_execution_times, 95)
        print(f"The 95th percentile execution time is: {ori_percentile_95}")

        re_avg = statistics.mean(rewritten_execution_times)
        print(f"The average execution time is: {re_avg}")
        # Calculate median
        re_median = statistics.median(rewritten_execution_times)
        print(f"The median execution time is: {re_median}")
        # Calculate 75th percentile
        re_percentile_75 = np.percentile(rewritten_execution_times, 75)
        print(f"The 75th percentile execution time is: {re_percentile_75}")
        # Calculate 95th percentile
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
    parser.add_argument("-t", "--time_out", type=int, required=True, help="timeout")
    return parser.parse_args()     

if __name__ == "__main__":
    args = parse_arguments()
    queries_path = args.queries_path
    storage_path = args.storage_path
    filtered_path = args.filtered_path
    time_out = args.time_out

    
    ensure_file_exists(storage_path)
    ensure_file_exists(filtered_path)
    # test part
    model = Evaluation(queries_path,storage_path,filtered_path,time_out)

    with open(queries_path, 'r') as file:
        json_content = file.read()
    data = json.loads(json_content)
    print("data load sucessfully!")
    result = []
    iteration = 0
    equiv_number = 0
    sucess_run_number = 0
    for i, query_info in enumerate(data, start=0):
        query_id = query_info.get("id","")
        # Get original_query and rewritten_query
        iteration += 1
        print("this is the {}-th iteration".format(iteration))
        original_query = query_info.get("original_query", "No original query found")
        rewritten_query = query_info.get("rewritten_query", "No rewritten query found")
        # Output results
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


    # Write results back to result.json file
    with open(storage_path, 'w') as result_file:
        json.dump([model.convert_to_serializable(item) for item in result], result_file, indent=4)
        print(f"Experiment results appended to {storage_path}")
        print(f"the number of equivalent query is {equiv_number}")
        print(f"the number of sucess run query is {sucess_run_number}/ {iteration}")

    model.cal()
