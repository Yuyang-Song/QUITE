# SQLStorm Example 4: Removing Output-Irrelevant Work Across CTEs

## Original Query

> **Execution Time:** 300s timeout

> All execution times and execution-consistency labels on this page are taken from the released records in `experiments_results/sqlstorm/`. The original query is record `id = 38` in `QUITE_sqlstorm_43queries.json`.

```sql
WITH RankedPosts AS (
    SELECT
        p.Id AS PostID,
        p.Title,
        p.Score,
        p.ViewCount,
        p.OwnerUserId,
        p.Tags,
        ROW_NUMBER() OVER (
            PARTITION BY p.PostTypeId
            ORDER BY p.Score DESC
        ) AS ScoreRank,
        COUNT(c.Id) OVER (PARTITION BY p.Id) AS CommentCount,
        (
            CASE
                WHEN COALESCE(p.AnswerCount, 0) < 0 THEN 0
                ELSE COALESCE(p.AnswerCount, 0)
            END
        )
        + (
            CASE
                WHEN COALESCE(p.FavoriteCount, 0) < 0 THEN 0
                ELSE COALESCE(p.FavoriteCount, 0)
            END
        ) AS EngagementScore
    FROM Posts p
    LEFT JOIN Comments c ON p.Id = c.PostId
    WHERE p.CreationDate >= DATE '2023-01-01'
),
ClosedPosts AS (
    SELECT
        ph.PostId,
        COUNT(ph.Id) AS CloseHistoryCount
    FROM PostHistory ph
    WHERE ph.PostHistoryTypeId = 10
    GROUP BY ph.PostId
),
ActiveUsers AS (
    SELECT
        u.Id AS UserID,
        MAX(u.Reputation) AS Reputation,
        COUNT(DISTINCT p.Id) AS PostCount,
        COUNT(DISTINCT b.Id) AS BadgeCount
    FROM Users u
    LEFT JOIN Posts p ON u.Id = p.OwnerUserId
    LEFT JOIN Badges b ON u.Id = b.UserId
    WHERE u.LastAccessDate >= CAST('2024-10-01' AS DATE) - INTERVAL '90' DAY
    GROUP BY u.Id
),
EngagedPosts AS (
    SELECT
        rp.PostID,
        rp.Title,
        rp.Score,
        rp.ViewCount,
        rp.Tags,
        CASE
            WHEN cp.CloseHistoryCount IS NULL THEN 'Active'
            ELSE 'Closed'
        END AS PostStatus,
        au.UserID,
        au.Reputation AS UserReputation,
        rp.EngagementScore
    FROM RankedPosts rp
    LEFT JOIN ClosedPosts cp ON rp.PostID = cp.PostId
    LEFT JOIN ActiveUsers au ON rp.OwnerUserId = au.UserID
)
SELECT
    ep.PostID,
    MIN(ep.Title) AS Title,
    MIN(ep.Score) AS Score,
    MIN(ep.ViewCount) AS ViewCount,
    MIN(ep.PostStatus) AS PostStatus,
    MIN(ep.UserReputation) AS UserReputation,
    MIN(ep.EngagementScore) AS EngagementScore,
    REPLACE(
        SUBSTRING(MIN(ep.Tags) FROM 2 FOR CHAR_LENGTH(MIN(ep.Tags)) - 2),
        '><',
        ', '
    ) AS Tags
FROM EngagedPosts ep
WHERE ep.EngagementScore > 10
GROUP BY ep.PostID
ORDER BY
    MIN(ep.EngagementScore) DESC,
    MIN(ep.ViewCount) DESC
LIMIT 50;
```

## Rewrite Results

LearnedRewrite and every evaluated LLM-R2 and R-Bot configuration return the original query unchanged. Each therefore reaches the same 300s timeout.

QUITE produces the following execution-consistent rewrite:

> **Execution Time:** 2.07s

```sql
WITH RankedPosts AS (
    SELECT
        p.Id AS PostID,
        p.Title,
        p.Score,
        p.ViewCount,
        p.OwnerUserId,
        p.Tags,
        GREATEST(COALESCE(p.AnswerCount, 0), 0)
        + GREATEST(COALESCE(p.FavoriteCount, 0), 0) AS EngagementScore
    FROM Posts p
    WHERE p.CreationDate >= DATE '2023-01-01'
),
ClosedPosts AS (
    SELECT DISTINCT ph.PostId
    FROM PostHistory ph
    WHERE ph.PostHistoryTypeId = 10
),
ActiveUsers AS (
    SELECT u.Id AS UserID, u.Reputation
    FROM Users u
    WHERE u.LastAccessDate >= CAST('2024-10-01' AS DATE) - INTERVAL '90' DAY
)
SELECT
    rp.PostID,
    rp.Title,
    rp.Score,
    rp.ViewCount,
    CASE
        WHEN cp.PostId IS NULL THEN 'Active'
        ELSE 'Closed'
    END AS PostStatus,
    au.Reputation AS UserReputation,
    rp.EngagementScore,
    REPLACE(
        SUBSTRING(rp.Tags FROM 2 FOR CHAR_LENGTH(rp.Tags) - 2),
        '><',
        ', '
    ) AS Tags
FROM RankedPosts rp
LEFT JOIN ClosedPosts cp ON rp.PostID = cp.PostId
LEFT JOIN ActiveUsers au ON rp.OwnerUserId = au.UserID
WHERE rp.EngagementScore > 10
ORDER BY
    rp.EngagementScore DESC,
    rp.ViewCount DESC
LIMIT 50;
```

## Full Metrics

Execution consistency means that the original and rewritten queries return the same result on the benchmark database. It is not a claim of formal semantic equivalence on every possible database state.

| Method | Result | Execution Time (s) | Execution Consistent |
|---|---|---:|:---:|
| LearnedRewrite | Unchanged | 300 timeout | Yes |
| LLM-R2, all three models | Unchanged | 300 timeout | Yes |
| R-Bot, all three models | Unchanged | 300 timeout | Yes |
| LLM Agent, Claude-3.7 | Rewritten | 3.33 | Yes |
| LLM Agent, DeepSeek-R1 | Rewritten | 1.86 | Yes |
| LLM Agent, DeepSeek-V3 | Rewritten | 300 timeout | No |
| LLM Agent, GPT-4o | Rewritten | 300 timeout | Yes |
| QUITE | Rewritten | 2.07 | Yes |

The direct DeepSeek-R1 agent is slightly faster on this individual query. The relevant comparison here is with the evaluated fixed-rule inventories. LearnedRewrite, LLM-R2, and R-Bot make no change, whereas QUITE reduces execution time by 144.9 times.

## Structural Simplicity

| Measure | Original | QUITE | R-Bot |
|---|---:|---:|---:|
| SQL characters in the released result | 1,919 | 1,055 | approximately 1,919 |
| CTEs | 4 | 3 | 4 |
| Joins | 5 | 2 | 5 |
| `GROUP BY` clauses | 3 | 0 | 3 |
| Window functions | 2 | 0 | 2 |
| Execution time (s) | 300 timeout | 2.07 | 300 timeout |

These counts are descriptive rather than a formal maintainability metric. They show that QUITE removes redundant operators and intermediate dependencies, making the result substantially easier to inspect and maintain than the unchanged R-Bot output.

## Why the Rewrite Works

1. **Trace only output-relevant values.** `ScoreRank` and `CommentCount` are never consumed. QUITE removes both window functions and the `Comments` join that exists only to compute `CommentCount`.
2. **Remove unused aggregates.** `PostCount` and `BadgeCount` are never consumed. QUITE removes their joins and aggregation, retaining only the user identifier and reputation.
3. **Replace a count with existence information.** Downstream logic checks only whether a matching close-history group exists. `SELECT DISTINCT PostId` preserves that information without computing `CloseHistoryCount`.
4. **Remove duplicate cleanup.** After the redundant joins are removed, the outer `MIN` aggregates and `GROUP BY` no longer serve a purpose.

Each individual transformation could be encoded as a rule after the fact. This example does not claim a theoretical limit on rule languages. It shows that the evaluated fixed inventories did not discover and compose the query-specific transformations, while QUITE produced a shorter execution-consistent query without adding a bespoke rule.
