## Q2: Original Query

> **Execution Time:** 34.91s

> All execution times on this page are taken verbatim from the released per-query results in `experiments_results/calcite/`. Because the per-method result files do not share a common id ordering, records are matched by the literal constants of the original query.

```sql
SELECT t4.NAME FROM (SELECT NAME, DEPTNO, DEPTNO - 10 AS DEPTNOMINUS FROM DEPT) AS t4 INNER JOIN (SELECT DEPTNO, SAL + 1 AS f9 FROM EMP GROUP BY DEPTNO, SAL + 1) AS t6 ON t4.DEPTNOMINUS = t6.f9 AND t4.DEPTNO = t6.DEPTNO
```

## 1. Rewrite Results

### 1.1. LearnedRewrite

> **Execution Time:** 50.67s

```sql
SELECT t4.NAME FROM (SELECT NAME, DEPTNO, DEPTNO - 10 AS DEPTNOMINUS FROM DEPT)  AS t4 INNER JOIN (SELECT DEPTNO, SAL + 1 AS f9 FROM EMP GROUP BY DEPTNO, SAL + 1) AS t6 ON t4.DEPTNOMINUS = t6.f9 AND t4.DEPTNO = t6.DEPTNO
```

### 1.2. LLM-R2 (DS-R1, best equivalent model)

> **Execution Time:** 3.78s

```sql
SELECT DEPT.NAME FROM DEPT INNER JOIN EMP ON DEPT.DEPTNO - 10 = EMP.SAL + 1 AND DEPT.DEPTNO = EMP.DEPTNO
```

### 1.3. R-Bot (GPT-4o, fastest of three models)

> **Execution Time:** 35.76s  *(non-equivalent: rejected by our validation protocol)*

```sql
SELECT NAME FROM (SELECT name AS NAME, deptno AS DEPTNO, deptno - 10 AS DEPTNOMINUS         FROM dept         WHERE EXISTS (SELECT 1                 FROM (SELECT deptno0, sal + 1 AS f9                         FROM emp AS emp (empno, ename, job, mgr, hiredate, sal, comm, deptno0, slacker)) AS t0                 WHERE DEPTNOMINUS = t0.f9 AND DEPTNO = t0.deptno0)) AS t;
```

### 1.4. LLM Agent (DS-R1, best of four models)

> **Execution Time:** 41.35s

```sql
SELECT "DEPT"."NAME" FROM "DEPT" INNER JOIN (SELECT DISTINCT "DEPTNO", "SAL" + 1 AS "f9" FROM "EMP") AS "t6" ON "DEPT"."DEPTNO" = "t6"."DEPTNO" AND ("DEPT"."DEPTNO" - 10) = "t6"."f9"
```

### 1.5. QUITE

> **Execution Time:** 0.74s

```sql
SELECT d.NAME
FROM DEPT d
INNER JOIN (
    SELECT DISTINCT DEPTNO
    FROM EMP
    WHERE SAL = DEPTNO - 11
) e ON d.DEPTNO = e.DEPTNO
```


## 2. Deep Analysis

### 2.1 Query Context and Full Metrics

| Method | Execution Time (s) | Equivalent |
|---|---|---|
| LearnedRewrite | 50.67 | ✓ |
| LLM-R² (Claude-3.7) | 3.59 | ✗ (non-equivalent) |
| LLM-R² (DS-R1) | 3.78 | ✓ |
| LLM-R² (GPT-4o) | 3.64 | ✓ |
| R-Bot (Claude-3.7) | 36.20 | ✗ (non-equivalent) |
| R-Bot (DS-R1) | 36.01 | ✗ (non-equivalent) |
| R-Bot (GPT-4o) | 35.76 | ✗ (non-equivalent) |
| LLM Agent (Claude-3.7) | 52.95 | ✓ |
| LLM Agent (DS-R1) | 41.35 | ✓ |
| LLM Agent (DS-V3) | 52.12 | ✓ |
| LLM Agent (GPT-4o) | 50.14 | ✓ |
| QUITE | 0.74 | ✓ |

QUITE runs in 0.74s, a 47x speedup over the original and 4.9x ahead of the best equivalent baseline (LLM-R2 DS-R1, 3.78s). All three R-Bot variants and LLM-R2 Claude-3.7 are non-equivalent. LearnedRewrite and all four LLM Agent variants are slower than the original (41s--53s).

### 2.2 Why the Rewrite Is Fast

1. **Algebraic predicate propagation.** The join condition equates `DEPTNO - 10` (from the `DEPT` side) with `SAL + 1` (from the `EMP` side). QUITE rewrites this as a direct filter on `EMP`: `SAL = DEPTNO - 11`. The grouped derived table over `EMP` disappears entirely.
2. **Aggregation-to-DISTINCT collapse.** The original `GROUP BY DEPTNO, SAL + 1` exists only to deduplicate join keys; the rewrite replaces it with `SELECT DISTINCT DEPTNO`, removing the expression evaluation per row.
3. **Projection pruning.** Only `NAME` survives to the output, so the computed columns (`DEPTNOMINUS`, `f9`) vanish.

Deriving `SAL = DEPTNO - 11` requires solving the join equation across two derived tables, which is arithmetic reasoning rather than rule matching. This is the kind of rewrite that separates reasoning-based systems from pattern-based ones.
