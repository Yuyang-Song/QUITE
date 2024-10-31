import os
import json
input_path = "./parsed_data.json"
out_path = "./lr_result_quries.json"

result = []
with open(input_path, "r") as file:
    data = json.load(file)

for item in data:
    info = item.get('sql_info', {})
    id = info.get('id', '')
    origin_sql = info.get('origin_sql', '')
    rewritten_sql = info.get('rewritten_sql', '')
    data = {
        "id": id,
        "original_sql": origin_sql,
        "rewritten_sql": rewritten_sql
    }
    result.append(data)

with open(out_path, "w") as file:
    json.dump(result, file, indent=4)
print("Done!") # Debug line to check if the script has finished running

