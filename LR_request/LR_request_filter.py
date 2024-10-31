import requests
import json
# Define the API endpoint and the payload

url = "http://localhost:6336/rewriter"
sql_path = "./queries.json"
saved_path = "./parsed_data.json"
schema_path = "./schema.json"

def request_lr(url, sql_path,schema,saved_path):
    result = []
    with open(schema_path, "r") as file:
        schema = json.load(file)
    with open(sql_path, "r") as file:
        queries = json.load(file)

    for item in queries:
        query = item.get('query', '')
        id_number = item.get('id', '')
        payload = {
            "sql": query,
            "schema": schema
        }
        # Make the POST request
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            
            # Extract JSON response
            response_data = response.json()
            # print("Response from API:", response_data)
            
            # Ensure 'data' field exists in response
            if 'data' not in response_data:
                print(f"Warning: 'data' field missing in response for query: {query}")
                continue
            
            # Parse each section from the response
            parsed_data = {
                "sql_info": {
                    "id": id_number,
                    "origin_sql": response_data['data'].get('origin_sql'),
                    "rewritten_sql": (response_data['data'].get('rewritten_sql', "")
                            .replace('\r', '')
                            .replace('\n', ' ')
                            .replace('\\"', '')
                            .replace('\"', ''))
                },
                "execution_cost": {
                    "origin_cost": response_data['data'].get('origin_cost'),
                    "rewritten_cost": response_data['data'].get('rewritten_cost')
                },
                "rewrite_info": {
                    "is_rewritten": response_data['data'].get('is_rewritten'),
                    "origin_sql_node": response_data['data'].get('origin_sql_node'),
                    "rewritten_sql_node": response_data['data'].get('rewritten_sql_node')
                },
                "execution_plan_tree": response_data['data'].get('treeJson'),
                "meta": {
                    "message": response_data.get('message'),
                    "status": response_data.get('status')
                }
            }
            result.append(parsed_data)

        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)
            if 'response' in locals():
                print("Response text:", response.text)  # Only print response if available

    result = sorted(result, key=lambda x: int(x.get("id", 0)))  # 按照 id 排序
    # Save parsed data to a JSON file
    with open(saved_path, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)

    print(f"Parsed data saved to {saved_path}")

request_lr(url, sql_path , schema_path, saved_path)






    
