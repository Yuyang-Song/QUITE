"""
structured knowledge about sql server trnasformisson script with LLM
"""
import os
import json
import textwrap
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from utils.gpt import GPT

class SQL_server_file_preparation_model(GPT):
    def __init__(self, db = "postgres"):
        super().__init__()
        self._define_path()

    def _define_path(self):
        self.sql_server_path = f"../knowledge_pool/official_documents/sql_server"
        self.sql_server_file_path = f"../knowledge_pool/official_documents/sql_server/rewrite_methods"