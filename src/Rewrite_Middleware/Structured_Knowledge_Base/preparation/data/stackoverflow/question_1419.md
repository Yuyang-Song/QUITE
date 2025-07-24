# How can I add a column to a right join select query
[Link to question](https://stackoverflow.com/questions/75448187/how-can-i-add-a-column-to-a-right-join-select-query)
**Creation Date:** 1676379540
**Score:** 0
**Tags:** mysql
## Question Body
<p>I am trying to find a way to add a country code to a database call record based on a phone number column. I have a table with countries and their dialling codes called countries. I can query all records and add the country code after but I need to be able to filter and paginate the results.</p>
<p>I am working with a system I don't have much control over so adding new columns to tables or rewriting large blocks of code isn't really an option. This is what I have to work with.</p>
<p>Countries Table.</p>
<div class="s-table-container">
<table class="s-table">
<thead>
<tr>
<th>id</th>
<th>name</th>
<th>dialling_code</th>
</tr>
</thead>
<tbody>
<tr>
<td>1</td>
<td>Ireland</td>
<td>353</td>
</tr>
<tr>
<td>2</td>
<td>America</td>
<td>1</td>
</tr>
</tbody>
</table>
</div>
<p>Call Record table.</p>
<div class="s-table-container">
<table class="s-table">
<thead>
<tr>
<th>id</th>
<th>startdatetime</th>
<th>enddatetime</th>
<th>route_id</th>
<th>phonenumber</th>
<th>duration_seconds</th>
</tr>
</thead>
<tbody>
<tr>
<td>1</td>
<td>2014-12-18 18:51:12</td>
<td>2014-12-18 18:52:12</td>
<td>23</td>
<td>3538700000</td>
<td>60</td>
</tr>
<tr>
<td>2</td>
<td>2014-12-18 17:41:02</td>
<td>2014-12-18 17:43:02</td>
<td>43</td>
<td>18700000</td>
<td>120</td>
</tr>
</tbody>
</table>
</div>
<p>Routes table.</p>
<div class="s-table-container">
<table class="s-table">
<thead>
<tr>
<th>id</th>
<th>number</th>
<th>enabled</th>
</tr>
</thead>
<tbody>
<tr>
<td>23</td>
<td>1234567890</td>
<td>1</td>
</tr>
<tr>
<td>43</td>
<td>0987654321</td>
<td>1</td>
</tr>
</tbody>
</table>
</div>
<p>I need to get sum values of duration, total unique phone numbers all grouped by route_id, route_number but now we need to group these results by country_id so we can group callers by country. I use the mysql query below to get sum values of duration, total unique phone numbers all grouped by route_id, route_number. This query was written by another developer a long time ago.</p>
<pre class="lang-sql prettyprint-override"><code>SELECT 
    phone_number,
    route_number, 
    COUNT(callrecord_id) AS total_calls, 
    SUM(duration_sec) AS total_duration, 
    callrecord_join.route_id
FROM routes
RIGHT JOIN (
    SELECT 
        DATE(a.startdatetime) AS call_date, 
        a.id AS callrecord_id, 
        a.route_id AS route_id, 
        a.phonenumber AS phone_number,
        a.duration_seconds as duration_sec,
        b.inboundnumber AS route_number, 
    FROM callrecord AS a
    INNER JOIN routes AS b ON a.route_id = b.id
    WHERE DATE_FORMAT(a.startdatetime, '%Y-%m-%d') &gt;= '2014-12-18' 
    AND DATE_FORMAT(a.startdatetime, '%Y-%m-%d') &lt;= '2014-12-18' 
    AND b.isenabled = 1 
) AS callrecord_join ON routes.id = callrecord_join.route_id
GROUP BY route_id, route_number
LIMIT 10 offset 0;
</code></pre>
<p>I have everything up to adding a country_id in the right join table so I can group by the country_id.</p>
<p>I know I could loop through each country using php and get the results using a where clause, something like the below but I cannot paginate these results or filter them easily.</p>
<p><code>WHERE LEFT(a.phonenumber, strlen($dialling_code)) = $dialling_code</code></p>
<p>How can I use the countries table to add a column to the join table query with the country id so I can group by route_id, route_number and country_id? Something like the table below.</p>
<div class="s-table-container">
<table class="s-table">
<thead>
<tr>
<th>id</th>
<th>startdatetime</th>
<th>enddatetime</th>
<th>route_id</th>
<th>phonenumber</th>
<th>duration_seconds</th>
<th>country_id</th>
</tr>
</thead>
<tbody>
<tr>
<td>1</td>
<td>2014-12-18 18:51:12</td>
<td>2014-12-18 18:52:12</td>
<td>23</td>
<td>3538700000</td>
<td>60</td>
<td>1</td>
</tr>
<tr>
<td>2</td>
<td>2014-12-18 17:41:02</td>
<td>2014-12-18 17:43:02</td>
<td>43</td>
<td>18700000</td>
<td>120</td>
<td>2</td>
</tr>
</tbody>
</table>
</div>
## Answers
### Answer ID: 75449560
<p>The <code>RIGHT JOIN</code> from <code>routes</code> to <code>callrecord_join</code> serves no purpose, as you already have the <code>INNER JOIN</code> between <code>routes</code> and <code>callrecord</code> in the sub-query, which is on the righthand side of the join.</p>
<p>You can use the join you have described -</p>
<pre><code>JOIN countries c ON LEFT(a.phonenumber, LENGTH(c.dialling_code)) = c.dialling_code
</code></pre>
<p>but it will give the same result as:</p>
<pre><code>JOIN countries c ON a.phonenumber LIKE CONCAT(c.dialling_code, '%')
</code></pre>
<p>which should be slightly less expensive.</p>
<p>You should test the join to <code>countries</code> to make sure none of your numbers in <code>callrecord</code> join to multiple countries. Some international dialling codes are ambiguous, so it depends on which list of dialling codes you are using.</p>
<pre><code>SELECT a.*, COUNT(*), GROUP_CONCAT(c.dialling_code)
FROM callrecord a
JOIN country c ON a.phonenumber LIKE CONCAT(c.dialling_code, '%')
GROUP BY a.id
HAVING COUNT(*) &gt; 1;
</code></pre>
<p>Obviously, you will need to batch the above query if your dataset is very large.</p>
<p>I hope I am not grossly over-simplifying things, but from what I understand of your question the query is just:</p>
<pre><code>SELECT
    r.id AS route_id,
    r.number AS route_number,
    c.name AS country_name,
    SUM(a.duration_seconds) AS total_duration,
    COUNT(a.id) AS total_calls,
    COUNT(DISTINCT a.phonenumber) AS unique_numbers
FROM callrecord AS a
JOIN routes AS r ON a.route_id = r.id
JOIN countries c ON a.phonenumber LIKE CONCAT(c.dialling_code, '%')
WHERE a.startdatetime &gt;= '2014-12-18' 
AND a.startdatetime &lt; '2014-12-19'
AND r.isenabled = 1
GROUP BY r.id, r.number, c.name
LIMIT 10 offset 0;
</code></pre>
<p>Please note the removal of <code>DATE_FORMAT()</code> from the <code>startdatetime</code> to make these criteria sargable, assuming a suitable index is available.</p>

