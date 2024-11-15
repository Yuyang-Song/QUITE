#!/bin/bash

# 定义路径变量
input_sql_path="/home/orderheart/syy/sql_rewriter/query_template/tpch/queries.json"
schema_file_path="/path/to/your/schema_file.sql"

output_rewrite_path="/path/to/your/output_file.json"
execution_file_path="/path/to/your/execution_file.json"



# 运行 Python 脚本并传入参数
python /home/orderheart/syy/sql_rewriter/multi_agent.py -i "$input_file_path" -o "$output_file_path" -s "$schema_file_path"
pytthon /home/orderheart/syy/sql_rewriter/evaluation_multi_execute.py -i "$output_file_path" -o "$execution_file_path"
