# Several layers of nested subqueries with Exists/In, best performance?
[Link to question](https://stackoverflow.com/questions/15369099/several-layers-of-nested-subqueries-with-exists-in-best-performance)
**Creation Date:** 1363112534
**Score:** 0
**Tags:** sql, db2, nested, subquery
## Question Body
<p>I'm working on some rather large queries for a search function. There are a number of different inputs and the queries are pretty big as a result. It's grown to where there are nested subqueries 2 layers deep. Performance has become an issue on the ones that will return a large dataset and likely have to sift through a massive load of records to do so. The ones that have less comparing to do perform fine, but some of these are getting pretty bad. The database is DB2 and has all of the necessary indexes, so that shouldn't be an issue. I'm wondering how to best write/rewrite these queries to perform as I'm not quite sure how the optimizer is going to handle it. I obviously can't dump the whole thing here, but here's an example:</p>

<pre><code>Select A, B 
from TableA
      --A series of joins--
WHERE TableA.A IN (
      Select C 
      from TableB
              --A few joins--
      WHERE TableB.C IN (
              Select D from TableC
              --More joins and conditionals--
              )
       )
</code></pre>

<p>There are also plenty of conditionals sprinkled throughout, the vast majority of which are simple equality. You get the idea. The subqueries do not provide any data to the initial query. They exist only to filter the results. A problem I ran into early on is that the backend is written to contain a number of partial query strings that get assembled into the final query (with 100+ possible combinations due to the search options, it simply isn't feasible to write a query for each), which has complicated the overall method a bit. I'm wondering if EXISTS instead of IN might help at one or both levels, or another bunch of joins instead of subqueries, or perhaps using WITH above the initial query for TableC, etc. I'm definitely looking to remove bottlenecks and would appreciate any feedback that folks might have on how to handle this.</p>

<p>I should probably also add that there are potential unions within both subqueries.</p>

## Answers
### Answer ID: 15377983
<p>I found out "IN" predicate is good for small subqueries and "EXISTS" for large subqueries.
Try to execute query with "EXISTS" predicate for large ones.</p>

<pre><code>SELECT A, B 
FROM TableA
WHERE EXISTS (
      Select C 
      FROM TableB
      WHERE TableB.C = TableA.A)
</code></pre>

### Answer ID: 15369375
<p>It would probably help to use inner joins instead.</p>

<pre><code>Select A, B
from TableA
  inner join TableB on TableA.A = TableB.C
  inner join TableC on TableB.C = TableC.D
</code></pre>

<p>Databases were designed for joins, but the optimizer might not figure out that it can use an index for a sub-query.  Instead it will probably try to run the sub-query, hold the results in memory, and then do a linear search to evaluate the IN operator for every record.</p>

<p>Now, you say that you have all of the necessary indexes.  Consider this for a moment.</p>

<p>If one optional condition is TableC.E = 'E' and another optional condition is TableC.F = 'F',
then a query with both would need an index on fields TableC.E <strong>AND</strong> TableC.F.  Many young programmers today think they can have one index on TableC.E and one index on TableC.F, and that's all they need.  In fact, if you have both fields in the query, you need an index on both fields.</p>

<p>So, for 100+ combinations, "all of the necessary indexes" could require 100+ indexes.</p>

<p>Now an index on TableC.E, TableC.F could be use in a query with a TableC.E condition and no TableC.F condition, but could not be use when there is a TableC.F condition and no TableC.E condition.</p>

<p>Hundreds of indexes?  What am I going to do?</p>

<p>In practice it's not that bad.  Let's say you have N optional conditions which are either in the where clause or not.  The number of combinations is 2 to the nth, or for hundreds of combinations, N is log2 of the number of combinations, which is between 6 and 10.  Also, those log2 conditions are spread across three tables.  Some databases support multiple table indexes, but I'm not sure DB2 does, so I'd stick with single table indexes.</p>

<p>So, what I am saying is, say for the TableC.E, and TableC.F example, it's not enough to have just the following indexes:</p>

<pre><code>TableB ON C
TableC ON D
TableC ON E
TableC ON F
</code></pre>

<p>For one thing, the optimizer has to pick among which <em>one</em> of the last three indexes to use.  Better would be to include the D field in the last two indexes, which gives us</p>

<pre><code>TableB ON C
TableC ON D, E
TableC ON D, F
</code></pre>

<p>Here, if neither field E nor F is in the query, it can still index on D, but if either one is in the query, it can index on both D and one other field.</p>

<p>Now suppose you have an index for 10 fields which may or may not be in the query.  Why ever have just one field in the index?  Why not add other fields in descending order of likelihood of being in the query?</p>

<p>Consider that when planning your indexes.</p>

