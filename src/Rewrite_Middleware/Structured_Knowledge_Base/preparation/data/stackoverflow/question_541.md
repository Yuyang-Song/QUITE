# MySQL query performance?
[Link to question](https://stackoverflow.com/questions/30789319/mysql-query-performance)
**Creation Date:** 1434049427
**Score:** 0
**Tags:** mysql, sql
## Question Body
<p>I have MySQL database and 5 tables called <code>tribes(groups)</code>, <code>posts</code>, <code>posts_to_groups</code>, <code>post_comments</code> and <code>posts_votes</code>.</p>

<p>Relationship between groups and posts is MANY_2_MANY so each post can belong to many groups and each group can contain 0-* posts. This is what table posts_to_groups does.</p>

<p>I'm searching for the 3 most popular posts that were posted into the groups that this user follows(associated via posts_to_tribes - table for MANY_2_MANY relationship) for the last 24 hours from this moment and ordered by sum of (comments_count + votes_count) DESC</p>

<p>This is my current query:</p>

<pre><code>SELECT DISTINCT
    p.post_id,
    p.description,
    p.link,
    p.user_id,
    p.total_comments,
    p.total_votes,
    (SELECT 
            COUNT(*)
        FROM
            comments
        WHERE
            last_edited &gt; DATE_SUB(NOW(), INTERVAL 24 HOUR)
                AND post_id = p.post_id) AS comments_count,
    (SELECT 
            COUNT(*)
        FROM
            posts_votes
        WHERE
            date_voted &gt; DATE_SUB(NOW(), INTERVAL 24 HOUR)
                AND post_id = p.post_id) AS votes_count
FROM
    posts p
        JOIN
    posts_to_tribes pt ON pt.post_id = p.post_id
WHERE
    pt.tribe_id IN (3 , 38, 107)
ORDER BY (comments_count + votes_count) DESC , p.last_edited DESC
LIMIT 3;
</code></pre>

<p>This query is extremely slow and took right now <strong>~500ms</strong>.</p>

<p>Is any way to rewrite this query in order to improve performance ?</p>

<p><strong>UPDATED:</strong></p>

<p>EXPLAIN output:</p>

<p><img src="https://i.sstatic.net/XfxFK.png" alt="enter image description here"></p>

<p>Query suggested by <strong>Tim3880</strong>:</p>

<pre><code>SELECT 
    p.post_id,
    p.description,
    p.link,
    p.user_id,
    p.total_comments,
    p.total_votes,
    t.comments_count,
    t.votes_count
FROM posts p
JOIN (
    SELECT 
        p.post_id,
        (SELECT 
                COUNT(*)
            FROM
                comments
            WHERE
                last_edited &gt; DATE_SUB(NOW(), INTERVAL 24 HOUR)
                    AND post_id = p.post_id) AS comments_count,
        (SELECT 
                COUNT(*)
            FROM
                posts_votes
            WHERE
                date_voted &gt; DATE_SUB(NOW(), INTERVAL 24 HOUR)
                    AND post_id = p.post_id) AS votes_count
    FROM
        posts p
            JOIN
        posts_to_tribes pt ON pt.post_id = p.post_id
    WHERE
        pt.tribe_id IN (3 , 38, 107)
    ORDER BY (comments_count + votes_count) DESC , p.last_edited DESC
    LIMIT 3
) t
ON p.post_id = t.post_id
ORDER BY (t.comments_count + t.votes_count) DESC , p.last_edited DESC
</code></pre>

<p>It took now <strong>~280ms</strong>.</p>

<p>EXPLAIN output:</p>

<p><img src="https://i.sstatic.net/2FHw9.png" alt="enter image description here"></p>

## Answers
### Answer ID: 30808314
<p>If you post_id is a primary key (or unique), try get the 3 post_id first:</p>

<pre><code>SELECT 
    p.post_id,
    p.description,
    p.link,
    p.user_id,
    p.total_comments,
    p.total_votes,
    t.comments_count,
    t.votes_count
FROM posts p 
JOIN (
    SELECT 
        p.post_id,
        (SELECT 
                COUNT(*)
            FROM
                comments
            WHERE
                last_edited &gt; DATE_SUB(NOW(), INTERVAL 24 HOUR)
                    AND post_id = p.post_id) AS comments_count,
        (SELECT 
                COUNT(*)
            FROM
                posts_votes
            WHERE
                date_voted &gt; DATE_SUB(NOW(), INTERVAL 24 HOUR)
                    AND post_id = p.post_id) AS votes_count
    FROM
        posts p
            JOIN
        posts_to_tribes pt ON pt.post_id = p.post_id
    WHERE
        pt.tribe_id IN (3 , 38, 107)
        AND p.last_edited &gt;  DATE_SUB(NOW(), INTERVAL 24 HOUR)
    ORDER BY (comments_count + votes_count) DESC , p.last_edited DESC
    LIMIT 3
) t
ON p.post_id = t.post_id
ORDER BY (t.comments_count + t.votes_count) DESC , p.last_edited DESC
</code></pre>

<p>Edit:  This is the join version:</p>

<pre><code>SELECT 
    p.post_id,
    p.description,
    p.link,
    p.user_id,
    p.total_comments,
    p.total_votes,
    t.comments_count,
    t.votes_count
FROM posts p 
JOIN (
    SELECT 
        p.post_id,Comments_Count, Votes_Count
    FROM
        posts p
        JOIN
        posts_to_tribes pt ON pt.post_id = p.post_id
        LEFT JOIN (SELECT 
                post_id, COUNT(*) Comments_Count
            FROM
                comments
            WHERE
                last_edited &gt; DATE_SUB(NOW(), INTERVAL 24 HOUR)
            GROUP BY post_id) cc
        ON p.post_id = cc.post_id
        LEFT JOIN 
        ( 
            SELECT 
                post_id, COUNT(*) Votes_Count
            FROM
                posts_votes
            WHERE
                date_voted &gt; DATE_SUB(NOW(), INTERVAL 24 HOUR)
            GROUP BY post_id
        ) vc
        ON p.post_id = vc.post_id
        WHERE pt.tribe_id IN (3 , 38, 107)
    ORDER BY (comments_count + votes_count) DESC , p.last_edited DESC
    LIMIT 3
) t
ON p.post_id = t.post_id
ORDER BY (t.comments_count + t.votes_count) DESC , p.last_edited DESC
</code></pre>

<p>If the performance is still not acceptable, you may have to think about updating the total_comments, total_votes directly or using trigger or scheduled job. </p>

### Answer ID: 30790273
<p>You have used 2 <a href="https://dev.mysql.com/doc/refman/5.5/en/correlated-subqueries.html" rel="nofollow noreferrer">correlated subqueries</a>. Each one from the correlated subqueries will be executed once for every row from the outer query. Hence, if you can avoid them it's likely to get faster query.</p>

<blockquote>
  <p>[..] they are inefficient and likely to be slow. Rewriting the query as a join might improve performance.</p>
</blockquote>

<p>You have to avoid them by using join. This may help you: <a href="https://stackoverflow.com/questions/26278054/mysql-can-i-avoid-these-correlated-dependant-subqueries">MySQL - can I avoid these correlated / dependant subqueries?</a></p>

