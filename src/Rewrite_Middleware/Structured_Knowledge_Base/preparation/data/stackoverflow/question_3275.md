# How would I use divide each row by the SUM of another column?
[Link to question](https://stackoverflow.com/questions/74945692/how-would-i-use-divide-each-row-by-the-sum-of-another-column)
**Creation Date:** 1672267904
**Score:** 0
**Tags:** sql, denodo
## Question Body
<p>The database is as follows:</p>
<div class="s-table-container">
<table class="s-table">
<thead>
<tr>
<th>ID</th>
<th>Classification</th>
<th>emissions</th>
<th>market_value</th>
</tr>
</thead>
<tbody>
<tr>
<td>1</td>
<td>Type A</td>
<td>0.04</td>
<td>5.67</td>
</tr>
<tr>
<td>2</td>
<td>Type B</td>
<td>0.01</td>
<td>6.12</td>
</tr>
</tbody>
</table>
</div>
<p>I am trying to add a column whose formula will be as follows:</p>
<pre><code>(emissions * market_value) / SUM(market_value) AS Contribution
</code></pre>
<p>Doing so will turn the database into this:</p>
<div class="s-table-container">
<table class="s-table">
<thead>
<tr>
<th>ID</th>
<th>Classification</th>
<th>emissions</th>
<th>market_value</th>
<th>contribution</th>
</tr>
</thead>
<tbody>
<tr>
<td>1</td>
<td>Type A</td>
<td>0.04</td>
<td>5.67</td>
<td>0.192</td>
</tr>
<tr>
<td>2</td>
<td>Type B</td>
<td>0.01</td>
<td>6.12</td>
<td>0.005</td>
</tr>
</tbody>
</table>
</div>
<p>I've tried writing my scripts as follow but have had no luck:</p>
<ul>
<li><strong>Attempt 1:</strong></li>
</ul>
<pre><code>SELECT
id,
classification,
emissions,
market_value
(emissions * market_value / (SELECT SUM(market_value) from database)) AS contribution
FROM database 

</code></pre>
<p>However, the platform I am doing SQL on, Denodo, does not allow for subqueries within a select statemen.</p>
<p>I've also tried rewriting my query as follows:</p>
<ul>
<li><strong>Attempt 2:</strong></li>
</ul>
<pre><code>SELECT
id,
classification,
emissions,
market_value,
(emissions* market_value / SUM(market_value)) AS contribution
FROM database 
GROUP BY id, classification, emissions, market_value
</code></pre>
<p>But this doesn't seem to work either. The SUM function using this format just returns the same value as the &quot;emissions&quot; column per row for some reason.</p>

## Answers
### Answer ID: 74946423
<p>I have no denodo to try it out, but it seems to support Common Table Expression (CTE). <a href="https://community.denodo.com/docs/html/browse/6.0/vdp/vql/queries_select_statement/with_clause/with_clause" rel="nofollow noreferrer">https://community.denodo.com/docs/html/browse/6.0/vdp/vql/queries_select_statement/with_clause/with_clause</a></p>
<p>Try this maybe:</p>
<pre><code>WITH sum_table (mval_sum) AS
    (SELECT SUM(market_value) AS mval_sum
       FROM database)
SELECT id
     , classification
     , emissions
     , market_value
     , (emissions * market_value / mval_sum) AS contribution
  FROM database
  JOIN sum_table
</code></pre>
<p>MySQL 8.0 Playground:
<a href="https://www.db-fiddle.com/f/ajfdrdXsgK1z4UnrDgbPCL/0" rel="nofollow noreferrer">https://www.db-fiddle.com/f/ajfdrdXsgK1z4UnrDgbPCL/0</a></p>

