# TPC-H Dataset:





## Q1：Original Query

> **Execution Time：** > 300s

```sql
SELECT
  s_acctbal,
  s_name,
  n_name,
  p_partkey,
  p_mfgr,
  s_address,
  s_phone,
  s_comment
FROM
  part,
  supplier,
  partsupp,
  nation,
  region
WHERE
  p_partkey = ps_partkey
  AND s_suppkey = ps_suppkey
  AND p_size = 3
  AND p_type LIKE '%NICKEL'
  AND s_nationkey = n_nationkey
  AND n_regionkey = r_regionkey
  AND r_name = 'AMERICA'
  AND ps_supplycost = (
    SELECT
      MIN(ps_supplycost)
    FROM
      partsupp,
      supplier,
      nation,
      region
    WHERE
      p_partkey = ps_partkey
      AND s_suppkey = ps_suppkey
      AND s_nationkey = n_nationkey
      AND n_regionkey = r_regionkey
      AND r_name = 'AMERICA'
  )
ORDER BY
  s_acctbal DESC,
  n_name,
  s_name,
  p_partkey
LIMIT 100;
````



## 1. Rewrite Results

### 1.1. LearnedRewrite

> **Execution Time：** 74.71s

```sql
SELECT
  t1561.s_acctbal,
  t1561.s_name,
  t1561.n_name,
  t1561.p_partkey,
  t1561.p_mfgr,
  t1561.s_address,
  t1561.s_phone,
  t1561.s_comment
FROM (
  SELECT
    t1547.p_partkey,
    t1547.p_name,
    t1547.p_mfgr,
    t1547.p_brand,
    t1547.p_type,
    t1547.p_size,
    t1547.p_container,
    t1547.p_retailprice,
    t1547.p_comment,
    t1547.s_suppkey,
    t1547.s_name,
    t1547.s_address,
    t1547.s_nationkey,
    t1547.s_phone,
    t1547.s_acctbal,
    t1547.s_comment,
    t1547.ps_partkey,
    t1547.ps_suppkey,
    t1547.ps_availqty,
    t1547.ps_supplycost,
    t1547.ps_comment,
    t1547.n_nationkey,
    t1547.n_name,
    t1547.n_regionkey,
    t1547.n_comment,
    t1547.r_regionkey,
    t1547.r_name,
    t1547.r_comment,
    CAST(t1558.ps_partkey AS INTEGER) AS ps_partkey0,
    CAST(t1558.EXPR0 AS DECIMAL(19, 0)) AS EXPR0
  FROM (
    SELECT *
    FROM (
      SELECT *
      FROM (
        SELECT *
        FROM (
          SELECT *
          FROM part
          WHERE p_size = 3
            AND p_type LIKE '%NICKEL'
        ) AS t1543,
        supplier AS supplier201,
        partsupp AS partsupp201
        WHERE t1543.p_partkey = partsupp201.ps_partkey
          AND supplier201.s_suppkey = partsupp201.ps_suppkey
      ) AS t1544,
      nation AS nation201
      WHERE t1544.s_nationkey = nation201.n_nationkey
    ) AS t1545,
    (
      SELECT *
      FROM region
      WHERE r_name = 'AMERICA'
    ) AS t1546
    WHERE t1545.n_regionkey = t1546.r_regionkey
  ) AS t1547,
  (
    SELECT
      t1554.ps_partkey,
      MIN(t1554.EXPR0) AS EXPR0
    FROM (
      SELECT
        t1551.ps_partkey,
        t1552.n_regionkey,
        MIN(t1551.EXPR0) AS EXPR0
      FROM (
        SELECT
          t1548.ps_partkey,
          t1549.s_nationkey,
          MIN(t1548.EXPR0) AS EXPR0
        FROM (
          SELECT
            ps_partkey,
            ps_suppkey,
            MIN(ps_supplycost) AS EXPR0
          FROM
            partsupp
          GROUP BY
            ps_partkey,
            ps_suppkey
        ) AS t1548,
        (
          SELECT
            s_suppkey,
            s_nationkey
          FROM
            supplier
          GROUP BY
            s_suppkey,
            s_nationkey
        ) AS t1549
        WHERE t1549.s_suppkey = t1548.ps_suppkey
        GROUP BY
          t1548.ps_partkey,
          t1549.s_nationkey
      ) AS t1551,
      (
        SELECT
          n_nationkey,
          n_regionkey
        FROM
          nation
        GROUP BY
          n_nationkey,
          n_regionkey
      ) AS t1552
      WHERE t1551.s_nationkey = t1552.n_nationkey
      GROUP BY
        t1551.ps_partkey,
        t1552.n_regionkey
    ) AS t1554,
    (
      SELECT
        r_regionkey
      FROM
        region
      WHERE
        r_name = 'AMERICA'
      GROUP BY
        r_regionkey
    ) AS t1556
    WHERE t1554.n_regionkey = t1556.r_regionkey
    GROUP BY
      t1554.ps_partkey
  ) AS t1558
  WHERE
    t1547.p_partkey = t1558.ps_partkey
    AND t1547.ps_supplycost = t1558.EXPR0
  ORDER BY
    t1547.s_acctbal DESC,
    t1547.n_name,
    t1547.s_name,
    t1547.p_partkey
  FETCH NEXT 100 ROWS ONLY
) AS t1561;
```

---

### 1.2. LLM-R2

> **State：** Fails to rewrite

---

### 1.3. R-Bot 

> **Execution Time：**  14.76s

```sql
SELECT
  "supplier"."s_acctbal",
  "supplier"."s_name",
  "nation"."n_name",
  "t"."p_partkey",
  "t"."p_mfgr",
  "supplier"."s_address",
  "supplier"."s_phone",
  "supplier"."s_comment"
FROM (
  SELECT *
  FROM "part"
  WHERE
    "p_size" = 3
    AND "p_type" LIKE '%NICKEL'
) AS "t"
  CROSS JOIN "supplier"
  INNER JOIN "partsupp"
    ON "t"."p_partkey" = "partsupp"."ps_partkey"
    AND "supplier"."s_suppkey" = "partsupp"."ps_suppkey"
  INNER JOIN "nation"
    ON "supplier"."s_nationkey" = "nation"."n_nationkey"
  INNER JOIN (
    SELECT *
    FROM "region"
    WHERE "r_name" = 'AMERICA'
  ) AS "t0" ON "nation"."n_regionkey" = "t0"."r_regionkey"
  INNER JOIN (
    SELECT
      "partsupp00"."ps_partkey0",
      MIN("partsupp00"."ps_supplycost0") AS "EXPR$0"
    FROM
      "partsupp" AS "partsupp00" ("ps_partkey0", "ps_suppkey0", "ps_availqty0", "ps_supplycost0", "ps_comment0")
      INNER JOIN "supplier" AS "supplier00" ("s_suppkey0", "s_name0", "s_address0", "s_nationkey0", "s_phone0", "s_acctbal0", "s_comment0")
        ON "partsupp00"."ps_suppkey0" = "supplier00"."s_suppkey0"
      INNER JOIN "nation" AS "nation00" ("n_nationkey0", "n_name0", "n_regionkey0", "n_comment0")
        ON "supplier00"."s_nationkey0" = "nation00"."n_nationkey0"
      INNER JOIN (
        SELECT *
        FROM "region" AS "region0" ("r_regionkey0", "r_name0", "r_comment0")
        WHERE "r_name0" = 'AMERICA'
      ) AS "t1"
        ON "nation00"."n_regionkey0" = "t1"."r_regionkey0"
    GROUP BY
      "partsupp00"."ps_partkey0"
  ) AS "t3"
    ON "t"."p_partkey" = "t3"."ps_partkey0"
    AND "partsupp"."ps_supplycost" = "t3"."EXPR$0"
ORDER BY
  "supplier"."s_acctbal" DESC,
  "nation"."n_name",
  "supplier"."s_name",
  "t"."p_partkey"
FETCH NEXT 100 ROWS ONLY;
```



### 1.4. QUITE 

> **Execution Time：** > 3.35s

```sql
WITH min_ps AS (
  SELECT
    ps_partkey,
    MIN(ps_supplycost) AS min_supplycost
  FROM
    partsupp
    JOIN part
      ON part.p_partkey = partsupp.ps_partkey
    JOIN supplier
      ON supplier.s_suppkey = partsupp.ps_suppkey
    JOIN nation
      ON nation.n_nationkey = supplier.s_nationkey
    JOIN region
      ON region.r_regionkey = nation.n_regionkey
  WHERE
    region.r_name = 'AMERICA'
    AND part.p_size = 3
    AND part.p_type LIKE '%NICKEL'
  GROUP BY
    ps_partkey
)
SELECT
  s_acctbal,
  s_name,
  n_name,
  p_partkey,
  p_mfgr,
  s_address,
  s_phone,
  s_comment
FROM
  part
  JOIN partsupp
    ON part.p_partkey = partsupp.ps_partkey
  JOIN supplier
    ON supplier.s_suppkey = partsupp.ps_suppkey
  JOIN nation
    ON nation.n_nationkey = supplier.s_nationkey
  JOIN region
    ON region.r_regionkey = nation.n_regionkey
  JOIN min_ps
    ON min_ps.ps_partkey = part.p_partkey
    AND partsupp.ps_supplycost = min_ps.min_supplycost
WHERE
  region.r_name = 'AMERICA'
  AND part.p_size = 3
  AND part.p_type LIKE '%NICKEL'
ORDER BY
  s_acctbal DESC,
  n_name,
  s_name,
  p_partkey
LIMIT 100;
```





## 2. Deep Analysis

### **2.1 Query Context and Baseline Metrics**

- **LR (Rule-Based Rewrite)**: 74.71 seconds  
- **R-Bot (Template-Driven Rewrite)**: 14.76 seconds  
- **QUITE (LLM-Aided, CTE-Based Rewrite)**: 3.35 seconds  

The numbers above highlight a clear performance gap: QUITE completes the same logical task in roughly one-twentieth the time of LR, and approximately one-fifth the time of R-Bot. The remainder of this document details, in professional English, why QUITE’s rewrite delivers such a pronounced efficiency advantage.anal



### **2.2 Quantifying the Runtime Gap**

1. **LR vs. QUITE**  
   - LR’s execution of 74.71 seconds arises from deeply nested derived tables and repeated evaluation of `MIN(ps_supplycost)` in a correlated subquery.  
   - QUITE’s runtime of 3.35 seconds demonstrates nearly a 20× speedup over LR.  

2. **R-Bot vs. QUITE**  
   - R-Bot, at 14.76 seconds, eliminates some nesting compared to LR but still performs redundant join and aggregate operations without cost-aware pre-aggregation.  
   - QUITE runs ~4.4× faster than R-Bot by pushing filters into a single CTE and minimizing data movement.  

3. **Original vs. QUITE**  
   - The original, uncatalyzed query fails to complete within practical time bounds (> 300 seconds).  
   - By contrast, QUITE’s 3.35 seconds represents an exponential improvement—orders of magnitude faster—rendering the query feasible in production workloads.



### **2.3 Core Reasons for QUITE’s Superior Efficiency**

#### **2.3.1 Single Aggregation CTE vs. Correlated Subquery**

- **LR & R-Bot Approach:**  

  - Both methods compute `MIN(ps_supplycost)` through either a nested correlated subquery (LR) or a separate inline aggregation (R-Bot).  
  - These patterns force multiple scans of `partsupp` and related tables for each qualifying part or supplier row, leading to repeated I/O and large intermediate result sets.

- **QUITE’s CTE-Based Precomputation:**  

  - The `WITH min_ps AS (…)` block aggregates `ps_supplycost` exactly once for all relevant `ps_partkey` values, filtered by `region`, `size`, and `type` at the lowest possible level.  
  - This decouples the expensive aggregation from the outer join path, allowing the optimizer to perform a single, parallelized aggregation step rather than re-evaluating the minimum cost per row.

  

#### **2.3.2 Early Filter Pushdown**

- **Alternative Methods:**  

  - LR often applies `p_size = 3`, `p_type LIKE '%NICKEL'`, and `r_name = 'AMERICA'` only in the outer query block, resulting in larger intermediate joins.  
  - R-Bot may push some predicates earlier but still repeats join logic across multiple derived tables, missing the opportunity to prune data before aggregation.

- **QUITE’s Predicate Placement:**  

  - All selective predicates (region name, part size, part type) are included inside the CTE. Consequently, only the minimal set of rows traverse to the aggregation stage.  
  - This dramatically reduces the cardinality fed into `min_ps`, cutting down on CPU, memory, and I/O required for subsequent operations.

  

#### **2.3.3 Elimination of Redundant Joins and Projections**

- **LR & R-Bot Tactics:**  
  - Both methods re-join `part`, `supplier`, `nation`, and `region` multiple times—once in the correlated subquery and again in the main SELECT.  
  - They project large row widths (all columns of intermediate tables), inflating data movement and memory usage.

- **QUITE’s Streamlined Join Strategy:**  
  - By computing `min_ps` over a join of all four base tables once, then joining that result with only the necessary columns in the final SELECT, QUITE avoids double-scanning and oversized projections.  
  - The final join touches only `(part ⋈ partsupp ⋈ supplier ⋈ nation ⋈ region)` for rows that already satisfy the minimum cost condition, further reducing intermediate workload.



#### **2.3.4 Optimizer-Friendly Materialization**

- **Traditional Rewrites:**  
  - Nested views and inline aggregations obscure the true data lineage. The optimizer often has to unfold complex subqueries, which can inhibit cost-based optimizations such as join reordering, parallel hash aggregation, or predicate pushdown.

- **QUITE’s Named Subquery Advantage:**  
  - Modern database engines can recognize `min_ps` as a self-contained intermediate result. This allows them to decide whether to materialize it, push down filters, or apply parallel aggregation more effectively.  
  - By presenting a clean CTE, QUITE gives the optimizer full visibility into the aggregation boundary, enabling advanced internal rewrites (e.g., converting the CTE to a temporary table when beneficial).



### **2.4 Illustrative Runtime Breakdown**

| Rewrite Method | Key Characteristics                                          | Execution Time (s) | Relative Speedup vs. QUITE |
| -------------- | ------------------------------------------------------------ | ------------------ | -------------------------- |
| **Original**   | Correlated subquery; no pre-aggregation; nested loops        | > 300              | —                          |
| **LR**         | Deeply nested derived tables; repeated correlated `MIN(…)` lookups | 74.71              | ~ 22× slower               |
| **R-Bot**      | Template-driven joins; inline aggregation; limited predicate pushdown | 14.76              | ~ 4.4× slower              |
| **QUITE**      | Single CTE for `MIN(ps_supplycost)` + early filters + optimized joins | **3.35**           | Baseline                   |

