import json

def pretty_print_json(json_data):
    # 使用 json.dumps 格式化输出，设置缩进为 4 个空格
    print(json.dumps(json_data, indent=4, ensure_ascii=False))

# 示例 JSON 数据
analysis = {
    "agent_candidate_sql": "WITH min_supplycost AS (\n    SELECT p_partkey, MIN(ps_supplycost) AS min_cost\n    FROM partsupp ps\n    JOIN supplier s ON ps.s_suppkey = s.s_suppkey\n    JOIN nation n ON s.s_nationkey = n.n_nationkey\n    JOIN region r ON n.n_regionkey = r.r_regionkey\n    WHERE r.r_name = 'ASIA'\n    GROUP BY p_partkey\n)\nSELECT s.s_acctbal, s.s_name, n.n_name, p.p_partkey, p.p_mfgr, s.s_address, s.s_phone, s.s_comment\nFROM part p\nJOIN partsupp ps ON p.p_partkey = ps.ps_partkey\nJOIN supplier s ON ps.ps_suppkey = s.s_suppkey\nJOIN nation n ON s.s_nationkey = n.n_nationkey\nJOIN region r ON n.n_regionkey = r.r_regionkey\nJOIN min_supplycost msc ON p.p_partkey = msc.p_partkey AND ps.ps_supplycost = msc.min_cost\nWHERE p.p_size = 46\nAND p.p_type LIKE '%NICKEL'\nAND r.r_name = 'ASIA'\nORDER BY s.s_acctbal DESC, n.n_name, s.s_name, p.p_partkey\nLIMIT 100;",
    "agent_analysis": "The original query uses implicit joins and a correlated subquery with a MIN function, which can degrade performance. The subquery is recalculated for each row, which is inefficient. Additionally, the LIKE '%NICKEL' predicate can hinder performance, and the query lacks explicit joins, which can lead to confusion and poor readability. The rewritten query uses explicit joins and optimizes the subquery by converting it into a Common Table Expression (CTE) to precompute the minimum supply cost.",
    "is_optimized": "true",
    "agent_suggestions": [
        "Rewrite the query using explicit JOIN syntax for better clarity and optimization.",
        "Convert the subquery with MIN(ps_supplycost) into a CTE to avoid recalculating it for every row in the outer query.",
        "Consider indexing on columns used in the joins and where clauses, especially 'p_partkey', 'ps_partkey', 's_suppkey', 'ps_supplycost', and 's_acctbal'.",
        "Review the use of the LIKE '%NICKEL' predicate and consider alternatives like full-text indexing if appropriate."
    ]
}

# 调用函数输出格式化后的 JSON 数据
pretty_print_json(analysis)