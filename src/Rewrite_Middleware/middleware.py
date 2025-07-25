import psycopg2
import concurrent.futures
import os
import json
import time
import subprocess
import tempfile
import signal
from pathlib import Path
import sys
sys.path.append('../')
sys.path.append('../../')
sys.path.append('./')
from dotenv import load_dotenv
from typing import List, Dict,Any, Optional,Tuple
from psycopg2.extras import RealDictCursor
from src.Rewrite_Middleware.Structured_Knowledge_Base.knowledge_base import Structured_Knowledge_Base
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
            self.connection = psycopg2.connect(
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port
            )
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        except Exception as e:
            print(f"Failed to connect the database system!: {e}")
            raise

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

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
        self.connect()
        try:
            self.cursor.execute(f"EXPLAIN (FORMAT JSON) {sql}")
            result = self.cursor.fetchone()
            explain_result = result['QUERY PLAN'] if result else None

            # Check if explain_result is a string or list and parse accordingly
            if isinstance(explain_result, str):
                self.close()
                return True, json.loads(explain_result)
            elif isinstance(explain_result, list):
                self.close()
                return True, explain_result  # Return list directly
            else:
                self.close()
                return False, "Unexpected EXPLAIN result format."
        except Exception as e:
            error_message = str(e)
            print(f"Error executing EXPLAIN: {error_message}")
            self.close()
            return False, error_message
    
    def execute_ddl(self, sql: str) -> Tuple[bool, Any]:
        """Execute DDL statements (CREATE/ALTER/DROP VIEW)"""
        try:
            self.connect()
            self.cursor.execute(sql)
            self.connection.commit()  # DDL requires explicit commit
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
            # Automatically clean up residual views
            self.connection.set_session(autocommit=False)  # Enable transaction
            for i, query in enumerate(queries):
                clean_query = query.strip().lower()
                # Automatically add IF EXISTS check
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
        try:
            with open(json_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return [item['query'] for item in data]
        except Exception as e:
            print(f"Error reading JSON file: {e}")
            return []

    def execute_statement(self, sql: str):
        """Execute a single SQL statement (non-EXPLAIN)"""
        self.connect()
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            self.close()
        except Exception as e:
            self.close()
            print(f"Error executing statement: {e}")
            raise

# tool_1
async def DBMS_EXPLAIN_Tool(dbms: DBMS, input_sql: str) -> str:
    print("DBMS_EXPLAIN_Tool starts...")

    # Split SQL script into individual statements by semicolon
    statements = [stmt.strip() for stmt in input_sql.split(';') if stmt.strip()]
    
    query_plans = []
    
    try:
        # Iterate through each statement
        for stmt in statements:
            # If it's a CREATE VIEW, execute it first
            if stmt.upper().startswith("CREATE VIEW"):
                dbms.execute_statement(stmt)

            # If it's a SELECT or other statement that needs EXPLAIN, get its execution plan
            if not stmt.upper().startswith("CREATE VIEW") and not stmt.upper().startswith("DROP VIEW"):
                result = dbms.get_pure_plan(stmt)
                if isinstance(result, list):
                    query_plans.extend([item['QUERY PLAN'] for item in result])
                else:
                    query_plans.append(f"Error: {result}")

            # If it's a DROP VIEW, execute it first
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
    # Specify folder path
    folder_path = PROJECT_ROOT / "src" / "Rewrite_Middleware" / "Structured_Knowledge_Base" / "storage"
    json_file_path = folder_path / "documents.json"
    document_path = folder_path / "documents_document_store.pkl"
    print(f"Folder path: {folder_path}")
    print(f"Prject root: {PROJECT_ROOT}")
    rag = Structured_Knowledge_Base(folder_path, json_file_path,document_path)

    start = time.time()

    def retrieve_for_bottleneck(bn_item: Dict[str, Any]) -> str:
        return rag.retrieval(input_sql, bn_item)

    # Use thread pool for concurrent retrieval operations
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers = 8) as executor:
        future_to_bottleneck = {
            executor.submit(retrieve_for_bottleneck, bn): bn
            for bn in origin_suggestion_list
        }

        # Collect execution results from each task and merge them in completion order
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

    # Further process or combine results based on requirements
    final_output = json.dumps(results, indent=2, ensure_ascii=False)
    print("Knowledge Pool ends! Retrieved Knowledge:",final_output)
    return final_output



# tool_3
async def DBMS_Syntax_Tool(dbms: DBMS, test_sql: str) -> Dict[str, Any]:
    print("DBMS_syntax_Tool starts...")

    dbms.connect()

    # Call execute_explain to test SQL syntax
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
    Call sqlsolver.jar and return results, terminate process and return UNKNOWN if timeout occurs.
    
    Args:
        sql1_query (str): Content of the first SQL query
        sql2_query (str): Content of the second SQL query
        schema_file_path (str): Path to the schema file
        jar_path (str, optional): Path to jar package
        timeout (int): Timeout duration (seconds)
        verbose (bool): Whether to print detailed information
    
    Returns:
        str: Output result from jar execution, returns "UNKNOWN_TIMEOUT" if timeout occurs
    """
    os.environ['LD_LIBRARY_PATH'] = str(PROJECT_ROOT / "src" / "Rewrite_Middleware" / "Hybrid_SQL_Corrector" )

    jar_path = PROJECT_ROOT / "src" / "Rewrite_Middleware" / "Hybrid_SQL_Corrector" / "sqlsolver-v1.1.0.jar"
    
    sql1_query = sql1_query.replace('\n', ' ')
    sql1_query = sql1_query.replace('\"', '')
    sql2_query = sql2_query.replace('\n', ' ')
    sql2_query = sql2_query.replace('\"', '')

    # print(f"This is the original query: {sql1_query}")
    # print(f"This is the rewritten query: {sql2_query}")

    # Create temporary files to save SQL queries
    with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', delete=False) as sql1_file:
        sql1_file.write(sql1_query)
        sql1_path = sql1_file.name
        
    with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', delete=False) as sql2_file:
        sql2_file.write(sql2_query)
        sql2_path = sql2_file.name
    
    # Create temporary file for output
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
        
        # Start process
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        try:
            # Execute command with timeout parameter
            stdout, stderr = process.communicate(timeout=timeout)
            
            if process.returncode != 0:
                if verbose:
                    print(f"Command failed with exit code {process.returncode}")
                    print(f"Error: {stderr}")
                return None
            
            # Read output file
            with open(output_path, 'r') as f:
                result = f.read()
                
            if verbose:
                print(f"Command output: {stdout}")
                print(f"Result: {result}")
                
            return result
            
        except subprocess.TimeoutExpired:
            # Timeout handling
            if verbose:
                print(f"Process timed out after {timeout} seconds")
            
            # Force terminate process
            process.kill()
            try:
                process.wait(timeout=2)  # Give process some time to complete termination
            except subprocess.TimeoutExpired:
                if verbose:
                    print("Process still alive after kill, force terminating")
                os.kill(process.pid, signal.SIGKILL)
            
            # Return UNKNOWN result
            return "UNKNOWN_TIMEOUT"
    
    finally:
        # Ensure process is terminated
        if process and process.poll() is None:
            try:
                process.kill()
            except:
                pass
        
        # Clean up temporary files
        for file_path in [sql1_path, sql2_path, output_path]:
            try:
                os.unlink(file_path)
            except Exception as e:
                if verbose:
                    print(f"Error removing temporary file {file_path}: {e}")