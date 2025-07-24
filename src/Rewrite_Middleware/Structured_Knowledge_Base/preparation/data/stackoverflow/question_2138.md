# Explanation of SQL query
[Link to question](https://stackoverflow.com/questions/20379232/explanation-of-sql-query)
**Creation Date:** 1386170664
**Score:** 1
**Tags:** mysql, sql, stored-procedures
## Question Body
<p>I am having some issues with this SQL query. This actually comes from a PROCEDURE that is dealing with spatial calculations. The procedure finds locations within a certain radius. Really I am having a hard time understanding what is going on. I just need to rewrite it for my purposes if someone could help explain a couple of things. I will be forever grateful to whoever attempts to help. Thanks so much in advance!</p>

<p>Link To Source: <a href="http://www.scribd.com/doc/2569355/Geo-Distance-Search-with-MySQL" rel="nofollow">http://www.scribd.com/doc/2569355/Geo-Distance-Search-with-MySQL</a></p>

<p><strong>Full Procedure - I Just Need Some Explanation Help On The Actual SELECT Statement - Is Here Just For Some Clarification So Whoever Is Reading Can Get A Better Understanding</strong></p>

<pre><code>CREATE PROCEDURE geodist (IN userid int, IN dist int)BEGINdeclare mylon double; declare mylat double;declare lon1 float; declare lon2 float;declare lat1 float; declare lat2 float;
-- get the original lon and lat for the userid 
select longitude, latitude into mylon, mylat from users5where id=userid limit 1;
-- calculate lon and lat for the rectangle:
set lon1 = mylon-dist/abs(cos(radians(mylat))*69);set lon2 = mylon+dist/abs(cos(radians(mylat))*69);set lat1 = mylat-(dist/69); set lat2 = mylat+(dist/69);
-- run the query:
SELECT destination.*,3956 * 2 * ASIN(SQRT( POWER(SIN((orig.lat -dest.lat) * pi()/180 / 2), 2) +COS(orig.lat * pi()/180) * COS(dest.lat * pi()/180) *POWER(SIN((orig.lon -dest.lon) * pi()/180 / 2), 2) )) asdistance FROM users destination, users originWHERE origin.id=userid
and destination.longitude between lon1 and lon2 and destination.latitude between lat1 and lat2 
having distance &lt; dist ORDER BY Distance limit 10;END $$
</code></pre>

<p><strong>Full Query The Part I Need a Little Clarification On:</strong></p>

<pre><code>SELECT destination.*,3956 * 2 * ASIN(SQRT( POWER(SIN((orig.lat -dest.lat) * pi()/180 / 2), 2) +COS(orig.lat * pi()/180) * COS(dest.lat * pi()/180) *POWER(SIN((orig.lon -dest.lon) * pi()/180 / 2), 2) )) as distance FROM users destination, users origin WHERE origin.id=userid
and locations.longitude between lon1 and lon2 and locations.latitude between lat1 and lat2 
having distance &lt; dist ORDER BY Distance;
</code></pre>

<p><strong>First Part:</strong></p>

<pre><code>SELECT destination.*
</code></pre>

<blockquote>
  <p>Question: What is with the period and * after the word destination? Sure we are selecting destination but is this concatenating? Like prefixing the word destination to every column in the table?</p>
</blockquote>

<p><strong>Next Part:</strong></p>

<pre><code>3956 * 2 * ASIN(SQRT( POWER(SIN((orig.lat -dest.lat) * pi()/180 / 2), 2) +COS(orig.lat * pi()/180) * COS(dest.lat * pi()/180) *POWER(SIN((orig.lon -dest.lon) * pi()/180 / 2), 2) )) as distance
</code></pre>

<blockquote>
  <p>Question: Is this just performing the calculation and storing it as the keyword destination? The keyword "as" is throwing me off here. Is it searching the database for a column destination?</p>
</blockquote>

<p><strong>Third Part:</strong></p>

<pre><code>FROM users destination, users origin WHERE origin.id=userid
</code></pre>

<blockquote>
  <p>Question: a little confused on where the query is headed. users destination? users origin? What is this grabbing? </p>
</blockquote>

<p><strong>Last Part:</strong></p>

<pre><code>having distance &lt; dist ORDER BY Distance;
</code></pre>

<blockquote>
  <p>Question: Confused about the "having" keyword and where having distance comes into play. Is it trying to grab distance from the table because this is something that is obviously calculated on the fly.</p>
</blockquote>

## Answers
### Answer ID: 22357469
<p>I feel like I'm missing something here... Why doesn't the code use the 'mylon' and 'mylat' in the math part of the final query?</p>

<p>So, this:</p>

<pre><code>SELECT destination.*,
    3956 * 2 * ASIN(SQRT( POWER(SIN((orig.lat -
        destination.lat) * pi()/180 / 2), 2) +
        COS(orig.lat * pi()/180) * COS(destination.lat * pi()/180) *
        POWER(SIN((orig.lon -destination.lon) * pi()/180 / 2), 2) ))
    as distance
FROM users AS destination, users AS orig
WHERE origin.id=userid
    AND destination.longitude BETWEEN lon1 AND lon2
    AND destination.latitude BETWEEN lat1 AND lat2
HAVING distance &lt; dist ORDER BY Distance limit 10;
</code></pre>

<p>becomes this:</p>

<pre><code>SELECT destination.*,
    3956 * 2 * ASIN(SQRT( POWER(SIN((mylat -
        dest.lat) * pi()/180 / 2), 2) +
        COS(mylat * pi()/180) * COS(dest.lat * pi()/180) *
        POWER(SIN((mylon -dest.lon) * pi()/180 / 2), 2) ))
    as distance
FROM users AS destination
WHERE
    destination.longitude BETWEEN lon1 AND lon2
    AND destination.latitude BETWEEN lat1 AND lat2
HAVING distance &lt; dist ORDER BY Distance limit 10;
</code></pre>

<p>edit: my best guess is that "origin.id=userid" should read "origin.id=destination.id".  Am I correct in thinking that this join is done to filter out all users who are outside of the "distance box" -- in order to avoid calculating the actual geo distance?</p>

### Answer ID: 20379488
<h3>First Part</h3>

<p><code>*</code> selects all columns.  You can specify all columns for a particular table using the dot notation as you would use to specify an individual column for a table.  For example:</p>

<pre><code>SELECT t1.* FROM t1 NATURAL JOIN t2
</code></pre>

<p>Will only <code>SELECT</code> columns from <code>t1</code> even though <code>t2</code> is used in the JOIN.</p>

<h3>Next Part</h3>

<p>This just does a mathematical calculation on some columns and aliases the result in <code>distance</code> (not "destination").  You can reference the result as <code>distance</code> in the result set.  The <code>AS</code> keyword sets the column alias, but it is optional.</p>

<h3>Third Part</h3>

<p><code>destination</code> and <code>origin</code> are aliases.  They are leaving off the optional <code>AS</code> keyword.  It would be the same to write:</p>

<pre><code>FROM users AS destination, users AS origin
</code></pre>

<p>The <code>users</code> table is being renamed for the duration of the query so it can be referenced by the alias but also to avoid the collision of two of the same table name in the query which would be invalid.</p>

<h3>Last Part</h3>

<p><code>distance</code> is an alias for the mathematical calculation above.  <code>HAVING</code> is like <code>WHERE</code>, but it has to be used for aggregation (e.g. <code>GROUP BY</code>).  I could be wrong, but I don't think it's necessary in this query.</p>

