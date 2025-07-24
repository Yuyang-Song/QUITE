# Optimizing AND conditions in postgresql
[Link to question](https://stackoverflow.com/questions/38317207/optimizing-and-conditions-in-postgresql)
**Creation Date:** 1468276228
**Score:** 2
**Tags:** postgresql, query-optimization, conditional-statements, where-clause
## Question Body
<p>I am writing analytics software that generates complicated queries. When building the where clause, it may happen that multiple constraints are added on the same database field. I was wondering if PostgreSQL rewrites multiple constraints into simpler ones. I did some tests:</p>

<pre><code>SELECT COUNT(id) FROM employee WHERE age BETWEEN 18 AND 40;
</code></pre>

<p>I ran this 10 times and the average time spent was 65ms. Now I make the query a bit longer but trivial to optimize:</p>

<pre><code>SELECT COUNT(id) FROM employee WHERE
(age BETWEEN 18 AND 40) AND
(age BETWEEN 18 AND 40) AND
(age BETWEEN 18 AND 40);
</code></pre>

<p>This query takes 100ms on average, which is a lot slower. Also, the following query:</p>

<pre><code>SELECT COUNT(id) FROM employee WHERE
(age BETWEEN 28 AND 70) AND
(age BETWEEN 25 AND 40) AND
(age BETWEEN 22 AND 33) AND
(age BETWEEN 18 AND 30);
</code></pre>

<p>takes 105ms on average, while it is equivalent to:</p>

<pre><code>SELECT COUNT(id) FROM employee WHERE age BETWEEN 28 AND 30;
</code></pre>

<p>which runs twice as fast. </p>

<p>These queries are semantically equivalent and I was expecting them to be optimized into the very same query before even the planner touches them. This seems like low-hanging fruit for the query rewriter. Is there any hidden configuration option I'm missing? I'm using postgresql 9.4.5.</p>

<p>Thank you!</p>

## Answers
### Answer ID: 38319850
<p>The optimiser doesn't fold contiguous ranges together. It doesn't do that sort of datatype-level analysis.</p>

<p>PostgreSQL doesn't really care if you're testing ranges of integers, floating point values, or text strings. Range-folding like this would only be correct for types that are discrete countable ordinals. If you tried it for, say, floating point values you might get subtly wrong answers.</p>

<p>PostgreSQL doesn't know which types would satisfy the requrirements for this to be safe, so it can't do it. Also, every possible optimisation done by the query planner has a computational cost to check whether the optimisation might apply, so there's a trade-off between planning and execution costs.</p>

<p>TL;DR: This case won't be auto-optimised by the planner.</p>

<p>In future, though: <em>always</em> provide your PostgreSQL version and <code>explain (buffers, analyze)</code> output for the query/queries.</p>

