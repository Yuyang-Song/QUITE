# 打开输入的 test.txt 文件，读取所有行
with open('./pre_transformed.txt', 'r', encoding='utf-8') as infile:
    lines = infile.readlines()

# 将所有行合并成一行，使用空格连接
merged_line = ' '.join(line.strip() for line in lines)

# 将合并后的内容保存到 result.txt 文件
with open('./transformed_result.txt', 'w', encoding='utf-8') as outfile:
    outfile.write(merged_line)

print("合并完成，结果已保存到 transformed_result.txt 文件中。")