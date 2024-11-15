import json
import os

input_path = "/home/orderheart/syy/sql_rewriter/data/result_execution/learned_rewrite/tpch/result_ls.json"
output_path = "/home/orderheart/syy/sql_rewriter/data/result_execution/learned_rewrite/tpch/result_ls_transformed.json"

with open(input_path, "r") as file:
    data = json.load(file)

result = []
for item in data:
    # print(item)  # Debug line to check the content of each item
    data = {
        "equivalence": item["equivalence"],
        "original_query": item["original_query"],
        "rewritten_query": item["rewritten_query"],
        "original_execution_time": item["original_execution_time"],
        "rewrite_execution_time": item["rewrite_execution_time"],
        "speed_up": item["speed_up"],
        "times_up": item["times_up"],
    }
    print(data)
    result.append(data)

with open(output_path, "w") as file:
    json.dump(result, file, indent=4)
    print("Done!")  # Debug line to check if the script has finished running

