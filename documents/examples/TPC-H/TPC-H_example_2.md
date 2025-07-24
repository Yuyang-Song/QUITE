## Q2：Original Query

> **Execution Time：** > 300s

```sql
SELECT 
    SUM(l_extendedprice) / 7.0 AS avg_yearly
FROM 
    lineitem,
    part
WHERE 
    p_partkey = l_partkey
    AND p_brand = 'Brand#35'
    AND p_container = 'LG PKG'
    AND l_quantity < (
        SELECT 
            0.2 * AVG(l_quantity)
        FROM 
            lineitem
        WHERE 
            l_partkey = p_partkey
    );

````



## 1. Rewrite Results

### 1.1. LearnedRewrite

> **Execution Time：** 38.39s

```sql
SELECT 
    SUM(lineitem1.l_extendedprice) / 7.0 AS avg_yearly
FROM 
    lineitem AS lineitem1
INNER JOIN (
    SELECT * 
    FROM part 
    WHERE p_brand = 'Brand#35' 
      AND p_container = 'LG PKG'
) AS t8 
    ON lineitem1.l_partkey = t8.p_partkey
INNER JOIN (
    SELECT 
        l_partkey, 
        AVG(l_quantity) AS f1 
    FROM 
        lineitem 
    GROUP BY 
        l_partkey
) AS t9 
    ON t8.p_partkey = t9.l_partkey 
   AND lineitem1.l_quantity < 0.2 * t9.f1;

```

---

### 1.2. LLM-R2

> **Execution Time：** 34.79s
>
> ```sql
> SELECT 
>  SUM(lineitem.l_extendedprice) / 7.0 AS avg_yearly
> FROM 
>  lineitem
> INNER JOIN (
>  SELECT * 
>  FROM part 
>  WHERE p_brand = 'Brand#35' 
>    AND p_container = 'LG PKG'
> ) AS t 
>  ON lineitem.l_partkey = t.p_partkey
> INNER JOIN (
>  SELECT 
>      l_partkey, 
>      AVG(l_quantity) AS f1 
>  FROM 
>      lineitem 
>  GROUP BY 
>      l_partkey
> ) AS t1 
>  ON t.p_partkey = t1.l_partkey
> AND lineitem.l_quantity < 0.2 * t1.f1;
> ```

---

### 1.3. R-Bot 

> **Execution Time：** 67.05s

```sql
SELECT 
    SUM("lineitem"."l_extendedprice") / 7.0 AS "avg_yearly"
FROM 
    "lineitem"
INNER JOIN (
    SELECT * 
    FROM "part"
    WHERE "p_brand" = 'Brand#35' 
      AND "p_container" = 'LG PKG'
) AS "t" 
    ON "lineitem"."l_partkey" = "t"."p_partkey"
INNER JOIN (
    SELECT 
        "l_partkey0", 
        AVG("l_quantity0") AS "$f1"
    FROM 
        "lineitem" AS "lineitem0"
            ("l_orderkey0", "l_partkey0", "l_suppkey0", "l_linenumber0", 
             "l_quantity0", "l_extendedprice0", "l_discount0", "l_tax0", 
             "l_returnflag0", "l_linestatus0", "l_shipdate0", "l_commitdate0", 
             "l_receiptdate0", "l_shipinstruct0", "l_shipmode0", "l_comment0")
    GROUP BY 
        "l_partkey0"
) AS "t0" 
    ON "t"."p_partkey" = "t0"."l_partkey0"
   AND "lineitem"."l_quantity" < 0.2 * "t0"."$f1";

```



### 1.4. QUITE 

> **Execution Time：** 3.96s

```sql
WITH filtered_parts AS (
    SELECT 
        p_partkey
    FROM 
        part
    WHERE 
        p_brand = 'Brand#35'
        AND p_container = 'LG PKG'
),
relevant_lineitems AS (
    SELECT 
        l.l_extendedprice,
        l.l_quantity,
        0.2 * AVG(l.l_quantity) OVER (PARTITION BY l.l_partkey) AS threshold
    FROM 
        lineitem l
    JOIN 
        filtered_parts fp 
        ON l.l_partkey = fp.p_partkey
)
SELECT 
    SUM(l_extendedprice) / 7.0 AS avg_yearly
FROM 
    relevant_lineitems
WHERE 
    l_quantity < threshold;

```



### **2. Deep Analysis**

#### **2.1 Query Context and Baseline Metrics**

| **Rewrite Method** | **Execution Time (s)** |
| ------------------ | ---------------------- |
| Original           | > 300                  |
| LearnedRewrite     | 38.39                  |
| LLM-R2             | 34.79                  |
| R-Bot              | 67.05                  |
| **QUITE**          | **3.96**               |

The rewritten versions reveal a stark performance gap. QUITE outperforms all alternatives, running over **8.8×**faster than the next best rewrite (LLM-R2) and at least **75×** faster than the original query. Below, we explore the underlying reasons for this superior efficiency.

#### **2.2 Quantifying the Runtime Gap**

- Original vs. QUITE

  The original query suffers from a highly inefficient correlated subquery. For each row in the lineitem table, the database must re-execute the inner query to calculate AVG(l_quantity). This nested, row-by-row execution pattern leads to catastrophic performance, failing to complete in over 300 seconds. QUITE avoids this entirely, reducing the execution time to just 3.96s—an improvement of at least 75×.

- R-Bot vs. QUITE

  R-Bot's rewrite materializes the average quantity but employs a verbose and heavyweight join pipeline. Its unnecessary projection of all columns (SELECT *) and complex aliasing adds overhead. QUITE’s streamlined logic outperforms it by approximately 17×.

- LearnedRewrite vs. QUITE

  LearnedRewrite successfully decorrelates the subquery by pre-calculating the average quantity in a derived table (t9) and joining it back. However, this strategy requires multiple passes over the lineitem data and creates large intermediate tables. QUITE’s single-pass approach is fundamentally more efficient, making it ~9.7× faster.

- LLM-R2 vs. QUITE

  LLM-R2 is structurally identical to LearnedRewrite, using a GROUP BY subquery to pre-compute the average quantities. While it is the fastest of the non-QUITE rewrites, it shares the same core inefficiency: a multi-step process of aggregation followed by joining. QUITE’s integrated computation and filtering within a single operation gives it a ~8.8× speedup.

#### **2.3 Core Reasons for QUITE’s Superior Efficiency**

##### **2.3.1 Use of Window Function vs. Multi-Pass Aggregation**

- **Original Query:** Uses a **correlated subquery**. This is a classic anti-pattern where the inner query depends on the outer query (`l_partkey = p_partkey`) and is re-evaluated for every single row processed by the outer query, leading to extreme inefficiency.
- **Other Rewrites (LearnedRewrite, LLM-R2, R-Bot):** These methods replace the correlated subquery with a standard decorrelation technique:
  1. First, they perform one pass over the `lineitem` table to calculate `AVG(l_quantity)` for each `l_partkey` via `GROUP BY`, materializing the results into a temporary table.
  2. Second, they perform another pass over `lineitem` while joining it with the `part` table and the temporary aggregation table to apply the filter. This multi-pass approach is a significant improvement over the original but still requires expensive joins and significant data movement.
- **QUITE:** Uses a **window function** (`AVG(l_quantity) OVER (PARTITION BY l_partkey)`). This is the optimal strategy. It computes the average for each part's group of rows *inline* during a **single scan** of the `lineitem`table. Each row is enhanced with the average of its group, allowing for direct filtering in the `WHERE`clause. This eliminates an entire aggregation pass and a complex join, drastically reducing I/O, CPU, and memory usage.

##### **2.3.2 Early and Aggressive Filtering**

QUITE’s `filtered_parts` Common Table Expression (CTE) is executed first. It identifies the small subset of relevant `p_partkey` values from the `part` table. The subsequent scan of the much larger `lineitem` table can then immediately discard any rows that do not match this small pre-filtered set, massively reducing the amount of data that needs to be processed for the window function calculation.

##### **2.3.3 Join Minimization and Reduced Data Movement**

The other rewrites join three tables: `part`, the full `lineitem` table, and the aggregated results table. In contrast, QUITE performs only **one, highly-selective join** from `lineitem` to the minimal `filtered_parts` CTE. The final aggregation (`SUM`) operates on a pre-filtered, lean set of rows, minimizing data shuffling and computational overhead.

##### **2.3.4 Better Optimizer Alignment**

The clean, declarative structure of CTEs and window functions in QUITE provides clear logical blocks to the database optimizer.

- `filtered_parts`: A small, independent set that can be materialized as an efficient hash table.
- `relevant_lineitems`: A single, clear data flow that is highly amenable to pipelined and parallel execution. This modern syntax allows the optimizer to create a more efficient execution plan compared to the tangled dependencies of correlated subqueries or the multi-step process of derived table joins.

#### **2.4 Illustrative Runtime Breakdown**

| **Rewrite Method** | **Key Traits**                              | **Runtime (s)** | **Speedup vs. QUITE** |
| ------------------ | ------------------------------------------- | --------------- | --------------------- |
| Original           | Correlated subquery (row-by-row execution)  | > 300           | —                     |
| R-Bot              | Template joins, verbose intermediate tables | 67.05           | ~17× slower           |
| LLM-R2             | Pre-aggregation via `GROUP BY` + Joins      | 34.79           | ~8.8× slower          |
| LearnedRewrite     | Pre-aggregation via `GROUP BY` + Joins      | 38.39           | ~9.7× slower          |
| **QUITE**          | **CTE + Window Function + Minimal Join**    | **3.96**        | **Baseline**          |