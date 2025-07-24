# Rewrite MySQL Query without NESTED SELECT?
[Link to question](https://stackoverflow.com/questions/13427637/rewrite-mysql-query-without-nested-select)
**Creation Date:** 1353125935
**Score:** 0
**Tags:** mysql, sql
## Question Body
<p>I have a MySQL query that is currently using a nested select, and I am wondering if it is possible to rewrite the query to not use a nested select, and if so how?</p>

<p>The query is as follows</p>

<pre><code>SELECT
  b.id,
  b.name,
  b.description,
  b.order,
  b.icon,
  b.locked,
  u.username     AS lastPoster,
  p.time         AS lastPostTime,
  p1.subject     AS lastPostTopicSubject,
  p2.postscount  AS totalPosts,
  t1.topicscount AS totalTopics,
  p.subject      AS lastPostSubject,
  t.id           AS lastPostTopicId
FROM      kf_boards                                AS b
LEFT JOIN kf_topics                                AS t  ON (t.boardid = b.id)
LEFT JOIN (SELECT posterid, topicid, time, subject
           FROM kf_posts
           ORDER BY time DESC)                     AS p  ON (p.topicid = t.id)
LEFT JOIN (SELECT subject
           FROM kf_posts
           ORDER BY time ASC)                      AS p1 ON (p.topicid = t.id)
LEFT JOIN (SELECT COUNT(id) AS postscount
           FROM kf_posts)                          AS p2 ON (p.topicid = t.id)
LEFT JOIN (SELECT COUNT(id) AS topicscount
           FROM kf_topics)                         AS t1 ON (t.boardid = b.id)
LEFT JOIN kf_users                                 AS u  ON (p.posterid = u.id)
WHERE b.categoryid = :catid
GROUP BY b.name
ORDER BY b.order
</code></pre>

<p>And the database structure is as follows</p>

<p><img src="https://i.sstatic.net/75tpp.png" alt="enter image description here"></p>

<p>Any help would be much appriciated!</p>

<p>Thanks!</p>

<p>Edit: Tried below query, results returned</p>

<p><img src="https://i.sstatic.net/IoM8t.png" alt="enter image description here"></p>

<p>Results should be as follows</p>

<p><img src="https://i.sstatic.net/2R1ie.png" alt="enter image description here"></p>

## Answers
### Answer ID: 13435778
<p>It seems possible to remove all the subqueries,
but the query will be more clear if the last post, and the first post on the corresponding
topic is found using subqueries:</p>

<pre><code>SELECT b.id, b.name, b.description, b.sortorder, b.icon, b.locked,
       u.username AS lastPoster,
       p1.time AS lastpostTime,
       p0.subject AS lastPostTopicSubject,
       COUNT(DISTINCT p.id) AS totalPosts,
       COUNT(DISTINCT t.id) AS totalTopics,
       p1.subject AS lastPostSubject,
       p1.topicid AS lastPostTopicId
FROM  kf_boards b
LEFT JOIN kf_topics t ON t.boardid = b.id
LEFT JOIN kf_posts p ON p.topicid = t.id
LEFT JOIN kf_posts p1
ON p1.time = (SELECT MAX(time) FROM kf_posts p
              INNER JOIN kf_topics t
              ON p.topicid = t.id
              WHERE t.boardid = b.id)
LEFT JOIN kf_users u ON u.id = p1.posterid
LEFT JOIN kf_posts p0
ON p0.time = (SELECT MIN(time) FROM kf_posts p0
              WHERE p0.topicid = p1.topicid)
WHERE b.categoryid = :catid
GROUP BY b.id
ORDER BY b.sortorder;
</code></pre>

<p>However, the following query, using self joins to find posts that have no related previous/nest post should give the same answer:</p>

<pre><code>SELECT b.id, b.name, b.description, b.sortorder, b.icon, b.locked,
       u.username AS lastPoster,
       lastpost.time AS lastpostTime,
       firstpost.subject AS lastPostTopicSubject,
       COUNT(DISTINCT p.id) AS totalPosts,
       COUNT(DISTINCT t.id) AS totalTopics,
       lastpost.subject AS lastPostSubject,
       lastpost.topicid AS lastPostTopicId
FROM  kf_boards b
LEFT JOIN kf_topics t ON t.boardid = b.id
LEFT JOIN kf_posts p ON p.topicid = t.id

LEFT JOIN kf_topics lasttopic ON lasttopic.boardid = b.id
LEFT JOIN kf_posts lastpost ON lastpost.topicid = lasttopic.id
LEFT JOIN kf_topics nexttopic ON nexttopic.boardid = b.id
LEFT JOIN kf_posts nextpost              -- order posts
ON nextpost.topicid = nexttopic.id       -- in same board
AND nextpost.time &gt; lastpost.time        -- by time

LEFT JOIN kf_users u ON u.id = lastpost.posterid

LEFT JOIN kf_posts AS firstpost ON firstpost.topicid = lastpost.topicid
LEFT JOIN kf_posts prevpost              -- order posts
ON prevpost.topicid = firstpost.topicid  -- on same topic
AND prevpost.time &lt; firstpost.time       -- by time

WHERE nextpost.id IS NULL                -- last post has no next
AND prevpost.id IS NULL                  -- first post on topic has no previous

AND b.categoryid = :catid
GROUP BY b.id
ORDER BY b.sortorder;
</code></pre>

<p>Check the result at <a href="http://sqlfiddle.com/#!2/1c042/1/0" rel="nofollow">http://sqlfiddle.com/#!2/1c042/1/0</a></p>

### Answer ID: 13436156
<p>Here's a solution that might help, however, I have additional suggestions to simplify all querying later via triggers.  I'll explain that later.</p>

<p>I'm starting with the inner-most query on just board IDs for category (your parameter) and that the board HAS POSTINGS (not via LEFT-JOIN).  From this, I am getting just the maximum post ID per board regardless of topic (just that it must be of a valid board per the joins).</p>

<p>Once I have that, the next query out re-joins to the posts table based on the last post to determine the topic... then re-joins THAT to the posts again on the same topic ID.  With that, I can get the FIRST Post ID and total Entries for this topic for the board... all grouped per "board ID".  </p>

<p>These are obviously only boards that HAVE AT LEAST 1 Board, but that's not what you want.  You want ALL boards regardless of a post.  So, I'm back to the beginning to query kf_boards again with same WHERE on category ID = your parameter...  THIS gets you all the boards for the category...</p>

<p>NOW, you can left-join to the pre-aggregate query for min/max post and entries count... Then take THAT to left-join to the posts table again but TWICE... Once for the FIRST post (so you can get the initial subject caption, time and whatever else you might care about), and AGAIN for the LAST POST to get ITs time, subject, etc... You already have the total post entries for this topic from the pre-aggregate query.  Finally, a left-join on the last post to the users table to see who posted it last.</p>

<p>I've tested the syntax on it and it works, just can't confirm based on actual data.</p>

<pre><code>SELECT 
      B.ID,
      B.Name,
      B.Description,
      B.Order,
      B.Icon,
      FP.Subject as FirstPostSubject,
      FP.Time as FirstPostTime,
      LP.Subject as LastPostSubject,
      LP.Time as LastPostTime,
      U.UserName as LastPostUserName,
      QryPerBoard.PostEntries
   from 
      kf_boards B
         LEFT JOIN
              ( select 
                      PQ1.ID,
                      PQ1.LastPostID,
                      MIN( P2.ID ) as FirstPostID,
                      COUNT(*) as PostEntries
                   from 
                      ( SELECT
                              B1.ID,
                              MAX( P1.ID ) as LastPostID
                           from
                              kf_boards B1
                                 join kf_topics T1
                                    ON B1.ID = T1.BoardID
                                    join kf_posts P1
                                       ON T1.ID = P1.TopicID
                           where
                              B1.CategoryID = 1    &lt;-- Insert your Category Parameter ID here
                           group by
                              B1.ID ) as PQ1
                      LEFT JOIN kf_posts P1
                         ON PQ1.LastPostID = P1.ID
                         LEFT JOIN kf_posts P2
                            ON P1.TopicID = P2.TopicID
                   group by
                      PQ1.ID ) QryPerBoard
            ON B.ID = QryPerBoard.ID
            LEFT JOIN kf_posts FP
               ON QryPerBoard.FirstPostID = FP.ID
            LEFT JOIN kf_posts LP
               ON QryPerBoard.LastPostID = LP.ID
               LEFT JOIN kf_users U
                  ON LP.PosterID = U.ID
   where
      B.CategoryID = 1    &lt;-- Insert your Category Parameter ID here (second copy for parameter)
</code></pre>

<p>Now, how I would adjust to prevent the recursive level of querying, especially for a website.  Use triggers.  When a POST is created and saved, have a trigger that does a few things...</p>

<p>REVISED THOUGHT on trigger impact.</p>

<p>Update the kf_Boards with the latest TOPIC ID any post was created for the respective board ID so you never have to look for it later, just take whatever is the last and run with it.  In addition, update the TOPIC record.  Have a column for the FIRST POST, LAST POST and TOTAL POSTS for the topic.  If its the first post to the topic, update both first AND last post with the new ID and increment the total post count.</p>

<p>The time to incorporate these triggers to update the "extra" columns would save such complexities for future queries.  You'll basically be able to do something like</p>

<pre><code>select
      B.*,
      LP.Fields,  &lt;obviously apply specific fields you want per table&gt;
      FP.Fields,
      U.Fields
   from
      kf_boards B
         LEFT JOIN kf_topics T
            on B.LastTopicID = T.ID
            LEFT JOIN kf_posts FP
               on T.FirstPostID = FP.ID
            LEFT JOIN kf_posts LP
               on T.LastPostID = LP.ID
               LEFT JOIN kf_users U
                  on LP.PosterID = U.ID
   where
      B.CategoryID = 1  &lt;-- your parameterID  
</code></pre>

### Answer ID: 13427698
<p>try:</p>

<pre><code>SELECT 
   b.id, b.name, b.description, b.order, b.icon, b.locked, 
   u.username AS lastPoster, p.time AS lastPostTime, 
   p.subject AS lastPostSubject, t.id AS lastPostTopicId
FROM kf_boards AS b
LEFT JOIN kf_topics AS t ON t.boardid = b.id
LEFT JOIN kf_posts AS p ON p.topicid = t.id
LEFT JOIN kf_users AS u ON p.posterid = u.id
WHERE b.categoryid = :catid
GROUP BY b.name 
ORDER BY b.order ASC, p.time DESC
</code></pre>

<h2>UPDATE: bellow is for your new query.</h2>

<pre><code>SELECT b.id, b.name, b.description, b.order, b.icon, b.locked, 
    u.username AS lastPoster, MAX(p.time) AS lastPostTime, 
    p.subject AS lastPostTopicSubject, count(p.id) AS totalPosts, 
    count(t.id) AS totalTopics, p.subject AS lastPostSubject, 
    max(t.id) AS lastPostTopicId
FROM kf_boards AS b 
LEFT JOIN kf_topics AS t ON t.boardid = b.id
LEFT JOIN kf_posts AS p ON p.topicid = t.id
LEFT JOIN kf_users AS u ON p.posterid = u.id
WHERE b.categoryid = :catid
GROUP BY b.name, b.id, b.name, b.description, b.order, b.icon, 
    b.locked, u.username, p.subject
ORDER BY b.order
</code></pre>

