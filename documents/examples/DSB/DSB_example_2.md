## Q2: Original Query

> **Execution Time:** 55.04s

> All execution times on this page are taken verbatim from the released per-query results in `experiments_results/dsb/`. Because the per-method result files do not share a common id ordering, records are matched by the literal constants of the original query.

```sql
select   i_item_id  ,i_item_desc  ,s_store_id  ,s_store_name  ,min(ss_net_profit) as store_sales_profit  ,min(sr_net_loss) as store_returns_loss  ,min(cs_net_profit) as catalog_sales_profit  from  store_sales  ,store_returns  ,catalog_sales  ,date_dim d1  ,date_dim d2  ,date_dim d3  ,store  ,item  where  d1.d_moy = 6  and d1.d_year = 2002  and d1.d_date_sk = ss_sold_date_sk  and i_item_sk = ss_item_sk  and s_store_sk = ss_store_sk  and ss_customer_sk = sr_customer_sk  and ss_item_sk = sr_item_sk  and ss_ticket_number = sr_ticket_number  and sr_returned_date_sk = d2.d_date_sk  and d2.d_moy               between 6 and  6 + 2  and d2.d_year              = 2002  and sr_customer_sk = cs_bill_customer_sk  and sr_item_sk = cs_item_sk  and cs_sold_date_sk = d3.d_date_sk  and d3.d_moy               between 6 and  6 + 2  and d3.d_year              = 2002  group by  i_item_id  ,i_item_desc  ,s_store_id  ,s_store_name  order by  i_item_id  ,i_item_desc  ,s_store_id  ,s_store_name  limit 100;
```

## 1. Rewrite Results

### 1.1. LearnedRewrite

> **Execution Time:** 188.07s

```sql
SELECT t1544.i_item_id, t1544.i_item_desc, t1543.s_store_id, t1543.s_store_name, MIN(t1543.store_sales_profit) AS store_sales_profit, MIN(t1543.store_returns_loss) AS store_returns_loss, MIN(t1543.catalog_sales_profit) AS catalog_sales_profit FROM (SELECT t1540.ss_item_sk, t1541.s_store_id, t1541.s_store_name, MIN(t1540.store_sales_profit) AS store_sales_profit, MIN(t1540.store_returns_loss) AS store_returns_loss, MIN(t1540.catalog_sales_profit) AS catalog_sales_profit FROM (SELECT t1536.ss_item_sk, t1536.ss_store_sk, MIN(t1536.store_sales_profit) AS store_sales_profit, MIN(t1536.store_returns_loss) AS store_returns_loss, MIN(t1536.catalog_sales_profit) AS catalog_sales_profit FROM (SELECT t1532.ss_item_sk, t1532.ss_store_sk, t1532.cs_sold_date_sk, MIN(t1532.store_sales_profit) AS store_sales_profit, MIN(t1532.store_returns_loss) AS store_returns_loss, MIN(t1532.catalog_sales_profit) AS catalog_sales_profit FROM (SELECT t1528.ss_item_sk, t1528.ss_store_sk, t1528.sr_returned_date_sk, t1528.cs_sold_date_sk, MIN(t1528.store_sales_profit) AS store_sales_profit, MIN(t1528.store_returns_loss) AS store_returns_loss, MIN(t1528.catalog_sales_profit) AS catalog_sales_profit FROM (SELECT t1525.ss_sold_date_sk, t1525.ss_item_sk, t1525.ss_store_sk, t1525.sr_returned_date_sk, t1526.cs_sold_date_sk, MIN(t1525.store_sales_profit) AS store_sales_profit, MIN(t1525.store_returns_loss) AS store_returns_loss, MIN(t1526.catalog_sales_profit) AS catalog_sales_profit FROM (SELECT t1522.ss_sold_date_sk, t1522.ss_item_sk, t1522.ss_store_sk, t1523.sr_returned_date_sk, t1523.sr_item_sk, t1523.sr_customer_sk, MIN(t1522.store_sales_profit) AS store_sales_profit, MIN(t1523.store_returns_loss) AS store_returns_loss FROM (SELECT ss_sold_date_sk, ss_item_sk, ss_customer_sk, ss_store_sk, ss_ticket_number, MIN(ss_net_profit) AS store_sales_profit FROM store_sales GROUP BY ss_sold_date_sk, ss_item_sk, ss_customer_sk, ss_store_sk, ss_ticket_number) AS t1522, (SELECT sr_returned_date_sk, sr_item_sk, sr_customer_sk, sr_ticket_number, MIN(sr_net_loss) AS store_returns_loss FROM store_returns GROUP BY sr_returned_date_sk, sr_item_sk, sr_customer_sk, sr_ticket_number) AS t1523 WHERE t1522.ss_customer_sk = t1523.sr_customer_sk AND t1522.ss_item_sk = t1523.sr_item_sk AND t1522.ss_ticket_number = t1523.sr_ticket_number GROUP BY t1522.ss_sold_date_sk, t1522.ss_item_sk, t1522.ss_store_sk, t1523.sr_returned_date_sk, t1523.sr_item_sk, t1523.sr_customer_sk) AS t1525, (SELECT cs_sold_date_sk, cs_bill_customer_sk, cs_item_sk, MIN(cs_net_profit) AS catalog_sales_profit FROM catalog_sales GROUP BY cs_sold_date_sk, cs_bill_customer_sk, cs_item_sk) AS t1526 WHERE t1525.sr_customer_sk = t1526.cs_bill_customer_sk AND t1525.sr_item_sk = t1526.cs_item_sk GROUP BY t1525.ss_sold_date_sk, t1525.ss_item_sk, t1525.ss_store_sk, t1525.sr_returned_date_sk, t1526.cs_sold_date_sk) AS t1528, (SELECT d_date_sk FROM date_dim WHERE d_moy = 6 AND d_year = 2002 GROUP BY d_date_sk) AS t1530 WHERE t1530.d_date_sk = t1528.ss_sold_date_sk GROUP BY t1528.ss_item_sk, t1528.ss_store_sk, t1528.sr_returned_date_sk, t1528.cs_sold_date_sk) AS t1532, (SELECT d_date_sk FROM date_dim WHERE d_moy >= 6 AND d_moy <= 6 + 2 AND d_year = 2002 GROUP BY d_date_sk) AS t1534 WHERE t1532.sr_returned_date_sk = t1534.d_date_sk GROUP BY t1532.ss_item_sk, t1532.ss_store_sk, t1532.cs_sold_date_sk) AS t1536, (SELECT d_date_sk FROM date_dim WHERE d_moy >= 6 AND d_moy <= 6 + 2 AND d_year = 2002 GROUP BY d_date_sk) AS t1538 WHERE t1536.cs_sold_date_sk = t1538.d_date_sk GROUP BY t1536.ss_item_sk, t1536.ss_store_sk) AS t1540, (SELECT s_store_sk, s_store_id, s_store_name FROM store GROUP BY s_store_sk, s_store_id, s_store_name) AS t1541 WHERE t1541.s_store_sk = t1540.ss_store_sk GROUP BY t1540.ss_item_sk, t1541.s_store_id, t1541.s_store_name) AS t1543, (SELECT i_item_sk, i_item_id, i_item_desc FROM item GROUP BY i_item_sk, i_item_id, i_item_desc) AS t1544 WHERE t1544.i_item_sk = t1543.ss_item_sk GROUP BY t1543.s_store_id, t1543.s_store_name, t1544.i_item_id, t1544.i_item_desc ORDER BY t1544.i_item_id, t1544.i_item_desc, t1543.s_store_id, t1543.s_store_name FETCH NEXT 100 ROWS ONLY
```

### 1.2. LLM-R2 (GPT-4o, best of three models)

> **Execution Time:** 67.84s

```sql
SELECT item.i_item_id, item.i_item_desc, store.s_store_id, store.s_store_name, MIN(store_sales.ss_net_profit) AS store_sales_profit, MIN(store_returns.sr_net_loss) AS store_returns_loss, MIN(catalog_sales.cs_net_profit) AS catalog_sales_profit FROM store_sales, store_returns, catalog_sales, date_dim, date_dim AS date_dim0, date_dim AS date_dim1, store, item WHERE date_dim.d_moy = 6 AND date_dim.d_year = 2002 AND (date_dim.d_date_sk = store_sales.ss_sold_date_sk AND item.i_item_sk = store_sales.ss_item_sk) AND (store.s_store_sk = store_sales.ss_store_sk AND store_sales.ss_customer_sk = store_returns.sr_customer_sk AND (store_sales.ss_item_sk = store_returns.sr_item_sk AND (store_sales.ss_ticket_number = store_returns.sr_ticket_number AND store_returns.sr_returned_date_sk = date_dim0.d_date_sk))) AND (date_dim0.d_moy >= 6 AND date_dim0.d_moy <= 6 + 2 AND (date_dim0.d_year = 2002 AND store_returns.sr_customer_sk = catalog_sales.cs_bill_customer_sk) AND (store_returns.sr_item_sk = catalog_sales.cs_item_sk AND catalog_sales.cs_sold_date_sk = date_dim1.d_date_sk AND (date_dim1.d_moy >= 6 AND (date_dim1.d_moy <= 6 + 2 AND date_dim1.d_year = 2002)))) GROUP BY store.s_store_id, store.s_store_name, item.i_item_id, item.i_item_desc ORDER BY item.i_item_id, item.i_item_desc, store.s_store_id, store.s_store_name LIMIT 100
```

### 1.3. R-Bot (DS-R1, best of three models)

> **Execution Time:** 74.20s

```sql
SELECT "item"."i_item_id", "item"."i_item_desc", "store"."s_store_id", "store"."s_store_name", MIN("store_sales"."ss_net_profit") AS "store_sales_profit", MIN("store_returns"."sr_net_loss") AS "store_returns_loss", MIN("catalog_sales"."cs_net_profit") AS "catalog_sales_profit" FROM "store_sales"     INNER JOIN "store_returns" ON "store_sales"."ss_customer_sk" = "store_returns"."sr_customer_sk" AND "store_sales"."ss_item_sk" = "store_returns"."sr_item_sk" AND "store_sales"."ss_ticket_number" = "store_returns"."sr_ticket_number"     INNER JOIN "catalog_sales" ON "store_returns"."sr_customer_sk" = "catalog_sales"."cs_bill_customer_sk" AND "store_returns"."sr_item_sk" = "catalog_sales"."cs_item_sk"     INNER JOIN (SELECT *         FROM "date_dim"         WHERE "d_moy" = 6 AND "d_year" = 2002) AS "t" ON "store_sales"."ss_sold_date_sk" = "t"."d_date_sk"     INNER JOIN (SELECT *         FROM "date_dim" AS "date_dim0" ("d_date_sk0", "d_date_id0", "d_date0", "d_month_seq0", "d_week_seq0", "d_quarter_seq0", "d_year0", "d_dow0", "d_moy0", "d_dom0", "d_qoy0", "d_fy_year0", "d_fy_quarter_seq0", "d_fy_week_seq0", "d_day_name0", "d_quarter_name0", "d_holiday0", "d_weekend0", "d_following_holiday0", "d_first_dom0", "d_last_dom0", "d_same_day_ly0", "d_same_day_lq0", "d_current_day0", "d_current_week0", "d_current_month0", "d_current_quarter0", "d_current_year0")         WHERE "d_moy0" >= 6 AND "d_moy0" <= 8 AND "d_year0" = 2002) AS "t0" ON "store_returns"."sr_returned_date_sk" = "t0"."d_date_sk0"     INNER JOIN (SELECT *         FROM "date_dim" AS "date_dim1" ("d_date_sk1", "d_date_id1", "d_date1", "d_month_seq1", "d_week_seq1", "d_quarter_seq1", "d_year1", "d_dow1", "d_moy1", "d_dom1", "d_qoy1", "d_fy_year1", "d_fy_quarter_seq1", "d_fy_week_seq1", "d_day_name1", "d_quarter_name1", "d_holiday1", "d_weekend1", "d_following_holiday1", "d_first_dom1", "d_last_dom1", "d_same_day_ly1", "d_same_day_lq1", "d_current_day1", "d_current_week1", "d_current_month1", "d_current_quarter1", "d_current_year1")         WHERE "d_moy1" >= 6 AND "d_moy1" <= 8 AND "d_year1" = 2002) AS "t1" ON "catalog_sales"."cs_sold_date_sk" = "t1"."d_date_sk1"     INNER JOIN "store" ON "store_sales"."ss_store_sk" = "store"."s_store_sk"     INNER JOIN "item" ON "store_sales"."ss_item_sk" = "item"."i_item_sk" GROUP BY "store"."s_store_id", "store"."s_store_name", "item"."i_item_id", "item"."i_item_desc" ORDER BY "item"."i_item_id", "item"."i_item_desc", "store"."s_store_id", "store"."s_store_name" FETCH NEXT 100 ROWS ONLY;
```

### 1.4. LLM Agent (Claude-3.7, best baseline overall)

> **Execution Time:** 11.83s

```sql
WITH joined_sales AS (
 SELECT ss.ss_customer_sk, ss.ss_item_sk, ss.ss_ticket_number,
 ss.ss_net_profit as store_sales_profit,
 i.i_item_id, i.i_item_desc,
 s.s_store_id, s.s_store_name
 FROM store_sales ss
 JOIN date_dim d1 ON d1.d_date_sk = ss.ss_sold_date_sk
 JOIN item i ON i.i_item_sk = ss.ss_item_sk
 JOIN store s ON s.s_store_sk = ss.ss_store_sk
 WHERE d1.d_year = 2002 AND d1.d_moy = 6
),
joined_returns AS (
 SELECT sr.sr_customer_sk, sr.sr_item_sk,
 sr.sr_ticket_number, sr.sr_net_loss
 FROM store_returns sr
 JOIN date_dim d2 ON d2.d_date_sk = sr.sr_returned_date_sk
 WHERE d2.d_year = 2002 AND d2.d_moy BETWEEN 6 AND 8
),
joined_catalog AS (
 SELECT cs.cs_bill_customer_sk, cs.cs_item_sk,
 cs.cs_net_profit as catalog_sales_profit
 FROM catalog_sales cs
 JOIN date_dim d3 ON d3.d_date_sk = cs.cs_sold_date_sk
 WHERE d3.d_year = 2002 AND d3.d_moy BETWEEN 6 AND 8
)
SELECT js.i_item_id,
 js.i_item_desc,
 js.s_store_id,
 js.s_store_name,
 MIN(js.store_sales_profit) as store_sales_profit,
 MIN(jr.sr_net_loss) as store_returns_loss,
 MIN(jc.catalog_sales_profit) as catalog_sales_profit
FROM joined_sales js
JOIN joined_returns jr ON jr.sr_customer_sk = js.ss_customer_sk
 AND jr.sr_item_sk = js.ss_item_sk
 AND jr.sr_ticket_number = js.ss_ticket_number
JOIN joined_catalog jc ON jc.cs_bill_customer_sk = jr.sr_customer_sk
 AND jc.cs_item_sk = jr.sr_item_sk
GROUP BY js.i_item_id, js.i_item_desc, js.s_store_id, js.s_store_name
ORDER BY js.i_item_id, js.i_item_desc, js.s_store_id, js.s_store_name
LIMIT 100
```

### 1.5. QUITE

> **Execution Time:** 3.87s

```sql
SELECT 
    i_item_id,
    i_item_desc,
    s_store_id,
    s_store_name,
    MIN(ss_net_profit) AS store_sales_profit,
    MIN(sr_net_loss) AS store_returns_loss,
    MIN(cs_agg.min_cs_net_profit) AS catalog_sales_profit
FROM store_sales
JOIN date_dim d1 ON d1.d_date_sk = store_sales.ss_sold_date_sk
    AND d1.d_moy = 6
    AND d1.d_year = 2002
JOIN item ON item.i_item_sk = store_sales.ss_item_sk
JOIN store ON store.s_store_sk = store_sales.ss_store_sk
JOIN store_returns ON store_sales.ss_customer_sk = store_returns.sr_customer_sk
    AND store_sales.ss_item_sk = store_returns.sr_item_sk
    AND store_sales.ss_ticket_number = store_returns.sr_ticket_number
JOIN date_dim d2 ON store_returns.sr_returned_date_sk = d2.d_date_sk
    AND d2.d_moy BETWEEN 6 AND 8
    AND d2.d_year = 2002
JOIN (
    SELECT 
        cs_bill_customer_sk,
        cs_item_sk,
        MIN(cs_net_profit) AS min_cs_net_profit
    FROM catalog_sales
    JOIN date_dim d3 ON catalog_sales.cs_sold_date_sk = d3.d_date_sk
        AND d3.d_moy BETWEEN 6 AND 8
        AND d3.d_year = 2002
    GROUP BY cs_bill_customer_sk, cs_item_sk
) cs_agg ON store_returns.sr_customer_sk = cs_agg.cs_bill_customer_sk
    AND store_returns.sr_item_sk = cs_agg.cs_item_sk
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


## 2. Deep Analysis

### 2.1 Query Context and Full Metrics

| Method | Execution Time (s) | Equivalent |
|---|---|---|
| LearnedRewrite | 188.07 | ✓ |
| LLM-R² (Claude-3.7) | 67.88 | ✓ |
| LLM-R² (DS-R1) | 75.29 | ✓ |
| LLM-R² (GPT-4o) | 67.84 | ✓ |
| R-Bot (Claude-3.7) | 105.69 | ✓ |
| R-Bot (DS-R1) | 74.20 | ✓ |
| R-Bot (GPT-4o) | 75.07 | ✓ |
| LLM Agent (Claude-3.7) | 11.83 | ✓ |
| LLM Agent (DS-R1) | 13.12 | ✓ |
| LLM Agent (DS-V3) | 70.28 | ✓ |
| LLM Agent (GPT-4o) | 73.87 | ✓ |
| QUITE | 3.87 | ✓ |

The original query joins three fact tables (`store_sales`, `store_returns`, `catalog_sales`) with three copies of `date_dim`, then computes per-item, per-store minima. QUITE finishes in 3.87s, a 14.2x speedup over the original and 3.1x ahead of the best baseline (LLM Agent, Claude-3.7). Every rule- or template-based rewrite makes the query slower than the original: LearnedRewrite runs at 188.07s (3.4x worse), and all LLM-R2 and R-Bot variants land between 67s and 106s.

### 2.2 Why the Rewrite Is Fast

1. **Pre-aggregation before the star join.** The rewrite computes `MIN(cs_net_profit)` per `(customer, item)` inside a derived table (`cs_agg`) before joining. The catalog side shrinks from raw fact rows to one row per group, so the three-way fact join multiplies far fewer rows.
2. **Date predicates pushed into join conditions.** Each `date_dim` copy is filtered (`d_moy`, `d_year`) inside its join clause, so every fact table is pruned by its time window before joining.

### 2.3 Why the Baselines Degrade

LearnedRewrite and LLM-R2 apply local, pattern-level transformations that reshape the join tree without introducing pre-aggregation; the reshaped plans materialize larger intermediates than the original. R-Bot's template-driven rewrites have the same blind spot. Recognizing that the catalog branch can be aggregated early requires reasoning about which columns the outer aggregation actually consumes, which is beyond fixed rule patterns.
