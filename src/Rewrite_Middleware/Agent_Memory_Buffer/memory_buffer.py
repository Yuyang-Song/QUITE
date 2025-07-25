import sys

class AgentMemoryBuffer:
    """
    Simplified memory buffer for storing key information during the SQL rewriting process
    """
    
    def __init__(self, data_statistics: str = None, schema_file: str = None):
        """Initialize memory buffer"""

        # Query related information
        self.initial_sql = None
        self.data_statistics = data_statistics
        self.schema_file = schema_file

        # Rewriting process results
        self.optimization_advice = None
        self.produced_sql = None
        self.enhanced_sql = None

        # Execution plan related
        self.ori_explain_result = None
        self.re_explain_result = None
        self.imp_explain_result = None

        # Report and guidance information
        self.report = None
        self.guide_info = None
    
    def clear_volatile_memory(self):
        """
        Clear volatile memory content while retaining stable configuration information
        Retain: data_statistics, schema_file
        Clear: All other content
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
        """Get current status for debugging"""
        status = {}
        for attr in ['initial_sql', 'data_statistics', 'schema_file', 
                    'optimization_advice', 'produced_sql', 'enhanced_sql',
                    'ori_explain_result', 're_explain_result', 'imp_explain_result',
                    'report', 'guide_info']:
            value = getattr(self, attr)
            status[attr] = 'has_content' if value is not None else 'empty'
        return status

class OutputCollector:
    """Tool class for collecting terminal output"""
    def __init__(self):
        self.outputs = []
        self.original_stdout = sys.stdout
        self.current_output = ""
    
    def start_collecting(self):
        """Start collecting output"""
        self.original_stdout = sys.stdout
        sys.stdout = self
    
    def stop_collecting(self):
        """Stop collecting output and return the collected content"""
        sys.stdout = self.original_stdout
        collected = self.current_output
        self.current_output = ""
        return collected
    
    def write(self, text):
        """Override write method to capture output"""
        self.current_output += text
        self.original_stdout.write(text)
    
    def flush(self):
        """Implement flush method to satisfy stdout interface"""
        self.original_stdout.flush()


def create_memory_buffer(data_statistics: str = None, schema_file: str = None) -> AgentMemoryBuffer:
    """
    Simple factory function to create a memory buffer
    """
    return AgentMemoryBuffer(data_statistics, schema_file)



