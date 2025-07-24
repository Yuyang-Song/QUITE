# How can I use GROUP_CONCAT with MATCH, but still display all items in GROUP_CONCAT?
[Link to question](https://stackoverflow.com/questions/14759925/how-can-i-use-group-concat-with-match-but-still-display-all-items-in-group-conc)
**Creation Date:** 1360267177
**Score:** 3
**Tags:** mysql
## Question Body
<p>I'm currently working on a MySQL query that pulls information from three tables in my database: <code>category</code> <code>category_industry</code> and <code>industry</code>. They are related based on ID, as such:</p>

<pre><code>category            category_industry        industry
------------------  ------------------       ------------------
ID | Title          c_id | i_id              ID | Title
 1 | Fab Floor         1 |    1               1 | Beef
                       1 |    2               2 | Pork
</code></pre>

<p>The <code>category_industry</code> table lists which industries a category belongs to by ID of the category, and the industry. What I'm doing is getting the ID of each industry, and pulling the title of that industry from the <code>industry</code> table. I use a <code>GROUP_CONCAT</code> statement to put the titles together. Without doing a search in the query, this is how the result should, and does look:</p>

<pre><code>Fabrication Floor
(Beef, Pork)
</code></pre>

<p>However, if I do a search, and one of the titles is matched in the search, it will only display that title, rather than all of them. Here's my query as it stands if I'm searching for "Beef":</p>

<pre><code>SELECT *,
    GROUP_CONCAT(i.industry_title ORDER BY i.industry_title ASC SEPARATOR ', ') AS industries,
    MATCH (c.category_title, c.category_details) AGAINST ('Beef*' IN BOOLEAN MODE) AS cscore,
    MATCH (i.industry_title) AGAINST ('Beef*' IN BOOLEAN MODE) AS iscore,
    c.category_id AS cat_id
FROM category c
LEFT JOIN category_industry t  ON t.category_id = c.category_id
LEFT JOIN industry i ON i.industry_id = t.industry_id
WHERE
    MATCH (c.category_title, c.category_details) AGAINST ('Beef*' IN BOOLEAN MODE)
    OR MATCH (i.industry_title) AGAINST ('Beef*' IN BOOLEAN MODE)
    GROUP BY c.category_id
    ORDER BY (cscore + iscore) DESC, c.added_date ASC
</code></pre>

<p>This query provides the following result:</p>

<pre><code>Fabrication Floor
(Beef)
</code></pre>

<p>It will show all categories that are in the <code>Beef</code> industry, but removes all other industries from the list. I'd like it to still show the other industries.</p>

<p>Does anyone know a solution to my problem? I've tried rewriting my statements many different ways, but cannot seem to get the list to stay complete. Thank you in advance.</p>

