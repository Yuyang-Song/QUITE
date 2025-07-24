# QueryDSL AND/ OR Operator Not Working with BooleanExpression
[Link to question](https://stackoverflow.com/questions/23509502/querydsl-and-or-operator-not-working-with-booleanexpression)
**Creation Date:** 1399440808
**Score:** 9
**Tags:** querydsl
## Question Body
<p>We are Doing a search on an entity , we are using Query DSL . </p>

<p>the table structure is as follows </p>

<pre><code>TableA : shop -&gt; has manytoOne relationship to TableB : Discount
</code></pre>

<p>We need to build a predicate which returns all the shops which does not have discounted<br>
Sale and also that has discounted Sale . </p>

<p>We are Using MySQL Database and JPA as our persistence framework . </p>

<p>Scenario is that we are performing a search and search should get out all the shops with no discounts and shops with discounts approved.  </p>

<p>the below are our boolean expressions that we have it at present. </p>

<pre><code>BooleanExpression A = shop.id.eq(SomeId);
BooleanExpression B = shop.name.eq(SomeName)
BooleanExpression C = shop.discount.isNotNull;
BooleanExpression D = shop.discount.isNull;
BooleanExpression E = shop.disccount.approved.eq(SomeValue)
</code></pre>

<p>now we need to build query to get all the shops which don't have a discount , and also all the shops which have a discount and Approved .</p>

<p>we tried with the predicate </p>

<pre><code>A
.and(B)
.and(D .or(C.and(D).and(E))
)
</code></pre>

<p>We expect the query to be </p>

<pre><code>where shop.id=#someid and shop.name = 'some name' and (shop.discount is Null Or (shop.discount is not null and shop.approved='#some Value'))
</code></pre>

<p>but what the query generated is </p>

<pre><code>where  shop.id=`#someid` and shop.name = `'some name'` and (shop.discount is Null Or shop.discount is not null and shop.approved='`#some Value`')
</code></pre>

<p>we are not getting out the proper resultset with this predicate , </p>

<p>Is there any Way I can rewrite the predicate to make it working as expected ? kindly help me with suggestions. </p>

<p>thanks 
Saravana.</p>

## Answers
### Answer ID: 23524830
<pre><code>A.and(B).and(D .or(C.and(D).and(E)))
</code></pre>

<p>is equivalent to</p>

<pre><code>A and B and (D or C and D and E)
</code></pre>

<p>See here for MySQL operator precedence <a href="https://dev.mysql.com/doc/refman/5.0/en/operator-precedence.html" rel="nofollow">https://dev.mysql.com/doc/refman/5.0/en/operator-precedence.html</a></p>

<p>Concerning your example this should work</p>

<pre><code>shop.discount.isNull()
.or(shop.discount.isNotNull()
    .and(shop.discount.approved.eq(SomeValue)))
</code></pre>

