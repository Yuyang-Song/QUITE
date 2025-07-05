## Q1：Original Query

> **Execution Time：** 126.66s

```sql
SELECT
    i_item_id,
    i_item_desc,
    s_store_id,
    s_store_name,
    SUM(ss_net_profit) AS store_sales_profit,
    SUM(sr_net_loss) AS store_returns_loss,
    SUM(cs_net_profit) AS catalog_sales_profit
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
    d1.d_moy = 8
    AND d1.d_year = 2001
    AND d1.d_date_sk = ss_sold_date_sk
    AND i_item_sk = ss_item_sk
    AND s_store_sk = ss_store_sk
    AND ss_customer_sk = sr_customer_sk
    AND ss_item_sk = sr_item_sk
    AND ss_ticket_number = sr_ticket_number
    AND sr_returned_date_sk = d2.d_date_sk
    AND d2.d_moy BETWEEN 8 AND 8 + 2
    AND d2.d_year = 2001
    AND sr_customer_sk = cs_bill_customer_sk
    AND sr_item_sk = cs_item_sk
    AND cs_sold_date_sk = d3.d_date_sk
    AND d3.d_moy BETWEEN 8 AND 8 + 2
    AND d3.d_year = 2001
GROUP BY
    i_item_id,
    i_item_desc,
    s_store_id,
    s_store_name
ORDER BY
    i_item_id,
    i_item_desc,
    s_store_id,
    s_store_name
LIMIT 100;
````



## 1. Rewrite Results

### 1.1. LearnedRewrite

> **Execution Time：** 273.57s

```sql
SELECT 
    t1120.i_item_id,
    t1120.i_item_desc,
    t1119.s_store_id,
    t1119.s_store_name,
    SUM(t1119.store_sales_profit * t1120.f3) AS store_sales_profit,
    SUM(t1119.store_returns_loss * t1120.f3) AS store_returns_loss,
    SUM(t1119.catalog_sales_profit * t1120.f3) AS catalog_sales_profit
FROM (
    SELECT 
        t1116.ss_item_sk,
        t1117.s_store_id,
        t1117.s_store_name,
        SUM(t1116.store_sales_profit * t1117.f3) AS store_sales_profit,
        SUM(t1116.store_returns_loss * t1117.f3) AS store_returns_loss,
        SUM(t1116.catalog_sales_profit * t1117.f3) AS catalog_sales_profit
    FROM (
        SELECT 
            t1112.ss_item_sk,
            t1112.ss_store_sk,
            SUM(t1112.store_sales_profit * t1114.f1) AS store_sales_profit,
            SUM(t1112.store_returns_loss * t1114.f1) AS store_returns_loss,
            SUM(t1112.catalog_sales_profit * t1114.f1) AS catalog_sales_profit
        FROM (
            SELECT 
                t1108.ss_item_sk,
                t1108.ss_store_sk,
                t1108.cs_sold_date_sk,
                SUM(t1108.store_sales_profit * t1110.f1) AS store_sales_profit,
                SUM(t1108.store_returns_loss * t1110.f1) AS store_returns_loss,
                SUM(t1108.catalog_sales_profit * t1110.f1) AS catalog_sales_profit
            FROM (
                SELECT 
                    t1104.ss_item_sk,
                    t1104.ss_store_sk,
                    t1104.sr_returned_date_sk,
                    t1104.cs_sold_date_sk,
                    SUM(t1104.store_sales_profit * t1106.f1) AS store_sales_profit,
                    SUM(t1104.store_returns_loss * t1106.f1) AS store_returns_loss,
                    SUM(t1104.catalog_sales_profit * t1106.f1) AS catalog_sales_profit
                FROM (
                    SELECT 
                        t1101.ss_sold_date_sk,
                        t1101.ss_item_sk,
                        t1101.ss_store_sk,
                        t1101.sr_returned_date_sk,
                        t1102.cs_sold_date_sk,
                        SUM(t1101.store_sales_profit * t1102.f3) AS store_sales_profit,
                        SUM(t1101.store_returns_loss * t1102.f3) AS store_returns_loss,
                        SUM(t1101.f8 * t1102.catalog_sales_profit) AS catalog_sales_profit
                    FROM (
                        SELECT 
                            t1098.ss_sold_date_sk,
                            t1098.ss_item_sk,
                            t1098.ss_store_sk,
                            t1099.sr_returned_date_sk,
                            t1099.sr_item_sk,
                            t1099.sr_customer_sk,
                            SUM(t1098.store_sales_profit * t1099.f4) AS store_sales_profit,
                            SUM(t1098.f6 * t1099.store_returns_loss) AS store_returns_loss,
                            COALESCE(SUM(t1098.f6 * t1099.f4), 0) AS f8
                        FROM (
                            SELECT 
                                ss_sold_date_sk,
                                ss_item_sk,
                                ss_customer_sk,
                                ss_store_sk,
                                ss_ticket_number,
                                SUM(ss_net_profit) AS store_sales_profit,
                                COUNT(*) AS f6
                            FROM store_sales
                            GROUP BY ss_sold_date_sk, ss_item_sk, ss_customer_sk, ss_store_sk, ss_ticket_number
                        ) AS t1098
                        INNER JOIN (
                            SELECT 
                                sr_returned_date_sk,
                                sr_item_sk,
                                sr_customer_sk,
                                sr_ticket_number,
                                COUNT(*) AS f4,
                                SUM(sr_net_loss) AS store_returns_loss
                            FROM store_returns
                            GROUP BY sr_returned_date_sk, sr_item_sk, sr_customer_sk, sr_ticket_number
                        ) AS t1099
                        ON t1098.ss_customer_sk = t1099.sr_customer_sk
                           AND t1098.ss_item_sk = t1099.sr_item_sk
                           AND t1098.ss_ticket_number = t1099.sr_ticket_number
                        GROUP BY 
                            t1098.ss_sold_date_sk,
                            t1098.ss_item_sk,
                            t1098.ss_store_sk,
                            t1099.sr_returned_date_sk,
                            t1099.sr_item_sk,
                            t1099.sr_customer_sk
                    ) AS t1101
                    INNER JOIN (
                        SELECT 
                            cs_sold_date_sk,
                            cs_bill_customer_sk,
                            cs_item_sk,
                            COUNT(*) AS f3,
                            SUM(cs_net_profit) AS catalog_sales_profit
                        FROM catalog_sales
                        GROUP BY cs_sold_date_sk, cs_bill_customer_sk, cs_item_sk
                    ) AS t1102
                    ON t1101.sr_customer_sk = t1102.cs_bill_customer_sk
                       AND t1101.sr_item_sk = t1102.cs_item_sk
                    GROUP BY 
                        t1101.ss_sold_date_sk,
                        t1101.ss_item_sk,
                        t1101.ss_store_sk,
                        t1101.sr_returned_date_sk,
                        t1102.cs_sold_date_sk
                ) AS t1104
                INNER JOIN (
                    SELECT 
                        d_date_sk,
                        COUNT(*) AS f1
                    FROM date_dim
                    WHERE d_moy = 8 AND d_year = 2001
                    GROUP BY d_date_sk
                ) AS t1106
                ON t1104.ss_sold_date_sk = t1106.d_date_sk
                GROUP BY 
                    t1104.ss_item_sk,
                    t1104.ss_store_sk,
                    t1104.sr_returned_date_sk,
                    t1104.cs_sold_date_sk
            ) AS t1108
            INNER JOIN (
                SELECT 
                    d_date_sk,
                    COUNT(*) AS f1
                FROM date_dim
                WHERE d_moy BETWEEN 8 AND 8 + 2
                  AND d_year = 2001
                GROUP BY d_date_sk
            ) AS t1110
            ON t1108.sr_returned_date_sk = t1110.d_date_sk
            GROUP BY 
                t1108.ss_item_sk,
                t1108.ss_store_sk,
                t1108.cs_sold_date_sk
        ) AS t1112
        INNER JOIN (
            SELECT 
                d_date_sk,
                COUNT(*) AS f1
            FROM date_dim
            WHERE d_moy BETWEEN 8 AND 8 + 2
              AND d_year = 2001
            GROUP BY d_date_sk
        ) AS t1114
        ON t1112.cs_sold_date_sk = t1114.d_date_sk
        GROUP BY 
            t1112.ss_item_sk,
            t1112.ss_store_sk
    ) AS t1116
    INNER JOIN (
        SELECT 
            s_store_sk,
            s_store_id,
            s_store_name,
            COUNT(*) AS f3
        FROM store
        GROUP BY s_store_sk, s_store_id, s_store_name
    ) AS t1117
    ON t1116.ss_store_sk = t1117.s_store_sk
    GROUP BY 
        t1116.ss_item_sk,
        t1117.s_store_id,
        t1117.s_store_name
) AS t1119
INNER JOIN (
    SELECT 
        i_item_sk,
        i_item_id,
        i_item_desc,
        COUNT(*) AS f3
    FROM item
    GROUP BY i_item_sk, i_item_id, i_item_desc
) AS t1120
ON t1119.ss_item_sk = t1120.i_item_sk
GROUP BY 
    t1119.s_store_id,
    t1119.s_store_name,
    t1120.i_item_id,
    t1120.i_item_desc
ORDER BY 
    t1120.i_item_id,
    t1120.i_item_desc,
    t1119.s_store_id,
    t1119.s_store_name
FETCH NEXT 100 ROWS ONLY;
```



### 1.2. LLM-R2

*>* ***State：*** *Fails to rewrite*

---

### 1.3. R-Bot 

> **Execution Time：** 146.62s

```sql
SELECT 
    "item"."i_item_id",
    "item"."i_item_desc",
    "store"."s_store_id",
    "store"."s_store_name",
    SUM("store_sales"."ss_net_profit") AS "store_sales_profit",
    SUM("store_returns"."sr_net_loss") AS "store_returns_loss",
    SUM("catalog_sales"."cs_net_profit") AS "catalog_sales_profit"
FROM 
    "store_sales",
    "store_returns",
    "catalog_sales",
    "date_dim",
    "date_dim" AS "date_dim00" (
        "d_date_sk0", "d_date_id0", "d_date0", "d_month_seq0", "d_week_seq0",
        "d_quarter_seq0", "d_year0", "d_dow0", "d_moy0", "d_dom0", "d_qoy0",
        "d_fy_year0", "d_fy_quarter_seq0", "d_fy_week_seq0", "d_day_name0",
        "d_quarter_name0", "d_holiday0", "d_weekend0", "d_following_holiday0",
        "d_first_dom0", "d_last_dom0", "d_same_day_ly0", "d_same_day_lq0",
        "d_current_day0", "d_current_week0", "d_current_month0",
        "d_current_quarter0", "d_current_year0"
    ),
    "date_dim" AS "date_dim10" (
        "d_date_sk1", "d_date_id1", "d_date1", "d_month_seq1", "d_week_seq1",
        "d_quarter_seq1", "d_year1", "d_dow1", "d_moy1", "d_dom1", "d_qoy1",
        "d_fy_year1", "d_fy_quarter_seq1", "d_fy_week_seq1", "d_day_name1",
        "d_quarter_name1", "d_holiday1", "d_weekend1", "d_following_holiday1",
        "d_first_dom1", "d_last_dom1", "d_same_day_ly1", "d_same_day_lq1",
        "d_current_day1", "d_current_week1", "d_current_month1",
        "d_current_quarter1", "d_current_year1"
    ),
    "store",
    "item"
WHERE 
    "date_dim"."d_moy" = 8
    AND "date_dim"."d_year" = 2001
    AND "date_dim"."d_date_sk" = "store_sales"."ss_sold_date_sk"
    AND "item"."i_item_sk" = "store_sales"."ss_item_sk"
    AND "store"."s_store_sk" = "store_sales"."ss_store_sk"
    AND "store_sales"."ss_customer_sk" = "store_returns"."sr_customer_sk"
    AND "store_sales"."ss_item_sk" = "store_returns"."sr_item_sk"
    AND "store_sales"."ss_ticket_number" = "store_returns"."sr_ticket_number"
    AND "store_returns"."sr_returned_date_sk" = "date_dim00"."d_date_sk0"
    AND "date_dim00"."d_moy0" >= 8 AND "date_dim00"."d_moy0" <= 10
    AND "date_dim00"."d_year0" = 2001
    AND "store_returns"."sr_customer_sk" = "catalog_sales"."cs_bill_customer_sk"
    AND "store_returns"."sr_item_sk" = "catalog_sales"."cs_item_sk"
    AND "catalog_sales"."cs_sold_date_sk" = "date_dim10"."d_date_sk1"
    AND "date_dim10"."d_moy1" >= 8 AND "date_dim10"."d_moy1" <= 10
    AND "date_dim10"."d_year1" = 2001
GROUP BY 
    "store"."s_store_id",
    "store"."s_store_name",
    "item"."i_item_id",
    "item"."i_item_desc"
ORDER BY 
    "item"."i_item_id",
    "item"."i_item_desc",
    "store"."s_store_id",
    "store"."s_store_name"
FETCH NEXT 100 ROWS ONLY;
```



### 1.4. QUITE 

> **Execution Time：** 21.80s

```sql
WITH filtered_dates_1 AS (
    SELECT d_date_sk
    FROM date_dim
    WHERE d_moy = 8 AND d_year = 2001
),
filtered_dates_2 AS (
    SELECT d_date_sk
    FROM date_dim
    WHERE d_moy BETWEEN 8 AND 10 AND d_year = 2001
),
filtered_sales AS (
    SELECT 
        ss_customer_sk, 
        ss_item_sk, 
        ss_ticket_number, 
        ss_store_sk, 
        ss_net_profit
    FROM store_sales
    JOIN filtered_dates_1 ON ss_sold_date_sk = d_date_sk
),
filtered_returns AS (
    SELECT 
        sr_customer_sk, 
        sr_item_sk, 
        sr_ticket_number, 
        sr_net_loss
    FROM store_returns
    JOIN filtered_dates_2 ON sr_returned_date_sk = d_date_sk
),
filtered_catalog AS (
    SELECT 
        cs_bill_customer_sk, 
        cs_item_sk, 
        cs_net_profit
    FROM catalog_sales
    JOIN filtered_dates_2 ON cs_sold_date_sk = d_date_sk
)
SELECT 
    i_item_id,
    i_item_desc,
    s_store_id,
    s_store_name,
    SUM(fs.ss_net_profit) AS store_sales_profit,
    SUM(fr.sr_net_loss) AS store_returns_loss,
    SUM(fc.cs_net_profit) AS catalog_sales_profit
FROM filtered_sales fs
JOIN filtered_returns fr 
    ON fs.ss_customer_sk = fr.sr_customer_sk
    AND fs.ss_item_sk = fr.sr_item_sk
    AND fs.ss_ticket_number = fr.sr_ticket_number
JOIN filtered_catalog fc 
    ON fr.sr_customer_sk = fc.cs_bill_customer_sk
    AND fr.sr_item_sk = fc.cs_item_sk
JOIN store s 
    ON fs.ss_store_sk = s.s_store_sk
JOIN item i 
    ON fs.ss_item_sk = i.i_item_sk
GROUP BY 
    i_item_id, 
    i_item_desc, 
    s_store_id, 
    s_store_name
ORDER BY 
    i_item_id, 
    i_item_desc, 
    s_store_id, 
    s_store_name
LIMIT 100;
```





### **2. Deep Analysis**

#### **2.1 Query Context and Baseline Metrics**

This query performs a complex analysis of sales and returns across multiple channels (`store` and `catalog`) for a specific period. It is a classic star-schema query, joining three large fact tables (`store_sales`, `store_returns`, `catalog_sales`) with several dimension tables (`date_dim`, `store`, `item`). The main challenge is efficiently handling the joins and filters across these very large tables.

| **Rewrite Method**  | **Execution Time (s)** |
| ------------------- | ---------------------- |
| Original            | 126.66                 |
| LearnedRewrite (LR) | 273.57                 |
| LLM-R2              | Failed to Rewrite      |
| R-Bot               | 146.42                 |
| **QUITE**           | **21.80**              |

The performance results are stark. QUITE's rewrite is **5.8×** faster than the original query and **12.5×** faster than the pathological LR rewrite. It demonstrates a clear strategic advantage over all other versions.

#### **2.2 Quantifying the Runtime Gap**

- Original vs. QUITE

  The original query presents all seven tables to the optimizer at once, forcing it to solve a complex puzzle of finding the optimal join order and filtering strategy. This often leads to suboptimal plans where large tables are joined before being filtered. QUITE dictates a more efficient strategy, resulting in a 5.8× speedup.

- LearnedRewrite vs. QUITE

  The LR rewrite is a catastrophic failure. It attempts to break the query into deeply nested pre-aggregations, creating massive intermediate tables and adding enormous computational overhead. This "brute-force factorization" is the opposite of an optimization. QUITE’s elegant filtering approach is 12.5× faster, highlighting the dramatic difference between a sound strategy and a flawed one.

- R-Bot vs. QUITE

  The R-Bot rewrite is a trivial syntactic modification of the original. It offers no strategic improvement, and its slightly worse performance (146.42s vs 126.66s) is likely due to minor variations in the optimizer's plan. It fails to address the core performance bottleneck. QUITE's strategic rewrite outperforms it by 6.7×.

#### **2.3 Core Reasons for QUITE’s Superior Efficiency**

##### **2.3.1 The "Filter Early, Join Late" Strategy**

This is the canonical optimization technique for star-schema queries and the primary reason for QUITE's success. Instead of joining massive tables and then filtering the result, QUITE reverses the process:

1. **Filter First:** It first identifies the small number of relevant rows from the dimension tables (specifically, the dates).
2. **Reduce Facts:** It uses these small, filtered dimension sets to shrink the massive fact tables (`store_sales`, etc.).
3. **Join Last:** Only after all fact tables have been reduced to their minimal size does it perform the final joins between them.

This dramatically reduces the number of rows involved in each subsequent join, minimizing I/O and CPU costs.

##### **2.3.2 Effective Data Reduction via CTEs**

QUITE implements its strategy perfectly using Common Table Expressions (CTEs):

- **`filtered_dates_1` / `filtered_dates_2`:** These initial CTEs create tiny, in-memory tables containing only the `d_date_sk` keys for the specified time frame.
- **`filtered_sales` / `filtered_returns` / `filtered_catalog`:** These are the key workhorses. They perform a highly selective join between the multi-billion-row fact tables and the tiny `filtered_dates` CTEs. This effectively discards millions of irrelevant rows from the fact tables at the earliest possible stage, creating lean, intermediate results.

##### **2.3.3 Simplified Final Join Logic**

By the time the final `SELECT` statement in QUITE's rewrite is executed, the problem has been vastly simplified. Instead of joining three massive fact tables, the engine is now joining three much smaller, pre-filtered tables (`fs`, `fr`, `fc`). The expensive work is already done, and the final assembly of the result is cheap and fast.

##### **2.3.4 Guiding the Query Optimizer**

The original query's "bag of tables" structure gives the query optimizer many choices, most of which are bad. The CTEs in QUITE's rewrite provide a clear and efficient "recipe." This structure guides the optimizer to a near-perfect execution plan: start with the smallest tables, use them to shrink the largest tables, and assemble the results at the end.

#### **2.4 Illustrative Runtime Breakdown**

| **Rewrite Method** | **Key Traits**                                               | **Runtime (s)** | **Speedup vs. QUITE** |
| ------------------ | ------------------------------------------------------------ | --------------- | --------------------- |
| Original           | Complex multi-table join; optimizer overload.                | 126.66          | ~5.8× slower          |
| LearnedRewrite     | Pathological rewrite via excessive nested aggregation.       | 273.57          | ~12.5× slower         |
| R-Bot              | Trivial syntactic change; no strategic improvement.          | 146.42          | ~6.7× slower          |
| **QUITE**          | **"Filter Early, Join Late"; Strategic CTE data reduction.** | **21.80**       | **Baseline**          |