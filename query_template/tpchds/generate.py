import os
import json

def clean_sql(sql):
    """
    清理SQL语句，去掉注释和空行，并将其转换为单行字符串，使用空格间隔每个单词。
    """
    lines = sql.split('\n')
    clean_lines = []
    
    for line in lines:
        line = line.strip()
        if line.startswith('--') or not line:
            continue
        clean_lines.append(line)
    
    return ' '.join(clean_lines)

def process_sql_files(directory):
    """
    处理指定目录下的所有SQL文件，将其转换为JSON格式并保存。
    """
    data = []
    
    for filename in os.listdir(directory):
        if filename.endswith('.sql'):
            with open(os.path.join(directory, filename), 'r') as file:
                sql_content = file.read()
                query_name = os.path.splitext(filename)[0].replace('query', '', 1)  # 去除前缀 'query'  # 使用文件名作为查询名称
                result = {
                    "id": query_name, 
                    "query": clean_sql(sql_content)
                }
            data.append(result)
    
    # 将数据保存为JSON格式
    with open(os.path.join(directory, 'queries.json'), 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Processed {len(data)} SQL files and saved to queries.json")

# 使用示例
directory = './'  # 指定包含SQL文件的目录
process_sql_files(directory)