import json
import regex
import requests

def request_explain_api(sql, plan):
    plan = json.dumps(plan)
    url = 'https://explain.tensor.ru/explain'
    question = {"query":sql, "plan": plan, "name": "Q1"}
    question = json.dumps(question)
    
    pattern = r'let explain\s*=\s*(\[(?:[^][]++|(?1))*\])'
    response = requests.post(url, headers={'Content-Type': 'application/json'}, data=question)
    matches = regex.finditer(pattern, response.text, regex.DOTALL)
    for match in matches:
        info = json.loads(match.group(1))
        break  # 只显示第一个匹配的结果
    return info

sql = """select o_year, sum(case when nation = 'BRAZIL' then volume else 0 end) / sum(volume) as mkt_share from ( select extract(year from o_orderdate) as o_year, l_extendedprice * (1 - l_discount) as volume, n2.n_name as nation from part, supplier, lineitem, orders, customer, nation n1, nation n2, region where p_partkey = l_partkey and s_suppkey = l_suppkey and l_orderkey = o_orderkey and o_custkey = c_custkey and c_nationkey = n1.n_nationkey and n1.n_regionkey = r_regionkey and r_name = 'AMERICA' and s_nationkey = n2.n_nationkey and o_orderdate between date '1995-01-01' and date '1996-12-31' and p_type = 'ECONOMY ANODIZED STEEL' ) as all_nations group by o_year order by o_year;"""
plan  = ""
request_explain_api(sql, plan)