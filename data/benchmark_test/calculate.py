import os
import statistics
import numpy as np
import json


input_path = "/home/orderheart/syy/sql_rewriter/data/benchmark_test/Formal_imdb_s1.json"

result = []
with open(input_path, "r") as file:
    data = json.load(file)

execution_times = [info['execution time'] for info in data]

# 计算平均数
avg = statistics.mean(execution_times)
print(f"The average execution time is: {avg}")

# 计算中位数
median = statistics.median(execution_times)
print(f"The median execution time is: {median}")

# 计算75th百分位数
percentile_75 = np.percentile(execution_times, 75)
print(f"The 75th percentile execution time is: {percentile_75}")

# 计算95th百分位数
percentile_95 = np.percentile(execution_times, 95)
print(f"The 95th percentile execution time is: {percentile_95}")

