# Standard SQL to replace GREATEST() in MySQL query
[Link to question](https://stackoverflow.com/questions/7929061/standard-sql-to-replace-greatest-in-mysql-query)
**Creation Date:** 1319803897
**Score:** 4
**Tags:** mysql, sql, hive
## Question Body
<p>I have a MySQL query that uses the <code>GREATEST()</code> function, and I want to rewrite it in standard ANSI SQL to run on others databases. I know GREATEST is supported by most SQL databases, but I'm probably going to run the query in Hive, which supports things like CASE but not GREATEST.</p>

<p>Can anyone think of an elegant way to rewrite this query without using <code>GREATEST()</code>?</p>

<p>Thanks!</p>

<pre><code>select 
greatest(play,play_25,play_50,play_75,play_100) as play,
greatest(play_25,play_50,play_75,play_100) as play_25,
greatest(play_50,play_75,play_100) as play_50,
greatest(play_75,play_100) as play_75,
play_100 as play_100 
from video_buckets
</code></pre>

## Answers
### Answer ID: 7929713
<p>This should work, although I am not sure if you could call it 'elegant':</p>

<pre><code>SELECT
  CASE WHEN play_25 &gt; play THEN play_25 ELSE play END AS play,
  play_25,
  play_50,
  play_75,
  play_100
FROM (
  SELECT
    play,
    CASE WHEN play_50 &gt; play_25 THEN play_50 ELSE play_25 END AS play_25,
    play_50,
    play_75,
    play_100
  FROM (
    SELECT
      play,
      play_25,
      CASE WHEN play_75 &gt; play_50 THEN play_75 ELSE play_50 END AS play_50,
      play_75,
      play_100
    FROM (
      SELECT
        play,
        play_25,
        play_50,
        CASE WHEN play_100 &gt; play_75 THEN play_100 ELSE play_75 END AS play_75,
        play_100
      FROM video_buckets
    ) s
  ) s
) s
</code></pre>

### Answer ID: 7929340
<p>This won't work in MySQL but <a href="http://developer.mimer.com/validator/parser92/index.tml#parser" rel="nofollow">validates as Full SQL-92</a></p>

<pre><code>SELECT (SELECT MAX(c)
        FROM   (VALUES(play),
                      (play_25),
                      (play_50),
                      (play_75),
                      (play_100)) T (c))  AS play,
       (SELECT MAX(c)
        FROM   (VALUES (play_25),
                       (play_50),
                       (play_75),
                       (play_100)) T (c)) AS play_25
FROM   video_buckets  
</code></pre>

