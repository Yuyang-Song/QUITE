import os

# 文件夹路径
folder_path = './'

# 获取文件夹内所有以 .sql 结尾的文件
sql_files = [f for f in os.listdir(folder_path) if f.endswith('.sql')]

for file_name in sql_files:
    file_path = os.path.join(folder_path, file_name)
    
    # 新文件名：在原文件名前加上 'query_'
    new_file_name = f"query{file_name}"
    new_file_path = os.path.join(folder_path, new_file_name)
    
    # 修改文件名
    os.rename(file_path, new_file_path)

print("文件名修改完成!")