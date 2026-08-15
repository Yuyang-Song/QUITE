# Concrete Rewrite Examples Beyond the Evaluated Fixed Inventories

This document gives two concrete examples of QUITE producing useful rewrites that the evaluated fixed rule inventories did not produce. The claim is empirical. Each individual transformation could be encoded as a rule after the fact. These examples do not establish a theoretical limit on rule-language expressiveness.

## 1. Calcite: Composing Algebraic and Aggregation Simplifications

The complete query, every baseline output, and the released measurements are available in [Calcite Example 2](examples/Calcite/Calcite_example_2.md).

The original query joins two derived tables using both `DEPTNO - 10 = SAL + 1` and equality on `DEPTNO`:

```sql
SELECT t4.NAME
FROM (
    SELECT NAME, DEPTNO, DEPTNO - 10 AS DEPTNOMINUS
    FROM DEPT
) AS t4
INNER JOIN (
    SELECT DEPTNO, SAL + 1 AS f9
    FROM EMP
    GROUP BY DEPTNO, SAL + 1
) AS t6
    ON t4.DEPTNOMINUS = t6.f9
   AND t4.DEPTNO = t6.DEPTNO;
```

QUITE produces:

```sql
SELECT d.NAME
FROM DEPT d
INNER JOIN (
    SELECT DISTINCT DEPTNO
    FROM EMP
    WHERE SAL = DEPTNO - 11
) e ON d.DEPTNO = e.DEPTNO;
```

This rewrite composes three transformations. It propagates the arithmetic join condition into `SAL = DEPTNO - 11`, replaces the grouped derived table with the required distinct key, and removes unused projections. Runtime falls from 34.91s to 0.74s. The released SQL shrinks from 219 to 133 characters.

All three R-Bot configurations instead produce a 369-character rewrite that takes 35.76s to 36.20s and fails the execution-consistency check. The result shows a query-specific composition that the evaluated R-Bot inventory did not produce. It does not imply that no rule system could express the same transformation.

## 2. SQLStorm: Removing Output-Irrelevant Work Across CTEs

The complete SQL, all measurements, and the step-by-step explanation are available in [SQLStorm Example 4](examples/SQLStorm/SQLStorm_example_4.md).

The original four-CTE query computes `ScoreRank`, `CommentCount`, `PostCount`, and `BadgeCount`, although none contributes to the final result. QUITE traces the output-relevant values across the CTEs and removes the associated joins, aggregations, and window functions. It also replaces a count used only for a nullness check with distinct identifiers and removes the final duplicate-cleanup aggregation.

| Measure | Original | QUITE | R-Bot |
|---|---:|---:|---:|
| SQL characters in the released result | 1,919 | 1,055 | approximately 1,919 |
| CTEs | 4 | 3 | 4 |
| Joins | 5 | 2 | 5 |
| `GROUP BY` clauses | 3 | 0 | 3 |
| Window functions | 2 | 0 | 2 |
| Execution time (s) | 300 timeout | 2.07 | 300 timeout |

LearnedRewrite, every LLM-R2 configuration, and every R-Bot configuration return the original query unchanged. QUITE produces an execution-consistent rewrite and reduces runtime by 144.9 times. The smaller number of operators and intermediate dependencies also makes the rewritten SQL easier to inspect and maintain. These structural counts are descriptive and are not presented as a formal maintainability metric.

## What the Examples Support

Together, the examples support three limited claims:

1. QUITE can compose query-specific transformations without adding a bespoke rule for each query.
2. Its successful rewrites can be substantially shorter and structurally simpler than R-Bot outputs.
3. On these cases, the broader empirical coverage produces large execution-time improvements.

They do not support the universal claim that these transformations are inexpressible in every possible rule language.
