## Q1: Original Query

> **Execution Time:** >300s (timeout)

> All execution times on this page are taken verbatim from the released per-query results in `experiments_results/sqlstorm/`. Because the per-method result files do not share a common id ordering, records are matched by the literal constants of the original query.

```sql
SELECT     p.Id AS PostId,    p.Title,    p.CreationDate AS PostCreationDate,    p.ViewCount,    p.Score,    p.AnswerCount,    u.DisplayName AS OwnerDisplayName,    COUNT(DISTINCT v.Id) AS VoteCount,    COUNT(DISTINCT c.Id) AS CommentCount,    MAX(b.Date) AS LastBadgeDate,    COUNT(DISTINCT b.Id) AS BadgeCount FROM     Posts p JOIN     Users u ON p.OwnerUserId = u.Id LEFT JOIN     Votes v ON p.Id = v.PostId LEFT JOIN     Comments c ON p.Id = c.PostId LEFT JOIN     Badges b ON u.Id = b.UserId WHERE     p.CreationDate >= '2023-01-01'  GROUP BY     p.Id, p.Title, p.CreationDate, p.ViewCount, p.Score, p.AnswerCount, u.DisplayName ORDER BY     p.CreationDate DESC;
```

## 1. Rewrite Results

### 1.1. LearnedRewrite

> **Execution Time:** >300s

```sql
SELECT t.id AS PostId, t.title AS Title, t.creationdate AS PostCreationDate, t.viewcount AS ViewCount, t.score AS Score, t.answercount AS AnswerCount, users.displayname AS OwnerDisplayName, COUNT(DISTINCT votes.id) AS VoteCount, COUNT(DISTINCT comments.id) AS CommentCount, MAX(badges.date) AS LastBadgeDate, COUNT(DISTINCT badges.id) AS BadgeCount FROM (SELECT * FROM posts WHERE creationdate >= TIMESTAMP '2023-01-01 00:00:00') AS t INNER JOIN users ON t.owneruserid = users.id LEFT JOIN votes ON t.id = votes.postid LEFT JOIN comments ON t.id = comments.postid LEFT JOIN badges ON users.id = badges.userid GROUP BY t.id, t.title, t.creationdate, t.viewcount, t.score, t.answercount, users.displayname ORDER BY t.creationdate DESC
```

### 1.2. LLM-R2 (GPT-4o)

> **Execution Time:** >300s

```sql
SELECT     p.Id AS PostId,    p.Title,    p.CreationDate AS PostCreationDate,    p.ViewCount,    p.Score,    p.AnswerCount,    u.DisplayName AS OwnerDisplayName,    COUNT(DISTINCT v.Id) AS VoteCount,    COUNT(DISTINCT c.Id) AS CommentCount,    MAX(b.Date) AS LastBadgeDate,    COUNT(DISTINCT b.Id) AS BadgeCount FROM     Posts p JOIN     Users u ON p.OwnerUserId = u.Id LEFT JOIN     Votes v ON p.Id = v.PostId LEFT JOIN     Comments c ON p.Id = c.PostId LEFT JOIN     Badges b ON u.Id = b.UserId WHERE     p.CreationDate >= '2023-01-01'  GROUP BY     p.Id, p.Title, p.CreationDate, p.ViewCount, p.Score, p.AnswerCount, u.DisplayName ORDER BY     p.CreationDate DESC;
```

### 1.3. R-Bot (Claude-3.7)

> **Execution Time:** >300s

```sql
SELECT     p.Id AS PostId,    p.Title,    p.CreationDate AS PostCreationDate,    p.ViewCount,    p.Score,    p.AnswerCount,    u.DisplayName AS OwnerDisplayName,    COUNT(DISTINCT v.Id) AS VoteCount,    COUNT(DISTINCT c.Id) AS CommentCount,    MAX(b.Date) AS LastBadgeDate,    COUNT(DISTINCT b.Id) AS BadgeCount FROM     Posts p JOIN     Users u ON p.OwnerUserId = u.Id LEFT JOIN     Votes v ON p.Id = v.PostId LEFT JOIN     Comments c ON p.Id = c.PostId LEFT JOIN     Badges b ON u.Id = b.UserId WHERE     p.CreationDate >= '2023-01-01'  GROUP BY     p.Id, p.Title, p.CreationDate, p.ViewCount, p.Score, p.AnswerCount, u.DisplayName ORDER BY     p.CreationDate DESC;
```

### 1.4. LLM Agent (Claude-3.7)

> **Execution Time:** 10.34s  *(non-equivalent: rejected by our validation protocol)*  -- fast, but returns a different result set

```sql
SELECT p.Id AS PostId, p.Title, p.CreationDate AS PostCreationDate, p.ViewCount, p.Score, p.AnswerCount, u.DisplayName AS OwnerDisplayName, v.VoteCount, c.CommentCount, b.LastBadgeDate, b.BadgeCount FROM Posts p JOIN Users u ON p.OwnerUserId = u.Id LEFT JOIN (SELECT PostId, COUNT(*) AS VoteCount FROM Votes GROUP BY PostId) v ON p.Id = v.PostId LEFT JOIN (SELECT PostId, COUNT(*) AS CommentCount FROM Comments GROUP BY PostId) c ON p.Id = c.PostId LEFT JOIN (SELECT UserId, MAX(Date) AS LastBadgeDate, COUNT(*) AS BadgeCount FROM Badges GROUP BY UserId) b ON u.Id = b.UserId WHERE p.CreationDate >= '2023-01-01' ORDER BY p.CreationDate DESC;
```

### 1.5. QUITE (rewrite only)

> **Execution Time:** 14.66s

```sql
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

### 1.6. QUITE (with hint injection)

> **Execution Time:** 11.71s

```sql
/*+ Rows(p v #255709) */
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

## 2. Deep Analysis

### 2.1 Query Context and Full Metrics

| Method | Execution Time (s) | Equivalent |
|---|---|---|
| LearnedRewrite | >300 | ✓ |
| LLM-R² (Claude-3.7) | >300 | ✓ |
| LLM-R² (DS-R1) | >300 | ✓ |
| LLM-R² (GPT-4o) | >300 | ✓ |
| R-Bot (Claude-3.7) | >300 | ✓ |
| R-Bot (DS-R1) | >300 | ✓ |
| R-Bot (GPT-4o) | >300 | ✓ |
| LLM Agent (Claude-3.7) | 10.34 | ✗ (non-equivalent) |
| LLM Agent (DS-R1) | 16.63 | ✗ (non-equivalent) |
| LLM Agent (DS-V3) | >300 | ✗ (non-equivalent) |
| LLM Agent (GPT-4o) | >300 | ✓ |
| QUITE | 14.66 | ✓ |
| QUITE + hints | 11.71 | ✓ |

This LLM-generated query is the hardest case in the workload: no baseline produces a usable result. Every rule- and template-based rewrite (LearnedRewrite, all LLM-R2 and R-Bot variants) stays at the 300s timeout. The two agent rewrites that do finish quickly (Claude-3.7 at 10.34s, DS-R1 at 16.63s) are both non-equivalent, so a system that trusted them would silently return wrong answers. QUITE is the only method that returns the correct result, at 11.71s with hints (at least 25x over the original).

### 2.2 Why the Rewrite Works

The original joins `Posts` with `Votes`, `Comments`, and `Badges` and computes several `COUNT(DISTINCT ...)` aggregates over the joined result, with the date filter applied late. The multi-way join multiplies rows before any aggregation, which is what the baselines fail to undo. QUITE first restricts `Posts` by the date predicate (`FilteredPosts`), then computes each aggregate in its own pre-aggregated CTE (`VoteCounts`, `CommentCounts`, ...) and joins the small per-post results back. The join fan-out disappears, and the hints further steer the join order (14.66s to 11.71s).
