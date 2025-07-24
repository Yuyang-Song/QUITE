# Convert Hibernate @Formula to JOOQ field
[Link to question](https://stackoverflow.com/questions/28166107/convert-hibernate-formula-to-jooq-field)
**Creation Date:** 1422347442
**Score:** 1
**Tags:** sql, hibernate, jpa, dsl, jooq
## Question Body
<p>I am rewriting entire DB access layer from Hibernate to JOOQ and I face following issue.</p>

<p>One of JPA models is annotated with <a href="https://docs.jboss.org/hibernate/orm/3.5/api/org/hibernate/annotations/Formula.html" rel="nofollow">@Formula</a> annotation as follows: </p>

<pre><code>@Formula("fee1 + fee2 + fee3 + fee4")
private BigDecimal fee5;
</code></pre>

<p>Later in the code, a JPA query is made against the database which compares <strong>fee5</strong> to parameter:</p>

<pre><code>SELECT ... FROM ... WHERE fee5 &gt; input;
</code></pre>

<p>How can above query be translated to JOOQ DSL?</p>

## Answers
### Answer ID: 72818281
<p>Starting from jOOQ 3.17, the most direct translation of a <code>@Formula</code> would be a <a href="https://blog.jooq.org/create-dynamic-views-with-jooq-3-17s-new-virtual-client-side-computed-columns/" rel="nofollow noreferrer">virtual client side computed column</a>, i.e. a synthetic column that is attached to a table and produces an expression in every query that projects the column.</p>
<p>That way, you could just write:</p>
<pre class="lang-java prettyprint-override"><code>ctx.select(...)
   .from(TABLE)
   .where(FEE5.gt(input))
   .fetch();
</code></pre>
<p>But you don't strictly need this feature. Every jOOQ query is a <a href="https://www.jooq.org/doc/latest/manual/sql-building/dynamic-sql/" rel="nofollow noreferrer">dynamic SQL query</a>, so you can add whatever expression you choose to refactor into a utility method to any query you like. For example:</p>
<pre class="lang-java prettyprint-override"><code>ctx.select(...)
   .from(TABLE)
   .where(fee5(TABLE).gt(input))
   .fetch();
</code></pre>
<p>With:</p>
<pre class="lang-java prettyprint-override"><code>Field&lt;BigDecimal&gt; fee5(MyTable t) {
    return t.FEE1.add(t.FEE2).add(t.FEE3).add(t.FEE4);
}
</code></pre>

### Answer ID: 28166484
<p>I managed to resolve the issue with following JOOQ query:</p>

<pre><code>BigDecimal input = ...;
Field&lt;BigDecimal&gt; fee5 = TABLE.FEE1.add(TABLE.FEE2).add(TABLE.FEE3).add(TABLE.FEE4).as("fee5");
Condition cond = fee5.greaterThan(input);
</code></pre>

