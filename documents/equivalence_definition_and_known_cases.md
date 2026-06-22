# Equivalence Definition and Known Cases

## How QUITE defines equivalence

Throughout this work, the equivalence between an original query and its rewrite is
verified by **execution-result equivalence on the benchmark database**: a rewrite is
accepted as equivalent if, when executed against the benchmark instance, it returns
the same result set as the original query.

This is the standard, practical notion of equivalence used by query-rewrite systems,
because deciding **strict semantic (provable) equivalence** for arbitrary SQL is
undecidable in general and intractable for the SQL fragments that appear in these
benchmarks. Execution-result equivalence is what can be checked automatically and at
scale, and it is the criterion behind every `equivalence` flag in
[`experiments_results/`](../experiments_results).

The trade-off is that the two notions can disagree on rare inputs: a rewrite produced
by the model may be judged *equivalent* because it happens to return identical results
**on this particular benchmark instance**, even though it is **not strictly semantically
equivalent** and could diverge on a different database state. This is a limitation of
the model that produces the rewrite, not of the verification: the verifier faithfully
reports what the two queries return on the benchmark.

Below we document a concrete case we found, so the distinction is transparent and the
fully-equivalent rewrite is on record.

---

## Known case: TPC-H Q2 (`tpch`, `id = 4`)

**Status in the result files:** the `equivalence` flag for this query has been set to
`false` in `experiments_results/tpch/QUITE_tpch_63queries.json` and
`experiments_results/tpch/QUITE_hint_tpch_63queries.json` (the same rewrite appears in
both). It is the one case where the model's rewrite returns the same result on the
TPC-H instance but is not strictly semantically equivalent.

### Original query

```sql
select s_acctbal, s_name, n_name, p_partkey, p_mfgr, s_address, s_phone, s_comment
from part, supplier, partsupp, nation, region
where p_partkey = ps_partkey
  and s_suppkey = ps_suppkey
  and p_size = 6
  and p_type like '%NICKEL'
  and s_nationkey = n_nationkey
  and n_regionkey = r_regionkey
  and r_name = 'EUROPE'
  and ps_supplycost = (
        select min(ps_supplycost)
        from partsupp, supplier, nation, region
        where p_partkey = ps_partkey
          and s_suppkey = ps_suppkey
          and s_nationkey = n_nationkey
          and n_regionkey = r_regionkey
          and r_name = 'EUROPE'
      )
order by s_acctbal desc, n_name, s_name, p_partkey
limit 100;
```

The displayed supplier must be located in `EUROPE`, **and** its supply cost must equal
the minimum supply cost for that part **among EUROPE suppliers**.

### Model rewrite (not strictly equivalent)

```sql
WITH min_supplycosts AS (
    SELECT ps_partkey, MIN(ps_supplycost) AS min_ps_supplycost
    FROM partsupp
    INNER JOIN supplier ON supplier.s_suppkey = partsupp.ps_suppkey
    INNER JOIN nation   ON nation.n_nationkey = supplier.s_nationkey
    INNER JOIN region   ON region.r_regionkey = nation.n_regionkey
    WHERE region.r_name = 'EUROPE'
    GROUP BY ps_partkey
)
SELECT s.s_acctbal, s.s_name, n.n_name, p.p_partkey, p.p_mfgr, s.s_address, s.s_phone, s.s_comment
FROM part p
INNER JOIN partsupp ps ON p.p_partkey = ps.ps_partkey
INNER JOIN supplier s  ON s.s_suppkey = ps.ps_suppkey
INNER JOIN nation   n  ON n.n_nationkey = s.s_nationkey
INNER JOIN min_supplycosts m ON p.p_partkey = m.ps_partkey
                            AND ps.ps_supplycost = m.min_ps_supplycost
WHERE p.p_size = 6
  AND p.p_type LIKE '%NICKEL'
ORDER BY s.s_acctbal DESC, n.n_name, s.s_name, p.p_partkey
LIMIT 100;
```

The CTE correctly computes the EUROPE minimum supply cost per part. However, the outer
query **dropped the `region` join and the `r_name = 'EUROPE'` filter on the displayed
supplier**. The outer supplier is now constrained to EUROPE only *indirectly*, through
the cost match `ps.ps_supplycost = m.min_ps_supplycost`.

### Why it is not strictly equivalent

The rewrite returns a **superset** of the original result. Consider a qualifying part
`P` (size 6, type ending in `NICKEL`) where:

- a EUROPE supplier supplies `P` at cost `100.00` (the EUROPE minimum), and
- a non-EUROPE supplier *also* supplies `P` at exactly `100.00`.

- **Original:** the outer `r_name = 'EUROPE'` filter keeps only the EUROPE supplier.
- **Rewrite:** the non-EUROPE supplier's row also satisfies
  `ps_supplycost = 100.00 = min_ps_supplycost` and the part-key match, so it is **also
  returned** — with a non-EUROPE nation/supplier shown.

Every original row is still present, so the difference is strictly *extra*, incorrect
rows whenever a non-EUROPE supplier ties the EUROPE minimum cost.

### Why it passed the execution check

In TPC-H, `ps_supplycost` is a random decimal in `[1.00, 1000.00]` and each part has
only a few suppliers. An exact tie between a non-EUROPE supplier and the EUROPE minimum
for a qualifying part essentially never occurs in the generated instance, so the rewrite
returns the same result set as the original on this database — hence it initially passed
the execution-result check.

### Complete fix (strictly equivalent rewrite)

Restore the `region` join and the `EUROPE` predicate on the displayed supplier in the
outer query (the same shape used by the equivalent Q2 rewrites in
[`effective_rewrite_types/CTE.json`](./effective_rewrite_types/CTE.json) for the ASIA
and AMERICA variants):

```sql
WITH min_supplycosts AS (
    SELECT ps_partkey, MIN(ps_supplycost) AS min_ps_supplycost
    FROM partsupp
    INNER JOIN supplier ON supplier.s_suppkey = partsupp.ps_suppkey
    INNER JOIN nation   ON nation.n_nationkey = supplier.s_nationkey
    INNER JOIN region   ON region.r_regionkey = nation.n_regionkey
    WHERE region.r_name = 'EUROPE'
    GROUP BY ps_partkey
)
SELECT s.s_acctbal, s.s_name, n.n_name, p.p_partkey, p.p_mfgr, s.s_address, s.s_phone, s.s_comment
FROM part p
INNER JOIN partsupp ps ON p.p_partkey = ps.ps_partkey
INNER JOIN supplier s  ON s.s_suppkey = ps.ps_suppkey
INNER JOIN nation   n  ON n.n_nationkey = s.s_nationkey
INNER JOIN region   r  ON r.r_regionkey = n.n_regionkey          -- restored region join
INNER JOIN min_supplycosts m ON p.p_partkey = m.ps_partkey
                            AND ps.ps_supplycost = m.min_ps_supplycost
WHERE p.p_size = 6
  AND p.p_type LIKE '%NICKEL'
  AND r.r_name = 'EUROPE'                                        -- restored EUROPE filter
ORDER BY s.s_acctbal DESC, n.n_name, s.s_name, p.p_partkey
LIMIT 100;
```

With the outer supplier constrained to EUROPE, only EUROPE suppliers achieving the
EUROPE minimum cost are returned — exactly the original semantics. The `region` join is
along `n_regionkey` (each nation maps to a single region), so it introduces no row
duplication and row multiplicities also match. The superset behavior disappears, making
the rewrite strictly semantically equivalent.
