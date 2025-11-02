# Effective SQL Rewrite Strategies — QUITE Benchmark Study

To analyze the **most effective rewrite types** observed in the **QUITE benchmark**,  
we collected all queries across four benchmark suites (`DSB`, `TPC-H`, `Calcite`, and `SQLStorm`)   where the **rewrite speedup exceeded 10×** and **query equivalence = true**.  

The file can be found in :
```
/QUITE/documents/effective_rewrite_types/CTE.json
/QUITE/documents/effective_rewrite_types/Join.json
/QUITE/documents/effective_rewrite_types/Predicate.json
/QUITE/documents/effective_rewrite_types/Constant.json
/QUITE/documents/effective_rewrite_types/Others.json
```

We then categorized these rewrites into **strategy types** — covering **CTE**, **Join**, **Predicate**, **Constant** and **Others** optimizations, and summarized their representative patterns and simplified before/after examples below.

---




## CTE Summary Table

| Category | Strategy Name | Main Feature | ID | Avg. timesup |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **CTE for Nested Subquery Rewrite** | Rewrite correlated subqueries in `WHERE` or `SELECT` into a single CTE joined once, reducing N×M executions to N+M. | DSB_5, DSB_6, DSB_55, DSB_57, DSB_109, DSB_110, DSB_111, DSB_138, TPC-H_5, TPC-H_6, TPC-H_47, TPC-H_56, SQLStorm_41 | 79.49654 |
| 2 | **CTE Pre-Aggregation / Filtering / Reuse** | Use CTEs to precompute, aggregate, or filter data (e.g., date ranges, GROUP BY, IN lists), then reuse or join the smaller result to avoid repetition and reduce join volume. | DSB_56, DSB_136, DSB_137, TPC-H_46, TPC-H_55, SQLStorm_8, SQLStorm_24, SQLStorm_27, SQLStorm_29 | 35.25680 |
| 3 | **Join or Filter Pushdown into CTE** | Push `JOIN` or `WHERE` filters down into each CTE (e.g., UNION ALL) branch to reduce data before merging. | DSB_79, DSB_80 | 66.80019 |
| 4 | **Move Join Out of CTE** | Move join operations from inside aggregated CTEs to the main query, allowing GROUP BY inside CTEs to run on smaller, simpler datasets (e.g., IDs instead of strings). | SQLStorm_25 | 11.95327 |


#### **1. CTE for Nested Subquery Rewrite**
```sql
--Before
SELECT c.customer_id,
       (SELECT SUM(o.amount)
        FROM orders o
        WHERE o.customer_id = c.customer_id) AS total_amount
FROM customers c;


--After
WITH order_sum AS (
  SELECT customer_id, SUM(amount) AS total_amount
  FROM orders
  GROUP BY customer_id
)
SELECT c.customer_id, o.total_amount
FROM customers c
LEFT JOIN order_sum o ON c.customer_id = o.customer_id;
```
**Explanation:**
- Avoid running the subquery once per row. Precompute once with a CTE and join it.

#### **2. CTE Pre-Aggregation / Filtering / Reuse**
```sql
--Before
SELECT SUM(s.sales_amount)
FROM sales s
JOIN date_dim d ON s.date_id = d.date_id
WHERE d.sales_date BETWEEN '2025-01-01' AND '2025-01-31';

--After
WITH jan_dates AS (
  SELECT date_id
  FROM date_dim
  WHERE sales_date BETWEEN '2025-01-01' AND '2025-01-31'
)
SELECT SUM(s.sales_amount)
FROM sales s
JOIN jan_dates d ON s.date_id = d.date_id;
```
**Explanation:**
- Filter once in a CTE (reduces scanned data). The main query becomes simpler and faster.


#### **3. Join or Filter Pushdown into CTE**
```sql
--Before
WITH all_sales AS (
  SELECT * FROM web_sales
  UNION ALL
  SELECT * FROM store_sales
)
SELECT * 
FROM all_sales
WHERE sale_date >= '2025-01-01';


--After
WITH all_sales AS (
  SELECT * FROM web_sales WHERE sale_date >= '2025-01-01'
  UNION ALL
  SELECT * FROM store_sales WHERE sale_date >= '2025-01-01'
)
SELECT * FROM all_sales;
```
**Explanation:**
- Filter early inside each branch before merging — smaller result set, faster execution.

#### **4. Move Join Out of CTE**
```sql
-- Before
WITH sales_revenue AS (
  SELECT c.customer_name, SUM(s.amount) AS total
  FROM sales s
  JOIN customers c ON s.customer_id = c.customer_id
  GROUP BY c.customer_name
)
SELECT * FROM sales_revenue;

--After
WITH sales_revenue AS (
  SELECT customer_id, SUM(amount) AS total
  FROM sales
  GROUP BY customer_id
)
SELECT sr.total, c.customer_name
FROM sales_revenue sr
JOIN customers c ON sr.customer_id = c.customer_id;
```
**Explanation:**

- Let the CTE group by a simpler key (ID), then join later to reduce data inside aggregation.

## Join Summary Table

| Category | Strategy Name | Main Feature | ID | Avg. timesup |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Join Order Optimization** | Reorder joins so that filtered or smaller tables join first, reducing the number of rows processed later. | DSB_38, DSB_80, DSB_136, DSB_137, Calcite_40, Calcite_53, SQLStorm_25 | 39.60429 |
| 2 | **Use EXISTS Instead of Complex JOIN** | Replace `LEFT JOIN` + aggregation with `EXISTS` when only checking for existence to avoid unnecessary intermediate results. | Calcite_6 | 20.43797 |
| 3 | **Use DISTINCT Instead of Complex JOIN** | Replace `JOIN` + `GROUP BY` with `DISTINCT` when the goal is only to get unique values. | Calcite_50 | 27.93877 |

---

### Join Case Examples

#### **1. Join Order Optimization**

| Table | Row Count | Description |
| --- | --- | --- |
| `customers` | 1,000,000 | All customers |
| `orders` | 10,000,000 | Each customer can have multiple orders |
| `order_items` | 100,000,000 | Each order has many items |

```sql
-- Before
SELECT c.customer_name, o.order_id
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE oi.product_category = 'Electronics';

--After
SELECT c.customer_name, o.order_id
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
JOIN customers c ON o.customer_id = c.customer_id
WHERE oi.product_category = 'Electronics';
```
**Explanation:**
- Filtering happens earlier (order_items with 'Electronics' reduces data from 100M → ~2M rows).

- Later joins (orders, customers) process fewer rows, significantly improving performance.

#### **2. Use EXISTS Instead of Complex JOIN**
```sql
-- Before
SELECT DISTINCT e.employee_name
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.dept_id
WHERE d.dept_name = 'Sales';

-- After
SELECT e.employee_name
FROM employees e
WHERE EXISTS (
  SELECT 1
  FROM departments d
  WHERE d.dept_id = e.dept_id
    AND d.dept_name = 'Sales'
);
```

**Explanation:**
- Replaced a LEFT JOIN that materialized many rows with a lightweight EXISTS check.
- Avoids building a large intermediate result when only existence matters.

#### 3. Use DISTINCT Instead of Complex JOIN
```sql
-- Before
SELECT e.mgr, d.mgr
FROM emp AS e
FULL OUTER JOIN emp AS d ON e.mgr = d.mgr
GROUP BY d.mgr, e.mgr;

-- After
SELECT DISTINCT mgr
FROM emp;
```
**Explanation:**
- The goal was only to get unique manager IDs.

- DISTINCT expresses intent more directly and runs much faster than JOIN + GROUP BY.

## Predicate Summary Table

| Category | Strategy Name | Main Feature | ID | Avg. timesup |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Predicate Pushdown** | Push `WHERE` filters (or `JOIN` conditions) down into CTEs, UNION ALL branches, or subqueries, or move them from `HAVING` to `WHERE` to filter earlier. | DSB_5, DSB_79, DSB_81, TPC-H_55, Calcite_44, Calcite_51, Calcite_53, SQLStorm_24, SQLStorm_27, SQLStorm_41 | 26.99197 |
| 2 | **Predicate or Expression Simplification** | Simplify arithmetic or multi-column expressions (especially in JOIN conditions) into simpler, equivalent predicates, or reduce redundant calculations in the SELECT list. | DSB_6, DSB_57, Calcite_40, SQLStorm_8 | 50.63979 |
| 3 | **Use EXISTS Instead of JOIN** | Replace full `JOIN` operations with `EXISTS` (semi-join) when only checking for the existence of related rows to avoid large intermediate result sets. | Calcite_6 | 20.43797 |

#### **1. Predicate Pushdown**
```sql
-- Before
SELECT NAME AS NAME, DEPTNO AS DDEPTNO, COUNT(*) AS C
FROM DEPT
GROUP BY GROUPING SETS((NAME, DEPTNO), NAME)
HAVING NAME = 'Charlie';


--After
SELECT NAME AS NAME, DEPTNO AS DDEPTNO, COUNT(*) AS C
FROM DEPT
WHERE NAME = 'Charlie'
GROUP BY GROUPING SETS((NAME, DEPTNO), NAME);
```
**Explanation:**
- Move NAME = 'Charlie' from the HAVING clause to WHERE since it filters on a non-aggregated column.

#### **2. Predicate or Expression Simplification**
```sql
--Before
SELECT sr_customer_sk, sr_store_sk, sr_reason_sk
FROM store_returns, date_dim
WHERE sr_returned_date_sk = d_date_sk
  AND d_year = 2000
  AND sr_return_amt / sr_return_quantity BETWEEN 107 AND 166;


--After
SELECT sr_customer_sk, sr_store_sk, sr_reason_sk
FROM store_returns
JOIN date_dim ON sr_returned_date_sk = d_date_sk
WHERE d_year = 2000
  AND sr_return_quantity > 0
  AND sr_return_amt BETWEEN 107 * sr_return_quantity
                        AND 166 * sr_return_quantity;
```
**Explanation:**
- Replace sr_return_amt / sr_return_quantity with multiplication — avoids division, prevents divide-by-zero

#### **3. Use EXISTS Instead of JOIN**
```sql
--Before
SELECT t6.ENAME
FROM (
  SELECT JOB FROM EMP WHERE ENAME = 'A' GROUP BY JOB
) AS t5
LEFT JOIN (
  SELECT ENAME, JOB FROM EMP GROUP BY ENAME, JOB
) AS t6
ON t5.JOB = t6.JOB
GROUP BY t6.ENAME;


--After
SELECT DISTINCT E.ENAME
FROM EMP E
WHERE EXISTS (
  SELECT 1
  FROM EMP A
  WHERE A.ENAME = 'A'
    AND A.JOB = E.JOB
);
```
**Explanation:**
- Use EXISTS (semi-join) to check for matching jobs directly to
avoids building large intermediate join results and simplifies logic.

---

## Constant Summary Table

| Category | Strategy Name | Main Feature | ID | Avg. timesup |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Constant Folding/Arithmetic Simplification** | Precompute pure constant expressions (e.g., `6 + 2` becomes `8`, or `69 * 0.01` becomes `0.69`) to simplify queries. | DSB_38, DSB_56, DSB_138 | 46.79554 |
| 2 | **Arithmetic Expression Rewrite** | Rewrite arithmetic operations in predicates (e.g., replace division involving columns with multiplication) to improve performance. | DSB_55 | 30.50860 |
| 3 | **Merge Constant Lookups** | Replace multiple subqueries for retrieving constants (e.g., dates) with methods like `CROSS JOIN` to reduce redundant scans. | DSB_81 | 23.92862 |

---

### Constant Case Examples

#### **1. Constant Folding/Arithmetic Simplification**
```sql
--Before
select  sum(cs_ext_discount_amt)  as "excess discount amount" from    catalog_sales    ,item    ,date_dim where (i_manufact_id in (291, 335, 604, 696, 887) or i_manager_id BETWEEN 35 and 64) and i_item_sk = cs_item_sk and d_date between '1998-03-22' and         cast('1998-03-22' as date) + interval '90' day and d_date_sk = cs_sold_date_sk and cs_ext_discount_amt      > (          select             1.3 * avg(cs_ext_discount_amt)          from             catalog_sales            ,date_dim          where               cs_item_sk = i_item_sk           and d_date between '1998-03-22' and                              cast('1998-03-22' as date) + interval '90' day           and d_date_sk = cs_sold_date_sk           and cs_list_price between 119 and 148           and cs_sales_price / cs_list_price BETWEEN 58 * 0.01 AND 78 * 0.01       ) order by sum(cs_ext_discount_amt) limit 100;

--After
WITH date_range AS (
    SELECT d_date_sk
    FROM date_dim
    WHERE d_date BETWEEN '1998-03-22' AND (CAST('1998-03-22' AS DATE) + INTERVAL '90' DAY)
),
subquery_avg AS (
    SELECT cs_item_sk, 1.3 * AVG(cs_ext_discount_amt) AS avg_discount
    FROM catalog_sales cs
    JOIN date_range dr ON cs.cs_sold_date_sk = dr.d_date_sk
    WHERE cs.cs_list_price BETWEEN 119 AND 148
      AND (cs.cs_sales_price / cs.cs_list_price) BETWEEN 0.58 AND 0.78
    GROUP BY cs.cs_item_sk
)
SELECT SUM(cs.cs_ext_discount_amt) AS "excess discount amount"
FROM catalog_sales cs
JOIN item i ON cs.cs_item_sk = i.i_item_sk
JOIN date_range dr ON cs.cs_sold_date_sk = dr.d_date_sk
JOIN subquery_avg sa ON cs.cs_item_sk = sa.cs_item_sk
WHERE (i.i_manufact_id IN (291, 335, 604, 696, 887) OR i.i_manager_id BETWEEN 35 AND 64)
  AND cs.cs_ext_discount_amt > sa.avg_discount
ORDER BY SUM(cs.cs_ext_discount_amt)
LIMIT 100;
```
**Explanation:**
- Replace the correlated subquery with a CTE to precompute the average discount per item once instead of calculating it for each row in the main query.
- Precompute the constant expressions `58 * 0.01` and `78 * 0.01` as `0.58` and `0.78` for better readability and potentially improved performance.

#### **2. Arithmetic Expression Rewrite**
```sql
--Before
select  sum(cs_ext_discount_amt)  as "excess discount amount" from    catalog_sales    ,item    ,date_dim where (i_manufact_id in (117, 306, 658, 849, 891) or i_manager_id BETWEEN 28 and 57) and i_item_sk = cs_item_sk and d_date between '1999-01-14' and         cast('1999-01-14' as date) + interval '90' day and d_date_sk = cs_sold_date_sk and cs_ext_discount_amt      > (          select             1.3 * avg(cs_ext_discount_amt)          from             catalog_sales            ,date_dim          where               cs_item_sk = i_item_sk           and d_date between '1999-01-14' and                              cast('1999-01-14' as date) + interval '90' day           and d_date_sk = cs_sold_date_sk           and cs_list_price between 236 and 265           and cs_sales_price / cs_list_price BETWEEN 45 * 0.01 AND 65 * 0.01       ) order by sum(cs_ext_discount_amt) limit 100;

--After
WITH avg_discount AS (
  SELECT 
    cs_item_sk, 
    1.3 * avg(cs_ext_discount_amt) as avg_disc
  FROM 
    catalog_sales, 
    date_dim
  WHERE 
    d_date between '1999-01-14' and cast('1999-01-14' as date) + interval '90' day
    AND cs_sold_date_sk = d_date_sk
    AND cs_list_price between 236 and 265
    AND cs_sales_price BETWEEN 0.45 * cs_list_price AND 0.65 * cs_list_price
  GROUP BY 
    cs_item_sk
)
SELECT 
  sum(cs.cs_ext_discount_amt) as "excess discount amount"
FROM 
  catalog_sales cs
  JOIN item i ON cs.cs_item_sk = i.i_item_sk
  JOIN date_dim d ON cs.cs_sold_date_sk = d.d_date_sk
  JOIN avg_discount ad ON cs.cs_item_sk = ad.cs_item_sk
WHERE 
  (i.i_manufact_id in (117, 306, 658, 849, 891) or i.i_manager_id BETWEEN 28 and 57)
  AND d.d_date between '1999-01-14' and cast('1999-01-14' as date) + interval '90' day
  AND cs.cs_ext_discount_amt > ad.avg_disc
ORDER BY 
  sum(cs.cs_ext_discount_amt)
LIMIT 100;
```
**Explanation:**
- Convert the correlated subquery to a CTE with GROUP BY to avoid executing it for each row in the main query.
- Replace division `cs_sales_price / cs_list_price BETWEEN 45 * 0.01 AND 65 * 0.01` with multiplication `cs_sales_price BETWEEN 0.45 * cs_list_price AND 0.65 * cs_list_price` to improve performance.

#### **3. Merge Constant Lookups**
```sql
--Before
with my_customers as (  select distinct c_customer_sk         , c_current_addr_sk  from         ( select cs_sold_date_sk sold_date_sk,                  cs_bill_customer_sk customer_sk,                  cs_item_sk item_sk,                  cs_wholesale_cost wholesale_cost           from   catalog_sales           union all           select ws_sold_date_sk sold_date_sk,                  ws_bill_customer_sk customer_sk,                  ws_item_sk item_sk,                  ws_wholesale_cost wholesale_cost           from   web_sales          ) cs_or_ws_sales,          item,          date_dim,          customer  where   sold_date_sk = d_date_sk          and item_sk = i_item_sk          and i_category = 'Electronics'          and i_class = 'portable'          and c_customer_sk = cs_or_ws_sales.customer_sk          and d_moy = 6          and d_year = 2002          and wholesale_cost BETWEEN 70 AND 100          and c_birth_year BETWEEN 1978 AND 1991  )  , my_revenue as (  select c_customer_sk,         sum(ss_ext_sales_price) as revenue  from   my_customers,         store_sales,         customer_address,         store,         date_dim  where  c_current_addr_sk = ca_address_sk         and ca_county = s_county         and ca_state = s_state         and ss_sold_date_sk = d_date_sk         and c_customer_sk = ss_customer_sk         and ss_wholesale_cost BETWEEN 70 AND 100         and s_state in ('AL','AR','FL'                     ,'MN','MO','NC'                     ,'NY','OK','PA'                     ,'WI')         and d_month_seq between (select distinct d_month_seq+1                                  from   date_dim where d_year = 2002 and d_moy = 6)                            and  (select distinct d_month_seq+3                                  from   date_dim where d_year = 2002 and d_moy = 6)  group by c_customer_sk  )  , segments as  (select cast((revenue/50) as int) as segment   from   my_revenue  )   select  segment, count(*) as num_customers, segment*50 as segment_base  from segments  group by segment  order by segment, num_customers  limit 100;

--After
WITH my_customers AS (
  SELECT DISTINCT c_customer_sk, c_current_addr_sk
  FROM (
    SELECT cs_sold_date_sk AS sold_date_sk, 
           cs_bill_customer_sk AS customer_sk, 
           cs_item_sk AS item_sk, 
           cs_wholesale_cost AS wholesale_cost
    FROM catalog_sales
    JOIN item ON catalog_sales.cs_item_sk = item.i_item_sk
    JOIN date_dim ON catalog_sales.cs_sold_date_sk = date_dim.d_date_sk
    WHERE item.i_category = 'Electronics'
      AND item.i_class = 'portable'
      AND date_dim.d_moy = 6
      AND date_dim.d_year = 2002
      AND catalog_sales.cs_wholesale_cost BETWEEN 70 AND 100
    UNION ALL
    SELECT ws_sold_date_sk AS sold_date_sk,
           ws_bill_customer_sk AS customer_sk,
           ws_item_sk AS item_sk,
           ws_wholesale_cost AS wholesale_cost
    FROM web_sales
    JOIN item ON web_sales.ws_item_sk = item.i_item_sk
    JOIN date_dim ON web_sales.ws_sold_date_sk = date_dim.d_date_sk
    WHERE item.i_category = 'Electronics'
      AND item.i_class = 'portable'
      AND date_dim.d_moy = 6
      AND date_dim.d_year = 2002
      AND web_sales.ws_wholesale_cost BETWEEN 70 AND 100
  ) cs_or_ws_sales
  JOIN customer ON customer.c_customer_sk = cs_or_ws_sales.customer_sk
  WHERE customer.c_birth_year BETWEEN 1978 AND 1991
), 
my_revenue AS (
  SELECT c_customer_sk,
         SUM(ss_ext_sales_price) AS revenue
  FROM my_customers
  JOIN store_sales ON my_customers.c_customer_sk = store_sales.ss_customer_sk
  JOIN customer_address ON my_customers.c_current_addr_sk = customer_address.ca_address_sk
  JOIN store ON customer_address.ca_county = store.s_county 
            AND customer_address.ca_state = store.s_state
  JOIN date_dim ON store_sales.ss_sold_date_sk = date_dim.d_date_sk
  CROSS JOIN (SELECT d_month_seq AS base FROM date_dim WHERE d_year = 2002 AND d_moy = 6) d
  WHERE store_sales.ss_wholesale_cost BETWEEN 70 AND 100
    AND store.s_state IN ('AL','AR','FL','MN','MO','NC','NY','OK','PA','WI')
    AND date_dim.d_month_seq BETWEEN d.base + 1 AND d.base + 3
  GROUP BY c_customer_sk
), 
segments AS (
  SELECT CAST((revenue / 50) AS INT) AS segment
  FROM my_revenue
)
SELECT segment, 
       COUNT(*) AS num_customers, 
       segment * 50 AS segment_base
FROM segments
GROUP BY segment
ORDER BY segment, num_customers
LIMIT 100;
```
**Explanation:**
- Push item and date_dim joins into each UNION ALL subquery in my_customers CTE to filter data early before the union operation, reducing the amount of data processed.
- Replace two separate date_dim subqueries with a single `CROSS JOIN` in my_revenue CTE to reduce redundant scans of the date_dim table.

---

## Others Summary Table

| Category | Strategy Name | Main Feature | ID | Avg. timesup |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Deduplication/Uniqueness Optimization** | Use `DISTINCT` instead of `GROUP BY` when the goal is only deduplication; or use `DISTINCT ON` to replace `ROW_NUMBER()` window functions to get the latest row per group. | Calcite_6, Calcite_40, SQLStorm_8 | 30.71919 |
| 2 | **Query Structure Simplification** | Remove redundant subquery levels that can be flattened; or use column aliases in `ORDER BY` clause instead of complex expressions. | Calcite_51, SQLStorm_41 | 26.62415 |
| 3 | **COALESCE for NULL Handling** | Use `COALESCE` in the `SELECT` list to handle potential `NULL` values from `LEFT JOIN`, ensuring data correctness (e.g., counts). | SQLStorm_27 | 20.46237 |

---

### Others Case Examples

#### **1. Deduplication/Uniqueness Optimization**
```sql
--Before
SELECT t6.ENAME FROM (SELECT JOB FROM EMP WHERE ENAME = 'A' GROUP BY JOB) AS t5 LEFT JOIN (SELECT ENAME, JOB FROM EMP GROUP BY ENAME, JOB) AS t6 ON t5.JOB = t6.JOB GROUP BY t6.ENAME

--After
SELECT DISTINCT E.ENAME
FROM EMP E
WHERE EXISTS (
  SELECT 1 
  FROM EMP A 
  WHERE A.ENAME = 'A' 
    AND A.JOB = E.JOB
)
```
**Explanation:**
- Replace the complex `LEFT JOIN` between two derived tables with an `EXISTS` semi-join to avoid unnecessary intermediate result sets.
- Replace final `GROUP BY` with `DISTINCT` to achieve the same result with clearer intent.

#### **2. Query Structure Simplification**
```sql
--Before
select dname, ddeptno, c from              (select name dname, deptno ddeptno, count(*) as c              from dept group by grouping sets ((name,deptno),(name))) t               where dname = 'Charlie'

--After
select name as dname, deptno as ddeptno, count(*) as c
from dept
where name = 'Charlie'
group by grouping sets ((name, deptno), (name));
```
**Explanation:**
- Push the filter condition `dname = 'Charlie'` into the base query to reduce the amount of data processed in the aggregation.
- Eliminate the unnecessary subquery since the filter can be applied directly.

#### **3. COALESCE for NULL Handling**
```sql
--Before
SELECT     p.Id AS PostId,    p.Title,    p.CreationDate AS PostCreationDate,    p.ViewCount,    p.Score,    p.AnswerCount,    u.DisplayName AS OwnerDisplayName,    COUNT(DISTINCT v.Id) AS VoteCount,    COUNT(DISTINCT c.Id) AS CommentCount,    MAX(b.Date) AS LastBadgeDate,    COUNT(DISTINCT b.Id) AS BadgeCount FROM     Posts p JOIN     Users u ON p.OwnerUserId = u.Id LEFT JOIN     Votes v ON p.Id = v.PostId LEFT JOIN     Comments c ON p.Id = c.PostId LEFT JOIN     Badges b ON u.Id = b.UserId WHERE     p.CreationDate >= '2023-01-01'  GROUP BY     p.Id, p.Title, p.CreationDate, p.ViewCount, p.Score, p.AnswerCount, u.DisplayName ORDER BY     p.CreationDate DESC;

--After
WITH FilteredPosts AS (
    SELECT *
    FROM Posts
    WHERE CreationDate >= '2023-01-01'
),
VoteCounts AS (
    SELECT 
        v.PostId, 
        COUNT(DISTINCT v.Id) AS VoteCount
    FROM Votes v
    JOIN FilteredPosts fp ON v.PostId = fp.Id
    GROUP BY v.PostId
),
CommentCounts AS (
    SELECT 
        c.PostId, 
        COUNT(DISTINCT c.Id) AS CommentCount
    FROM Comments c
    JOIN FilteredPosts fp ON c.PostId = fp.Id
    GROUP BY c.PostId
),
BadgeInfo AS (
    SELECT 
        b.UserId, 
        MAX(b.date) AS LastBadgeDate, 
        COUNT(DISTINCT b.Id) AS BadgeCount
    FROM Badges b
    WHERE b.UserId IN (SELECT DISTINCT p.OwnerUserId FROM FilteredPosts p)
    GROUP BY b.UserId
)
SELECT 
    p.Id AS PostId, 
    p.Title, 
    p.CreationDate AS PostCreationDate, 
    p.ViewCount, 
    p.Score, 
    p.AnswerCount, 
    u.DisplayName AS OwnerDisplayName, 
    COALESCE(v.VoteCount, 0) AS VoteCount, 
    COALESCE(c.CommentCount, 0) AS CommentCount, 
    b.LastBadgeDate, 
    COALESCE(b.BadgeCount, 0) AS BadgeCount
FROM FilteredPosts p
JOIN Users u ON p.OwnerUserId = u.Id
LEFT JOIN VoteCounts v ON p.Id = v.PostId
LEFT JOIN CommentCounts c ON p.Id = c.PostId
LEFT JOIN BadgeInfo b ON u.Id = b.UserId
ORDER BY p.CreationDate DESC;
```
**Explanation:**
- Use CTEs to pre-filter posts by date before joining with other tables.
- Pre-aggregate Comments and Votes data before joining to reduce the number of rows processed.
- Use `COALESCE` to handle NULL values for posts without comments or votes.
