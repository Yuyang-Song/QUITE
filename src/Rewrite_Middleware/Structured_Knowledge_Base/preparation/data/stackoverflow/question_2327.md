# Alternate to ORDER BY subquery
[Link to question](https://stackoverflow.com/questions/29486667/alternate-to-order-by-subquery)
**Creation Date:** 1428393693
**Score:** 2
**Tags:** mysql, subquery, sql-order-by
## Question Body
<p>From the database at <a href="http://www.w3schools.com/sql/trysql.asp?filename=trysql_select_orderby2" rel="nofollow">http://www.w3schools.com/sql/trysql.asp?filename=trysql_select_orderby2</a>, for example (Click "Run SQL"), I want to list the customer who has the largest CustomerID that is greater than 80 first among a list of all customers from USA.  So I use</p>

<pre><code>SELECT * FROM Customers
WHERE Country = 'USA'
ORDER BY CustomerID = (SELECT MAX(CustomerID) FROM Customers 
    WHERE CustomerID &gt; 80 AND Country = 'USA') DESC, PostalCode;
</code></pre>

<p>but this is not the real query I'm using.  If the SELECT... FROM... WHERE... portion of the query is more complex, what is a more elegant query?</p>

<p>The actual query I am trying to modify is</p>

<pre><code>SELECT post.postid, post.visible, post.userid, post.parentid, post.vote_count
FROM " . TABLE_PREFIX . "post AS post
WHERE post.threadid = $threadid
AND post.visible IN (1" . (!empty($deljoin) ? ", 2" : "") . 
    ($show['approvepost'] ? ", 0" : "") . ")
ORDER BY post.postid = {$threadinfo['firstpostid']} DESC, post.vote_count &gt; 5 DESC, 
    post.dateline $postorder
</code></pre>

<p>where the <code>post.vote_count &gt; 5 DESC</code> portion I am trying to replace with only the largest post.vote_count that is larger than 5.  So I use:</p>

<pre><code>SELECT post.postid, post.visible, post.userid, post.parentid, post.vote_count
FROM " . TABLE_PREFIX . "post AS post
WHERE post.threadid = $threadid
AND post.visible IN (1" . (!empty($deljoin) ? ", 2" : "") . 
    ($show['approvepost'] ? ", 0" : "") . ")
ORDER BY post.postid = {$threadinfo['firstpostid']} DESC, post.vote_count = (
    SELECT MAX(post.vote_count)
    FROM " . TABLE_PREFIX . "post AS post
    WHERE post.threadid = $threadid
    AND post.visible IN (1" . (!empty($deljoin) ? ", 2" : "") . 
        ($show['approvepost'] ? ", 0" : "") . ")
    AND post.vote_count &gt; 5
)
DESC, post.dateline $postorder
</code></pre>

<p>and all is good.  But you can imagine a more complex query, perhaps with INNER JOIN, whose SELECT... FROM... WHERE... etc. must all be duplicated in the subquery.</p>

<p>So my question is, I suspect, can you order query results so the first item (<em>within those results</em>) has the maximum of a field, and the remainder ordered otherwise, without essentially rewriting the entire query in a subquery?</p>

## Answers
### Answer ID: 29510826
<p>MySQL does not support CTE's, which would have been the perfect solution to simplify your query. They can be emulated with a view though :</p>

<pre><code>CREATE VIEW c AS (SELECT Customer.* FROM Customer WHERE Country = "USA");
SELECT c.* FROM c ORDER BY CustomerID = (SELECT MAX(CustomerID) FROM c) DESC;
DROP VIEW c;
</code></pre>

<p>In your case, this would give :</p>

<pre><code>CREATE VIEW p AS (
    SELECT post.postid, post.visible, post.userid, post.parentid, post.vote_count
    FROM " . TABLE_PREFIX . "post AS post
    WHERE post.threadid = $threadid
    AND post.visible IN (1" . (!empty($deljoin) ? ", 2" : "") . 
        ($show['approvepost'] ? ", 0" : "") . ")
);
SELECT p.* FROM p
ORDER BY p.postid = {$threadinfo['firstpostid']} DESC, p.vote_count = (
    SELECT MAX(p.vote_count)
    FROM p
    WHERE p.vote_count &gt; 5
)
DESC, post.dateline $postorder;
DROP VIEW p;
</code></pre>

### Answer ID: 29488529
<p>This query will list  data in descending order of CustomerID  </p>

<pre><code> SELECT * FROM Customers
    WHERE Country = 'USA'
    ORDER BY CustomerID  DESC, PostalCode;
</code></pre>

