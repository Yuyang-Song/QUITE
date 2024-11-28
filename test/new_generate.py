import sys
sys.path.append(".")
sys.path.append("..")
import json
import time

import csv
import logging
import signal
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.query_patcher import QueryPatcher
from core.rule_generator import RuleGenerator
from save_path import rules_pool
import functools
import ctypes
import threading


input_path = "/home/orderheart/syy/QueryBooster/experiments/calcite_tests.csv" # 
save_path = "/home/orderheart/syy/QueryBooster/tests/save_path.py" # 
log_path = "/home/orderheart/syy/QueryBooster/tests/error.log"  # 错误日志路径
TIME_OUT = 5  # 设置超时为5秒

# # 配置日志记录
# logging.basicConfig(
#     filename=log_path,
#     level=logging.ERROR,
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )
# 配置日志记录
logging.basicConfig(
    filename=log_path,
    level=logging.DEBUG,  # Changed to DEBUG to capture more info
    format='%(asctime)s - %(levelname)s - %(message)s'
)
class FuncTimeoutError(TimeoutError):
    """自定义超时错误"""
    pass
# 超时异常

class ThreadKiller(threading.Thread):
    """separate thread to kill TerminableThread"""

    def __init__(self, target_thread, exception_cls, repeat_sec=2.0):
        threading.Thread.__init__(self)
        self.target_thread = target_thread
        self.exception_cls = exception_cls
        self.repeat_sec = repeat_sec
        self.daemon = True

    def run(self):
        """loop raising exception incase it's caught hopefully this breaks us far out"""
        while self.target_thread.is_alive():
            ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(self.target_thread.ident),
                                                       ctypes.py_object(self.exception_cls))
            self.target_thread.join(self.repeat_sec)
class TerminableThread(threading.Thread):
    """a thread that can be stopped by forcing an exception in the execution context"""

    def terminate(self, exception_cls, repeat_sec=2.0):
        if self.is_alive() is False:
            return True
        killer = ThreadKiller(self, exception_cls, repeat_sec=repeat_sec)
        killer.start()

def timeout(sec, repeat_sec=1):
    """
    timeout decorator
    :param sec: function raise TimeoutError after ? seconds
    :param repeat_sec: retry kill thread per ? seconds
        default: 1 second
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):

            result, exception = [], []

            def run_func():
                try:
                    res = func(*args, **kwargs)
                except FuncTimeoutError:
                    pass
                except Exception as e:
                    exception.append(e)
                else:
                    result.append(res)

            # typically, a python thread cannot be terminated, use TerminableThread instead
            thread = TerminableThread(target=run_func, daemon=True)
            thread.start()
            thread.join(timeout=sec)

            if thread.is_alive():
                # a timeout thread keeps alive after join method, terminate and raise TimeoutError
                exc = type('TimeoutError', FuncTimeoutError.__bases__, dict(FuncTimeoutError.__dict__))
                thread.terminate(exception_cls=exc, repeat_sec=repeat_sec)
                err_msg = f'Function {func.__name__} timed out after {sec} seconds'
                raise TimeoutError(err_msg)
            elif exception:
                # if exception occurs during the thread running, raise it
                raise exception[0]
            else:
                # if the thread successfully finished, return its results
                return result[0]

        return wrapped_func
    return decorator

class TimeoutException(Exception):
    pass

# 使用装饰器设置超时为 5 秒
@timeout(sec=5, repeat_sec=1)
def generate_rule_with_timeout(q0, q1, timeout=TIME_OUT):
    result = RuleGenerator.generate_general_rule(q0, q1)
    return result


def process_query(row):
    name = row["name"]
    q0 = row["q2"]
    q1 = row["q1"]
    try:
        recommend_rule_json = generate_rule_with_timeout(q0, q1, timeout=TIME_OUT)

        if recommend_rule_json is None:
            print(f"Error processing query: {name}")
            return None

        print(f"Successfully processed query: {name}")
        recommend_rule_json['pattern'] = QueryPatcher.patch(recommend_rule_json['pattern'], 'postgresql')
        recommend_rule_json['rewrite'] = QueryPatcher.patch(recommend_rule_json['rewrite'], 'postgresql')

        return recommend_rule_json
    except TimeoutError as e:
        print("Timeout Error:", e)
    except Exception as e:
        logging.error(f"Error processing query {name}, q0: {q0}, q1: {q1}, Error: {str(e)}")
        print(f"Error processing query {name}. See log for details.")
        return None

def main():
    rules_pool = []

    # 打开 CSV 文件读取数据
    with open(input_path, 'r') as f:
        reader = csv.DictReader(f)  # 使用 DictReader 读取带有列名的 CSV
        rows = list(reader)
        logging.info(f"Processing {len(rows)} queries...")

        for row in rows:
            result = process_query(row)
            if result is None:
                continue

            print(f"loading {row['name']} into rules_pool")
            input = {
                "id": row["id"],
                "name": row["name"],
                "pattern": result["pattern"],
                "rewrite": result["rewrite"],
                "pattern_json": result["pattern_json"],
                "rewrite_json": result["rewrite_json"],
                "mapping": result["mapping"],
                "constraints": result["constraints"],
                "constraints_json": result["constraints_json"],
                "actions": result["actions"],
                "actions_json": result["actions_json"]
            }
            rules_pool.append(input)

    # 更新 save_path.py 文件
    with open(save_path, 'r') as f:
        content = f.read()

    # print(rules_pool)
    # 替换原有的 rules_pool 定义
    new_content = content.replace("rules_pool = []", f"rules_pool = {json.dumps(rules_pool, indent=4)}")

    # 将更新后的内容写回文件
    with open(save_path, 'w') as f:
        f.write(new_content)

    logging.info("Processing complete.")

if __name__ == "__main__":
    main()