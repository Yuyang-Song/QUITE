from dotenv import load_dotenv
import json
import os
import asyncio
import sys
import json
import time
from tools import DBMS, RAG
import textwrap
import time
from tools import DBMS_EXPLAIN_Tool, DBMS_syntax_Tool, Knowledge_Pool_Tool, run_sql_solver

sys.path.append('../')
sys.path.append('../utils')
sys.path.append('./')

from agent_role import ReasoningAgent, AssistantAgent, DecisionAgent
from utils.gpt_request import GPT
from utils.agent_template import MessageContent, Message, MemoryWindow, MessageQueue


# os.environ['HTTP_PROXY'] = 'socks5h://127.0.0.1:1080'
# os.environ['HTTPS_PROXY'] = 'socks5h://127.0.0.1:1080'


# load_dotenv(dotenv_path='/root/syy/ MARter_5/config_file/.env')  
# gpt = GPT(
#     api_key=os.getenv("REASONING_MODEL_API_KEY"),
#     model=os.getenv("REASONING_MODEL"),
#     base_url=os.getenv("REASONING_MODEL_URL")
# )
# mq = MessageQueue(window_size=8)
class OutputCollector:
    """收集终端输出的工具类"""
    def __init__(self):
        self.outputs = []
        self.original_stdout = sys.stdout
        self.current_output = ""
    
    def start_collecting(self):
        """开始收集输出"""
        self.original_stdout = sys.stdout
        sys.stdout = self
    
    def stop_collecting(self):
        """停止收集输出并返回收集到的内容"""
        sys.stdout = self.original_stdout
        collected = self.current_output
        self.current_output = ""
        return collected
    
    def write(self, text):
        """重写write方法以捕获输出"""
        self.current_output += text
        self.original_stdout.write(text)
    
    def flush(self):
        """实现flush方法以满足stdout接口"""
        self.original_stdout.flush()




class SQLRewriteFSM:
    """SQL重写有限状态机"""
    def __init__(self, message_queue: MessageQueue, gpt: GPT, dbms: DBMS, data_statistics, schema_file, MAX_ITERATION_LOOP=3):
        self.current_state = "REASONING"
        # self.current_state = "SUMMARY"
        # self.current_state = "VERIFICATION"
        self.llm = gpt
        self.data_statistics = data_statistics
        self.initial_sql = None
        self.optimization_advice = None
        self.produced_sql = None
        self.enhanced_sql = None
        self.re_explain_result = None
        self.ori_explain_result = None
        self.imp_explain_result = None
        self.report = None
        self.dbms = dbms
        self.guide_info = None
        self.iteration = 0
        self.schema_file = schema_file
        self.MAX_ITERATION_LOOP = MAX_ITERATION_LOOP    
        self.terminal_output = None
        self.output_collector = OutputCollector()
        
        # 初始化各Agent
        self.reasoning_agent = ReasoningAgent(message_queue, gpt)
        self.assistant_agent = AssistantAgent(message_queue, gpt)
        self.decision_agent = DecisionAgent(message_queue)
            # 指定文件夹路径
        folder_path = '/root/syy/ MARter_5/src/knowledge_pool/data/results'
        # 指定 JSON 文件存储路径
        json_file_path = '/root/syy/ MARter_5/src/knowledge_pool/data/documents.json'
        self.rag_tool = RAG(folder_path, json_file_path)
        # self.syntax_tool = DBMS_syntax_Tool()
        # self.explain_tool = DBMS_EXPLAIN_Tool()
        
        # 设置观察关系
        self.decision_agent.watch(["ReasoningAgent","ExplainAgent"])
        self.assistant_agent.watch(["SummaryAgent","ExplainAgent"])

    
    async def clear(self):
        """清除所有初始化变量"""
        self.initial_sql = None
        self.current_state = "REASONING"
        self.optimization_advice = None
        self.produced_sql = None
        self.enhanced_sql = None
        self.re_explain_result = None
        self.ori_explain_result = None
        self.imp_explain_result = None
        self.guide_info = None
        self.report = None
        self.iteration = 0
    
    async def clear_log(self):
        if hasattr(self, 'terminal_output'):
            del self.terminal_output
        
    async def run(self):
        self.output_collector.start_collecting()

        while self.current_state != "TERMINATED":
            # with open("./chain.txt", "r") as f:
            #     thought_chain = f.read()
            
            # self.reasoning_agent.send_message(
            # MessageContent(text=thought_chain),
            # role="ReasoiningAgent",
            # receiver="SummaryAgent"
            # )
            if self.current_state == "REASONING":
                await self.state_reasoning()
            # elif self.current_state == "SUMMARY":
            #     await self.state_summary()
            elif self.current_state == "VERIFICATION":
                await self.state_verification()

            elif self.current_state == "DECISION":
                await self.state_decision()
            await asyncio.sleep(0.1)  # 防止事件循环阻塞
        
        terminal_output = self.output_collector.stop_collecting()
        # 将输出存储到FSM的属性中
        self.terminal_output = terminal_output
        
        return self.enhanced_sql
    

    async def state_reasoning(self):
        """推理状态"""
        print("\n=== 进入推理状态 ===")
        explain_info = await DBMS_EXPLAIN_Tool(self.dbms,self.initial_sql)
        if self.report == None:
            reasoning_result = await self.reasoning_agent.analyze_sql(self.initial_sql,self.data_statistics, explain_info)
        else:
            reasoning_result = await self.reasoning_agent.analyze_sql_report(self.initial_sql, self.data_statistics,self.report, explain_info)
        if "TERMINATE" in reasoning_result:
            print("This sql is well down or too easy to give a rewrite process, no need to optimize")
            self.produced_sql = self.initial_sql
            self.enhanced_sql = self.initial_sql
            self.optimization_advice = "No need to optimize"

            self.current_state = "TERMINATED"
        else:
            print("\n=== 开始重写 ===")
            chain = self.decision_agent.retrieve_reasoning_chain()
        
            # with open("./chain.txt", "r") as f:
            #     chain = f.read()
            summary = await self.decision_agent.summarize_chain(chain, self.initial_sql, self.data_statistics)
            
            # 提取结构化结果
            self.produced_sql = self.decision_agent.extract_sql_candidate_content(summary)
            self.enhanced_sql = self.decision_agent.extract_enhanced_sql_content(summary)
            self.optimization_advice = self.decision_agent.extract_advice_content(summary)
            
            self.current_state = "VERIFICATION"

            # self.current_state = "SUMMARY"
        # return reasoning_result

    # async def state_summary(self):
    #     """总结状态"""
    #     print("\n=== 进入总结状态 ===")
    #     # 获取推理过程的思维链
    #     chain = self.decision_agent.retrieve_reasoning_chain()
        
    #     # with open("./chain.txt", "r") as f:
    #     #     chain = f.read()
    #     summary = await self.decision_agent.summarize_chain(chain, self.initial_sql, self.data_statistics)
        
    #     # 提取结构化结果
    #     self.produced_sql = self.decision_agent.extract_sql_candidate_content(summary)
    #     self.enhanced_sql = self.decision_agent.extract_enhanced_sql_content(summary)
    #     self.optimization_advice = self.decision_agent.extract_advice_content(summary)
        
    #     self.current_state = "VERIFICATION"

    async def state_verification(self):
        """报告状态"""
        print("\n=== 进入报告状态 ===")
        syntax_check = await DBMS_syntax_Tool(self.dbms,self.enhanced_sql)
        MAX_CORRECT_TIMES = 0
        MAX_CORRECT_FLAG = False

        # Syntax Check
        if not syntax_check["flag"]:
            print(f"语法错误: {syntax_check['error']}, 尝试优化")
            CHECK_FLAG = False
            while CHECK_FLAG == False and MAX_CORRECT_TIMES < 3:
                print("################ Start correct the error ################")
                checked_sql = await self.assistant_agent._correct_sql(self.initial_sql, self.enhanced_sql, syntax_check["error"]) 
                check_result = await DBMS_syntax_Tool(self.dbms, checked_sql)
                MAX_CORRECT_TIMES += 1
                if check_result["flag"]:
                    CHECK_FLAG = True
                    MAX_CORRECT_FLAG = True
                    print("✓ 语法检查通过")
                    self.enhanced_sql = checked_sql
            if MAX_CORRECT_FLAG == False:
                print("X 语法检查未通过，最大loop到达")
                self.current_state = "REASONING"
                # self.enhanced_sql = self.initial_sql

        else:
            print("✓ 语法检查通过")

        
        # 等价性检查
        MAX_EQUIV_TIMES = 0
        MAX_EQUIV_FLAG = False

        print("进行SQL等价性检查")

        result = await run_sql_solver(self.initial_sql, self.enhanced_sql, self.schema_file, timeout = 10)
        if "EQ" in result:
            print("✓ 通过优化器验证，优化SQL与原始SQL等价")
            CHECK_EQUIV_FLAG = True
            MAX_EQUIV_FLAG = True
        else:
            print("X 未通过优化器验证，调用LLM重写process")
            # 进行等价性检查
            CHECK_EQUIV_FLAG = False
            tmp_checked_sql = self.enhanced_sql
            while CHECK_EQUIV_FLAG == False and MAX_EQUIV_TIMES < 3:
                checked_report = await self.decision_agent.check_equivalence(self.initial_sql, tmp_checked_sql, self.optimization_advice)
                CHCKED_FLAG = self.decision_agent.extract_equivalence_content(checked_report)
                MAX_EQUIV_TIMES += 1
                
                if "true" in CHCKED_FLAG or "True" in CHCKED_FLAG:
                    CHECK_EQUIV_FLAG = True
                    MAX_EQUIV_FLAG = True
                    self.enhanced_sql = tmp_checked_sql
                    print("✓ 优化SQL与原始SQL等价")
                else:
                    print(f"X 优化SQL与原始SQL不等价 (尝试 {MAX_EQUIV_TIMES}/3)")
                    corrected_sql = self.decision_agent.extract_corrected_sql_content(checked_report)
                    if corrected_sql:
                        tmp_checked_sql = corrected_sql
                        print("修正后的优化SQL: ", tmp_checked_sql)
            
            if MAX_EQUIV_FLAG == False:
                print("X 等价性检查未通过，最大尝试次数到达，将使用原始SQL")
                self.enhanced_sql = self.initial_sql


        # checked_report = await self.decision_agent.check_equivalence(self.initial_sql, self.enhanced_sql)
        # CHCKED_FLAG = self.decision_agent.extract_equivalence_content(checked_report)
        # if "true" in CHCKED_FLAG or "True" in CHCKED_FLAG:
        #     print("✓ 优化SQL与原始SQL等价")
        # else:
        #     print("X 优化SQL与原始SQL不等价")
        #     self.enhanced_sql = self.decision_agent.extract_corrected_sql_content(checked_report)
        #     # print("✓ 修正后的优化SQL与原始SQL等价")
        #     print("修正后的优化SQL: ", self.enhanced_sql)
        print(f"原始SQL: {self.initial_sql}")
        print(type(self.initial_sql))
        print(f"优化建议: {self.optimization_advice}")
        print(type(self.optimization_advice))
        print(f"优化SQL: {self.enhanced_sql}")
        print(type(self.enhanced_sql))

        self.current_state = "DECISION"
    

# query_pairs = 
# [
#     {
#          "id" = "1",
#         "original_sql": "SELECT * FROM table WHERE condition",
#         "enhanced_sql": "SELECT * FROM table WHERE condition AND new_condition",
#          "info": [
#               "optimization_advice": ,
#               "report": ,     
#               ]
#     },
#     {
#         "id" = "2",
#         "original_sql": "SELECT * FROM table WHERE condition",
#         "enhanced_sql": "SELECT * FROM table WHERE condition AND new_condition",
#          "info": [    
#               "optimization_advice": ,    
#               "report": ,
#               ]
#     },
#     ...
# ]
    async def selection(self, parallel_output:dict):
        """选择最优SQL"""
        query_pairs = []
        original_sql = self.initial_sql
        for item in parallel_output:
                query_pairs.append({
                    "id": item["id"],
                    "enhanced_sql": ["enhanced_sql"],
                })
        selected_advice = await self.decision_agent.select_sql(original_sql, query_pairs)

        selected_id = await self.decision_agent.extract_selected_id_content(selected_advice)
        
        # 根据select id 组装 parameter
        # self.optimization_advice = 
        # self.report = 
        # self.enhanced_sql =


        # 进入下一个状态
        self.current_state = "DECISION"



    async def state_decision(self):
        """决策状态"""
        print("\n=== 进入决策状态 ===")

        # DBMS EXPLAIN Report Gneration
        print(f"improved SQL: {self.enhanced_sql}")
        self.ori_explain_result = await DBMS_EXPLAIN_Tool(self.dbms,self.initial_sql)
        # self.re_explain_result = await DBMS_EXPLAIN_Tool(self.dbms,self.enhanced_sql)
        self.imp_explain_result = await DBMS_EXPLAIN_Tool(self.dbms,self.enhanced_sql)
        report = await self.assistant_agent.generate_report(
            self.ori_explain_result,
            # self.re_explain_result,
            self.imp_explain_result
        )

        self.report = await self.assistant_agent.extract_analysis_content(report)


        decision = await self.decision_agent.evaluate(
            self.initial_sql,
            self.enhanced_sql,
            self.report
        )
        print("this is the state: ",self.current_state)
        # self.current_state = "TERMINATED"
        if self.iteration < self.MAX_ITERATION_LOOP:
            self.iteration += 1
            if "true" in decision or "True" in decision:
                print("this is the state: ",self.current_state)
                self.current_state = "TERMINATED"
            
            else: # false
                rag_knowledge = await Knowledge_Pool_Tool(self.enhanced_sql, self.optimization_advice)
                self.optimization_advice = await self.decision_agent.merge_advice(
                    self.enhanced_sql, 
                    self.optimization_advice,
                    rag_knowledge
                )
                input_report = {
                    "decision": decision,
                    "pre_rewrite_sql": self.enhanced_sql,
                    "corrected_guide_knowledge": rag_knowledge,
                    
                }
                # erase guide_knowledge in input_report
                self.guide_info = input_report
                self.current_state = "REASONING"
        
        else:
            print("this is the state: ",self.current_state)
            self.enhanced_sql = self.initial_sql
            self.current_state = "TERMINATED"
            self.optimization_advice = "No need to optimize"

        # if decision["terminate"]:
        #     print("✓ 达到终止条件，最终SQL:")
        #     print(textwrap.indent(decision["final_sql"], "    "))
        #     self.current_state = "TERMINATED"
        # else:
        #     print("↻ 需要进一步优化")
        #     self.current_state = "REASONING"


# 在每次保存JSON文件时，将终端输出保存到txt文件
def save_terminal_output_to_file(save_file_path, batch, original_stdout, temp_file):
    # 恢复标准输出
    sys.stdout = original_stdout
    temp_file.close()
    
    # 将临时文件的内容复制到最终文件
    with open(f"{save_file_path}/batch_{batch}.txt", "w") as f:
        with open("temp_output.txt", "r") as temp_f:
            f.write(temp_f.read())
    
    # 重新重定向标准输出到临时文件
    temp_file = open("temp_output.txt", "w")
    sys.stdout = temp_file
    return temp_file


                                                                                                                                                                                      
# 初始化运行示例
async def main():
    # tpch_s1
    # data_statistics = '[["region", "4"], ["nation", "24"], ["customer", "149999"], ["lineitem", "6001214"], ["orders", "1499999"], ["part", "199999"], ["partsupp", "799999"], ["supplier", "9999"]]'

    # tpch_s10
    data_statistics = '[["customer", "1499999"], ["lineitem", "59986051"], ["nation", "24"], ["orders", "14999999"], ["part", "1999999"], ["partsupp", "7999999"], ["region", "4"], ["supplier", "99999"]]'
    
    # tpch_s30
    # data_statistics = '[["region", "4"],["nation", "24"],["customer", "4499999"],["lineitem", "179998371"],["orders", "44999999"],["part", "5999999"],["partsupp", "23999999"],["supplier", "299999"]]'
    
    # tpcds
    # data_statistics = "[['call_center', '24'], ['catalog_page', '12000'], ['catalog_returns', '1439749'], ['catalog_sales', '14401261'], ['customer', '500000'], ['customer_address', '250000'], ['customer_demographics', '1920800'], ['date_dim', '73049'], ['dbgen_version', '1'], ['household_demographics', '7200'], ['income_band', '20'], ['inventory', '133110000'], ['item', '102000'], ['promotion', '500'], ['reason', '45'], ['ship_mode', '20'], ['store', '102'], ['store_returns', '2875432'], ['store_sales', '28800991'], ['time_dim', '86400'], ['warehouse', '10'], ['web_page', '200'], ['web_returns', '719217'], ['web_sales', '7197566'], ['web_site', '42']]"
    # dsb
    # data_statistics = "[['call_center', '24'], ['catalog_page', '12000'], ['customer_address', '250000'], ['customer_demographics', '1920800'], ['date_dim', '73049'], ['dbgen_version', '1'], ['household_demographics', '7200'], ['income_band', '20'], ['item', '102000'], ['reason', '45'], ['ship_mode', '20'], ['store', '102'], ['time_dim', '86400'], ['warehouse', '10'], ['web_site', '42'], ['catalog_returns', '1439749'], ['catalog_sales', '14401261'], ['inventory', '133110000'], ['promotion', '500'], ['web_page', '200'], ['web_returns', '719217'], ['web_sales', '7197566'], ['store_sales', '28800991'], ['customer', '500000'], ['store_returns', '2875432']]"
    # calcite
    # data_statistics = "[['BONUS', '29999999'], ['DEPT', '299999'], ['EMP_B', '29999999'], ['EMP', '29999999'], ['EMPNULLABLES_20', '55'], ['EMPNULLABLES', '29999999']]"
    # calcite_new
    
    # schema_file = "./dsb_schema.sql"
    schema_file = "./tpch_schema.sql"
    # schema_file = "./calcite_schema.sql"


    input_path ="/root/syy/query/tpch/bench_tpch_22.json"
    save_file_path = "/root/syy/MARter_5/src/agent/output/tpch_money_cal" 
    count = 0
    batch = 0
    result = []
    MAX_ITERATION_LOOP = 2

    load_dotenv(dotenv_path='/root/syy/MARter_5/config_file/.env')
    
    gpt = GPT(
        api_key=os.getenv("ASSISTANT_MODEL_API_KEY"),
        model=os.getenv("ASSISTANT_MODEL"),
        base_url=os.getenv("ASSISTANT_MODEL_URL")
    )
    dbms = DBMS()
    
    mq = MessageQueue(window_size=8)
    # initial_sql = "select n_name, sum(l_extendedprice * (1 - l_discount)) as revenue from customer, orders, lineitem, supplier, nation, region where c_custkey = o_custkey and l_orderkey = o_orderkey and l_suppkey = s_suppkey and c_nationkey = s_nationkey and s_nationkey = n_nationkey and n_regionkey = r_regionkey and r_name = 'ASIA' and o_orderdate >= date '1995-01-01' and o_orderdate < date '1995-01-01' + interval '1' year group by n_name order by revenue desc"
    
    with open(input_path, "r") as f:
        data = json.load(f)
        
    fsm = SQLRewriteFSM(mq, gpt, dbms, data_statistics, schema_file, MAX_ITERATION_LOOP)
    # temp_file = open("temp_output.txt", "w")
    # original_stdout = sys.stdout  # 保存原始的标准输出
    # sys.stdout = temp_file  # 将标准输出重定向到临时文件


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
                json.dump(result, f, indent=2)
            
            with open(txt_file_name, "w") as f:
                for r in result:
                    f.write(fsm.terminal_output)
                    f.write("\n")
                
            await fsm.clear_log()
            
            # 保存终端输出到txt文件
            # temp_file = save_terminal_output_to_file(save_file_path, batch, original_stdout, temp_file)

            result = [] # 清空结果列表
    
    # 保存剩余结果
    if result:
        batch += 1
        with open(f"{save_file_path}/batch_{batch}.json", "w") as f:
            json.dump(result, f, indent=2)
        
    #     # 保存终端输出到txt文件
    #     temp_file = save_terminal_output_to_file(save_file_path, batch, original_stdout, temp_file)
    
    # # 恢复标准输出
    # sys.stdout = original_stdout
    # temp_file.close()

    # # 删除临时文件
    # os.remove("temp_output.txt")

if __name__ == "__main__":
    asyncio.run(main())


