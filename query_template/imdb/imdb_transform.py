import os
import json

def row_transform_file(input_file_path, output_file_path):
    existing_results = []

    # 遍历目录下的所有 .sql 文件
    for file_name in os.listdir(input_file_path):
        if file_name.endswith(".sql") and file_name not in ["fkindexes.sql", "schema.sql"]:
            file_path = os.path.join(input_file_path, file_name)

            # 读取每个 SQL 文件的内容
            with open(file_path, 'r') as sql_file:
                # 读取所有行，并把它们合并为一行，行与行之间用空格分隔
                sql_query = " ".join(line.strip() for line in sql_file)

            # 将文件名去除后缀作为键名，保存结果
            file_key = os.path.splitext(file_name)[0]
            
            result = {
                "id": file_key,
                "query": sql_query
            }
        existing_results.append(result)

    # 将结果保存到输出的 JSON 文件中
    with open(output_file_path, 'w') as json_file:
        json.dump(existing_results, json_file, indent=4)

    print(f"SQL queries have been successfully transformed and saved to {output_file_path}")


row_transform_file('./join-order-benchmark','./imdb.json')
