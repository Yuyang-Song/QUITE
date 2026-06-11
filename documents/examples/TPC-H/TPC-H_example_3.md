## Q3：Original Query

> **Execution Time：** > 300s

```sql
SELECT 
    s_name, 
    COUNT(*) AS numwait
FROM 
    supplier
JOIN 
    lineitem l1 ON s_suppkey = l1.l_suppkey
JOIN 
    orders o ON o_orderkey = l1.l_orderkey
JOIN 
    nation n ON s_nationkey = n_nationkey
WHERE 
    o_orderstatus = 'F' 
    AND l1.l_receiptdate > l1.l_commitdate
    AND EXISTS (
        SELECT 1 
        FROM lineitem l2
        WHERE l2.l_orderkey = l1.l_orderkey 
        AND l2.l_suppkey <> l1.l_suppkey
    )
    AND NOT EXISTS (
        SELECT 1 
        FROM lineitem l3
        WHERE l3.l_orderkey = l1.l_orderkey 
        AND l3.l_suppkey <> l1.l_suppkey 
        AND l3.l_receiptdate > l3.l_commitdate
    )
    AND n_name = 'SAUDI ARABIA'
GROUP BY 
    s_name
ORDER BY 
    numwait DESC, 
    s_name
LIMIT 100;

````



## 1. Rewrite Results

### 1.1. LearnedRewrite

*>* ***State：*** *Fails to rewrite*

### 1.2. LLM-R2

*>* ***State：*** *Fails to rewrite*

---

### 1.3. R-Bot 

> **Execution Time：** >300s

```sql
SELECT 
    "supplier"."s_name", 
    COUNT(*) AS "numwait"
FROM 
    "supplier"
INNER JOIN (
    SELECT * 
    FROM "lineitem"
    WHERE "l_receiptdate" > "l_commitdate"
) AS "t" 
    ON "supplier"."s_suppkey" = "t"."l_suppkey"
INNER JOIN (
    SELECT * 
    FROM "orders"
    WHERE "o_orderstatus" = 'F'
) AS "t0" 
    ON "t"."l_orderkey" = "t0"."o_orderkey"
INNER JOIN (
    SELECT * 
    FROM "nation"
    WHERE "n_name" = 'SAUDI ARABIA'
) AS "t1" 
    ON "supplier"."s_nationkey" = "t1"."n_nationkey"
INNER JOIN (
    SELECT 
        "t5"."l_orderkey1", 
        "t5"."l_suppkey1", 
        TRUE AS "$f2"
    FROM "lineitem" AS "lineitem00"
    INNER JOIN (
        SELECT 
            "t2"."l_orderkey1", 
            "t2"."l_suppkey1"
        FROM "supplier" AS "supplier00"
        INNER JOIN (
            SELECT * 
            FROM "lineitem" AS "lineitem1"
            WHERE "l_receiptdate1" > "l_commitdate1"
        ) AS "t2" 
            ON "supplier00"."s_suppkey0" = "t2"."l_suppkey1"
        INNER JOIN (
            SELECT * 
            FROM "orders" AS "orders0"
            WHERE "o_orderstatus0" = 'F'
        ) AS "t3" 
            ON "t2"."l_orderkey1" = "t3"."o_orderkey0"
        INNER JOIN (
            SELECT * 
            FROM "nation" AS "nation0"
            WHERE "n_name0" = 'SAUDI ARABIA'
        ) AS "t4" 
            ON "supplier00"."s_nationkey0" = "t4"."n_nationkey0"
        GROUP BY 
            "t2"."l_orderkey1", 
            "t2"."l_suppkey1"
    ) AS "t5" 
        ON "lineitem00"."l_orderkey0" = "t5"."l_orderkey1" 
        AND "lineitem00"."l_suppkey0" <> "t5"."l_suppkey1"
    GROUP BY 
        "t5"."l_orderkey1", 
        "t5"."l_suppkey1"
) AS "t7" 
    ON "t"."l_orderkey" = "t7"."l_orderkey1" 
    AND "t"."l_suppkey" = "t7"."l_suppkey1"
LEFT JOIN (
    SELECT 
        "t12"."l_orderkey3", 
        "t12"."l_suppkey3", 
        TRUE AS "$f20"
    FROM (
        SELECT * 
        FROM "lineitem" AS "lineitem2"
        WHERE "l_receiptdate2" > "l_commitdate2"
    ) AS "t8"
    INNER JOIN (
        SELECT 
            "t9"."l_orderkey3", 
            "t9"."l_suppkey3"
        FROM "supplier" AS "supplier10"
        INNER JOIN (
            SELECT * 
            FROM "lineitem" AS "lineitem3"
            WHERE "l_receiptdate3" > "l_commitdate3"
        ) AS "t9" 
            ON "supplier10"."s_suppkey1" = "t9"."l_suppkey3"
        INNER JOIN (
            SELECT * 
            FROM "orders" AS "orders1"
            WHERE "o_orderstatus1" = 'F'
        ) AS "t10" 
            ON "t9"."l_orderkey3" = "t10"."o_orderkey1"
        INNER JOIN (
            SELECT * 
            FROM "nation" AS "nation1"
            WHERE "n_name1" = 'SAUDI ARABIA'
        ) AS "t11" 
            ON "supplier10"."s_nationkey1" = "t11"."n_nationkey1"
        GROUP BY 
            "t9"."l_orderkey3", 
            "t9"."l_suppkey3"
    ) AS "t12" 
        ON "t8"."l_orderkey2" = "t12"."l_orderkey3" 
        AND "t8"."l_suppkey2" <> "t12"."l_suppkey3"
    GROUP BY 
        "t12"."l_orderkey3", 
        "t12"."l_suppkey3"
) AS "t14" 
    ON "t"."l_orderkey" = "t14"."l_orderkey3" 
    AND "t"."l_suppkey" = "t14"."l_suppkey3"
WHERE 
    "t14"."$f20" IS NULL
GROUP BY 
    "supplier"."s_name"
ORDER BY 
    2 DESC, 
    "supplier"."s_name"
FETCH NEXT 100 ROWS ONLY;

```



### 1.4. QUITE 

> **Execution Time：** 86.50s

```sql
WITH filtered_orders AS (
    SELECT o_orderkey
    FROM orders
    WHERE o_orderstatus = 'F'
), 
lineitem_filtered AS (
    SELECT 
        l_orderkey, 
        l_suppkey, 
        l_receiptdate, 
        l_commitdate
    FROM lineitem
    WHERE l_orderkey IN (SELECT o_orderkey FROM filtered_orders)
),
filtered_suppliers AS (
    SELECT 
        s_suppkey, 
        s_name
    FROM supplier
    JOIN nation ON s_nationkey = n_nationkey
    WHERE n_name = 'SAUDI ARABIA'
)
SELECT 
    s.s_name, 
    COUNT(*) AS numwait
FROM 
    filtered_suppliers s
JOIN 
    lineitem_filtered l1 ON s.s_suppkey = l1.l_suppkey
WHERE 
    l1.l_receiptdate > l1.l_commitdate
    AND EXISTS (
        SELECT 1
        FROM lineitem_filtered l2
        WHERE 
            l2.l_orderkey = l1.l_orderkey 
            AND l2.l_suppkey <> l1.l_suppkey
    )
    AND NOT EXISTS (
        SELECT 1
        FROM lineitem_filtered l3
        WHERE 
            l3.l_orderkey = l1.l_orderkey 
            AND l3.l_suppkey <> l1.l_suppkey 
            AND l3.l_receiptdate > l3.l_commitdate
    )
GROUP BY 
    s.s_name
ORDER BY 
    numwait DESC, s.s_name
LIMIT 100;

```




### **2. Deep Analysis**

#### **2.1 Query Context and Baseline Metrics**

This complex query (TPC-H Q21) identifies suppliers in a specific nation who were uniquely responsible for late line items on multi-supplier orders. The logic involves three correlated subqueries, making it notoriously difficult to optimize.

| **Rewrite Method** | **Execution Time (s)** |
| ------------------ | ---------------------- |
| Original           | > 300                  |
| LR & LLM-R2        | Failed to Rewrite      |
| R-Bot              | > 300                  |
| **QUITE**          | **86.50**              |

The failures of `LR` and `LLM-R2` underscore the query's complexity. Both the Original and the R-Bot rewrite failed to complete within the time limit. QUITE is the only version that produces a result, demonstrating a speedup of at least **3.5×** over the others, though the actual improvement is likely far greater.

#### **2.2 Quantifying the Runtime Gap**

- Original vs. QUITE

  The original query's EXISTS and NOT EXISTS clauses are correlated and operate against the entire, multi-billion-row lineitem table. For every potential row from the main query, the database must perform multiple, expensive sub-scans on the full table, leading to an unmanageable execution plan. QUITE’s rewrite is at least 3.5x faster by fundamentally reducing the scope of these subqueries.

- R-Bot vs. QUITE

  The R-Bot rewrite attempts a brute-force transformation, converting the EXISTS clauses into a series of massive, deeply nested INNER and LEFT joins. This creates a syntactic explosion that is unreadable and even more inefficient than the original, as it forces the database to construct enormous intermediate tables. QUITE's intelligent pre-filtering is vastly superior to this convoluted join-based approach, also making it at least 3.5x faster.

#### **2.3 Core Reasons for QUITE’s Superior Efficiency**

##### **2.3.1 Strategic Pre-Filtering with CTEs**

This is the cornerstone of QUITE's success. Instead of operating on the full tables, it systematically carves out only the necessary data using Common Table Expressions (CTEs).

1. **`filtered_orders` & `filtered_suppliers`:** These CTEs create small, targeted sets of relevant `orderkey` and `suppkey` values. This initial filtering is fast and dramatically reduces the search space.
2. **`lineitem_filtered`:** This is the most critical step. QUITE creates a lean, intermediate version of `lineitem`that *only* contains rows relevant to the pre-filtered orders. This is the masterstroke that makes the rest of the query feasible.

##### **2.3.2 Preserving Subquery Logic on Reduced Data**

Unlike R-Bot, which tried to eliminate the subqueries through disastrous joins, QUITE correctly identifies that `EXISTS` and `NOT EXISTS` are the clearest and often most efficient way to express the desired business logic.

The key innovation is **not** rewriting the subqueries themselves, but **drastically reducing the size of the table they operate on**. By applying the `EXISTS` clauses to the compact `lineitem_filtered` CTE instead of the full `lineitem` table, QUITE transforms a prohibitively expensive operation into a manageable one.

##### **2.3.3 Avoiding Join Explosion and Maintaining Simplicity**

R-Bot's rewrite is a textbook example of a "join explosion," creating a query plan with exponential complexity. QUITE's approach is the opposite.

- **Clean Joins:** It uses simple, direct joins between the filtered CTEs.
- **No Redundancy:** The query avoids joining the same table multiple times or creating duplicative logic.

This clarity leads to a much more efficient execution plan that the database optimizer can easily handle, preventing the creation of massive intermediate data sets. The final result is a query that is not only faster but also readable and maintainable.

#### **2.4 Illustrative Runtime Breakdown**

| **Rewrite Method** | **Key Traits**                                               | **Runtime (s)** | **Speedup vs. QUITE** |
| ------------------ | ------------------------------------------------------------ | --------------- | --------------------- |
| Original           | Correlated subqueries on full, multi-billion row tables.     | > 300           | —                     |
| R-Bot              | Brute-force "join explosion"; unreadable and inefficient.    | > 300           | At least 3.5x slower  |
| **QUITE**          | **Strategic CTE pre-filtering; subqueries on reduced data.** | **86.50**       | **Baseline**          |