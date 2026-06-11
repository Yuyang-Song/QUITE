## Q1: Original Query

> **Execution Time:** 2.54s

> All execution times on this page are taken verbatim from the released per-query results in `experiments_results/calcite/`. Because the per-method result files do not share a common id ordering, records are matched by the literal constants of the original query.

```sql
SELECT COALESCE(SUM(EXPR0), 0), T2 FROM (SELECT t5.T2, COUNT(CASE WHEN EMP1.DEPTNO = 0 THEN 1 ELSE NULL END) AS EXPR0 FROM EMP AS EMP1, (VALUES (1)) AS t5 (T2) GROUP BY t5.T2 UNION ALL SELECT t8.T2, COUNT(CASE WHEN EMP2.DEPTNO = 0 THEN 1 ELSE NULL END) AS EXPR0 FROM EMP AS EMP2, (VALUES (2)) AS t8 (T2) GROUP BY t8.T2) AS t11 GROUP BY T2
```

## 1. Rewrite Results

### 1.1. LearnedRewrite

> **Execution Time:** 3.18s

```sql
SELECT COALESCE(SUM(EXPR0), 0), T2 FROM (SELECT t5.T2, COUNT(CASE WHEN EMP1.DEPTNO = 0 THEN 1 ELSE NULL END) AS EXPR0 FROM EMP AS EMP1, (VALUES (1)) AS t5 (T2) GROUP BY t5.T2 UNION ALL SELECT t8.T2, COUNT(CASE WHEN EMP2.DEPTNO = 0 THEN 1 ELSE NULL END) AS EXPR0 FROM EMP AS EMP2, (VALUES (2)) AS t8 (T2) GROUP BY t8.T2) AS t11 GROUP BY T2
```

### 1.2. LLM-R2 (GPT-4o, best of three models)

> **Execution Time:** 3.24s

```sql
SELECT COALESCE(SUM("EXPR0"), 0), "T2" FROM (SELECT "t5"."T2", COUNT(CASE WHEN "EMP1"."DEPTNO" = 0 THEN 1 ELSE NULL END) AS "EXPR0" FROM "EMP" AS "EMP1", (VALUES (1)) AS "t5" ("T2") GROUP BY "t5"."T2" UNION ALL SELECT "t8"."T2", COUNT(CASE WHEN "EMP2"."DEPTNO" = 0 THEN 1 ELSE NULL END) AS "EXPR0" FROM "EMP" AS "EMP2", (VALUES (2)) AS "t8" ("T2") GROUP BY "t8"."T2") AS "t11" GROUP BY "T2"
```

### 1.3. R-Bot (GPT-4o, fastest of three models)

> **Execution Time:** 2.70s  *(non-equivalent: rejected by our validation protocol)*

```sql
SELECT SUM(EXPR0) AS f1, T2 FROM (SELECT t0.T2, COUNT(*) FILTER (WHERE emp.deptno = 0) AS EXPR0             FROM emp,                     (VALUES (1)) AS t (T2),                     (VALUES (1)) AS t0 (T2)             GROUP BY t0.T2             UNION ALL             SELECT t4.T2 AS T20, COUNT(*) FILTER (WHERE emp00.deptno0 = 0) AS EXPR0             FROM emp AS emp00 (empno0, ename0, job0, mgr0, hiredate0, sal0, comm0, deptno0, slacker0),                     (VALUES (2)) AS t3 (T2),                     (VALUES (2)) AS t4 (T2)             GROUP BY t4.T2) AS t7 GROUP BY T2;
```

### 1.4. LLM Agent (DS-R1, best of four models)

> **Execution Time:** 3.12s

```sql
SELECT COALESCE(SUM("EXPR0"), 0), "T2" FROM (SELECT 1 AS "T2", COUNT(CASE WHEN "EMP"."DEPTNO" = 0 THEN 1 END) AS "EXPR0" FROM "EMP" UNION ALL SELECT 2 AS "T2", COUNT(CASE WHEN "EMP"."DEPTNO" = 0 THEN 1 END) AS "EXPR0" FROM "EMP") AS "t11" GROUP BY "T2"
```

### 1.5. QUITE

> **Execution Time:** 0.71s

```sql
WITH counts AS (
    SELECT COUNT(*) AS cnt 
    FROM EMP 
    WHERE DEPTNO = 0
)
SELECT counts.cnt, t.T2
FROM (VALUES (1), (2)) AS t(T2)
CROSS JOIN counts;
```


## 2. Deep Analysis

### 2.1 Query Context and Full Metrics

| Method | Execution Time (s) | Equivalent |
|---|---|---|
| LearnedRewrite | 3.18 | ✓ |
| LLM-R² (Claude-3.7) | 3.48 | ✓ |
| LLM-R² (DS-R1) | 3.37 | ✓ |
| LLM-R² (GPT-4o) | 3.24 | ✓ |
| R-Bot (Claude-3.7) | 2.86 | ✗ (non-equivalent) |
| R-Bot (DS-R1) | 3.03 | ✗ (non-equivalent) |
| R-Bot (GPT-4o) | 2.70 | ✗ (non-equivalent) |
| LLM Agent (Claude-3.7) | 3.17 | ✓ |
| LLM Agent (DS-R1) | 3.12 | ✓ |
| LLM Agent (DS-V3) | 7.18 | ✓ |
| LLM Agent (GPT-4o) | 7.13 | ✓ |
| QUITE | 0.71 | ✓ |

The original query unions two branches that compute the same `COUNT` over `EMP` and differ only in a constant from `VALUES`. QUITE is the only method that improves this query at all: it runs in 0.71s versus 2.54s for the original. Every equivalent baseline is slower than the original (3.12s--7.18s), and all three R-Bot variants return non-equivalent rewrites, which our validation protocol would reject.

### 2.2 Why the Rewrite Is Fast

QUITE recognizes that both UNION branches share one aggregation: `COUNT(*) FROM EMP WHERE DEPTNO = 0`. The rewrite computes that count once in a CTE and cross joins it with `(VALUES (1), (2))`, replacing two scans, two aggregations, and a union with a single scan. This is common-subexpression elimination across set operations, a transformation that requires recognizing semantic identity between branches rather than matching a syntactic pattern.
