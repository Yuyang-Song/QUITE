import os
import json

def row_transform_single(input_file_path, output_file_path):    
    # 打开输入的 test.txt 文件，读取所有行
    with open(input_file_path, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    # 将所有行合并成一行，使用空格连接
    merged_line = ' '.join(line.strip() for line in lines)

    # 将合并后的内容保存到 result.txt 文件
    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        outfile.write(merged_line)

    print(f"SQL queries have been successfully transformed and saved to  {output_file_path}")
    

def row_transform_file(input_file_path, output_file_path):
    result = {}

    # 遍历目录下的所有 .sql 文件
    for file_name in os.listdir(input_file_path):
        if file_name.endswith(".sql"):
            file_path = os.path.join(input_file_path, file_name)

            # 读取每个 SQL 文件的内容
            with open(file_path, 'r') as sql_file:
                # 读取所有行，并把它们合并为一行，行与行之间用空格分隔
                sql_query = " ".join(line.strip() for line in sql_file)

            # 将文件名去除后缀作为键名，保存结果
            file_key = os.path.splitext(file_name)[0]
            result[file_key] = {
                "query": sql_query
            }

    # 将结果保存到输出的 JSON 文件中
    with open(output_file_path, 'w') as json_file:
        json.dump(result, json_file, indent=4)

    print(f"SQL queries have been successfully transformed and saved to {output_file_path}")

    
# test
# row_transform_single('./pre_transformed.txt', './transformed_result.txt')

# input_path = "./queries"  
# output_path = "./result.json"  
# row_transform_file(input_path, output_path)