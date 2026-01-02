import psycopg2
import time
import subprocess
import json
import numpy as np
import statistics
import sys
import os
from pathlib import Path
import collections

# Setup project paths first
_current_file = Path(__file__).resolve()
_project_root = _current_file.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from src.utils.path_config import PROJECT_ROOT, setup_python_path, load_project_env
setup_python_path()
load_project_env()

from decimal import Decimal
from datetime import date
import argparse 

# ============================================================================
# IMPORTANT: Database Restart Warning
# ============================================================================
# This evaluation script uses `systemctl restart postgresql` (or similar) to 
# restart the PostgreSQL database between query executions to ensure fair 
# comparison by clearing database caches.
#
# If you don't have permission to restart PostgreSQL (e.g., shared database, 
# cloud database, or restricted environment), use the --no_restart flag:
#   python evaluation.py ... --no_restart
#
# The --no_restart mode will:
#   - Skip database restart operations
#   - Run each query 5 times instead of 3
#   - Remove the highest and lowest execution times
# ============================================================================

class Evaluation():
    def __init__(self, evaluation_queries_path, result_storage_path, filtered_path, timeout=300, no_restart=False):
        self.evaluation_queries_path = evaluation_queries_path
        self.result_storage_path = result_storage_path
        self.filtered_path = filtered_path
        self.timeout = timeout
        self.no_restart = no_restart
        
        # Set iteration count based on restart mode
        # no_restart mode: 5 iterations, remove max/min, average remaining 3
        # normal mode: 3 iterations, average all
        self.iteration_count = 5 if no_restart else 3

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
        """Convert non-serializable types like Decimal and date in data structures to serializable types."""
        if isinstance(obj, Decimal):
            return float(obj)  
        elif isinstance(obj, date):
            return obj.isoformat()  
        elif isinstance(obj, list):
            return [self.convert_to_serializable(item) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(self.convert_to_serializable(item) for item in obj)
        elif isinstance(obj, set):
            return [self.convert_to_serializable(item) for item in obj]  
        elif isinstance(obj, dict):
            return {key: self.convert_to_serializable(value) for key, value in obj.items()}
        return obj
    
    def restart_postgresql(self):
        """
        Restart PostgreSQL to clear database caches.
        
        This function requires appropriate system permissions:
        - On Linux: sudo systemctl restart postgresql
        - On macOS: brew services restart postgresql
        - On Windows: net stop postgresql && net start postgresql
        
        If you don't have restart permissions, use --no_restart flag.
        """
        if self.no_restart:
            print("⚠️  Database restart skipped (--no_restart mode)")
            return
            
        print("🔄 Restarting PostgreSQL to clear caches...")
        # Try different restart commands based on the system
        commands = [
            ["systemctl", "restart", "postgresql"],      # Linux with systemd
            ["service", "postgresql", "restart"],         # Linux with init.d
            ["brew", "services", "restart", "postgresql"], # macOS with Homebrew
        ]
        
        for cmd in commands:
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    print(f"✅ PostgreSQL restarted successfully using: {' '.join(cmd)}")
                    time.sleep(3)  # wait for PostgreSQL to be fully up
                    return
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
        
        print("⚠️  Warning: Could not restart PostgreSQL. Consider using --no_restart mode.")
        print("   Manual restart commands:")
        print("   - Linux: sudo systemctl restart postgresql")
        print("   - macOS: brew services restart postgresql")

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
                pass            

            if return_flag == False:
                return end_time - start_time
            else:
                return end_time - start_time, execution_result
        
        except psycopg2.OperationalError as e:
            if "canceling statement due to statement timeout" in str(e):
                try:
                    conn.rollback()
                except:
                    pass
                print(f"Query execution exceeded {timeout} seconds and was terminated.")
                # self.restart_postgresql()
                return -2, -2
            else:
                try:
                    conn.rollback()
                except:
                    pass
                print(f"Error exe cuting query: {e}")
                # self.restart_postgresql()
                return None
        
        except psycopg2.Error as e:
            try:
                conn.rollback()  # rollback transaction in case of error
            except:
                pass
            print(f"Error executing query: {e}")
            if return_flag == False:
                return -1  
            else:
                return None
            
        except Exception as e:
            try:
                conn.rollback()  # Rollback transaction in case of error
            except:
                pass
            raise e
        
        finally:
            try:
                cursor.execute("SET statement_timeout = 0;")
            except:
                pass



    def _calculate_average_time(self, times_list):
        """
        Calculate average execution time.
        
        In no_restart mode: Remove highest and lowest, average remaining.
        In normal mode: Average all times.
        """
        if not times_list:
            return 0.0
            
        if self.no_restart and len(times_list) >= 3:
            # Remove highest and lowest, average remaining
            sorted_times = sorted(times_list)
            trimmed_times = sorted_times[1:-1]  # Remove first (min) and last (max)
            avg_time = sum(trimmed_times) / len(trimmed_times)
            print(f"   📊 No-restart mode: Removed min({sorted_times[0]:.4f}s) and max({sorted_times[-1]:.4f}s)")
            print(f"   📊 Averaged {len(trimmed_times)} runs: {avg_time:.4f}s")
            return avg_time
        else:
            # Normal average
            return sum(times_list) / len(times_list)

    def compare_rewritten(self, original_query, rewritten_query, iteration=None):
        # Use instance iteration count if not specified
        if iteration is None:
            iteration = self.iteration_count
            
        conn = self.connect_to_database()
        cursor = conn.cursor()
        timeout = self.timeout
        original_times = []
        rewritten_times = []
        original_result = None
        rewritten_result = None
        
        print(f"📊 Running {iteration} iterations" + (" (no-restart mode)" if self.no_restart else ""))
        
        # execute original query
        for i in range(iteration + 1):
            ORIGINAL_TIME_OUT = False
            if conn is None:
                return None, None, None, None, None, None  
            
            if i == 0:
                print("start init hot database execution")
                original_time, original_result = self.execute_query(conn, cursor, original_query, timeout, return_flag=True)
                print(f"this is the init: original query excute time: {original_time}")
                if original_time == -2:
                    ORIGINAL_TIME_OUT = True
                    break
                elif original_time == -1:
                    break
                else:
                    continue

            original_time = self.execute_query(conn, cursor, original_query, timeout)
            print(f"the {i}-th/{iteration} iteration original query excute time: {original_time}")
            if original_time and original_time > 0:
                original_times.append(original_time)
        
        if ORIGINAL_TIME_OUT:
            total_original_time = timeout
        elif original_times:
            total_original_time = self._calculate_average_time(original_times)
        else:
            print("Original Query Execution Failed")
            return None, None, None, None, None, None 
        
        if total_original_time is not None:
            print(f"Original Query Execution Time: {total_original_time:.6f} seconds")
        else:
            print("Original Query Execution Failed")

        self.restart_postgresql()
        if conn is None:
            return None, None, None, None, None, None 
        
        conn = self.connect_to_database()
        cursor = conn.cursor()

        try:
            for i in range(iteration + 1):
                REWRITTEN_TIME_OUT = False 
                if conn is None:
                    return None, None, None, None, None, None 
                
                if i == 0:
                    print("start init hot database execution")
                    try:
                        rewritten_time, rewritten_result = self.execute_query(conn, cursor, rewritten_query, timeout, return_flag=True)
                    except Exception as e:
                        if "connection" in str(e).lower() or "cursor" in str(e).lower():
                            print(f"Connection error, retrying after restart: {e}")
                            try:
                                cursor.close()
                                conn.close()
                            except:
                                pass
                            self.restart_postgresql()
                            conn = self.connect_to_database()
                            if conn is None:
                                return None, None, None, None, None, None
                            cursor = conn.cursor()
                            rewritten_time, rewritten_result = self.execute_query(conn, cursor, rewritten_query, timeout, return_flag=True)
                        else:
                            raise e
                    print(f"this is the init: rewrite query excute time: {rewritten_time}")
                    if rewritten_time == -2:
                        REWRITTEN_TIME_OUT = True
                        break
                    elif rewritten_time == -1:
                        break
                    else:
                        continue
                rewritten_time = self.execute_query(conn, cursor, rewritten_query, timeout)
                print(f"the {i}-th/{iteration} iteration rewrite query excute time: {rewritten_time}")
                if rewritten_time and rewritten_time > 0:
                    rewritten_times.append(rewritten_time)

            if REWRITTEN_TIME_OUT:
                total_rewrite_time = timeout
            elif rewritten_times:
                total_rewrite_time = self._calculate_average_time(rewritten_times)
            else:
                print("Rewritten Query Execution Failed")
                return total_original_time, None, None, None, original_result, None
            
            if total_rewrite_time is not None:
                print(f"Rewritten Query Execution Time: {total_rewrite_time:.6f} seconds")


        except psycopg2.errors.SyntaxError as e:
            print(f"Rewritten query execution failed due to syntax error: {e}")
            return total_original_time, None, None, None, original_result, None
        except Exception as e:
            print(f"Rewritten query execution failed due to unexpected error: {e}")
            return total_original_time, None, None, None, original_result, None

        
        if total_original_time is not None and total_rewrite_time is not None:
            speed_up = (total_original_time - total_rewrite_time) / total_original_time
            times_up = total_original_time / total_rewrite_time
            print(f"speed_up : {speed_up}")
            print(f"times up: {times_up}x")
        

        return total_original_time, total_rewrite_time, speed_up, times_up, original_result, rewritten_result
            

    def evaluate(self):
        with open(self.evaluation_queries_path, 'r') as file:
            data = json.load(file)

        existing_results = []

        if os.path.exists(self.result_storage_path):
            with open(self.result_storage_path, 'r') as result_file:
                try:
                    existing_results = json.load(result_file)
                    if isinstance(existing_results, dict):
                        existing_results = [existing_results]
                    elif not isinstance(existing_results, list):
                        existing_results = []
                except json.JSONDecodeError:
                    existing_results = []

        for query_pair in data:
            query_id = query_pair.get('id', '')
            original_query = query_pair.get('original_sql', '')
            rewritten_query = query_pair.get('rewritten_sql', '')
            
            if original_query and rewritten_query:
                print(f"Running queries for pair: {original_query[:30]}... and rewritten query.")
                
                original_execution_time, rewrite_execution_time, speed_up, times_up,original_result,rewritten_result = self.compare_rewritten(
                    original_query, rewritten_query, iteration=3
                )
                if original_result != None and rewritten_result != None and original_execution_time != self.timeout and rewrite_execution_time != self.timeout:
                    original_counts = collections.Counter(original_result)
                    rewritten_counts = collections.Counter(rewritten_result)
                    equivalance = (original_counts == rewritten_counts)
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
                    "times_up": times_up              
                }

                existing_results.append(result_data)


        existing_results = sorted(existing_results, key=lambda x: int(x.get("id", 0)))  
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



        # calculate mean
        ori_avg = statistics.mean(original_execution_times)
        print(f"The average execution time is: {ori_avg}")
        # calculate median
        ori_median = statistics.median(original_execution_times)
        print(f"The median execution time is: {ori_median}")
        # calculate 75th percentile
        ori_percentile_75 = np.percentile(original_execution_times, 75)
        print(f"The 75th percentile execution time is: {ori_percentile_75}")
        # calculate 95th percentile
        ori_percentile_95 = np.percentile(original_execution_times, 95)
        print(f"The 95th percentile execution time is: {ori_percentile_95}")

        re_avg = statistics.mean(rewritten_execution_times)
        print(f"The average execution time is: {re_avg}")
        # calculate median
        re_median = statistics.median(rewritten_execution_times)
        print(f"The median execution time is: {re_median}")
        # calculate 75th percentile
        re_percentile_75 = np.percentile(rewritten_execution_times, 75)
        print(f"The 75th percentile execution time is: {re_percentile_75}")
        # calculate 95th percentile
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
    parser = argparse.ArgumentParser(
        description="QUITE Evaluation Script - Evaluate query rewrite performance",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
            Examples:
            # Normal mode (with database restart between queries)
            python evaluation.py -q queries.json -s results.json -f filtered.json -t 300

            # No-restart mode (for environments without restart permission)
            python evaluation.py -q queries.json -s results.json -f filtered.json -t 300 --no_restart

            Note:
            The --no_restart flag is useful when you don't have permission to restart PostgreSQL.
            In this mode, queries are run 5 times, and the average is calculated after removing
            the highest and lowest times to mitigate cold-start effects.
        """
    )
    parser.add_argument("-q", "--queries_path", type=str, required=True, 
                        help="Path to the queries SQL file (JSON format)")
    parser.add_argument("-s", "--storage_path", type=str, required=True, 
                        help="Path to the storage SQL file (JSON format)")
    parser.add_argument("-f", "--filtered_path", type=str, required=True, 
                        help="Path to the filtered SQL file (JSON format)")
    parser.add_argument("-t", "--time_out", type=int, required=True, 
                        help="Query timeout in seconds")
    parser.add_argument("--no_restart", action="store_true", default=False,
                        help="Disable database restart between queries (runs 5 times, removes min/max)")
    return parser.parse_args()     

if __name__ == "__main__":
    args = parse_arguments()
    queries_path = args.queries_path
    storage_path = args.storage_path
    filtered_path = args.filtered_path
    time_out = args.time_out
    no_restart = args.no_restart
    
    if no_restart:
        print("=" * 60)
        print("⚠️  NO-RESTART MODE ENABLED")
        print("=" * 60)
        print("Database will NOT be restarted between query executions.")
        print("Running 5 iterations per query, removing min/max for average.")
        print("=" * 60)

    ensure_file_exists(storage_path)
    ensure_file_exists(filtered_path)
    # test part
    model = Evaluation(queries_path, storage_path, filtered_path, time_out, no_restart=no_restart)
    # model.evaluate()


    with open(queries_path, 'r') as file:
        json_content = file.read()
    data = json.loads(json_content)
    print("data load sucessfully!")

    result = []
    iteration = 0
    equiv_number = 0
    sucess_run_number = 0
    for i, query_info in enumerate(data, start=0):
        query_id = query_info.get("id", "")
        iteration += 1
        print("this is the {}-th iteration".format(iteration))
        print(f"the query id is {query_id}")
        original_query = query_info.get("original_query", "No original query found")
        rewritten_query = query_info.get("rewritten_query", "No rewritten query found")
        print(f"Original Query: {original_query}")
        print(f"Rewritten Query: {rewritten_query}")
        total_original_time,total_rewrite_time,speed_up,times_up,original_result,rewritten_result = model.compare_rewritten(original_query,rewritten_query)
        
        equivalance = False
        if total_original_time != None and total_rewrite_time != None and original_result != -1 and rewritten_result != -1:
            sucess_run_number += 1
        
        if original_result != None and rewritten_result != None and original_result != -1 and rewritten_result != -1 and total_original_time != time_out and total_rewrite_time != time_out:
            original_counts = collections.Counter(original_result)
            rewritten_counts = collections.Counter(rewritten_result)
            equivalance = (original_counts == rewritten_counts)

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
            "times_up": times_up          
        }
        result.append(result_data)

    with open(storage_path, 'w') as result_file:
        # json.dump(result, result_file, indent=4)
        json.dump([model.convert_to_serializable(item) for item in result], result_file, indent=4)
        print(f"Experiment results appended to {storage_path}")
        print(f"the number of equivalent query is {equiv_number}")
        print(f"the number of sucess run query is {sucess_run_number}/ {iteration}")

    model.cal()

