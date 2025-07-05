import json
with open("./MARter_dsb_159.json", "r") as f:
    data = json.load(f)

result = []

for item in data:
    query_id = int(item["id"])
    if query_id % 3 == 1:
        result.append({
            "id": query_id,
            "original_query": item["original_query"],
            "rewritten_query": item["rewritten_query"],
        })

with open("./MARter_dsb_53.json", "w") as f:
    json.dump(result, f, indent=4)