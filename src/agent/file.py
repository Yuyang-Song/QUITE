import json
import os 

result = []
# 遍历当前目录下的所有json文件
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".json"):
            with open(os.path.join(root, file), "r") as f:
                try:
                    data = json.load(f)
                    for item in data:
                        result.append(item)
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from file: {file}")

with open("./result.json", "w") as f:
    json.dump(result, f, indent=4)