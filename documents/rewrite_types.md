# Effective SQL Rewrite Strategies — QUITE Benchmark Study

To analyze the **most effective rewrite types** observed in the **QUITE benchmark**,  
we collected all queries across four benchmark suites (`DSB`, `TPC-H`, `Calcite`, and `SQLStorm`)   where the **rewrite speedup exceeded 10×** and **query equivalence = true**.  

The file can be found in :
```
/QUITE/documents/effective_rewrite_types/CTE.json
/QUITE/documents/effective_rewrite_types/Join.json
/QUITE/documents/effective_rewrite_types/Predicate.json
```

We then categorized these rewrites into major **strategy types** — covering **CTE**, **Join**, and **Predicate** optimizations,   and summarized their representative patterns and simplified before/after examples below.

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