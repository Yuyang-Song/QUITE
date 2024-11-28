import sys
# append the current directory
sys.path.append(".")
# append the path of the parent；// directory
sys.path.append("..")
import json

from core.query_patcher import QueryPatcher
from core.query_rewriter import QueryRewriter
from core.rule_parser import RuleParser
from rules_pool import get_rule

request_data = {
    "query": "SELECT MAX(DISTINCT salary) FROM employees WHERE department = 'Engineering';",
    "db": "postgresql"
}

rule_keys = ['remove_max_distinct']
rules = [get_rule(k) for k in rule_keys]

original_query = request_data['query']
database = request_data['db']

rewritten_query, rewriting_path = QueryRewriter.rewrite(original_query, rules)
rewritten_query = QueryPatcher.patch(rewritten_query, database)
formatted_original_query = QueryRewriter.reformat(original_query)

print(f"original query: {original_query}")
print(f"rewritten query: {rewritten_query}")
print(f"rewriting path:{rewriting_path}")