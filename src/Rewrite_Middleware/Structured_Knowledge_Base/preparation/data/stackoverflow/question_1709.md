# FULLTEXT operations on a derived table
[Link to question](https://stackoverflow.com/questions/4687596/fulltext-operations-on-a-derived-table)
**Creation Date:** 1294974228
**Score:** 2
**Tags:** sql-server-2008, full-text-search, derived-table
## Question Body
<p>In my SQL Server 2008 RC2 database I have a table T that has a full text index defined on column FT.  I am trying to derive a table containing column FT, then select from this derived table using a full text operation as follows:</p>

<pre><code>SELECT ft_alias FROM
  (SELECT ft AS ft_alias FROM t) t_alias
WHERE CONTAINS(ft_alias, 'abc')
</code></pre>

<p>But this gives the error message:    </p>

<blockquote>
  <p>Cannot use a CONTAINS or FREETEXT
  predicate on column 'ft_alias' because
  it is not full-text indexed.</p>
</blockquote>

<p>No way!  The optimizer can't work out that this column is full text indexed?  I find this suprising, because it <strong>can and will</strong> use the index on columns with a standard index.</p>

<p>I realise that in this simple case I can just rewrite the query without a derived table, but our application is generating arbitrarily complex SQL from user queries, and using derived tables makes it much easier for us to generate the correct SQL.</p>

<p>Is there really no way around this?</p>

