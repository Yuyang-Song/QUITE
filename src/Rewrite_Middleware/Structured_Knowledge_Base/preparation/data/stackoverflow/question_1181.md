# Add WHERE clause condition starting with CASE using CodeIgniter&#39;s query builder methods
[Link to question](https://stackoverflow.com/questions/6239897/add-where-clause-condition-starting-with-case-using-codeigniters-query-builder)
**Creation Date:** 1307228404
**Score:** 7
**Tags:** php, mysql, codeigniter, activerecord, query-builder
## Question Body
<p>I am using active records to access the database. However, an additional feature requires me to use standard SQL query. Is it possible to use both active records and standard SQL query in the same query? Eg:</p>
<pre><code>$this-&gt;db-&gt;select(...)
         -&gt;from(...)
         -&gt; .....
         -&gt;query(WHERE CASE ..........);
</code></pre>
<p>In the standard SQL query, I want to use a WHERE clause with CASE. Is this possible without rewriting the entire query in standard SQL? The active record query is very complex.</p>

## Answers
### Answer ID: 78976433
<p>You can absolutely craft custom WHERE clauses without having the rendered SQL corrupted by automated quoting/escaping.</p>
<p>The third parameter of a <code>where()</code> method call is a nullable boolean value which defaults to <code>true</code>.  If set to <code>false</code>, then no automated quoting/escaping will be applied.</p>
<p>For example, if you wanted the following WHERE clause:</p>
<pre><code>WHERE CASE `foo` WHEN CURRENT_DATE - 1 THEN 'foo' END IS NOT NULL
</code></pre>
<p>then you could turn off escaping, and manually add identifier and string quoting as desired with the following method call.</p>
<pre class="lang-php prettyprint-override"><code>$this-&gt;db-&gt;where(
    'CASE ' . $this-&gt;db-&gt;escape_identifiers('foo') . ' WHEN CURRENT_DATE - 1 THEN ' . $this-&gt;db-&gt;escape('foo') . ' END',
    'IS NOT NULL',
    false
);
</code></pre>
<p>or using interpolation instead of concatenation:</p>
<pre class="lang-php prettyprint-override"><code>$this-&gt;db-&gt;where(
    sprintf(
        'CASE %s WHEN CURRENT_DATE - 1 THEN %s END',
        $this-&gt;db-&gt;escape_identifiers('foo'),
        $this-&gt;db-&gt;escape('foo')
    ),
    'IS NOT NULL',
    false
);

</code></pre>

### Answer ID: 6239913
<p>As far as I know, you can't combine standard SQL and active record like you're trying to do. </p>

<p>However, you can write your WHERE string manually if you want, and then submit that to the ActiveRecord class. I'm not entirely sure if that's what you're looking for as I have never even used CASE, but it sounds like it might be what you're looking for? Let me know!</p>

<pre><code>$where = "name='Joe' AND status='boss' OR status='active'";

$this-&gt;db-&gt;where($where);
</code></pre>

