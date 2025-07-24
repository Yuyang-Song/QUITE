# MySQL Nested Selected with Multiple Columns
[Link to question](https://stackoverflow.com/questions/15579549/mysql-nested-selected-with-multiple-columns)
**Creation Date:** 1363985148
**Score:** 1
**Tags:** mysql, subquery
## Question Body
<p>I am currently trying to retrieve the latest posts along with their related posts (x number for each post). I have the following query in hand:</p>

<pre><code>SELECT id, title, content
       (SELECT GROUP_CONCAT(title) FROM posts        -- Select title of related posts 
        WHERE id &lt;&gt; p.id AND id IN (                 
           SELECT p_id FROM tagsmap                  -- Select reletad post ids from tagsmap
           WHERE t_id IN (
              SELECT t_id FROM tagsmap               -- Select the tags of the current post 
              WHERE p_id = p.id) 
           ) ORDER BY id DESC LIMIT 0, 3) as related 
FROM posts as p ORDER BY id DESC LIMIT 5
</code></pre>

<p>My database structure is simple: A posts table. A tags table. And a tagsmap table where I associate posts with tags.</p>

<p>This query works fine (though I don't know its performance since I don't have many rows in the tables -- Maybe an explain could help me but that's not the case right now).</p>

<p><strong>What I really need is to retrieve the ids of the related posts along with their titles.</strong></p>

<p>So I'd like to do <code>SELECT GROUP_CONCAT(title), GROUP_CONCAT(id)</code>, but I know that will result in an error. So what is the best way to retrieve the id along with the title in this case? I do not want to rewrite the whole subquery to just retrieve the id. There should be another way. </p>

<p><strong>EDIT</strong></p>

<pre><code>SELECT p1.id, p1.title, p1.content,
    group_concat(DISTINCT p2.id) as 'P IDs',
    group_concat(DISTINCT p2.title) as 'P titles'
FROM posts as p1
LEFT JOIN tagsmap as tm1 on tm1.p_id = p1.id
LEFT JOIN tagsmap as tm2 on tm2.t_id = tm1.t_id and tm1.p_id &lt;&gt; tm2.p_id
LEFT JOIN posts as p2 on p2.id = tm2.p_id
GROUP BY p1.id
ORDER BY p1.id desc limit 5;
</code></pre>

<p>At the end this is the query that I've used. I removed the Where clause because it is unnecessary and used <code>LEFT JOIN</code> rather that <code>JOIN</code> because otherwise it would ignore the posts without tags. And finally added <code>DISTINCT</code> to group_concat because it was concatenating duplicate rows (If for example a post had multiple common tags with a related post it would result in a duplicate concatenation).</p>

<p>The query above works perfectly. Thanks for all.</p>

## Answers
### Answer ID: 15580187
<p>Okay - this will work, and it has the added advantage of eliminating the sub queries (which can slow you down when you get lots of records):</p>

<pre><code>SELECT p1.id, p1.title, p1.content,
    group_concat( p2.id) as 'P IDs',
    group_concat( p2.title) as 'P titles'
FROM posts as p1
JOIN tagsmap as tm1 on tm1.p_id = p1.id
JOIN tagsmap as tm2 on tm2.t_id = tm1.t_id and tm1.p_id &lt;&gt; tm2.p_id
JOIN posts as p2 on p2.id = tm2.p_id
WHERE p2.id &lt;&gt; p1.id
GROUP BY p1.id
ORDER BY p1.id desc limit 5;
</code></pre>

<p>What we're doing here is selecting what you want from the first version of posts, joining them to the tagsmap by their post.id, doing a self join to tagsmap by tag id to get all the related tags, and then joining back to another posts (p2) to get the posts that are pointed to by those related tags.</p>

<p>Use GROUP BY to discard the dups from all that joining, and you're there.</p>

### Answer ID: 15579868
<p>like this?</p>

<pre><code>SELECT id, title, content
       (SELECT GROUP_CONCAT(concat(cast(id as varchar(10)), ':', title)) FROM posts        -- Select title of related posts 
        WHERE id &lt;&gt; p.id AND id IN (                 
           SELECT p_id FROM tagsmap                  -- Select reletad post ids from tagsmap
           WHERE t_id IN (
              SELECT t_id FROM tagsmap               -- Select the tags of the current post 
              WHERE post_id = p.id) 
           ) ORDER BY id DESC LIMIT 0, 3) as related 
FROM posts as p ORDER BY id DESC LIMIT 5
</code></pre>

