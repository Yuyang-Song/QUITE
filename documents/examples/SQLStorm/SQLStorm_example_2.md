## Q2: Original Query

> **Execution Time:** 137.23s

> All execution times on this page are taken verbatim from the released per-query results in `experiments_results/sqlstorm/`. Because the per-method result files do not share a common id ordering, records are matched by the literal constants of the original query.

```sql
SELECT 
    u.DisplayName AS UserDisplayName,
    p.Title AS PostTitle,
    p.CreationDate AS PostCreationDate,
    ph.CreationDate AS HistoryCreationDate,
    p.Score AS PostScore,
    ph.Comment AS EditComment,
    p.ViewCount,
    p.AnswerCount,
    (SELECT COUNT(*) FROM Votes v WHERE v.PostId = p.Id AND v.VoteTypeId = 2) AS UpVoteCount,
    (SELECT COUNT(*) FROM Votes v WHERE v.PostId = p.Id AND v.VoteTypeId = 3) AS DownVoteCount
FROM 
    Posts p
JOIN 
    Users u ON p.OwnerUserId = u.Id
JOIN 
    PostHistory ph ON p.Id = ph.PostId
WHERE 
    ph.PostHistoryTypeId IN (4, 5, 6) 
ORDER BY 
    ph.CreationDate DESC
FETCH FIRST 100 ROWS ONLY
```

## 1. Rewrite Results

### 1.1. LearnedRewrite

> **Execution Time:** 14.47s

```sql
SELECT t1109.displayname AS UserDisplayName, t1109.title AS PostTitle, t1109.creationdate AS PostCreationDate, t1109.creationdate1 AS HistoryCreationDate, t1109.score AS PostScore, t1109.comment AS EditComment, t1109.viewcount AS ViewCount, t1109.answercount AS AnswerCount, t1109.EXPR$0 AS UpVoteCount, CASE WHEN t1112.EXPR$0 IS NULL THEN 0 ELSE t1112.EXPR$0 END AS DownVoteCount FROM (SELECT posts100.id, posts100.posttypeid, posts100.acceptedanswerid, posts100.parentid, posts100.creationdate, posts100.score, posts100.viewcount, posts100.body, posts100.owneruserid, posts100.ownerdisplayname, posts100.lasteditoruserid, posts100.lasteditordisplayname, posts100.lasteditdate, posts100.lastactivitydate, posts100.title, posts100.tags, posts100.answercount, posts100.commentcount, posts100.favoritecount, posts100.closeddate, posts100.communityowneddate, posts100.contentlicense, users100.id AS id0, users100.reputation, users100.creationdate AS creationdate0, users100.displayname, users100.lastaccessdate, users100.websiteurl, users100.location, users100.aboutme, users100.views, users100.upvotes, users100.downvotes, users100.profileimageurl, users100.accountid, t1105.id AS id1, t1105.posthistorytypeid, t1105.postid, t1105.revisionguid, t1105.creationdate AS creationdate1, t1105.userid, t1105.userdisplayname, t1105.comment, t1105.text, t1105.contentlicense AS contentlicense0, CASE WHEN t1108.EXPR$0 IS NULL THEN 0 ELSE t1108.EXPR$0 END AS EXPR$0 FROM posts AS posts100 INNER JOIN users AS users100 ON posts100.owneruserid = users100.id INNER JOIN (SELECT * FROM posthistory WHERE posthistorytypeid IN (4, 5, 6)) AS t1105 ON posts100.id = t1105.postid LEFT JOIN (SELECT postid, COUNT(*) AS EXPR$0 FROM votes WHERE votetypeid = 2 GROUP BY postid) AS t1108 ON posts100.id = t1108.postid) AS t1109 LEFT JOIN (SELECT postid, COUNT(*) AS EXPR$0 FROM votes WHERE votetypeid = 3 GROUP BY postid) AS t1112 ON t1109.id = t1112.postid ORDER BY t1109.creationdate1 DESC FETCH NEXT 100 ROWS ONLY
```

### 1.2. LLM-R2 (DS-R1, best of three models)

> **Execution Time:** 17.21s

```sql
SELECT t2.DisplayName AS UserDisplayName, t2.Title AS PostTitle, t2.CreationDate AS PostCreationDate, t2.CreationDate1 AS HistoryCreationDate, t2.Score AS PostScore, t2.Comment AS EditComment, t2.ViewCount, t2.AnswerCount, t2.EXPR0 AS UpVoteCount, CASE WHEN t4.EXPR0 IS NULL THEN 0 ELSE t4.EXPR0 END AS DownVoteCount FROM (SELECT Posts.Id, Posts.PostTypeId, Posts.AcceptedAnswerId, Posts.ParentId, Posts.CreationDate, Posts.Score, Posts.ViewCount, Posts.Body, Posts.OwnerUserId, Posts.OwnerDisplayName, Posts.LastEditorUserId, Posts.LastEditorDisplayName, Posts.LastEditDate, Posts.LastActivityDate, Posts.Title, Posts.Tags, Posts.AnswerCount, Posts.CommentCount, Posts.FavoriteCount, Posts.ClosedDate, Posts.CommunityOwnedDate, Posts.ContentLicense, Users.Id AS Id0, Users.Reputation, Users.CreationDate AS CreationDate0, Users.DisplayName, Users.LastAccessDate, Users.WebsiteUrl, Users.Location, Users.AboutMe, Users.Views, Users.UpVotes, Users.DownVotes, Users.ProfileImageUrl, Users.AccountId, t.Id AS Id1, t.PostHistoryTypeId, t.PostId, t.RevisionGUID, t.CreationDate AS CreationDate1, t.UserId, t.UserDisplayName, t.Comment, t.Text, t.ContentLicense AS ContentLicense0, CASE WHEN t1.EXPR0 IS NULL THEN 0 ELSE t1.EXPR0 END AS EXPR0 FROM Posts INNER JOIN Users ON Posts.OwnerUserId = Users.Id INNER JOIN (SELECT * FROM PostHistory WHERE PostHistoryTypeId IN (4, 5, 6)) AS t ON Posts.Id = t.PostId LEFT JOIN (SELECT PostId, COUNT(*) AS EXPR0 FROM Votes WHERE VoteTypeId = 2 GROUP BY PostId) AS t1 ON Posts.Id = t1.PostId) AS t2 LEFT JOIN (SELECT PostId, COUNT(*) AS EXPR0 FROM Votes WHERE VoteTypeId = 3 GROUP BY PostId) AS t4 ON t2.Id = t4.PostId ORDER BY t2.CreationDate1 DESC LIMIT 100
```

### 1.3. R-Bot (DS-R1, best of three models)

> **Execution Time:** 13.63s

```sql
SELECT "t5"."displayname", "t5"."title", "t5"."creationdate", "t5"."creationdate1", "t5"."score", "t5"."comment", "t5"."viewcount", "t5"."answercount", "t5"."EXPR0", CASE WHEN "t8"."EXPR0" IS NULL THEN 0 ELSE "t8"."EXPR0" END AS "downvotecount" FROM (SELECT "t1"."id", "t1"."posttypeid", "t1"."acceptedanswerid", "t1"."parentid", "t1"."creationdate", "t1"."score", "t1"."viewcount", "t1"."body", "t1"."owneruserid", "t1"."ownerdisplayname", "t1"."lasteditoruserid", "t1"."lasteditordisplayname", "t1"."lasteditdate", "t1"."lastactivitydate", "t1"."title", "t1"."tags", "t1"."answercount", "t1"."commentcount", "t1"."favoritecount", "t1"."closeddate", "t1"."communityowneddate", "t1"."contentlicense", "t1"."id0", "t1"."reputation", "t1"."creationdate0", "t1"."displayname", "t1"."lastaccessdate", "t1"."websiteurl", "t1"."location", "t1"."aboutme", "t1"."views", "t1"."upvotes", "t1"."downvotes", "t1"."profileimageurl", "t1"."accountid", "t1"."id1", "t1"."posthistorytypeid", "t1"."postid", "t1"."revisionguid", "t1"."creationdate1", "t1"."userid", "t1"."userdisplayname", "t1"."comment", "t1"."text", "t1"."contentlicense0", CASE WHEN "t4"."EXPR0" IS NULL THEN 0 ELSE "t4"."EXPR0" END AS "EXPR0"         FROM (SELECT *                 FROM (SELECT *                         FROM "posts",                             "users" AS "users" ("id0", "reputation", "creationdate0", "displayname", "lastaccessdate", "websiteurl", "location", "aboutme", "views", "upvotes", "downvotes", "profileimageurl", "accountid")                         WHERE "posts"."owneruserid" = "users"."id0") AS "t",                         (SELECT *                         FROM "posthistory" AS "posthistory" ("id1", "posthistorytypeid", "postid", "revisionguid", "creationdate1", "userid", "userdisplayname", "comment", "text", "contentlicense0")                         WHERE CAST("posthistorytypeid" AS INTEGER) IN (4, 5, 6)) AS "t0"                 WHERE "t"."id" = "t0"."postid") AS "t1"             LEFT JOIN (SELECT "postid0", COUNT(*) AS "EXPR0"                 FROM "votes" AS "votes" ("id2", "postid0", "votetypeid", "userid0", "creationdate2", "bountyamount")                 WHERE CAST("votetypeid" AS INTEGER) = 2                 GROUP BY "postid0") AS "t4" ON "t1"."id" = "t4"."postid0") AS "t5"     LEFT JOIN (SELECT "postid1", COUNT(*) AS "EXPR0"         FROM "votes" AS "votes0" ("id3", "postid1", "votetypeid0", "userid1", "creationdate3", "bountyamount0")         WHERE CAST("votetypeid0" AS INTEGER) = 3         GROUP BY "postid1") AS "t8" ON "t5"."id" = "t8"."postid1" ORDER BY "t5"."creationdate1" DESC FETCH NEXT 100 ROWS ONLY;
```

### 1.4. LLM Agent (DS-R1, best baseline overall)

> **Execution Time:** 6.98s

```sql
WITH main_data AS (
    SELECT 
        u.DisplayName AS UserDisplayName,
        p.Title AS PostTitle,
        p.CreationDate AS PostCreationDate,
        ph.CreationDate AS HistoryCreationDate,
        p.Score AS PostScore,
        ph.Comment AS EditComment,
        p.ViewCount,
        p.AnswerCount,
        p.Id AS PostId
    FROM 
        Posts p
    JOIN 
        Users u ON p.OwnerUserId = u.Id
    JOIN 
        PostHistory ph ON p.Id = ph.PostId
    WHERE 
        ph.PostHistoryTypeId IN (4, 5, 6)
    ORDER BY 
        ph.CreationDate DESC
    FETCH FIRST 100 ROWS ONLY
),
vote_counts AS (
    SELECT 
        v.PostId,
        COUNT(CASE WHEN v.VoteTypeId = 2 THEN 1 END) AS UpVoteCount,
        COUNT(CASE WHEN v.VoteTypeId = 3 THEN 1 END) AS DownVoteCount
    FROM Votes v
    WHERE v.PostId IN (SELECT PostId FROM main_data)
      AND v.VoteTypeId IN (2, 3)
    GROUP BY v.PostId
)
SELECT 
    m.UserDisplayName,
    m.PostTitle,
    m.PostCreationDate,
    m.HistoryCreationDate,
    m.PostScore,
    m.EditComment,
    m.ViewCount,
    m.AnswerCount,
    COALESCE(v.UpVoteCount, 0) AS UpVoteCount,
    COALESCE(v.DownVoteCount, 0) AS DownVoteCount
FROM main_data m
LEFT JOIN vote_counts v ON m.PostId = v.PostId
ORDER BY m.HistoryCreationDate DESC;
```

### 1.5. QUITE

> **Execution Time:** 2.46s

```sql
WITH TopPostHistory AS (
    SELECT ph.PostId, ph.CreationDate, ph.Comment
    FROM PostHistory ph
    WHERE ph.PostHistoryTypeId IN (4,5,6)
    ORDER BY ph.CreationDate DESC
    FETCH FIRST 100 ROWS ONLY
),
VoteCounts AS (
    SELECT 
        v.PostId,
        SUM(CASE WHEN v.VoteTypeId = 2 THEN 1 ELSE 0 END) AS UpVoteCount,
        SUM(CASE WHEN v.VoteTypeId = 3 THEN 1 ELSE 0 END) AS DownVoteCount
    FROM Votes v
    WHERE v.PostId IN (SELECT PostId FROM TopPostHistory)
    GROUP BY v.PostId
)
SELECT 
    u.DisplayName AS UserDisplayName,
    p.Title AS PostTitle,
    p.CreationDate AS PostCreationDate,
    tph.CreationDate AS HistoryCreationDate,
    p.Score AS PostScore,
    tph.Comment AS EditComment,
    p.ViewCount,
    p.AnswerCount,
    COALESCE(vc.UpVoteCount, 0) AS UpVoteCount,
    COALESCE(vc.DownVoteCount, 0) AS DownVoteCount
FROM TopPostHistory tph
JOIN Posts p ON tph.PostId = p.Id
JOIN Users u ON p.OwnerUserId = u.Id
LEFT JOIN VoteCounts vc ON p.Id = vc.PostId
ORDER BY tph.CreationDate DESC
```


## 2. Deep Analysis

### 2.1 Query Context and Full Metrics

| Method | Execution Time (s) | Equivalent |
|---|---|---|
| LearnedRewrite | 14.47 | ✓ |
| LLM-R² (Claude-3.7) | 130.61 | ✓ |
| LLM-R² (DS-R1) | 17.21 | ✓ |
| LLM-R² (GPT-4o) | 130.68 | ✓ |
| R-Bot (Claude-3.7) | 13.64 | ✓ |
| R-Bot (DS-R1) | 13.63 | ✓ |
| R-Bot (GPT-4o) | 16.25 | ✓ |
| LLM Agent (Claude-3.7) | 16.10 | ✗ (non-equivalent) |
| LLM Agent (DS-R1) | 6.98 | ✓ |
| LLM Agent (DS-V3) | 25.93 | ✗ (non-equivalent) |
| LLM Agent (GPT-4o) | 24.00 | ✗ (non-equivalent) |
| QUITE | 2.46 | ✓ |

QUITE runs in 2.46s, a 55.8x speedup over the original and 2.8x ahead of the best baseline (LLM Agent DS-R1, 6.98s). Three of the four agent variants are non-equivalent; the rule- and template-based methods are correct but stay between 13.6s and 130.7s.

### 2.2 Why the Rewrite Is Fast

1. **Limit pushdown.** The original orders the full edit history and applies the limit at the end. QUITE's `TopPostHistory` CTE selects the 100 most recent history rows first, so every later operator works on 100 rows instead of the whole table.
2. **Decorrelation by conditional aggregation.** The original computes per-row scalar subqueries (`SELECT COUNT(*) FROM Votes WHERE ...`) for up-votes and down-votes separately. QUITE replaces them with one `VoteCounts` CTE that scans `Votes` once and splits the counts with `SUM(CASE WHEN VoteTypeId = ...)`.
