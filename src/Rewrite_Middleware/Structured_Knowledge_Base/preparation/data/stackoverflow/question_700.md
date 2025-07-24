# PostgreSQL function round and JPA/Hibernate
[Link to question](https://stackoverflow.com/questions/37759993/postgresql-function-round-and-jpa-hibernate)
**Creation Date:** 1465619968
**Score:** 0
**Tags:** postgresql, jpa, hibernate-mapping
## Question Body
<p>I have a query which is executed from java application like this:</p>

<pre><code>Query query = getEntityManager().createQuery(hql);
</code></pre>

<p>The query looks like this:</p>

<pre><code>String hql = "select * from table a where round(column1, 3) = round(parameter, 3)";
</code></pre>

<p>Here <code>column1</code> is of type <code>Double</code>. The value it holds is like <code>143.02856666</code>. I need to retain the value as it is, but for some business logic just need to round and compare.</p>

<p>The initial database configured was H2 and this worked fine. Now the database has been changed to Postgres and this query now errors out.</p>

<blockquote>
  <p>ERROR: function round(double precision, integer) does not exist   Hint: No function matches the given name and argument types. You might
  need to add explicit type casts.</p>
</blockquote>

<p>The <code>round()</code> function in Postgres takes a numeric datatype and needs a cast.</p>

<p>The below query works fine if executed directly in Postgres console.</p>

<pre><code>select * from table a where round(cast(column1 as numeric), 3) = round(cast(parameter as numeric), 3);
</code></pre>

<p>The same from java application errors out.</p>

<blockquote>
  <p><strong>java.lang.IllegalArgumentException: org.hibernate.QueryException: Could not resolve requested type for CAST : numeric</strong></p>
</blockquote>

<p>Also tried <code>Query query = getEntityManager().createNativeQuery(hql);</code>
This results in a new error.</p>

<blockquote>
  <p><strong>org.hibernate.engine.jdbc.spi.SqlExceptionHelper  - ERROR: syntax error at or near "where"</strong></p>
</blockquote>

<p>If I debug, this errors out when the below line is executed.</p>

<pre><code>List resultList = query.getResultList();
</code></pre>

<p>How do I rewrite the query so that it works against Postgres ?</p>

## Answers
### Answer ID: 37794710
<p>What you are doing with <code>Query query = getEntityManager().createQuery(hql);</code> is calling a <code>jpql</code>-query, which does not support all db-functions like <code>round(v numeric, s integer)</code>.</p>

<p>Two Suggestions:</p>

<ol>
<li>Use <code>BETWEEN</code> and maintain jpql-mapping</li>
<li>Write a NativeQuery -> <code>Query query = em.createNativeQuery(queryString);</code></li>
</ol>

<p>Your <code>queryString</code> just has to be altered by your parameters.</p>

