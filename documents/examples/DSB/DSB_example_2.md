## Q2：Original Query

> **Execution Time：** 106.23s

```sql
SELECT  
    MIN(i_item_id),
    MIN(i_item_desc),
    MIN(s_store_id),
    MIN(s_store_name),
    MIN(ss_net_profit),
    MIN(sr_net_loss),
    MIN(cs_net_profit),
    MIN(ss_item_sk),
    MIN(sr_ticket_number),
    MIN(cs_order_number)
FROM  
    store_sales,
    store_returns,
    catalog_sales,
    date_dim d1,
    date_dim d2,
    date_dim d3,
    store,
    item
WHERE  
    d1.d_moy = 6
    AND d1.d_year = 2000
    AND d1.d_date_sk = ss_sold_date_sk
    AND i_item_sk = ss_item_sk
    AND s_store_sk = ss_store_sk
    AND ss_customer_sk = sr_customer_sk
    AND ss_item_sk = sr_item_sk
    AND ss_ticket_number = sr_ticket_number
    AND sr_returned_date_sk = d2.d_date_sk
    AND d2.d_moy BETWEEN 6 AND 6 + 2
    AND d2.d_year = 2000
    AND sr_customer_sk = cs_bill_customer_sk
    AND sr_item_sk = cs_item_sk
    AND cs_sold_date_sk = d3.d_date_sk
    AND d3.d_moy BETWEEN 6 AND 6 + 2
    AND d3.d_year = 2000;

````



## 1. Rewrite Results

### 1.1. LearnedRewrite

> **Execution Time：** 237.00s

```sql
SELECT 
    MIN(t842.EXPR0),
    MIN(t842.EXPR1),
    MIN(t841.EXPR2),
    MIN(t841.EXPR3),
    MIN(t841.EXPR4),
    MIN(t841.EXPR5),
    MIN(t841.EXPR6),
    MIN(t841.EXPR7),
    MIN(t841.EXPR8),
    MIN(t841.EXPR9)
FROM (
    SELECT 
        t838.ss_item_sk,
        MIN(t839.EXPR2) AS EXPR2,
        MIN(t839.EXPR3) AS EXPR3,
        MIN(t838.EXPR4) AS EXPR4,
        MIN(t838.EXPR5) AS EXPR5,
        MIN(t838.EXPR6) AS EXPR6,
        MIN(t838.EXPR7) AS EXPR7,
        MIN(t838.EXPR8) AS EXPR8,
        MIN(t838.EXPR9) AS EXPR9
    FROM (
        SELECT 
            t834.ss_item_sk,
            t834.ss_store_sk,
            MIN(t834.EXPR4) AS EXPR4,
            MIN(t834.EXPR5) AS EXPR5,
            MIN(t834.EXPR6) AS EXPR6,
            MIN(t834.EXPR7) AS EXPR7,
            MIN(t834.EXPR8) AS EXPR8,
            MIN(t834.EXPR9) AS EXPR9
        FROM (
            SELECT 
                t830.ss_item_sk,
                t830.ss_store_sk,
                t830.cs_sold_date_sk,
                MIN(t830.EXPR4) AS EXPR4,
                MIN(t830.EXPR5) AS EXPR5,
                MIN(t830.EXPR6) AS EXPR6,
                MIN(t830.EXPR7) AS EXPR7,
                MIN(t830.EXPR8) AS EXPR8,
                MIN(t830.EXPR9) AS EXPR9
            FROM (
                SELECT 
                    t826.ss_item_sk,
                    t826.ss_store_sk,
                    t826.sr_returned_date_sk,
                    t826.cs_sold_date_sk,
                    MIN(t826.EXPR4) AS EXPR4,
                    MIN(t826.EXPR5) AS EXPR5,
                    MIN(t826.EXPR6) AS EXPR6,
                    MIN(t826.EXPR7) AS EXPR7,
                    MIN(t826.EXPR8) AS EXPR8,
                    MIN(t826.EXPR9) AS EXPR9
                FROM (
                    SELECT 
                        t823.ss_sold_date_sk,
                        t823.ss_item_sk,
                        t823.ss_store_sk,
                        t823.sr_returned_date_sk,
                        t824.cs_sold_date_sk,
                        MIN(t823.EXPR4) AS EXPR4,
                        MIN(t823.EXPR5) AS EXPR5,
                        MIN(t824.EXPR6) AS EXPR6,
                        MIN(t823.EXPR7) AS EXPR7,
                        MIN(t823.EXPR8) AS EXPR8,
                        MIN(t824.EXPR9) AS EXPR9
                    FROM (
                        SELECT 
                            t820.ss_sold_date_sk,
                            t820.ss_item_sk,
                            t820.ss_store_sk,
                            t821.sr_returned_date_sk,
                            t821.sr_item_sk,
                            t821.sr_customer_sk,
                            MIN(t820.EXPR4) AS EXPR4,
                            MIN(t821.EXPR5) AS EXPR5,
                            MIN(t820.EXPR7) AS EXPR7,
                            MIN(t821.EXPR8) AS EXPR8
                        FROM (
                            SELECT 
                                ss_sold_date_sk,
                                ss_item_sk,
                                ss_customer_sk,
                                ss_store_sk,
                                ss_ticket_number,
                                MIN(ss_net_profit) AS EXPR4,
                                MIN(ss_item_sk) AS EXPR7
                            FROM store_sales
                            GROUP BY 
                                ss_sold_date_sk,
                                ss_item_sk,
                                ss_customer_sk,
                                ss_store_sk,
                                ss_ticket_number
                        ) AS t820,
                        (
                            SELECT 
                                sr_returned_date_sk,
                                sr_item_sk,
                                sr_customer_sk,
                                sr_ticket_number,
                                MIN(sr_net_loss) AS EXPR5,
                                MIN(sr_ticket_number) AS EXPR8
                            FROM store_returns
                            GROUP BY 
                                sr_returned_date_sk,
                                sr_item_sk,
                                sr_customer_sk,
                                sr_ticket_number
                        ) AS t821
                        WHERE 
                            t820.ss_customer_sk = t821.sr_customer_sk
                            AND t820.ss_item_sk = t821.sr_item_sk
                            AND t820.ss_ticket_number = t821.sr_ticket_number
                        GROUP BY 
                            t820.ss_sold_date_sk,
                            t820.ss_item_sk,
                            t820.ss_store_sk,
                            t821.sr_returned_date_sk,
                            t821.sr_item_sk,
                            t821.sr_customer_sk
                    ) AS t823,
                    (
                        SELECT 
                            cs_sold_date_sk,
                            cs_bill_customer_sk,
                            cs_item_sk,
                            MIN(cs_net_profit) AS EXPR6,
                            MIN(cs_order_number) AS EXPR9
                        FROM catalog_sales
                        GROUP BY 
                            cs_sold_date_sk,
                            cs_bill_customer_sk,
                            cs_item_sk
                    ) AS t824
                    WHERE 
                        t823.sr_customer_sk = t824.cs_bill_customer_sk
                        AND t823.sr_item_sk = t824.cs_item_sk
                    GROUP BY 
                        t823.ss_sold_date_sk,
                        t823.ss_item_sk,
                        t823.ss_store_sk,
                        t823.sr_returned_date_sk,
                        t824.cs_sold_date_sk
                ) AS t826
                INNER JOIN (
                    SELECT d_date_sk
                    FROM date_dim
                    WHERE d_moy = 6 AND d_year = 2000
                    GROUP BY d_date_sk
                ) AS t828
                ON t828.d_date_sk = t826.ss_sold_date_sk
                GROUP BY 
                    t826.ss_item_sk,
                    t826.ss_store_sk,
                    t826.sr_returned_date_sk,
                    t826.cs_sold_date_sk
            ) AS t830
            INNER JOIN (
                SELECT d_date_sk
                FROM date_dim
                WHERE d_moy BETWEEN 6 AND 6 + 2 AND d_year = 2000
                GROUP BY d_date_sk
            ) AS t832
            ON t830.sr_returned_date_sk = t832.d_date_sk
            GROUP BY 
                t830.ss_item_sk,
                t830.ss_store_sk,
                t830.cs_sold_date_sk
        ) AS t834
        INNER JOIN (
            SELECT d_date_sk
            FROM date_dim
            WHERE d_moy BETWEEN 6 AND 6 + 2 AND d_year = 2000
            GROUP BY d_date_sk
        ) AS t836
        ON t834.cs_sold_date_sk = t836.d_date_sk
        GROUP BY 
            t834.ss_item_sk,
            t834.ss_store_sk
    ) AS t838
    INNER JOIN (
        SELECT 
            s_store_sk,
            MIN(s_store_id) AS EXPR2,
            MIN(s_store_name) AS EXPR3
        FROM store
        GROUP BY s_store_sk
    ) AS t839
    ON t839.s_store_sk = t838.ss_store_sk
    GROUP BY t838.ss_item_sk
) AS t841
INNER JOIN (
    SELECT 
        i_item_sk,
        MIN(i_item_id) AS EXPR0,
        MIN(i_item_desc) AS EXPR1
    FROM item
    GROUP BY i_item_sk
) AS t842
ON t842.i_item_sk = t841.ss_item_sk;
```



### 1.2. LLM-R2

> **Execution Time：** 127.76s
>
> ```sql
> SELECT 
>     MIN(item.i_item_id),
>     MIN(item.i_item_desc),
>     MIN(t7.s_store_id),
>     MIN(t7.s_store_name),
>     MIN(t7.ss_net_profit),
>     MIN(t7.sr_net_loss),
>     MIN(t7.cs_net_profit),
>     MIN(t7.ss_item_sk),
>     MIN(t7.sr_ticket_number),
>     MIN(t7.cs_order_number)
> FROM (
>     SELECT * 
>     FROM (
>         SELECT * 
>         FROM (
>             SELECT * 
>             FROM (
>                 SELECT * 
>                 FROM (
>                     SELECT * 
>                     FROM (
>                         SELECT * 
>                         FROM store_sales, store_returns
>                         WHERE 
>                             store_sales.ss_customer_sk = store_returns.sr_customer_sk
>                             AND store_sales.ss_item_sk = store_returns.sr_item_sk
>                             AND store_sales.ss_ticket_number = store_returns.sr_ticket_number
>                     ) AS t,
>                     catalog_sales
>                     WHERE 
>                         t.sr_customer_sk = catalog_sales.cs_bill_customer_sk
>                         AND t.sr_item_sk = catalog_sales.cs_item_sk
>                 ) AS t0,
>                 (
>                     SELECT * 
>                     FROM date_dim 
>                     WHERE d_moy = 6 AND d_year = 2000
>                 ) AS t1
>                 WHERE t1.d_date_sk = t0.ss_sold_date_sk
>             ) AS t2,
>             (
>                 SELECT * 
>                 FROM date_dim 
>                 WHERE d_moy >= 6 AND d_moy <= 6 + 2 AND d_year = 2000
>             ) AS t3
>             WHERE t2.sr_returned_date_sk = t3.d_date_sk
>         ) AS t4,
>         (
>             SELECT * 
>             FROM date_dim 
>             WHERE d_moy >= 6 AND d_moy <= 6 + 2 AND d_year = 2000
>         ) AS t5
>         WHERE t4.cs_sold_date_sk = t5.d_date_sk
>     ) AS t6,
>     store
>     WHERE store.s_store_sk = t6.ss_store_sk
> ) AS t7,
> item
> WHERE item.i_item_sk = t7.ss_item_sk;
> 
> ```
>
> 

---

### 1.3. R-Bot 

> **Execution Time：** 112.52s

```sql
SELECT 
    MIN("item"."i_item_id"),
    MIN("item"."i_item_desc"),
    MIN("store"."s_store_id"),
    MIN("store"."s_store_name"),
    MIN("store_sales"."ss_net_profit"),
    MIN("store_returns"."sr_net_loss"),
    MIN("catalog_sales"."cs_net_profit"),
    MIN("store_sales"."ss_item_sk"),
    MIN("store_returns"."sr_ticket_number"),
    MIN("catalog_sales"."cs_order_number")
FROM 
    "store_sales"
INNER JOIN 
    "store_returns" 
    ON "store_sales"."ss_customer_sk" = "store_returns"."sr_customer_sk"
    AND "store_sales"."ss_item_sk" = "store_returns"."sr_item_sk"
    AND "store_sales"."ss_ticket_number" = "store_returns"."sr_ticket_number"
INNER JOIN 
    "catalog_sales" 
    ON "store_returns"."sr_customer_sk" = "catalog_sales"."cs_bill_customer_sk"
    AND "store_returns"."sr_item_sk" = "catalog_sales"."cs_item_sk"
INNER JOIN (
    SELECT * 
    FROM "date_dim"
    WHERE "d_moy" = 6 AND "d_year" = 2000
) AS "t" 
    ON "store_sales"."ss_sold_date_sk" = "t"."d_date_sk"
INNER JOIN (
    SELECT * 
    FROM "date_dim" AS "date_dim0" (
        "d_date_sk0", "d_date_id0", "d_date0", "d_month_seq0", "d_week_seq0",
        "d_quarter_seq0", "d_year0", "d_dow0", "d_moy0", "d_dom0", "d_qoy0",
        "d_fy_year0", "d_fy_quarter_seq0", "d_fy_week_seq0", "d_day_name0",
        "d_quarter_name0", "d_holiday0", "d_weekend0", "d_following_holiday0",
        "d_first_dom0", "d_last_dom0", "d_same_day_ly0", "d_same_day_lq0",
        "d_current_day0", "d_current_week0", "d_current_month0",
        "d_current_quarter0", "d_current_year0"
    )
    WHERE "d_moy0" >= 6 AND "d_moy0" <= 8 AND "d_year0" = 2000
) AS "t0" 
    ON "store_returns"."sr_returned_date_sk" = "t0"."d_date_sk0"
INNER JOIN (
    SELECT * 
    FROM "date_dim" AS "date_dim1" (
        "d_date_sk1", "d_date_id1", "d_date1", "d_month_seq1", "d_week_seq1",
        "d_quarter_seq1", "d_year1", "d_dow1", "d_moy1", "d_dom1", "d_qoy1",
        "d_fy_year1", "d_fy_quarter_seq1", "d_fy_week_seq1", "d_day_name1",
        "d_quarter_name1", "d_holiday1", "d_weekend1", "d_following_holiday1",
        "d_first_dom1", "d_last_dom1", "d_same_day_ly1", "d_same_day_lq1",
        "d_current_day1", "d_current_week1", "d_current_month1",
        "d_current_quarter1", "d_current_year1"
    )
    WHERE "d_moy1" >= 6 AND "d_moy1" <= 8 AND "d_year1" = 2000
) AS "t1" 
    ON "catalog_sales"."cs_sold_date_sk" = "t1"."d_date_sk1"
INNER JOIN 
    "store" 
    ON "store_sales"."ss_store_sk" = "store"."s_store_sk"
INNER JOIN 
    "item" 
    ON "store_sales"."ss_item_sk" = "item"."i_item_sk";

```



### 1.4. QUITE 

> **Execution Time：** 18.16s

```sql
SELECT
  MIN(i_item_id),
  MIN(i_item_desc),
  MIN(s_store_id),
  MIN(s_store_name),
  MIN(ss_net_profit),
  MIN(sr_net_loss),
  MIN(cs_net_profit),
  MIN(ss_item_sk),
  MIN(sr_ticket_number),
  MIN(cs_order_number)
FROM
  store_sales
JOIN 
  date_dim d1 
    ON d1.d_date_sk = ss_sold_date_sk 
   AND d1.d_moy = 6 
   AND d1.d_year = 2000
JOIN 
  store 
    ON s_store_sk = ss_store_sk
JOIN 
  item 
    ON i_item_sk = ss_item_sk
JOIN 
  store_returns 
    ON ss_customer_sk = sr_customer_sk 
   AND ss_item_sk = sr_item_sk 
   AND ss_ticket_number = sr_ticket_number
JOIN 
  date_dim d2 
    ON sr_returned_date_sk = d2.d_date_sk 
   AND d2.d_moy BETWEEN 6 AND 8 
   AND d2.d_year = 2000
JOIN 
  catalog_sales 
    ON sr_customer_sk = cs_bill_customer_sk 
   AND sr_item_sk = cs_item_sk
JOIN 
  date_dim d3 
    ON cs_sold_date_sk = d3.d_date_sk 
   AND d3.d_moy BETWEEN 6 AND 8 
   AND d3.d_year = 2000;


```





### **2. Deep Analysis**

#### **2.1 Query Context and Baseline Metrics**

This query analyzes combined sales and returns across three channels—`store_sales`, `store_returns`, and `catalog_sales`—for a particular month and its subsequent two months. It joins three large fact tables with `date_dim`, `store`, and `item` dimensions. The primary challenge is efficiently filtering each fact table by date before joining, to avoid excessive intermediate row counts.

| **Rewrite Method**  | **Execution Time (s)** |
| ------------------- | ---------------------- |
| Original            | 106.23                 |
| LearnedRewrite (LR) | 237.00                 |
| LLM-R2              | 127.76                 |
| R-Bot               | 112.52                 |
| **QUITE**           | **18.16**              |

QUITE’s rewrite is **5.8×** faster than the original and **13×**–**6×** faster than the pathological and template‐driven rewrites, respectively. This gap underscores the importance of early filtering and streamlined join logic.

------

#### **2.2 Quantifying the Runtime Gap**

- **Original vs. QUITE**
  The original query presents all six tables plus two additional copies of `date_dim` to the optimizer at once, forcing it to consider unwanted join orders and delaying filter application until late. QUITE pushes each date filter into its corresponding `JOIN … ON` clause, reducing each fact table’s input size early. This yields a **5.8×** speedup (106.23s → 18.16s).
- **LearnedRewrite vs. QUITE**
  LearnedRewrite breaks the query into cascaded aggregations, computing `MIN(...)` at every intermediate level and then again in the outer query. These repeated aggregations create huge temporary results and multiply scans of `store_sales`, `store_returns`, and `catalog_sales`. As a result, LR runs in 237.00s—**13×** slower than QUITE.
- **R-Bot vs. QUITE**
  R-Bot converts to ANSI joins but still issues three separate subqueries over `date_dim`, each scanning all rows for the given month/year. It doesn’t reduce each fact table early enough, so its runtime is 112.52s—**6.2×** slower than QUITE.
- **LLM-R2 vs. QUITE**
  LLM-R2 nests multiple `SELECT *` blocks, wrapping each filter in an additional layer that prevents the optimizer from pushing predicates into the most selective joins. It completes in 127.76s—**7×** slower than QUITE.

------

#### **2.3 Core Reasons for QUITE’s Superior Efficiency**

##### **2.3.1 The "Filter Early, Join Late" Strategy**

QUITE applies each date filter as soon as possible:

1. **Filter `store_sales` by month = 6, year = 2000**
2. **Filter `store_returns` by month ∈ [6, 8], year = 2000**
3. **Filter `catalog_sales` by month ∈ [6, 8], year = 2000**

Each filter resides in its respective `JOIN … ON` clause, so only prefiltered subsets of the fact tables participate in subsequent joins. By contrast, the original and template rewrites defer filter application until after multiple table combinations, inflating intermediate row counts.

##### **2.3.2 Effective Data Reduction via CTEs**

Although QUITE inlines filters directly—rather than using named CTEs—it achieves the same early reduction effect:

- **`JOIN date_dim d1 ON (d1.d_date_sk = ss_sold_date_sk AND d1.d_moy = 6 AND d1.d_year = 2000)`**
  immediately drops all `store_sales` rows outside June 2000.
- **`JOIN date_dim d2 ON (d2.d_date_sk = sr_returned_date_sk AND d2.d_moy BETWEEN 6 AND 8 AND d2.d_year = 2000)`**
  prunes `store_returns` to the three-month window before joining back to `store_sales`.
- **`JOIN date_dim d3 ON (d3.d_date_sk = cs_sold_date_sk AND d3.d_moy BETWEEN 6 AND 8 AND d3.d_year = 2000)`**
  further restricts `catalog_sales` early.

These “inline‐CTE”–like predicates discard millions of irrelevant rows at each step, so only a minimal number of rows flow into the final join chain.

##### **2.3.3 Simplified Final Join Logic**

By the time the final projection runs, QUITE has already:

1. Reduced `store_sales` to June-2000 rows joined with `store` and `item`.
2. Reduced `store_returns` to returns in June–August 2000.
3. Reduced `catalog_sales` to sales in June–August 2000.

Thus, the final join sequence is simply:

```
store_sales_filtered
  ⋈ store_returns_filtered
  ⋈ catalog_sales_filtered
  ⋈ store
  ⋈ item
```

Instead of joining three full‐sized fact tables, the engine joins three much smaller filtered subsets. LearnedRewrite, LLM-R2, and R-Bot all keep wide projections or nested subqueries that force them to handle many more rows before computing `MIN()`.

##### **2.3.4 Guiding the Query Optimizer**

QUITE’s flat join structure with inline filters gives the optimizer a crystal‐clear plan:

- Start with the tiny `date_dim` selection for June 2000.
- Probe `store_sales` (now small) by `ss_sold_date_sk`.
- Immediately join `store` and `item` (dimension lookups).
- Then join the small `store_returns` subset (filtered by d2).
- Finally join the small `catalog_sales` subset (filtered by d3).

Because each join is selective, the optimizer never contemplates a “bad” plan (e.g., joining unfiltered `store_sales` to unfiltered `store_returns`). The rewriting forces an ascending cardinality join order—smallest to largest—to minimize I/O and CPU.

------

#### **2.4 Illustrative Runtime Breakdown**

| **Rewrite Method** | **Key Traits**                                               | **Runtime (s)** | **Speedup vs. QUITE** |
| ------------------ | ------------------------------------------------------------ | --------------- | --------------------- |
| Original           | All tables in one WHERE clause; filters applied late; large multi‐table join | 106.23          | ~5.8× slower          |
| LearnedRewrite     | Cascaded nested GROUP BYs; repeated `MIN()` at each level; huge intermediate results | 237.00          | ~13× slower           |
| R-Bot              | ANSI joins, but three separate `date_dim` scans; no early reduction of fact tables | 112.52          | ~6.2× slower          |
| LLM-R2             | Deeply nested `SELECT *`; blocks predicate pushdown; multiple layers of materialized subqueries | 127.76          | ~7× slower            |
| **QUITE**          | **Inline date filters; single‐pass reduction of each fact table; flat join graph; final MIN at the end** | **18.16**       | **Baseline**          |

