import json

def process_sql_file(file_path):
    data = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
        for i in range(0, len(lines), 2):
            original_query = lines[i].strip()
            rewritten_query = lines[i+1].strip() if (i + 1) < len(lines) else ""
            
            data.append({
                "original_query": original_query,
                "rewritten_query": rewritten_query
            })
    
    # Convert list to JSON formatted string
    json_output = json.dumps(data, indent=4)
    
    # Output JSON to a file
    output_file = "sql_queries.json"
    with open(output_file, 'w') as json_file:
        json_file.write(json_output)
    
    print(f"Processed {len(data)} SQL queries into JSON format.")
    return output_file

# Use the function with the file path
output_json_file = process_sql_file("./calcite_tests.txt")
print(f"JSON output saved to {output_json_file}")