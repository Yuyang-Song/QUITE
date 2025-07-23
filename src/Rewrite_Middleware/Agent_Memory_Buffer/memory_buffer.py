"""
####################################################################
#                     Agent Memory Buffer                          #
####################################################################

简化的Agent Memory Buffer - 用于管理SQL重写过程中的各种信息

Author: System
Date: 2025-07-23
####################################################################
"""


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
    
    def clear_all_memory(self):
        """清除所有内存内容，包括配置信息"""
        self.initial_sql = None
        self.data_statistics = None
        self.schema_file = None
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
    
    def __repr__(self):
        """简单的字符串表示"""
        active_count = sum(1 for attr in ['initial_sql', 'optimization_advice', 'produced_sql', 
                                         'enhanced_sql', 'report', 'guide_info'] 
                          if getattr(self, attr) is not None)
        return f"AgentMemoryBuffer(active_fields={active_count})"


def create_memory_buffer(data_statistics: str = None, schema_file: str = None) -> AgentMemoryBuffer:
    """
    创建内存缓冲区的简单工厂函数
    """
    return AgentMemoryBuffer(data_statistics, schema_file)
