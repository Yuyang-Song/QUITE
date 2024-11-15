import os
import json
input_path = "/home/orderheart/syy/sql_rewriter/data/trash/result_queries_multi.json"
out_path = "/home/orderheart/syy/sql_rewriter/data/trash/_trans_result_queries_multi.json"

result = []
with open(input_path, "r") as file:
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

with open(out_path, "w") as file:
    result = sorted(result,key = lambda x: int(x["id"]))
    json.dump(result, file, indent=4)
print("Done!") # Debug line to check if the script has finished running

