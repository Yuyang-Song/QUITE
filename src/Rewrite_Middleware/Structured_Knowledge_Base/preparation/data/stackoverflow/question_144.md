# Get an average of variables in MySQL query as well as SUMS
[Link to question](https://stackoverflow.com/questions/14377258/get-an-average-of-variables-in-mysql-query-as-well-as-sums)
**Creation Date:** 1358419446
**Score:** 0
**Tags:** php, mysql, sql
## Question Body
<p>(This is a rewrite of my previous question which may not have been clear enough)</p>

<p>I have a query for a MYSQL database which is as follows:</p>

<pre><code>SELECT name,
SUM(IF(date_format (date, '%b, %Y')= 'Dec, 2011', 1,0)) AS `month1`, 
SUM(IF(date_format (date, '%b, %Y')= 'Jan, 2012', 1,0)) AS `month2`, 
SUM(IF(date_format (date, '%b, %Y')= 'Feb, 2012', 1,0)) AS `month3`, 
etc...
</code></pre>

<p>Which gets me a series of results like - month1=55, month2=70, month3=89 etc</p>

<p>In the query is a line -</p>

<pre><code>COUNT(*) AS total FROM table order by total
</code></pre>

<p>Which effectively gives me a total of month1+month2+month3+ etc</p>

<p>However I also need to get an average of those same monthly totals</p>

<p>So I need a MySQL function that would effectively be something like</p>

<pre><code>AVG (month1, month2, month3 etc) 
</code></pre>

<p>which would give the average of 55,70,89</p>

<p>Can anyone help?</p>

<p>Thanks very much</p>

<p>AS REQUESTED, COMPLETE QUERY IS -</p>

<pre><code>SELECT name, 
    SUM(IF(date_format (date, '%b, %Y')= 'Nov, 2011', 1,0))/list*1000 AS `month1`, 
    SUM(IF(date_format (date, '%b, %Y')= 'Dec, 2011', 1,0))/list*1000 AS `month2`, 
    SUM(IF(date_format (date, '%b, %Y')= 'Jan, 2012', 1,0))/list*1000 AS `month3`, 
    SUM(IF(date_format (date, '%b, %Y')= 'Feb, 2012', 1,0))/list*1000 AS `month4`, 
    SUM(IF(date_format (date, '%b, %Y')= 'Mar, 2012', 1,0))/list*1000 AS `month5`, 
    SUM(IF(date_format (date, '%b, %Y')= 'Apr, 2012', 1,0))/list*1000 AS `month6`, 
    SUM(IF(date_format (date, '%b, %Y')= 'May, 2012', 1,0))/list*1000 AS `month7`, 
    SUM(IF(date_format (date, '%b, %Y')= 'Jun, 2012', 1,0))/list*1000 AS `month8`, 
    SUM(IF(date_format (date, '%b, %Y')= 'Jul, 2012', 1,0))/list*1000 AS `month9`, 
    SUM(IF(date_format (date, '%b, %Y')= 'Aug, 2012', 1,0))/list*1000 AS `month10`, 
    SUM(IF(date_format (date, '%b, %Y')= 'Sep, 2012', 1,0))/list*1000 AS `month11`, 
    SUM(IF(date_format (date, '%b, %Y')= 'Oct, 2012', 1,0))/list*1000 AS `month12`, 
    COUNT(*) AS total 
FROM table 
group by name 
order by total 
</code></pre>

## Answers
### Answer ID: 14377435
<p>In your case you can use a subquery -</p>

<pre><code>SELECT name,
  `month1`, `month2`, `month3`
  total,
  (`month1` + `month2` + `month3`) / 3 AS `avg`
FROM
  (SELECT name, 
    SUM(IF(date_format (date, '%b, %Y')= 'Nov, 2011', 1,0))/list*1000 AS `month1`, 
    SUM(IF(date_format (date, '%b, %Y')= 'Dec, 2011', 1,0))/list*1000 AS `month2`, 
    SUM(IF(date_format (date, '%b, %Y')= 'Jan, 2012', 1,0))/list*1000 AS `month3`, 
    COUNT(*) AS total 
  FROM table 
  GROUP BY name 
  ORDER BY total
  ) t
</code></pre>

<hr>

<p>But I'd suggest you to use something like this -</p>

<pre><code>SELECT month, AVG(cnt) cnt FROM
  (SELECT MONTH(DATE) month, COUNT(*) cnt FROM table1 GROUP BY month) t
GROUP BY month WITH ROLLUP
</code></pre>

<p>...you only should add year support.</p>

### Answer ID: 14377399
<p>You can simply use</p>

<pre><code>SELECT name, month1,month2,...., AVG(month1,month2,...,month12) as Average FROM
(
SELECT name,
SUM(IF(date_format (date, '%b, %Y')= 'Dec, 2011', 1,0)) AS `month1`, 
SUM(IF(date_format (date, '%b, %Y')= 'Jan, 2012', 1,0)) AS `month2`, 
SUM(IF(date_format (date, '%b, %Y')= 'Feb, 2012', 1,0)) AS `month3`, 
etc...
) as t
</code></pre>

