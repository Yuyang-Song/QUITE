import subprocess
import tempfile
import os
import json
import signal

os.environ['LD_LIBRARY_PATH'] = '/root/syy/MARter_5/src/utils'


def run_sql_solver(sql1_query, sql2_query, schema_file_path, timeout=10, verbose=False):
    """
    调用sqlsolver.jar并返回结果，如果超时则终止进程并返回UNKNOWN
    
    参数:
        sql1_query (str): 第一个SQL查询的内容
        sql2_query (str): 第二个SQL查询的内容
        schema_file_path (str): schema文件的路径
        jar_path (str, optional): jar包路径
        timeout (int): 超时时间（秒）
        verbose (bool): 是否打印详细信息
    
    返回:
        str: jar包执行的输出结果，如果超时则返回"UNKNOWN"
    """
    jar_path = "/root/syy/MARter_5/src/utils/sqlsolver-v1.1.0.jar"
    sql1_query = sql1_query.replace('\n', ' ')
    sql1_query = sql1_query.replace('\"', '')
    sql2_query = sql2_query.replace('\n', ' ')
    sql2_query = sql2_query.replace('\"', '')

    #    print(f"This is the original query: {sql1}")
    #    print(f"This is the rewritten query: {sql2}")

    # 创建临时文件保存SQL查询
    with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', delete=False) as sql1_file:
        sql1_file.write(sql1_query)
        sql1_path = sql1_file.name
        
    with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', delete=False) as sql2_file:
        sql2_file.write(sql2_query)
        sql2_path = sql2_file.name
    
    # 创建临时文件用于输出
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as output_file:
        output_path = output_file.name
    
    process = None
    try:
        if jar_path is None:
            jar_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sqlsolver.jar")
        
        command = [
            "java", "-jar", jar_path,
            f"-sql1={sql1_path}",
            f"-sql2={sql2_path}",
            f"-schema={schema_file_path}",
            f"-output={output_path}"
        ]
        
        if verbose:
            print(f"Executing command: {' '.join(command)}")
            print(f"Setting timeout: {timeout} seconds")
        
        # 启动进程
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        try:
            # 使用超时参数执行命令
            stdout, stderr = process.communicate(timeout=timeout)
            
            if process.returncode != 0:
                if verbose:
                    print(f"Command failed with exit code {process.returncode}")
                    print(f"Error: {stderr}")
                return None
            
            # 读取输出文件
            with open(output_path, 'r') as f:
                result = f.read()
                
            if verbose:
                print(f"Command output: {stdout}")
                print(f"Result: {result}")
                
            return result
            
        except subprocess.TimeoutExpired:
            # 超时处理
            if verbose:
                print(f"Process timed out after {timeout} seconds")
            
            # 强制终止进程
            process.kill()
            try:
                process.wait(timeout=2)  # 给进程一点时间完成终止
            except subprocess.TimeoutExpired:
                if verbose:
                    print("Process still alive after kill, force terminating")
                os.kill(process.pid, signal.SIGKILL)
            
            # 返回UNKNOWN结果
            return "UNKNOWN_TIMEOUT"
    
    finally:
        # 确保进程已经终止
        if process and process.poll() is None:
            try:
                process.kill()
            except:
                pass
        
        # 清理临时文件
        for file_path in [sql1_path, sql2_path, output_path]:
            try:
                os.unlink(file_path)
            except Exception as e:
                if verbose:
                    print(f"Error removing temporary file {file_path}: {e}")


# 使用示例
if __name__ == "__main__":
    # 示例SQL查询
    # sql1 = "select n_name, sum(l_extendedprice * (1 - l_discount)) as revenue from customer, orders, lineitem, supplier, nation, region where c_custkey = o_custkey and l_orderkey = o_orderkey and l_suppkey = s_suppkey and c_nationkey = s_nationkey and s_nationkey = n_nationkey and n_regionkey = r_regionkey and r_name = 'AMERICA' and o_orderdate >= date '1993-01-01' and o_orderdate < date '1993-01-01' + interval '1' year group by n_name order by revenue desc;"
    # sql2 = "WITH america_nations AS (    SELECT n.n_nationkey, n.n_name    FROM nation n    JOIN region r ON n.n_regionkey = r.r_regionkey    WHERE r.r_name = 'AMERICA')SELECT     an.n_name,    SUM(l.l_extendedprice * (1 - l.l_discount)) AS revenueFROM     america_nations an    JOIN supplier s ON s.s_nationkey = an.n_nationkey    JOIN lineitem l ON l.l_suppkey = s.s_suppkey    JOIN orders o ON l.l_orderkey = o.o_orderkey    JOIN customer c ON c.c_custkey = o.o_custkey AND c.c_nationkey = s.s_nationkeyWHERE     o.o_orderdate >= DATE '1993-01-01'    AND o.o_orderdate < DATE '1994-01-01'GROUP BY     an.n_nameORDER BY     revenue DESC;"
    
    # with open("./query.json", "r") as f:
    #     data = json.load(f) 
    
    with open("./query.json", 'r') as file:
        result_data = json.load(file)

    ans = []
    for item in result_data:
        qid = int(item["id"])
        print("#########################################################")
        print(f"This is the query id: {qid}")

        sql1 = item["original_query"]
        sql2 = item["rewritten_query"]
        # sql1 = sql1.replace('\n', ' ')
        # sql1 = sql1.replace('\"', '')
        # sql2 = sql2.replace('\n', ' ')
        # sql2 = sql2.replace('\"', '')

        # print(f"This is the original query: {sql1}")
        # print(f"This is the rewritten query: {sql2}")

        # schema文件路径，请替换成实际路径
        schema_file = "./dsb_schema.sql"
        
        # 自定义jar包路径
        
        # 使用自定义jar包路径
        result = run_sql_solver(sql1, sql2, schema_file,  
                           timeout=10,  # 设置10秒超时
                           verbose=True) 
        
        # UNKOWN,EQ, NEQ, TIMEOUT
        if result == "EQ":
            print("The two queries are equivalent.")
        else:
            print("The two queries are not equivalent.")
            print(result)
            
    #         ans.append(
    #             {
    #                 "id": item["id"],
    #                 "original_query": sql1,
    #                 "rewritten_query": sql2,
    #                 "equivalence": item["equivalence"],
    #                 "result": result
    #             }
    #         )
    #         print(result)
    #     else:
    #         print("Failed to get result from the SQL solver")
    # with open("./dsb_lr_result.json", "w") as f:
    #     json.dump(ans,f, indent=4)
    # print("All queries processed.")


# export LD_LIBRARY_PATH=/root/syy/MARter_5/src/utils
