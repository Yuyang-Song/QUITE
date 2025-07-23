from pathlib import Path
import os
import sys

sys.path.append('../')
sys.path.append('./')

import json
import asyncio
import time
from dotenv import load_dotenv
from src.utils.data_distribution import get_statistics_list, get_available_databases
from src.utils.get_data_statistics import get_data_statistics
from src.Rewrite_Middleware.middleware import DBMS
from src.utils.agent_template import MessageContent, Message, MemoryWindow, MessageQueue
from src.Query_Rewriter.finite_state_machine import QueryRewriteFSM


PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT", Path(__file__).resolve().parents[2]))
LOAD_PATH = PROJECT_ROOT / "config_file" / ".env"
load_dotenv(dotenv_path= LOAD_PATH)                                                                                                                                                                                      
# 初始化运行示例



async def main():
    # 获取当前数据库的统计信息
    dbms = DBMS()
    DB_NAME = dbms.db_name
    if DB_NAME in get_available_databases():
        data_statistics = get_statistics_list(DB_NAME)
    else:
        data_statistics = get_data_statistics()
    
    print(f"Database {DB_NAME} statistics: {data_statistics}")
    
    schema_file = PROJECT_ROOT / "dataset" / "schemas" / "tpch.sql"
    with open(schema_file, 'r') as f:
        schema_content = f.read()
        if not schema_content.strip():
            raise ValueError(f"Schema file {schema_file} is empty or not found.")
        print(f"Schema content loaded from {schema_file}")

    # input_path = PROJECT_ROOT / "dataset" / "queries" / "tpch_hard.json"
    # if not input_path.exists():
    #     raise FileNotFoundError(f"Input file {input_path} does not exist.")
    # save_file_path = PROJECT_ROOT / "output" / "tpch_hard"
    # if not save_file_path.exists():
    #     os.makedirs(save_file_path, exist_ok=True)
    #     print(f"Output directory {save_file_path} created.")
        
    input_path ="/root/syy/QUITE/dataset/queries/tpch_test.json"
    save_file_path = "/root/syy/QUITE/output" 
    count = 0
    batch = 0
    result = []
    MAX_ITERATION_LOOP = 2

    mq = MessageQueue(window_size=8)
    
    with open(input_path, "r") as f:
        data = json.load(f)
        
    fsm = QueryRewriteFSM(mq, dbms, data_statistics, schema_file, MAX_ITERATION_LOOP)


    for item in data:
        print("################################################################################")
        print(f"This is the {count}-th iteration")
        
        initial_sql = item["query"]

        print("Trying to rewrite the SQL query: ", initial_sql)
        
        fsm.initial_sql = initial_sql
        start_time = time.time()
        rewritten_sql = await fsm.run()
        end_time = time.time()
        rewrite_time = end_time - start_time
        print("Rewrite time costs: ", rewrite_time)
        tmp = {
            "id": item["id"],
            "original_query": item["query"],
            "rewritten_query": rewritten_sql,
            "time_cost": end_time - start_time,
            "rewrite_suggestion": fsm.optimization_advice
        }
        result.append(tmp)
        count += 1
        await fsm.clear()
        
        # 每3条保存一次
        if count % 1 == 0:  
            batch += 1
            json_file_name = f"{save_file_path}/batch_{batch}.json"
            txt_file_name = f"{save_file_path}/batch_{batch}.txt"
            with open(json_file_name, "w") as f:
                json.dump(result, f, indent=4)
            
            with open(txt_file_name, "w") as f:
                for r in result:
                    f.write(fsm.terminal_output)
                    f.write("\n")
                
            await fsm.clear_log()

            result = [] # 清空结果列表
    
    # 保存剩余结果
    if result:
        batch += 1
        with open(f"{save_file_path}/batch_{batch}.json", "w") as f:
            json.dump(result, f, indent=4)
        

if __name__ == "__main__":
    asyncio.run(main())


