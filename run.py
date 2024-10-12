import os
import json
import textwrap
import sys
from dotenv import load_dotenv
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from utils.gpt import GPT
from sql_advicer import sql_advicer
from multi_agent import MultiAgentSQLRewriter
from evaluation import Evaluation

class SQLRewritePipeline:
    def __init__(self):
        self.original_sql = None
        self.rewritten_sql = None
        self.feedback = None

    # Step 1: Input SQL from JSON
    def input_sql(self, json_file):
        with open(json_file, 'r') as file:
            queries = json.load(file)
        return queries

    # Step 2: Selection Model
    def selection_model(self,input_sql):
        # Implement logic to select the appropriate rule for rewriting
        selection_model = sql_advicer(input_sql)
        response = selection_model.pipeline_rewrite_rule()
        # print(f"{calcite_rule["rewrite_methods_category"]}\n")
        # print(f"{calcite_rule["rewrite_detailed_methods"]}\n")
        # print(f"{calcite_rule["rewrite_analyse"]}\n")
        selected_rule = response["rewrite_detailed_methods"] # Example rule selection process
        selected_analyse = response["rewrite_analyse"]
        return selected_rule,selected_analyse
    
    def suggestion_model(self,input_sql):
        # Implement logic to select the appropriate rule for rewriting
        suggestion_model = sql_advicer(input_sql)
        response = suggestion_model.pipeline_suggestion()
        # print(f"{response["reversed_rewrite_suggestion"]}\n")
        # print(f"{response["reversed_rewrite_analyse"]}\n")
        rewrite_suggestion = response["reversed_rewrite_suggestion"]
        rewrite_analyse = response["reversed_rewrite_analyse"]
        return rewrite_suggestion,rewrite_analyse

    # Step 3: GPT-agent Analysis & DBA Context
    def gpt_agent_analysis(self, input_sql):
        # Mock GPT-agent analysis result
        multi_agent = MultiAgentSQLRewriter(input_sql)
        iteration = 2
        result_data = multi_agent.iterate_process(iteration)
        """            result = {
                "original_query": summary["agent_candidate_sql"],
                "rewritten_query": summary["agent_rewritten_sql"],
                "agent_analysis": summary["agent_analysis"],
            }
        """
        agent_rewrite_sql = result_data["agent_candidate_sql"]
        agent_analysis = result_data["agent_analysis"]
        
        return agent_rewrite_sql, agent_analysis

    # Step 4: Synchronous Request to Generate Rewrite Suggestions
    # def generate_suggestions(self, suggestion):
    #     # Simulate suggestions for SQL rewrite
    #     self.rewritten_sql = "SELECT * FROM table WHERE id IN (SELECT id FROM other_table)"
    #     return self.rewritten_sql

    # Step 5: Equivalence Checker
    def equivalence_checker(self):
        # Mock check for equivalence (use actual tools like SQLSolver or QED in practice)
        return self.original_sql == self.rewritten_sql  # Simplified equivalence check

    # Step 6: Query Plan & Execution Feedback
    def query_execution_feedback(self):
        # Mock feedback based on execution results
        
        self.feedback = "Execution time reduced by 20%"
        return self.feedback

    # Step 7: Inject Feedback and Iterate if Necessary
    def inject_feedback_and_iterate(self,queries_path,storage_path):
        evaluation = Evaluation(queries_path, storage_path)
        total_original_time, total_rewrite_time, speed_up, times_up, original_explain, rewritten_explain = evaluation.compare_rewritten(self.original_sql, self.rewritten_sql)
        
        # 根据EXPLAIN ANALYZE的反馈注入到逻辑中
        if original_explain and rewritten_explain:
            print("Original Query Plan:", original_explain)
            print("Rewritten Query Plan:", rewritten_explain)
            
            # 这里可以根据EXPLAIN结果进一步分析
            if speed_up > 0:
                print(f"Rewritten SQL is faster by {speed_up*100:.2f}%")
                self.feedback = f"Rewritten query is faster by {speed_up*100:.2f}%"
            else:
                print("No significant improvement.")
                self.feedback = "No improvement"
        else:
            print("Failed to get EXPLAIN ANALYZE output.")
            self.feedback = "Failed to analyze queries."

        # 决定使用哪个SQL，基于feedback
        if "faster" in self.feedback:
            return self.rewritten_sql
        else:
            return self.original_sql

    # Save the rewritten SQL back to JSON format
    def save_rewritten_sql(self, rewritten_queries, output_file):
        with open(output_file, 'w') as file:
            json.dump(rewritten_queries, file, indent=4)

    # Full pipeline execution for all queries
    def pipeline(self, input_json, output_json):
        # Load input queries from JSON
        queries = self.input_sql(input_json)
        rewritten_queries = []
        
        # Process each query
        for query_data in queries:
            query_id = query_data["id"]
            self.original_sql = query_data["query"]
            
            print(f"Processing Query ID: {query_id}")
            print("Original SQL:", self.original_sql)
            
            # Step 2: Selection Model
            # input : original_sql
            # output : selected_rule,selected_analyse
            selected_rule,selected_analyse = self.selection_model(self.original_sql)
            print("Selected Rule:", selected_rule,selected_analyse)
            print("Selected Rule:", selected_rule)
            
            # input : original_sql
            # output : rewrite_suggestion,rewrite_analyse
            rewrite_suggestion,rewrite_analyse = self.suggestion_model(self.original_sql)
            print("Rewrite Suggestion:", rewrite_suggestion,rewrite_analyse)
            print("Rewrite Suggestion:", rewrite_suggestion)
            
            # Step 3: GPT-agent Analysis & DBA Context
            
            # input : original_sql
            # output : agent_rewrite_sql, agent_analysis
            rewritten_sql,rewritten_analyse = self.gpt_agent_analysis(selected_rule)
            print("Agent Rewrite SQL:", rewritten_sql)
            print("Agent Analysis:", rewritten_analyse)
            
            # Step 4: Synchronous Request for Rewrite Suggestions
            # rewritten_sql = self.generate_suggestions(suggestion)
            # print("Rewritten SQL:", rewritten_sql)
            
            # Step 5: Equivalence Checker
            is_equivalent = self.equivalence_checker()
            print("Equivalence Check:", "Equivalent" if is_equivalent else "Not Equivalent")
            
            # Step 6: Query Plan & Execution Feedback
            self.query_execution_feedback()
            print("Feedback:", self.feedback)
            
            # Step 7: Inject Feedback and Iterate
            final_sql = self.inject_feedback_and_iterate()
            print("Final SQL:", final_sql)
            
            # Add the result to the rewritten_queries list
            rewritten_queries.append({
                "id": query_id,
                "original_query": self.original_sql,
                "rewritten_query": final_sql
            })
        
        # Save the rewritten queries to the output JSON file
        self.save_rewritten_sql(rewritten_queries, output_json)
        print(f"Rewritten queries saved to {output_json}")

# Example usage:
rewriter = SQLRewritePipeline()
input_json_file = './query_template/tpch/tpch_queries.json'  # Replace with the actual path of your input JSON file
output_json_file = './result/rewritten_queries.json'  # Path to save the rewritten SQLs

rewriter.pipeline(input_json_file, output_json_file)