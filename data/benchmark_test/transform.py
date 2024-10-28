import os
import json

def transform(input_file1,input_file2,output_file):
    with open(input_file1, 'r') as file:
        data1 = json.load(file)
    with open(input_file2, 'r') as file:
        data2 = json.load(file)

    
    data = []

    for queries in data1:
        query = queries["query"]
        time = queries["execution time"]
        for item in data2:
            if item["query"] == query:
                result = {
                    "id": item["id"],
                    "query": query,
                    "execution_time": time,
                }
                data.append(result)
    
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)
        #     with open(output_sql_file, 'w') as output_file:
#         json.dump(result, output_file, indent=4)
#     print(f"Experiment results appended to {output_sql_file}")

input_file1 = "/home/orderheart/syy/sql_rewriter/data/benchmark_test/result_tpch_1.json"
input_file2 = "/home/orderheart/syy/sql_rewriter/query_template/tpch/queries.json"
output_file = "/home/orderheart/syy/sql_rewriter/data/benchmark_test/transformed_result_tpch_1.json"

transform(input_file1,input_file2,output_file)
