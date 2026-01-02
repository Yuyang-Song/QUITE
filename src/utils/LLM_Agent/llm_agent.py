import json
from openai import OpenAI
import sys
import os
from pathlib import Path
from psycopg2.extras import RealDictCursor
from typing import List, Dict,Any, Optional,Tuple
import textwrap
from tqdm import tqdm 

# Setup project paths
_current_file = Path(__file__).resolve()
_project_root = _current_file.parents[3]
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from src.utils.path_config import setup_python_path, load_project_env
setup_python_path()
load_project_env()

from src.utils.llm_client import GPT
from src.utils.data_distribution import get_statistics_list, get_available_databases
from src.utils.get_data_statistics import get_data_statistics
from src.Rewrite_Middleware.middleware import DBMS


def con_prompt1(data, data_statistics):
    flag = True
    prompt = textwrap.dedent(f"""
    <mission>
    You are an experienced DBA, you are skilled in SQL analysis and optimization, especially in query rewriting. 
    Your mission is to do high-quality query rewrite work for the user.
    You are given a SQL statement document, please follow the steps below.
    Let's think step by step:
    
    <steps>
    1. According to the <doc>, analyze the SQL statement and check if it has any optimization opportunities, inefficiencies, or issues.
    2. Rewrite the SQL query if necessary, making sure to improve performance or readability without changing the expected result.
    3. Use <data_statistics> to help you understand the data distribution and make better decisions.
    4. Ensure the following three standards are met for query rewriting:
        - Executability: The rewritten query should be executable without any errors.
        - Equivalence: The rewritten query must yield identical results as the original query.
        - Efficiency: 
            - Execution Efficiency: The rewritten query should execute more efficiently than the original query.
            - Computational Efficiency: The overhead of the rewriting process should be justified by the time savings during query execution.
    5. Return the answer according to the <json format>.
    6. Do not output any content outside the <json format> block.
    
    <doc>
    {data}

    <data_statistics>
    {data_statistics}
    
    <json format>
    {{
        "rewritten_query": "",  
        "useful": {str(flag).lower()}     
    }}
    """)
    return prompt

def con_prompt2(history):
    
    formatted_history = ""
    for record in history:
        formatted_history += f"""
        ID: {record.get('id', '')}
        Original Query: {record.get('original_query', '')}
        Rewritten Query: {record.get('rewritten_query', '')}
        Explain: {record.get('explain', '')}
        ---
        """
    
    flag = True

    prompt = textwrap.dedent(f"""
    <mission>
    You are an experienced DBA, skilled in SQL analysis and optimization, especially in query rewriting.
    Your mission is to assist in improving the performance of SQL queries through optimization and rewriting.
    You are provided with the history of previous SQL optimization attempts. Your goal is to analyze the history and improve the SQL queries while adhering to the following standards.
    Let's think step by step:
    
    <steps>
    1. Review the <doc> containing historical optimization attempts. Examine the original SQL query and the rewrite attempts made previously.
    2. Analyze the query for optimization opportunities, inefficiencies, or any issues.
    3. Rewrite the SQL query if necessary, ensuring the rewritten query improves performance or readability without altering the expected result.
    4. Ensure the following three standards are met for query rewriting:
        - Executability: The rewritten query should be executable without any errors.
        - Equivalence: The rewritten query must yield identical results as the original query.
        - Efficiency: 
            - Execution Efficiency: The rewritten query should execute more efficiently than the original query.
            - Computational Efficiency: The overhead of the rewriting process should be justified by the time savings during query execution.
    5. Return the answer according to the <json format>.
    6. Do not output any content outside the <json format> block.

    <doc>
    {formatted_history}

    <json format>
    {{
        "rewritten_query": "",
        "useful": {str(flag).lower()}
    }}
    """)
    
    return prompt

history = []
output = []

def save_to_output(query_data):
    output.append(query_data)

def update_history(query_data):
    history.append(query_data)

def save_all_to_json():
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=4)
    
    with open(history_path, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=4)

if __name__ == '__main__':
    gpt = GPT("your_api_key", "model", "your_base_url")  # Replace with your actual API key, model and base URL
    dbms = DBMS()
    DB_NAME = dbms.db_name
    data_statistics = None
    if DB_NAME in get_available_databases():
        print(f"Database {DB_NAME} found, retrieving statistics...")
        data_statistics = get_statistics_list(DB_NAME)
    else:
        print(f"Database {DB_NAME} not found, retrieving statistics from default database...")
        data_statistics = get_data_statistics()
    print(f"Current database: {DB_NAME}")
    print(f"Data statistics: {data_statistics}")

    # Define input and output paths
    input_path = os.path.join(project_root, "dataset", "queries", "tpch_queries.json")
    output_path = os.path.join(current_dir, "output", "tpch_rewrite_output.json")
    history_path = os.path.join(current_dir, "output", "tpch_rewrite_history.json")
    

    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    input_queries = []
    
    with open(input_path, 'r', encoding='utf-8') as f:
        input_queries = json.load(f)
   
    for i in tqdm(range(len(input_queries)), desc="Processing queries"):
        prompt = con_prompt1(input_queries[i], data_statistics)
        res = gpt.get_LLM_response(prompt, json_format=True)
        
        # Handle case where response is a string instead of dict
        if isinstance(res, str):
            try:
                res = json.loads(res)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON response: {e}")
                print(f"Raw response: {res}")
                # Skip this query if we can't parse the response
                continue

        
        if res.get('useful', False):  # if the response is useful
            sql_query = input_queries[i].get('query', '')
            rewritten_sql_query = res.get('rewritten_query', '')
            id = input_queries[i].get('id', '')
            
            
            if sql_query:
                success, explain_info_or_error = dbms.execute_explain(sql_query)
                if success:
                    save_to_output({
                        "id": id,
                        "original_query": sql_query,
                        "rewritten_query": rewritten_sql_query
                    })
                else:
                    update_history({
                        "id": id,
                        "original_query": sql_query,
                        "rewritten_query": rewritten_sql_query,
                        "explain": explain_info_or_error
                    })
                    
                    iteration = 0
                    while iteration < 3:
                        prompt = con_prompt2(history)
                        response = gpt.get_LLM_response(prompt, json_format=True)
                        
                        # Handle case where response is a string instead of dict
                        if isinstance(response, str):
                            try:
                                response = json.loads(response)
                            except json.JSONDecodeError as e:
                                print(f"Error parsing JSON response in iteration {iteration}: {e}")
                                print(f"Raw response: {response}")
                                iteration += 1
                                continue
                        
                        if response.get('useful', False):
                            rewritten_sql_query = response.get('rewritten_query', '')
                            
                            success, explain_info_or_error = dbms.execute_explain(rewritten_sql_query)
                            if success:
                                save_to_output({
                                    "id": id,
                                    "original_query": sql_query,
                                    "rewritten_query": rewritten_sql_query
                                })
                                break
                            else:
                                update_history({
                                    "id": id,
                                    "original_query": sql_query,
                                    "rewritten_query": rewritten_sql_query,
                                    "explain": explain_info_or_error
                                })
                                iteration += 1
                        else:
                            save_to_output({
                                "id": id,
                                "original_query": sql_query,
                                "rewritten_query": rewritten_sql_query
                            })
        else:
            sql_query = input_queries[i].get('query', '')
            id = input_queries[i].get('id', '')
            save_to_output({
                "id": id,
                "original_query": sql_query,
                "rewritten_query": sql_query
            })
        
    save_all_to_json()


