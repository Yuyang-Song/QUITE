## Q3: Original Query

> **Execution Time:** >300s (timeout)

> All execution times on this page are taken verbatim from the released per-query results in `experiments_results/sqlstorm/`. Because the per-method result files do not share a common id ordering, records are matched by the literal constants of the original query.

```sql
WITH UserReputation AS (
    SELECT 
        U.Id AS UserId,
        U.DisplayName,
        U.Reputation,
        U.CreationDate,
        U.LastAccessDate,
        U.Views,
        ROW_NUMBER() OVER (PARTITION BY U.Id ORDER BY U.CreationDate DESC) AS RecentView,
        LAG(U.Reputation, 1, 0) OVER (PARTITION BY U.Id ORDER BY U.CreationDate DESC) AS PreviousReputation
    FROM 
        Users U
    WHERE 
        U.Reputation > 100
), 
ActivePosts AS (
    SELECT 
        P.Id AS PostId,
        P.OwnerUserId,
        P.PostTypeId,
        P.Title,
        P.CreationDate,
        COALESCE(P.AcceptedAnswerId, -1) AS AcceptedAnswerId,
        (SELECT COUNT(*) FROM Comments C WHERE C.PostId = P.Id) AS CommentCount,
        (SELECT COUNT(*) FROM Votes V WHERE V.PostId = P.Id AND V.VoteTypeId = 2) AS UpVotes,
        (SELECT COUNT(*) FROM Votes V WHERE V.PostId = P.Id AND V.VoteTypeId = 3) AS DownVotes
    FROM 
        Posts P
    WHERE 
        P.CreationDate > TIMESTAMP '2024-10-01 12:34:56' - INTERVAL '30' DAY
), 
PostHistoryDetails AS (
    SELECT 
        H.PostId,
        H.UserId,
        PH.Name AS HistoryType,
        COUNT(*) AS RevisionCount,
        MAX(H.CreationDate) AS LastRevisionDate
    FROM 
        PostHistory H
    JOIN 
        PostHistoryTypes PH ON H.PostHistoryTypeId = PH.Id
    GROUP BY 
        H.PostId, H.UserId, PH.Name
)
SELECT 
    U.UserId,
    U.DisplayName,
    U.Reputation,
    U.LastAccessDate,
    S.PostId,
    S.Title as PostTitle,
    S.CommentCount,
    S.UpVotes,
    S.DownVotes,
    COALESCE(PH.HistoryType, 'No Modifications') AS LastHistoryType,
    PH.RevisionCount,
    PH.LastRevisionDate,
    CASE 
        WHEN (U.Reputation - U.PreviousReputation) > 0 THEN 'Increased'
        WHEN (U.Reputation - U.PreviousReputation) < 0 THEN 'Decreased'
        ELSE 'No Change'
    END as ReputationChange
FROM 
    UserReputation U
LEFT JOIN 
    ActivePosts S ON U.UserId = S.OwnerUserId
LEFT JOIN 
    PostHistoryDetails PH ON S.PostId = PH.PostId
WHERE 
    (PH.RevisionCount > 5 OR S.CommentCount > 0)
ORDER BY 
    U.Reputation DESC, S.CreationDate DESC
FETCH FIRST 100 ROWS ONLY;
```

## 1. Rewrite Results

### 1.1. LearnedRewrite

> **Execution Time:** 16.65s  *(non-equivalent: rejected by our validation protocol)*

```sql
SELECT t20.UserId, t20.DisplayName, t20.Reputation, t20.LastAccessDate, t32.PostId, t32.Title AS PostTitle, t32.CommentCount, t32.UpVotes, t32.DownVotes, CASE WHEN t34.HistoryType IS NOT NULL THEN CAST(t34.HistoryType AS CHAR(16)) ELSE 'No Modifications' END AS LastHistoryType, t34.RevisionCount, t34.LastRevisionDate, CASE WHEN t20.Reputation - t20.PreviousReputation > 0 THEN 'Increased' WHEN t20.Reputation - t20.PreviousReputation < 0 THEN 'Decreased' ELSE 'No Change' END AS ReputationChange FROM (SELECT id AS UserId, displayname AS DisplayName, reputation AS Reputation, creationdate AS CreationDate, lastaccessdate AS LastAccessDate, views AS Views, ROW_NUMBER() OVER (PARTITION BY id ORDER BY creationdate DESC) AS RecentView, LAG(reputation, 1, 0) OVER (PARTITION BY id ORDER BY creationdate DESC) AS PreviousReputation FROM users WHERE reputation > 100) AS t20 LEFT JOIN (SELECT t28.id AS PostId, t28.owneruserid AS OwnerUserId, t28.posttypeid AS PostTypeId, t28.title AS Title, t28.creationdate AS CreationDate, t28.acceptedanswerid AS AcceptedAnswerId, t28.EXPR$0 AS CommentCount, t28.EXPR$023 AS UpVotes, CASE WHEN t31.EXPR$0 IS NULL THEN 0 ELSE t31.EXPR$0 END AS DownVotes FROM (SELECT t24.id, t24.posttypeid, t24.acceptedanswerid, t24.parentid, t24.creationdate, t24.score, t24.viewcount, t24.body, t24.owneruserid, t24.ownerdisplayname, t24.lasteditoruserid, t24.lasteditordisplayname, t24.lasteditdate, t24.lastactivitydate, t24.title, t24.tags, t24.answercount, t24.commentcount, t24.favoritecount, t24.closeddate, t24.communityowneddate, t24.contentlicense, t24.EXPR$0, CASE WHEN t27.EXPR$0 IS NULL THEN 0 ELSE t27.EXPR$0 END AS EXPR$023 FROM (SELECT t21.id, t21.posttypeid, t21.acceptedanswerid, t21.parentid, t21.creationdate, t21.score, t21.viewcount, t21.body, t21.owneruserid, t21.ownerdisplayname, t21.lasteditoruserid, t21.lasteditordisplayname, t21.lasteditdate, t21.lastactivitydate, t21.title, t21.tags, t21.answercount, t21.commentcount, t21.favoritecount, t21.closeddate, t21.communityowneddate, t21.contentlicense, CASE WHEN t23.EXPR$0 IS NULL THEN 0 ELSE t23.EXPR$0 END AS EXPR$0 FROM (SELECT * FROM posts WHERE creationdate > (TIMESTAMP '2024-10-01 12:34:56' - INTERVAL '30' DAY)) AS t21 LEFT JOIN (SELECT postid, COUNT(*) AS EXPR$0 FROM comments GROUP BY postid) AS t23 ON t21.id = t23.postid) AS t24 LEFT JOIN (SELECT postid, COUNT(*) AS EXPR$0 FROM votes WHERE votetypeid = 2 GROUP BY postid) AS t27 ON t24.id = t27.postid) AS t28 LEFT JOIN (SELECT postid, COUNT(*) AS EXPR$0 FROM votes WHERE votetypeid = 3 GROUP BY postid) AS t31 ON t28.id = t31.postid) AS t32 ON t20.UserId = t32.OwnerUserId LEFT JOIN (SELECT posthistory0.postid AS PostId, posthistory0.userid AS UserId, posthistorytypes0.name AS HistoryType, COUNT(*) AS RevisionCount, MAX(posthistory0.creationdate) AS LastRevisionDate FROM posthistory AS posthistory0 INNER JOIN posthistorytypes AS posthistorytypes0 ON posthistory0.posthistorytypeid = posthistorytypes0.id GROUP BY posthistory0.postid, posthistory0.userid, posthistorytypes0.name) AS t34 ON t32.PostId = t34.PostId WHERE t34.RevisionCount > 5 OR t32.CommentCount > 0 ORDER BY t20.Reputation DESC, t32.CreationDate DESC FETCH NEXT 100 ROWS ONLY
```

### 1.2. LLM-R2 (GPT-4o)

> **Execution Time:** 19.06s  *(non-equivalent: rejected by our validation protocol)*

```sql
SELECT t0.UserId, t0.DisplayName, t0.Reputation, t0.LastAccessDate, t12.PostId, t12.Title AS PostTitle, t12.CommentCount, t12.UpVotes, t12.DownVotes, CASE WHEN t14.HistoryType IS NOT NULL THEN CAST(t14.HistoryType AS CHAR(16)) ELSE 'No Modifications' END AS LastHistoryType, t14.RevisionCount, t14.LastRevisionDate, CASE WHEN t0.Reputation - t0.PreviousReputation > 0 THEN 'Increased' WHEN t0.Reputation - t0.PreviousReputation < 0 THEN 'Decreased' ELSE 'No Change' END AS ReputationChange FROM (SELECT Id AS UserId, DisplayName, Reputation, CreationDate, LastAccessDate, Views, ROW_NUMBER() OVER (PARTITION BY Id ORDER BY CreationDate DESC) AS RecentView, LAG(Reputation, 1, 0) OVER (PARTITION BY Id ORDER BY CreationDate DESC) AS PreviousReputation FROM Users WHERE Reputation > 100) AS t0 LEFT JOIN (SELECT t8.Id AS PostId, t8.OwnerUserId, t8.PostTypeId, t8.Title, t8.CreationDate, t8.AcceptedAnswerId, t8.EXPR0 AS CommentCount, t8.EXPR023 AS UpVotes, CASE WHEN t11.EXPR0 IS NULL THEN 0 ELSE t11.EXPR0 END AS DownVotes FROM (SELECT t4.Id, t4.PostTypeId, t4.AcceptedAnswerId, t4.ParentId, t4.CreationDate, t4.Score, t4.ViewCount, t4.Body, t4.OwnerUserId, t4.OwnerDisplayName, t4.LastEditorUserId, t4.LastEditorDisplayName, t4.LastEditDate, t4.LastActivityDate, t4.Title, t4.Tags, t4.AnswerCount, t4.CommentCount, t4.FavoriteCount, t4.ClosedDate, t4.CommunityOwnedDate, t4.ContentLicense, t4.EXPR0, CASE WHEN t7.EXPR0 IS NULL THEN 0 ELSE t7.EXPR0 END AS EXPR023 FROM (SELECT t1.Id, t1.PostTypeId, t1.AcceptedAnswerId, t1.ParentId, t1.CreationDate, t1.Score, t1.ViewCount, t1.Body, t1.OwnerUserId, t1.OwnerDisplayName, t1.LastEditorUserId, t1.LastEditorDisplayName, t1.LastEditDate, t1.LastActivityDate, t1.Title, t1.Tags, t1.AnswerCount, t1.CommentCount, t1.FavoriteCount, t1.ClosedDate, t1.CommunityOwnedDate, t1.ContentLicense, CASE WHEN t3.EXPR0 IS NULL THEN 0 ELSE t3.EXPR0 END AS EXPR0 FROM (SELECT * FROM Posts WHERE CreationDate > (TIMESTAMP '2024-10-01 12:34:56' - INTERVAL '30' DAY)) AS t1 LEFT JOIN (SELECT PostId, COUNT(*) AS EXPR0 FROM Comments GROUP BY PostId) AS t3 ON t1.Id = t3.PostId) AS t4 LEFT JOIN (SELECT PostId, COUNT(*) AS EXPR0 FROM Votes WHERE VoteTypeId = 2 GROUP BY PostId) AS t7 ON t4.Id = t7.PostId) AS t8 LEFT JOIN (SELECT PostId, COUNT(*) AS EXPR0 FROM Votes WHERE VoteTypeId = 3 GROUP BY PostId) AS t11 ON t8.Id = t11.PostId) AS t12 ON t0.UserId = t12.OwnerUserId LEFT JOIN (SELECT PostHistory.PostId, PostHistory.UserId, PostHistoryTypes.Name AS HistoryType, COUNT(*) AS RevisionCount, MAX(PostHistory.CreationDate) AS LastRevisionDate FROM PostHistory INNER JOIN PostHistoryTypes ON PostHistory.PostHistoryTypeId = PostHistoryTypes.Id GROUP BY PostHistory.PostId, PostHistory.UserId, PostHistoryTypes.Name) AS t14 ON t12.PostId = t14.PostId WHERE t14.RevisionCount > 5 OR t12.CommentCount > 0 ORDER BY t0.Reputation DESC, t12.CreationDate DESC LIMIT 100
```

### 1.3. R-Bot (Claude-3.7, fastest of three models)

> **Execution Time:** 14.67s  *(non-equivalent: rejected by our validation protocol)*

```sql
SELECT "t2"."userid", "t2"."displayname", "t2"."reputation", "t2"."lastaccessdate", "t14"."id0", "t14"."title", "t14"."EXPR0", "t14"."EXPR023", "t14"."downvotes0", CASE WHEN "t16"."name" IS NOT NULL THEN CAST("t16"."name" AS VARCHAR(16)) ELSE 'No Modifications' END AS "lasthistorytype", "t16"."revisioncount", "t16"."lastrevisiondate", CASE WHEN "t2"."reputation" - "t2"."previousreputation" > 0 THEN 'Increased' WHEN "t2"."reputation" - "t2"."previousreputation" < 0 THEN 'Decreased' ELSE 'No Change' END AS "reputationchange" FROM (SELECT "id" AS "userid", "displayname", "reputation", "creationdate", "lastaccessdate", "views", ROW_NUMBER() OVER (PARTITION BY "id" ORDER BY "creationdate" DESC) AS "recentview", LAG("reputation", 1, 0) OVER (PARTITION BY "id" ORDER BY "creationdate" DESC) AS "previousreputation"         FROM "users"         WHERE "reputation" > 100) AS "t2"     LEFT JOIN (SELECT "t10"."id0", "t10"."owneruserid", "t10"."posttypeid", "t10"."title", "t10"."creationdate0", CASE WHEN "t10"."acceptedanswerid" IS NOT NULL THEN CAST("t10"."acceptedanswerid" AS INTEGER) ELSE -1 END AS "acceptedanswerid0", "t10"."EXPR0", "t10"."EXPR023", CASE WHEN "t13"."EXPR0" IS NULL THEN 0 ELSE "t13"."EXPR0" END AS "downvotes0"         FROM (SELECT "t6"."id0", "t6"."posttypeid", "t6"."acceptedanswerid", "t6"."parentid", "t6"."creationdate0", "t6"."score", "t6"."viewcount", "t6"."body", "t6"."owneruserid", "t6"."ownerdisplayname", "t6"."lasteditoruserid", "t6"."lasteditordisplayname", "t6"."lasteditdate", "t6"."lastactivitydate", "t6"."title", "t6"."tags", "t6"."answercount", "t6"."commentcount", "t6"."favoritecount", "t6"."closeddate", "t6"."communityowneddate", "t6"."contentlicense", "t6"."EXPR0", CASE WHEN "t9"."EXPR0" IS NULL THEN 0 ELSE "t9"."EXPR0" END AS "EXPR023"                 FROM (SELECT "t3"."id0", "t3"."posttypeid", "t3"."acceptedanswerid", "t3"."parentid", "t3"."creationdate0", "t3"."score", "t3"."viewcount", "t3"."body", "t3"."owneruserid", "t3"."ownerdisplayname", "t3"."lasteditoruserid", "t3"."lasteditordisplayname", "t3"."lasteditdate", "t3"."lastactivitydate", "t3"."title", "t3"."tags", "t3"."answercount", "t3"."commentcount", "t3"."favoritecount", "t3"."closeddate", "t3"."communityowneddate", "t3"."contentlicense", CASE WHEN "t5"."EXPR0" IS NULL THEN 0 ELSE "t5"."EXPR0" END AS "EXPR0"                         FROM (SELECT *                                 FROM "posts" AS "posts" ("id0", "posttypeid", "acceptedanswerid", "parentid", "creationdate0", "score", "viewcount", "body", "owneruserid", "ownerdisplayname", "lasteditoruserid", "lasteditordisplayname", "lasteditdate", "lastactivitydate", "title", "tags", "answercount", "commentcount", "favoritecount", "closeddate", "communityowneddate", "contentlicense")                                 WHERE "creationdate0" > TIMESTAMP '2024-09-01 12:34:56') AS "t3"                             LEFT JOIN (SELECT "postid", COUNT(*) AS "EXPR0"                                 FROM "comments" AS "comments" ("id1", "postid", "score0", "text", "creationdate1", "userdisplayname", "userid", "contentlicense0")                                 GROUP BY "postid") AS "t5" ON "t3"."id0" = "t5"."postid") AS "t6"                     LEFT JOIN (SELECT "postid0", COUNT(*) AS "EXPR0"                         FROM "votes" AS "votes" ("id2", "postid0", "votetypeid", "userid0", "creationdate2", "bountyamount")                         WHERE CAST("votetypeid" AS INTEGER) = 2                         GROUP BY "postid0") AS "t9" ON "t6"."id0" = "t9"."postid0") AS "t10"             LEFT JOIN (SELECT "postid1", COUNT(*) AS "EXPR0"                 FROM "votes" AS "votes0" ("id3", "postid1", "votetypeid0", "userid1", "creationdate3", "bountyamount0")                 WHERE CAST("votetypeid0" AS INTEGER) = 3                 GROUP BY "postid1") AS "t13" ON "t10"."id0" = "t13"."postid1") AS "t14" ON "t2"."userid" = "t14"."owneruserid"     LEFT JOIN (SELECT "posthistory"."postid2", "posthistory"."userid2", "posthistorytypes"."name", COUNT(*) AS "revisioncount", MAX("posthistory"."creationdate4") AS "lastrevisiondate"         FROM "posthistory" AS "posthistory" ("id4", "posthistorytypeid", "postid2", "revisionguid", "creationdate4", "userid2", "userdisplayname0", "comment", "text0", "contentlicense1")             INNER JOIN "posthistorytypes" AS "posthistorytypes" ("id5", "name") ON "posthistory"."posthistorytypeid" = "posthistorytypes"."id5"         GROUP BY "posthistory"."postid2", "posthistory"."userid2", "posthistorytypes"."name") AS "t16" ON "t14"."id0" = "t16"."postid2" WHERE "t16"."revisioncount" > 5 OR "t14"."EXPR0" > 0 ORDER BY "t2"."reputation" DESC, "t14"."creationdate0" DESC FETCH NEXT 100 ROWS ONLY;
```

### 1.4. LLM Agent (DS-R1, the only equivalent baseline that finishes)

> **Execution Time:** 16.84s

```sql
WITH UserReputation AS (
    SELECT 
        U.Id AS UserId,
        U.DisplayName,
        U.Reputation,
        U.CreationDate,
        U.LastAccessDate,
        U.Views,
        1 AS RecentView,  -- Simplified: Single row per user
        0 AS PreviousReputation  -- Simplified: No historical data
    FROM 
        Users U
    WHERE 
        U.Reputation > 100
), 
ActivePosts AS (
    SELECT 
        P.Id AS PostId,
        P.OwnerUserId,
        P.PostTypeId,
        P.Title,
        P.CreationDate,
        COALESCE(P.AcceptedAnswerId, -1) AS AcceptedAnswerId,
        COALESCE(C.CommentCount, 0) AS CommentCount,  -- Pre-aggregated counts
        COALESCE(V_Up.UpVotes, 0) AS UpVotes,        -- Pre-aggregated counts
        COALESCE(V_Down.DownVotes, 0) AS DownVotes    -- Pre-aggregated counts
    FROM 
        Posts P
    LEFT JOIN (
        SELECT PostId, COUNT(*) AS CommentCount
        FROM Comments
        GROUP BY PostId
    ) C ON P.Id = C.PostId
    LEFT JOIN (
        SELECT PostId, COUNT(*) AS UpVotes
        FROM Votes
        WHERE VoteTypeId = 2
        GROUP BY PostId
    ) V_Up ON P.Id = V_Up.PostId
    LEFT JOIN (
        SELECT PostId, COUNT(*) AS DownVotes
        FROM Votes
        WHERE VoteTypeId = 3
        GROUP BY PostId
    ) V_Down ON P.Id = V_Down.PostId
    WHERE 
        P.CreationDate > TIMESTAMP '2024-10-01 12:34:56' - INTERVAL '30' DAY
), 
PostHistoryDetails AS (
    SELECT 
        H.PostId,
        H.UserId,
        PH.Name AS HistoryType,
        COUNT(*) AS RevisionCount,
        MAX(H.CreationDate) AS LastRevisionDate
    FROM 
        PostHistory H
    JOIN 
        PostHistoryTypes PH ON H.PostHistoryTypeId = PH.Id
    GROUP BY 
        H.PostId, H.UserId, PH.Name
)
SELECT 
    U.UserId,
    U.DisplayName,
    U.Reputation,
    U.LastAccessDate,
    S.PostId,
    S.Title AS PostTitle,
    S.CommentCount,
    S.UpVotes,
    S.DownVotes,
    COALESCE(PH.HistoryType, 'No Modifications') AS LastHistoryType,
    PH.RevisionCount,
    PH.LastRevisionDate,
    'Increased' AS ReputationChange  -- Simplified: Always 'Increased' due to >100 reputation
FROM 
    UserReputation U
LEFT JOIN 
    ActivePosts S ON U.UserId = S.OwnerUserId
LEFT JOIN 
    PostHistoryDetails PH ON S.PostId = PH.PostId
WHERE 
    (PH.RevisionCount > 5 OR S.CommentCount > 0)
ORDER BY 
    U.Reputation DESC, S.CreationDate DESC
FETCH FIRST 100 ROWS ONLY;
```

### 1.5. QUITE

> **Execution Time:** 10.76s

```sql
WITH ActivePostIds AS (
    SELECT Id
    FROM Posts
    WHERE CreationDate > TIMESTAMP '2024-10-01 12:34:56' - INTERVAL '30' DAY
),
UserReputation AS (
    SELECT 
        U.Id AS UserId,
        U.DisplayName,
        U.Reputation,
        U.CreationDate,
        U.LastAccessDate,
        U.Views,
        LAG(U.Reputation, 1, 0) OVER (PARTITION BY U.Id ORDER BY U.CreationDate DESC) AS PreviousReputation
    FROM 
        Users U
    WHERE 
        U.Reputation > 100
), 
ActivePosts AS (
    SELECT 
        P.Id AS PostId,
        P.OwnerUserId,
        P.PostTypeId,
        P.Title,
        P.CreationDate,
        COALESCE(P.AcceptedAnswerId, -1) AS AcceptedAnswerId,
        COALESCE(CC.CommentCount, 0) AS CommentCount,
        COALESCE(UV.UpVotes, 0) AS UpVotes,
        COALESCE(DV.DownVotes, 0) AS DownVotes
    FROM 
        Posts P
    JOIN ActivePostIds A ON P.Id = A.Id
    LEFT JOIN (
        SELECT C.PostId, COUNT(*) AS CommentCount
        FROM Comments C
        JOIN ActivePostIds A ON C.PostId = A.Id
        GROUP BY C.PostId
    ) CC ON P.Id = CC.PostId
    LEFT JOIN (
        SELECT V.PostId, COUNT(*) AS UpVotes
        FROM Votes V
        JOIN ActivePostIds A ON V.PostId = A.Id
        WHERE V.VoteTypeId = 2
        GROUP BY V.PostId
    ) UV ON P.Id = UV.PostId
    LEFT JOIN (
        SELECT V.PostId, COUNT(*) AS DownVotes
        FROM Votes V
        JOIN ActivePostIds A ON V.PostId = A.Id
        WHERE V.VoteTypeId = 3
        GROUP BY V.PostId
    ) DV ON P.Id = DV.PostId
), 
PostHistoryDetails AS (
    SELECT 
        H.PostId,
        H.UserId,
        PH.Name AS HistoryType,
        COUNT(*) AS RevisionCount,
        MAX(H.CreationDate) AS LastRevisionDate
    FROM 
        PostHistory H
    JOIN 
        PostHistoryTypes PH ON H.PostHistoryTypeId = PH.Id
    JOIN 
        ActivePostIds A ON H.PostId = A.Id
    GROUP BY 
        H.PostId, H.UserId, PH.Name
)
SELECT 
    U.UserId,
    U.DisplayName,
    U.Reputation,
    U.LastAccessDate,
    S.PostId,
    S.Title as PostTitle,
    S.CommentCount,
    S.UpVotes,
    S.DownVotes,
    COALESCE(PH.HistoryType, 'No Modifications') AS LastHistoryType,
    PH.RevisionCount,
    PH.LastRevisionDate,
    CASE 
        WHEN (U.Reputation - U.PreviousReputation) > 0 THEN 'Increased'
        WHEN (U.Reputation - U.PreviousReputation) < 0 THEN 'Decreased'
        ELSE 'No Change'
    END as ReputationChange
FROM 
    UserReputation U
LEFT JOIN 
    ActivePosts S ON U.UserId = S.OwnerUserId
LEFT JOIN 
    PostHistoryDetails PH ON S.PostId = PH.PostId
WHERE 
    (PH.RevisionCount > 5 OR S.CommentCount > 0)
ORDER BY 
    U.Reputation DESC, S.CreationDate DESC
FETCH FIRST 100 ROWS ONLY;
```


## 2. Deep Analysis

### 2.1 Query Context and Full Metrics

| Method | Execution Time (s) | Equivalent |
|---|---|---|
| LearnedRewrite | 16.65 | ✗ (non-equivalent) |
| LLM-R² (Claude-3.7) | >300 | ✓ |
| LLM-R² (DS-R1) | 21.96 | ✗ (non-equivalent) |
| LLM-R² (GPT-4o) | 19.06 | ✗ (non-equivalent) |
| R-Bot (Claude-3.7) | 14.67 | ✗ (non-equivalent) |
| R-Bot (DS-R1) | 16.29 | ✗ (non-equivalent) |
| R-Bot (GPT-4o) | >300 | ✗ (non-equivalent) |
| LLM Agent (Claude-3.7) | 19.96 | ✗ (non-equivalent) |
| LLM Agent (DS-R1) | 16.84 | ✓ |
| LLM Agent (DS-V3) | >300 | ✗ (non-equivalent) |
| LLM Agent (GPT-4o) | 15.71 | ✗ (non-equivalent) |
| QUITE | 10.76 | ✓ |

This long, machine-generated analytic query (window functions over users, posts, and reputation history) defeats almost every baseline on correctness: nine of the eleven baseline rewrites are non-equivalent, including all three R-Bot variants and LearnedRewrite. Only LLM Agent DS-R1 (16.84s) survives validation among the baselines. QUITE is both correct and the fastest, at 10.76s (at least 27x over the original).

### 2.2 Why This Case Matters

1. **Semantic drift is the norm on machine-generated SQL.** Long queries with stacked window functions give rewriters many chances to change semantics silently. The 9/11 non-equivalence rate here shows why unvalidated rewrites cannot be trusted in production.
2. **The rewrite itself.** QUITE prepends an `ActivePostIds` CTE that restricts posts to the 30-day window used downstream, and removes a `ROW_NUMBER` column that the outer query never consumes. Both transformations preserve semantics and cut the dominant scans.
