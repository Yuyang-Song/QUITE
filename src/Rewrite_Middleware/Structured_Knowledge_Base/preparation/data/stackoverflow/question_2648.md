# Alternative for case when exists subquery in select
[Link to question](https://stackoverflow.com/questions/44545111/alternative-for-case-when-exists-subquery-in-select)
**Creation Date:** 1497444087
**Score:** 1
**Tags:** sql, select, subquery, query-optimization, case-when
## Question Body
<p>I have a couple of questions regarding <code>CASE WHEN</code> expressions in a select clause. I am interested in knowing how these queries are executed in general in databases, and if there are alternate ways of writing such queries. </p>

<p>I have queries with <code>CASE WHEN</code> in the select clause as follows:</p>

<pre><code>SELECT
 (CASE WHEN cond1 THEN col2 ELSE NULL END),
 (CASE WHEN cond2 THEN col3 ELSE NULL END),
 (CASE WHEN cond3 THEN col4 ELSE NULL END), ...,
 simple-col-expr-list ... FROM
table-expr-list WHERE expr-list ...
</code></pre>

<p>The conditions in the <code>CASE WHEN</code> expression have following forms:</p>

<ol>
<li><code>T1.some_column = some_value</code></li>
<li><code>exists(select 1 from T2 where some conditions on columns from T2)</code></li>
<li><code>exists(select 1 from T2 where T2.key1 = T1.key1 and optionally more conditions on other columns from T2)</code></li>
<li><code>exists(select 1 from T1 as alias_T1 where alias_T1.key1 = T1.key1 and optionally some conditions on other columns from T1)</code></li>
<li><p><code>exists(select 1 from T2 join T3 on (T2.key1 = T3.key1) join T1 as alias_T1 on (alias_t1.key2 = T2.key2))</code>
and so on..</p></li>
<li><p>disjunction of two or more types of conditions from above</p></li>
</ol>

<p>In example 1, the condition is checking for a value in another or the same column that is to be projected. In examples 2 to 5 the <code>CASE WHEN</code> conditions are exists sub-queries on one or more tables, and they may or may not be correlated sub-queries.</p>

<p>As I understand, the <code>CASE WHEN</code> expression on a column would be evaluated on each row of the column, and this would be done for every column. Particularly, if two columns have the same <code>CASE WHEN</code> condition, they condition would be checked on both the columns and for all the rows separately.</p>

<p>Does any database system (e.g. mysql, postgresql, oracle, etc.) have heuristics to optimize the query plan for such queries, where they can perform the check once internally for both the columns? If the <code>CASE WHEN</code> expression does not have correlated sub-queries, then I believe there might be a way to do this. Could someone point me to some sources that explain these optimizations, if they exist?</p>

<p>I would also like to know if there are generic rules on how to rewrite such <code>CASE WHEN</code> expressions in the query to make the source query itself more efficient.</p>

<p>Thanks</p>

