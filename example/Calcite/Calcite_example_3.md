## Q3：Original Query

> **Execution Time：** >300s

```sql
WITH e2 AS (
  SELECT empno, CASE WHEN TRUE THEN deptno ELSE NULL END AS deptno
  FROM emp
)
SELECT empno,
       deptno IN (SELECT deptno FROM e2 WHERE empno < 20) AS d
FROM e2;
````



## 1. Rewrite Results

### 1.1. LearnedRewrite

> **State：Fails to rewrite**

### 1.2. LLM-R2

> **Execution Time：** 12.22s
>
> ```sql
> SELECT t4.empno,
>        t7.f1 IS NOT NULL AND t4.f0 <> 0 OR 
>        (t4.deptno0 IS NULL OR t4.f1 < t4.f0) AND NULL AND 
>        t4.f0 <> 0 AND t7.f1 IS NULL AS d
> FROM (
>   SELECT t.empno, t.deptno, t3.f0, t3.f1, t.deptno AS deptno0
>   FROM (
>     SELECT EMPNO AS empno, CAST(DEPTNO AS INTEGER) AS deptno FROM EMP
>   ) AS t,
>   (
>     SELECT COUNT(*) AS f0, COUNT(deptno) AS f1
>     FROM (
>       SELECT EMPNO AS empno, CAST(DEPTNO AS INTEGER) AS deptno
>       FROM EMP
>     ) AS t0
>     WHERE empno < 20
>   ) AS t3
> ) AS t4
> LEFT JOIN (
>   SELECT deptno, TRUE AS f1
>   FROM (
>     SELECT EMPNO AS empno, CAST(DEPTNO AS INTEGER) AS deptno
>     FROM EMP
>   ) AS t5
>   WHERE empno < 20
> ) AS t7 ON t4.deptno0 = t7.deptno
> 
> ```

---

### 1.3. R-Bot 

> **State：Fails to rewrite**

### 1.4. QUITE 

> **Execution Time：** 8.24s

```sql
WITH deptno_set AS (
    SELECT deptno
    FROM emp
    WHERE empno < 20
)
SELECT e.empno,
       e.deptno IN (SELECT deptno FROM deptno_set) AS d
FROM emp AS e;
```





### **2. Deep Analysis**

#### **2.1 Query Context and Baseline Metrics**

This query defines a CTE `e2` that selects every `empno` and `deptno` from `emp` (wrapping `deptno` in a `CASE WHEN TRUE …`for no semantic change). Then, it asks for each row in `e2` whether its `deptno` appears among those same `deptno` values whose `empno < 20`. In effect, it checks membership of `deptno` in a small “deptno set” (the first 19 employees) for every employee in the table. The core work is:

1. Build `e2` as a full scan of `emp`.
2. Build a sub‐CTE (inside the `IN`) that re‐scans `e2` (i.e., `emp`) but filters to `empno < 20` to produce a small set of `deptno`s.
3. For every row in `e2` (i.e., every employee), check whether its `deptno` is in that small set.

The naive plan likely rescans `emp` twice (once to build `e2` and once inside the `IN`), and then for each row of `e2` runs a semi‐join (or nested loop) against the small set. In large tables, this can blow past 300 s.

| **Rewrite Method**  | **Execution Time (s)** |
| ------------------- | ---------------------- |
| Original            | > 300                  |
| LearnedRewrite (LR) | Fails to rewrite       |
| LLM-R2              | 12.22                  |
| R-Bot               | Fails to rewrite       |
| **QUITE**           | **8.24**               |

QUITE’s rewrite executes in **8.24 s**, representing a **> 36×** speedup over the original. LLM-R2 (12.22 s) also succeeds, but still remains **~1.5×** slower than QUITE.

------

#### **2.2 Quantifying the Runtime Gap**

- **Original vs. QUITE**
  The original defines `e2` as a full copy of `emp` (via `CASE WHEN TRUE …`), then in the outer query treats that same CTE twice: once as the driving relation for every `empno`, and again inside the `IN (SELECT deptno FROM e2 WHERE empno < 20)`. This effectively scans `emp` at least twice and performs a membership test for every row, likely via nested loops or a semi‐join that cannot reuse the small set efficiently. QUITE replaces all of that work with a simple CTE that extracts `deptno` for `empno < 20` (one scan) and then a single scan of `emp` with a semi‐join to that small set (one more scan). This transformation cuts redundant scans and simplifies the membership test, resulting in a **> 300s → 8.24 s** reduction (at least **36×** faster).
- **LLM-R2 vs. QUITE**
  LLM-R2 also factors out the small “empno < 20” set, but it uses two separate aggregations (`COUNT(*)`, `COUNT(deptno)`) and a more convoluted left‐join to detect presence. It still scans `emp` multiple times: once to compute the counts, once to build the small set, and once to drive the outer query. QUITE’s plan scans `emp`exactly twice—once to build the small set (`deptno_set`), once to probe every `emp` row with a direct `IN` against a hash of that set. The difference yields **12.22 s → 8.24 s** (≈ 1.48× speedup).
- **LearnedRewrite / R-Bot vs. QUITE**
  Both LR and R-Bot fail to rewrite. Since they produce no valid alternative, QUITE’s **8.24 s** is the only successful performance measurement.

------

#### **2.3 Core Reasons for QUITE’s Superior Efficiency**

##### **2.3.1 Eliminate Redundant Full CTE Scan**

- **Original / LLM-R2 / R-Bot:**
   - **Original** builds `e2` scanning `emp` once, then immediately scans `e2` again inside the `IN` subquery to form a small set of `deptno` values for `empno < 20`. Meanwhile, the outer query uses `e2` as its driving relation—but most engines will re‐materialize or re‐scan `e2` rather than keeping two live streams simultaneously. Thus, you end up scanning `emp` multiple times, plus running a membership check for every row.

 - **LLM-R2** effectively scans `emp` to compute two aggregates (`COUNT(*) AS f0`, `COUNT(deptno) AS f1`), then scans `emp` again to build the small set `deptno WHERE empno < 20`, then scans `emp` a third time to join every row to that small hash. So LLM-R2 does **3×** full table scans of `emp`.

- **QUITE:**
   - Uses a single CTE `deptno_set`:

  ```sql
  WITH deptno_set AS (
    SELECT deptno
    FROM emp
    WHERE empno < 20
  )
  ```

 - That is **one** full scan of `emp` (with filter `empno < 20`), producing a small set of at most 19 rows. Then the outer query:

````
```sql
SELECT e.empno,
       e.deptno IN (SELECT deptno FROM deptno_set) AS d
FROM emp AS e;
```
````

 - Scans `emp` a **second** time, performing a semi‐join (via `IN`) against the tiny `deptno_set`. Because `deptno_set` is very small, the optimizer will typically build an in‐memory hash of its keys, then probe for each row of `emp`. Thus, QUITE does exactly **2×** scans of `emp`, rather than 3× or more.

##### **2.3.2 Replace `CASE WHEN TRUE` CTE Wrapping with Direct Scanning**

- **Original:**
  The CTE `e2` uses `CASE WHEN TRUE THEN deptno ELSE NULL END AS deptno`, which forces the engine to evaluate a trivial expression for every row. Although that “CASE WHEN TRUE” is a no-op logically, it can prevent the optimizer from pushing down the `WHERE empno < 20` inside the CTE. The engine may treat `e2` as opaque, requiring a full CTE materialization.

- **QUITE:**
  Removes the CTE wrapper entirely for inner membership checks. By writing:

  ```sql
  WITH deptno_set AS (
    SELECT deptno
    FROM emp
    WHERE empno < 20
  )
  ```

  we push the `empno < 20` predicate directly into the scan. That allows the optimizer to build a compact hash for `deptno_set` without scanning all of `emp`.

##### **2.3.3 Simple Semi‐Join via `IN` vs. Complex Left‐Join/Filter Logic**

- **LLM-R2:**
  Performs a `LEFT JOIN` from a derived table `t4` (which itself scans `emp` and a precomputed counts subquery) to another derived table `t7` (which is `emp WHERE empno < 20`). The `LEFT JOIN` then uses a combination of multiple boolean expressions (`f1 IS NOT NULL AND f0 <> 0 OR …`) to derive the final boolean. This introduces string‐of‐AND/OR conditions that the optimizer cannot simplify into a direct semi‐join. It thus must maintain large intermediate join buffers.

- **QUITE:**
  Uses the concise expression `e.deptno IN (SELECT deptno FROM deptno_set)`. Since `deptno_set` is small, the engine will compile this into a hash‐semi‐join or anti‐join under the hood. Conceptually:

  1. Build hash table of `deptno_set` (19 keys).
  2. For each row `e` in `emp`, probe `deptno`.
  3. Return TRUE/FALSE accordingly.

  This is far more efficient than LLM-R2’s multi‐expression left‐join and boolean logic, because it avoids building any large intermediate result—only the final column of TRUE/FALSE per row.

##### **2.3.4 Flat, Two‐Stage Plan vs. Nested Derived Tables**

- **Original / LLM-R2 / R-Bot:**
   Their plans force multiple nesting levels. With each nested derived table—for example, LLM-R2’s `t4` and then left‐joining `t7`—the optimizer must allocate work areas, spool ephemeral results, and cannot unify predicate pushdowns across levels. That yields significant overhead in both memory and CPU.

- **QUITE:**
  Exposes exactly two operators to the optimizer:

  1. **Aggregate** (build `deptno_set` via `SELECT deptno FROM emp WHERE empno < 20`).
  2. **Semi‐Join** (via `deptno IN (deptno_set)`) as a simple hash lookup while scanning `emp`.

  This flat structure allows cost‐based join reorderings (though trivial here), in‐memory hash building for the small set, and a streaming scan over `emp` with minimal branching. As a result, QUITE can finish in **8.24 s**.

------

#### **2.4 Illustrative Runtime Breakdown**

| **Rewrite Method** | **Key Traits**                                               | **Runtime (s)** | **Speedup vs. QUITE** |
| ------------------ | ------------------------------------------------------------ | --------------- | --------------------- |
| Original           | CTE `e2` wraps full `emp` scan; nested membership check re‐scans `e2` (again `emp`); potential nested loops | > 300           | > 36× slower          |
| LLM-R2             | Multiple derived tables: one to compute counts, one to build small set, one to join each row; 3× scans | 12.22           | ~1.48× slower         |
| **QUITE**          | **CTE `deptno_set` (empno<20) + single scan of `emp` probing a small hash of `deptno_set`** | **8.24**        | **Baseline**          |