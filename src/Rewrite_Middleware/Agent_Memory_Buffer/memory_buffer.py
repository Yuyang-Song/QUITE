"""
####################################################################
#                     Agent Memory Buffer                          #
####################################################################

简化的Agent Memory Buffer - 用于管理SQL重写过程中的各种信息

Author: Yuyang-Song
Date: 2025-07-23
####################################################################
"""
import sys

class AgentMemoryBuffer:
    """
    简化的内存缓冲区，存储SQL重写过程中的关键信息
    """
    
    def __init__(self, data_statistics: str = None, schema_file: str = None):
        """初始化内存缓冲区"""
        
        # 查询相关信息
        self.initial_sql = None
        self.data_statistics = data_statistics
        self.schema_file = schema_file
        
        # 重写过程结果
        self.optimization_advice = None
        self.produced_sql = None
        self.enhanced_sql = None
        
        # 执行计划相关
        self.ori_explain_result = None
        self.re_explain_result = None
        self.imp_explain_result = None
        
        # 报告和指导信息
        self.report = None
        self.guide_info = None
    
    def clear_volatile_memory(self):
        """
        清除易变的内存内容，保留稳定的配置信息
        保留：data_statistics, schema_file
        清除：其他所有内容
        """
        self.initial_sql = None
        self.optimization_advice = None
        self.produced_sql = None
        self.enhanced_sql = None
        self.ori_explain_result = None
        self.re_explain_result = None
        self.imp_explain_result = None
        self.report = None
        self.guide_info = None
    
    def get_status(self):
        """获取当前状态，用于调试"""
        status = {}
        for attr in ['initial_sql', 'data_statistics', 'schema_file', 
                    'optimization_advice', 'produced_sql', 'enhanced_sql',
                    'ori_explain_result', 're_explain_result', 'imp_explain_result',
                    'report', 'guide_info']:
            value = getattr(self, attr)
            status[attr] = 'has_content' if value is not None else 'empty'
        return status

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


def create_memory_buffer(data_statistics: str = None, schema_file: str = None) -> AgentMemoryBuffer:
    """
    创建内存缓冲区的简单工厂函数
    """
    return AgentMemoryBuffer(data_statistics, schema_file)



