import json

# 文件读取和转换的函数
def convert_txt_to_json(input_txt_file, output_json_file):
    # 读取txt文件内容
    with open(input_txt_file, 'r', encoding='utf-8') as file:
        agge_rewrite_rules_txt = file.read()

    # 初始化列表来保存每个规则的字典
    rules_list = []
    
    # 处理txt文件中的每一行
    for line in agge_rewrite_rules_txt.strip().splitlines():
        if line.strip():  # 跳过空行
            key, value = line.strip('[]').split(': ', 1)
            key = key.strip('"')
            value = value.strip('",')

            # 为每个规则生成字典并加入到列表
            rule_dict = {
                "method": key,
                "description": value,
                "summary": ""  # 预留 summary 字段，默认为空字符串
            }
            rules_list.append(rule_dict)

    # 将列表转换为JSON格式并写入到json文件
    with open(output_json_file, 'w', encoding='utf-8') as json_file:
        json.dump(rules_list, json_file, indent=4, ensure_ascii=False)

# 调用函数，将txt文件转换为json文件
convert_txt_to_json('./filt_rewrite_rules.txt', './union_rewrite_rules.json')

print("转换完成！JSON文件已生成。")