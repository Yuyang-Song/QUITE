# Incorrect count of one side during paginating a one-to-many relationship
[Link to question](https://stackoverflow.com/questions/76546477/incorrect-count-of-one-side-during-paginating-a-one-to-many-relationship)
**Creation Date:** 1687616308
**Score:** 1
**Tags:** postgresql, jooq
## Question Body
<p>I try to implement offset pagination of one side in a one-to-many relationship with filtering by many sides and count the total via a window function.</p>
<p>Because of the <a href="https://en.wiktionary.org/wiki/Cartesian_product#Noun" rel="nofollow noreferrer">Cartesian product</a> problem, I get an incorrect box total count available by the specified ball color filter value:</p>
<pre class="lang-java prettyprint-override"><code>Map&lt;Integer, List&lt;Box&gt;&gt; result = ctx.selectDistinct(
    Box.asterisk(), count().over().as(&quot;total&quot;))
    .from(BOX)
    .leftJoin(BALL).on(BALL.BOX_ID.eq(BOX.ID))
    .where(BALL.COLOR.eq(&quot;red&quot;))
    .orderBy(BOX.BOX_ID)
    .limit(size)
    .offset(size * page)
    .fetchGroups(field(&quot;total&quot;, Integer.class), record-{ mapping logic in dto });
</code></pre>
<p>I tried to rewrite the <a href="https://en.wikipedia.org/wiki/JOOQ_Object_Oriented_Querying" rel="nofollow noreferrer">JOOQ</a> query with <em>countDistinct</em> as:</p>
<pre class="lang-java prettyprint-override"><code>Map&lt;Integer, List&lt;Box&gt;&gt; result = ctx.selectDistinct(
    Box.asterisk(), countDistinct(BOX.ID).over().as(&quot;total&quot;))
        .from(BOX)
        .leftJoin(BALL).on(BALL.BOX_ID.eq(BOX.ID))
        .where(BALL.COLOR.eq(&quot;red&quot;))
        .orderBy(BOX.BOX_ID)
        .limit(size)
        .offset(size * page)
        .fetchGroups(field(&quot;total&quot;, Integer.class), record-{ mapping logic in projection});
</code></pre>
<p>And get:</p>
<blockquote>
<p>org.postgresql.util.PSQLException: ERROR: DISTINCT is not implemented for window functions</p>
</blockquote>
<p>How can I fix this? I don’t want to write two separate JOOQ queries to get the total count and to get the page.</p>
<p>I want to eliminate duplicates in the result set of a single JOOQ query and make it count the right global quantity of the available box records with red balls via one one select on the database side by the most efficient way.</p>

## Answers
### Answer ID: 76555638
<p>You're only projecting <code>BOX</code> columns, using the <code>BALL</code> join only to count red balls per box. So just use <code>GROUP BY</code>, instead (knowing that most usages of <code>DISTINCT</code> are probably not optimal):</p>
<pre><code>Map&lt;Integer, List&lt;Box&gt;&gt; result = 
ctx.select(BOX.fields())
   .select(count(BALL.ID).as(&quot;total&quot;))
   .from(BOX)
   .leftJoin(BALL)
       .on(BALL.BOX_ID.eq(BOX.ID))
       .and(BALL.COLOR.eq(&quot;red&quot;))
   .groupBy(BOX.ID)
   .orderBy(BOX.ID)
   .limit(size)
   .offset(size * page)
   .fetchGroups(field(&quot;total&quot;, Integer.class), record-{ mapping logic in dto });
</code></pre>
<p>A few remarks:</p>
<ul>
<li>This makes use of a standard SQL feature implemented by PostgreSQL, where you can <code>GROUP BY</code> a primary key, and still project all functionally dependent columns. <a href="https://blog.jooq.org/functional-dependencies-in-sql-group-by/" rel="nofollow noreferrer">I've blogged about it here</a>. If you're not using PostgreSQL, then, just list all <code>BOX.fields()</code> in <code>GROUP BY</code>, instead.</li>
<li>I've moved your <code>BALL.COLOR.eq(&quot;red&quot;)</code> predicate into the <code>LEFT JOIN</code>'s <code>ON</code> clause, <a href="https://blog.jooq.org/the-difference-between-sqls-join-on-clause-and-the-where-clause/" rel="nofollow noreferrer">see also this blog post I wrote that explains it</a>. In short, if you leave that predicate in the <code>WHERE</code> clause, you're turning your <code>LEFT JOIN</code> into an <code>INNER JOIN</code>, which you don't want. Note that you can't <code>COUNT(*)</code> anymore, in that case, but <code>COUNT(BALL.ID)</code>, to get a <code>0</code> count for <code>BOX</code>es without <code>BALL</code>s (instead of a <code>1</code> count).</li>
</ul>

