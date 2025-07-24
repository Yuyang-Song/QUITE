# Can prepared SQL statement be rewritten by the database?
[Link to question](https://stackoverflow.com/questions/28324926/can-prepared-sql-statement-be-rewritten-by-the-database)
**Creation Date:** 1423063248
**Score:** 3
**Tags:** java, sql, postgresql, jdbc
## Question Body
<p>I have this fairly innocent looking JDBC code:</p>

<pre><code>String sql = "UPDATE table_name SET column2 = column1";
try (PreparedStatement statement = dbConnection.prepareStatement(sql)) {
  statement.executeUpdate();
}
dbConnection.commit();
</code></pre>

<p>When running this on PostgreSQL I have noticed that the <em>actual running</em> query (which is visible from within PostgreSQL) is as follows:</p>

<pre><code>UPDATE table_name SET column2 = i.column1 FROM table_name i
</code></pre>

<p>The problem is that the rewritten query is <strong>much</strong> more expensive:</p>

<pre><code># explain update table_name set column2 = i.column1 from table_name i;

                         QUERY PLAN                                      

-------------------------------------------------------------------------------  
Update on table_name  (cost=0.00..3586127424.55 rows=206294914809 width=166)          
   -&gt;  Nested Loop  (cost=0.00..3586127424.55 rows=206294914809 width=166)
         -&gt;  Seq Scan on table_name (cost=0.00..15453.97 rows=454197 width=156)
         -&gt;  Materialize  (cost=0.00..19942.96 rows=454197 width=10)
               -&gt;  Seq Scan on table_name i  (cost=0.00..15453.97 rows=454197 width=10)

(5 rows)
</code></pre>

<p>instead of</p>

<pre><code># explain update table_name set column2 = column1;

                           QUERY PLAN                                

------------------------------------------------------------------------
Update on table_name  (cost=0.00..15453.97 rows=454197 width=156)
 -&gt;  Seq Scan on table_name  (cost=0.00..15453.97 rows=454197 width=156)
(2 rows)
</code></pre>

<p>The rewritten query takes virtually infinite amount of time to run whereas non-rewritten finishes in few minutes if not seconds.</p>

<p>Questions:</p>

<ul>
<li>Is it common for database (I presume) to rewrite queries?</li>
<li>If yes, how come PostgreSQL is stupid enough to shoot itself in the foot? Is this a known bug?</li>
<li>How can query rewrite be avoided - both at database but preferably JDBC level?</li>
</ul>

## Answers
### Answer ID: 28326724
<p>I <em>think</em> this is somehow related to the fact that the original query</p>

<pre><code>UPDATE table_name SET column2 = column1
</code></pre>

<p>doesn't have <code>WHERE</code> statement.</p>

<p>As soon as I changed the query into</p>

<pre><code>UPDATE table_name SET column2 = column1 WHERE 1=1
</code></pre>

<p>, it just worked the way I would expect it to work.</p>

<p>Sorry for this is no scientific/referenced explanation but hopefully this still may be helpful for somebody. I have used this trick earlier for different purpose (some legacy databases required <code>WHERE</code> clause) and it seems to do the job for this case too.</p>

### Answer ID: 28325150
<p>Some databases actually rewrite codes (though it's not the database that does that work but java -- java get to know how to convert your code once you have a valid connection) but your query is what's misleading Postgres.
Postgres did exactly what you requested because that query should actually affect all rows in the database. But if your plan was something different, then you should let us know what your aim is</p>

