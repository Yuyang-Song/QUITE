import sys
sys.path.append("../")
sys.path.append("./")
sys.path.append("../../")   
import re
import json
import os
from pathlib import Path
from dotenv import load_dotenv
from typing import List, Dict, Any, Tuple, Optional
from src.utils.llm_client import GPT
from src.Rewrite_Middleware.middleware import DBMS
from src.utils.data_distribution import get_statistics_list, get_available_databases
from src.utils.get_data_statistics import get_data_statistics
from src.Rewrite_Middleware.Agent_Memory_Buffer.memory_buffer import OutputCollector
import textwrap


PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT", Path(__file__).resolve().parents[2]))
LOAD_PATH = PROJECT_ROOT / "config_file" / ".env"
load_dotenv(dotenv_path= LOAD_PATH)   

class Hint_Recommender:
    
    def __init__(self, dbms : DBMS, db_name: Optional[str] = None):
        self.dbms = dbms
        self.llm = GPT(
            api_key=os.getenv("DECISION_MODEL_API_KEY"),
            model=os.getenv("DECISION_MODEL"),
            base_url=os.getenv("DECISION_MODEL_URL")
        )
        self.db_name = db_name or self.dbms.db_name
        self.data_statistics = self._get_data_statistics()
        
        print(f"Database {self.db_name} statistics: {self.data_statistics}")

    def load_data_from_file(self, file_path: str) -> List[Dict[str, Any]]:
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading data from {file_path}: {e}")
            return []
        
    
    def _get_data_statistics(self) -> Any:
        if self.db_name in get_available_databases():
            print(f"Fetching statistics for database: {self.db_name}")
            return get_statistics_list(self.db_name)
        else:
            print(f"Database {self.db_name} not found, using default statistics by scanning the whole database...")
            return get_data_statistics()
    
    def extract_total_cost(self, query_plan: List[Dict]) -> float:
        cost_pattern = re.compile(r'\(cost=\d+\.\d+\.\.(\d+\.\d+)')
        max_cost = 0.0
        
        try:
            for row in query_plan:
                print(row['QUERY PLAN'])
                query_plan_text = row['QUERY PLAN']
                match = cost_pattern.search(query_plan_text)
                if match:
                    cost_value = float(match.group(1))
                    if cost_value > max_cost:
                        max_cost = cost_value
        except (KeyError, TypeError) as e:
            print(f"Data type mismatch in extract_total_cost: {e}")
            print(f"Row type: {type(row)}, Row content: {row}")
            return -1
        
        return max_cost
    
    def get_cost_estimation(self, sql: str, max_retries: int = 3) -> Tuple[float, List[Dict]]:

        for attempt in range(max_retries + 1):
            try:
                print(f"Attempt {attempt + 1} to get plan for SQL")
                operation = self.dbms.get_pure_plan(sql)
                print(f"Operation type: {type(operation)}")
                if operation:
                    print(f"Operation sample: {operation[:2] if len(operation) > 0 else 'Empty'}")
                
                cost = self.extract_total_cost(operation)
                
                if cost == -1:
                    print(f"Data type mismatch detected, retrying... (attempt {attempt + 1})")
                    continue
                else:
                    return cost, operation
                    
            except Exception as e:
                print(f"Error in attempt {attempt + 1}: {e}")
                if attempt == max_retries:
                    print("Max retries reached, returning default cost 0")
                    return 0, []
                continue
        
        return 0, []
    
    def get_analysis_prompt(self, input_sql: str, physical_plan: List[Dict]) -> str:
        prompt = textwrap.dedent(f"""

        <Mission>    
        You are an experienced DBA. Your mission is to analyze the SQL physical plan and identify costly operations to inform efficient query hints。
        You have been given:
        - <input_sql>
        - <physical_plan>
        - <data_statistics> (for the database)
                                 
        <Steps>
        1. Analyze the SQL physical plan and identify the most impactful costly operations that can be addressed using pg_hint_plan hints. Do not modify the query structure, scans, indexes, parallelism, or other advanced features—focus only on hints.

        2. Concentrate on the following hint categories. Report only the most critical items (Recommend MAX 3 hints):
            ## Join Methods:  (NestLoop is used for small table driving large table, HashJoin is used for large data volume)
                Hash join, /*+ NoHashJoin(table table[ table...]) */ 
                No Nested loop join, /*+ NoNestLoop(table table[ table...]) */
                No Merge join, /*+ NoMergeJoin(table table[ table...]) */
                            
            ##  Advanced Control:
                Cardinality estimation(rows) correction,  changes the row number estimation of joins that comes from restrictions in the planner. 
                If you want to use this hint, please give a detailed calculation process in the analysis.
                    /*+ Rows(a b #10) */ (Sets rows of join result to 10)   

        3. Provide a suggestion report on how to improve query performance using only these methods. If you believe the query is not worth optimizing with pg_hint_plan hints, explicitly state that in your report.
                             
        4. If the SQL uses a CTE and you determine the CTE should NOT be materialized, include the hint `/*+ NO_MATERIALIZE(table) */`. Use the following principles:
        - MATERIALIZE if: 
            1) The CTE is referenced multiple times in the query.
            2) The CTE is large and complex.
        - NO MATERIALIZE if:
            1) The CTE is referenced only once.
            2) The CTE is small and simple.
                                                            
        5. Return the results in the following format:

        </analysis>
            //Fill in with your analysis
        </analysis>

        </report>
            //Fill in your report
        </report>

        
        <input_sql>
        {input_sql}

        <physical_plan>
        {physical_plan}

        <data_statistics>
        {self.data_statistics}

        """)
        return prompt
    
    def get_selection_prompt(self, input_sql: str, report: str) -> str:
        prompt = textwrap.dedent(f"""
        <Mission>
            You are an experienced DBA. Your mission is to provide the most efficient pg_hint_plan for the given SQL query based on the analysis report.
            You have been provided with:
            - A reference table illustrating how to use pg_hint_plan
            - <data_statistics> about the database
                                 
        <Steps>
            1. Based on the <report>, determine the single most effective pg_hint_plan to improve SQL performance.
            2. If the report indicates that pg_hint_plan optimization is warranted, return only the pg_hint_plan in JSON format as shown below. Otherwise, return an empty string ("").
            3. Classify hints into "context" hints and "preamble" hints if the SQL includes CTEs:
            - Context hints apply inside a CTE; you must specify the corresponding CTE name. If there are no CTEs, use an empty string ("") for both name and hints.
            - Preamble hints apply at the head of the query (before the main body).

        <Notation>
            1. Return only the pg_hint_plan content (without /*+ */ wrapper), not the entire SQL query.
            2. Provide as few hints as possible, formatted as a single string (not a list).

        <input_sql>
        {input_sql}

        <report>
        {report}

        Please return the answer in the following format:
        ```json
        {{
            "flag": {{flag}},           // true if pg_hint_plan is recommended, false otherwise
            "CTE_flag": {{CTE_flag}},   // true if the query includes CTEs, false otherwise
            "analysis": {{analysis}},   // Your analysis of the SQL query
            "context_pg_hint_plan": [
                {{
                    "CTE_name": "{{name}}",    // The CTE name for the context hint (or "" if none)
                    "pg_hint_plan": "{{hint_content}}"         // ONLY hint content, NO /*+ */ wrapper
                }},
                {{
                    ... // Include additional objects if multiple CTEs exist
                }}   
            ],
            "preamble_pg_hint_plan": "{{hint_content}}"  // ONLY hint content, NO /*+ */ wrapper
        }}
        ```
        """)
        return prompt
    
    def extract_func(self, text: str, label: str) -> str:
        # First, try using the correct XML tag format
        pattern1 = rf'<{label}>\s*(.*?)\s*</{label}>'
        match1 = re.search(pattern1, text, re.DOTALL)
        if match1:
            return match1.group(1).strip()
        
        # If not found, try special format (both start and end tags are the same)
        pattern2 = rf'</{label}>\s*(.*?)\s*</{label}>'
        match2 = re.search(pattern2, text, re.DOTALL)
        if match2:
            return match2.group(1).strip()
        
        return ""
    
    def extract_json(self, text: str) -> List[Dict]:
        pattern = r'```json\s*(.*?)\s*```'
        matches = re.findall(pattern, text, re.DOTALL)
        json_list = []
        for match in matches:
            json_str = match.strip()
            try:
                json_obj = json.loads(json_str)
                json_list.append(json_obj)
            except json.JSONDecodeError:
                print("Invalid JSON format")
                continue
        return json_list
    
    def hint_injection(self, input_sql: str, context_pg_hint_plan: List[Dict], preamble_pg_hint_plan: str) -> str:
        result_sql = input_sql.strip()
        
        # 1. Handle preamble hints (hints before the main query)
        if preamble_pg_hint_plan and preamble_pg_hint_plan.strip():
            formatted_hint = preamble_pg_hint_plan.strip()
            if not formatted_hint.startswith('/*+'):
                formatted_hint = f"/*+ {formatted_hint} */"
            result_sql = f"{formatted_hint}\n{result_sql}"
        
        # 2. Handle CTE context hints
        for cte_hint in context_pg_hint_plan:
            if not cte_hint.get("CTE_name") or not cte_hint.get("pg_hint_plan"):
                continue
                
            cte_name = cte_hint["CTE_name"].strip()
            hint_str = cte_hint["pg_hint_plan"].strip()
            
            if not hint_str:
                continue
            
            # Search for the location of the CTE definition
            pattern = re.compile(
                rf'''
                (                       # Capture Group 1: Prefix (WITH or ,)
                    (?:WITH\s+|,\s*)
                )
                ({re.escape(cte_name)})  # Capture Group 2: CTE name
                (\s+AS\s*)              # Capture Group 3: AS keyword
                (\()                    # Capture Group 4: Opening parenthesis
                ''',
                re.IGNORECASE | re.VERBOSE
            )

            # Check if "NO_MATERIALIZE" is included
            is_no_materialize = f"NO_MATERIALIZE({cte_name})" in hint_str
            
            # Remove the "NO_MATERIALIZE" part from hint_str in order to handle the remaining normal hints
            remaining_hint = hint_str.replace(f"NO_MATERIALIZE({cte_name})", "").strip()
            
            #  Remove empty Hint shells
            if remaining_hint in ["/*+", "*/", "/*+ */"]:
                remaining_hint = ""
            
            # Ensure that the remaining hints are formatted correctly
            if remaining_hint and not remaining_hint.startswith('/*+'):
                remaining_hint = f"/*+ {remaining_hint} */"

            # Build Replacement String
            replacement_parts = [rf'\1{cte_name}'] # # Prefix Sum CTE Name
            
            if is_no_materialize:
                replacement_parts.append(rf' AS NOT MATERIALIZED\4') # AS NOT MATERIALIZED (
            else:
                replacement_parts.append(rf'\3\4') # AS (
                
            if remaining_hint:
                replacement_parts.append(f" {remaining_hint}\n") # Inject the remaining Hint
            
            replacement = "".join(replacement_parts)
            
            # Perform the replacement
            result_sql = pattern.sub(replacement, result_sql, count=1)
        
        return result_sql
    
    def process_single_query(self, original_query : str, input_sql: str,  query_id: str = "unknown") -> Dict[str, Any]:
        print("################################################")
        print(f"this is the query {query_id}")
        hint_cost = 0.0
        # obtain the original query cost estimation
        original_cost, operation = self.get_cost_estimation(input_sql)
        if not operation:
            print("Failed to get execution plan, skipping this query")
            return {
                "id": query_id,
                "original_query": original_query ,
                "rewritten_query_without_hints": input_sql,
                "rewritten_query": input_sql,
                "original_cost": 0,
                "hint_cost": 0,
                "error": "Failed to get execution plan"
            }

        # generate analysis prompt
        report_prompt = self.get_analysis_prompt(input_sql, operation)
        report_result = self.llm.get_LLM_response(report_prompt)
        report = self.extract_func(report_result, "report")

        # generate selection prompt
        prompt = self.get_selection_prompt(input_sql, report)
        result = self.llm.get_LLM_response(prompt)
        json_list = self.extract_json(result)
        
        if json_list and len(json_list) > 0:
            result = json_list[0]
        else:
            # if no valid JSON is returned, return the original query without hints
            return {
                "id": query_id,
                "original_query": original_query,
                "rewritten_query_without_hints": input_sql,
                "rewritten_query": input_sql,
                "original_cost": original_cost,
                "hint_cost": original_cost
            }

        # handle the result
        if result.get("flag", False):
            if result.get("CTE_flag", False):
                context_pg_hint_plan = list(result.get("context_pg_hint_plan", []))
            else:
                context_pg_hint_plan = []
                
            preamble_pg_hint_plan = str(result.get("preamble_pg_hint_plan", ""))
            pg_hint_query = self.hint_injection(input_sql, context_pg_hint_plan, preamble_pg_hint_plan)

            hint_cost, hint_operation = self.get_cost_estimation(pg_hint_query)
            print(f"hint_cost is : {hint_cost}")

            if hint_cost > original_cost * 1.1:
                pg_hint_query = input_sql  # If the cost of the hint is higher than the original cost, then do not use the hint
                hint_cost = original_cost
            else:
                pass
        else:
            pg_hint_query = input_sql  # If no prompt is needed, use the original query
            hint_cost = original_cost  

        return {
            "id": query_id, 
            "original_query": original_query,
            "rewritten_query_without_hints": input_sql,
            "rewritten_query": pg_hint_query,
            "original_cost": original_cost,
            "hint_cost": hint_cost,
        }
    
    def process_batch(self, data_list: List[Dict[str, Any]], save_file_path: str, batch_size: int = 3) -> List[Dict[str, Any]]:
        ans = []
        count = 0
        batch = 0
        
        for item in data_list:
            count += 1
            query_id = item.get("id", f"query_{count}")
            original_query = item.get("original_query", "")
            input_sql = item.get("rewritten_query", "")
            
            if not input_sql:
                print(f"Warning: No SQL found for query {query_id}")
                continue
            
            result = self.process_single_query(input_sql, original_query , query_id)
            
            print("********************************")
            print(json.dumps(result, indent=4))
            print("********************************")
            
            ans.append(result)
            
            # Batch Saving
            if count % batch_size == 0:
                batch += 1
                with open(f"{save_file_path}/batch_{batch}.json", "w") as f:
                    json.dump(ans, f, indent=2)
        


        
