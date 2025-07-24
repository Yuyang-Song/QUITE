# Why does this query only return one result?
[Link to question](https://stackoverflow.com/questions/78899670/why-does-this-query-only-return-one-result)
**Creation Date:** 1724296753
**Score:** 0
**Tags:** postgresql
## Question Body
<p>This is a strange test case from the Postgres regression test suite.</p>
<p>It starts with a table named <code>tenk</code>, which has 10,000 rows in it.  The table has a column called <code>unique1</code>, both of which contain values from 0 to 9999, each row in the table having a unique value for that column for each column.  (ie. one row has 369 for <code>unique1</code> and 6521 for <code>unique2</code>, and no other row has those values, though there's a row that has 369 for <code>unique2</code> and a row that has 6521 for <code>unique1</code>.)</p>
<p>The test query is:</p>
<pre><code>select
  (select max((select i.unique2 from tenk1 i where i.unique1 = o.unique1)))
from tenk1 o;
</code></pre>
<p>This returns a single row with a value of <code>9999</code>.  And that feels odd.  Here's how I parse the query in my own head:</p>
<pre><code>Select [subquery] from tenk1 o

Subquery selects max(i.unique2) from tenki, where i.unique1 = o.unique1

This is basically a really weird way to write a self-join.

For each row in o, select the max i.unique2 value that corresponds to it.

There are 10,000 rows in o, each will have exactly 1 match in i.

Return 10,000 rows in the result set.
</code></pre>
<p>Where am I getting this wrong?</p>
<p><strong>EDIT:</strong> The behavior is even stranger when you change the code around a little.</p>
<p>The SELECT seems to be equivalent to a join between tables <code>i</code> and <code>o</code>, but if you rewrite it as one:</p>
<pre><code>select
  (select max((select i.unique2 from tenk1 i join tenk1 o on i.unique1 = o.unique1)))
</code></pre>
<p>it errors out:</p>
<blockquote>
<p>ERROR:  more than one row returned by a subquery used as an expression</p>
</blockquote>
<p>But if you instead remove the <code>max</code> from the original query,</p>
<pre><code>select
  (select (select i.unique2 from tenk1 i where i.unique1 = o.unique1))
from tenk1 o;
</code></pre>
<p>you get a result set of 10,000 elements, as expected.  The database seems to have no trouble with a subquery returning more than one row here!  Remove the table <code>o</code> from that inexplicably valid query,</p>
<pre><code>select
  (select (select i.unique2 from tenk1 i))
</code></pre>
<p>and the &quot;more than one row&quot; error returns!</p>
<p>This is official PostgreSQL behavior, that the test suite requires the database to uphold.  The rule set forth by the error message says you can't have a subquery used as an expression that returns more than one row.  What it it about this strange not-quite-join to a table in an external scope that circumvents this rule?</p>

## Answers
### Answer ID: 78902787
<p>It is test for a regression.</p>
<p>Per <a href="https://git.postgresql.org/gitweb/?p=postgresql.git;a=blob;f=src/test/regress/sql/aggregates.sql;h=ca6d1bcfb7fa7fc3388833ca1bf8086ab7efc460;hb=HEAD" rel="nofollow noreferrer">aggregrate.sql</a>:</p>
<blockquote>
<p>-- Test handling of sublinks within outer-level aggregates.<br />
-- Per bug report from Daniel Grace.*</p>
</blockquote>
<p>Where bug report is <a href="https://www.postgresql.org/message-id/8a80df380904241703i3e2fb96bk380ab25657a5e6b1%40mail.gmail.com" rel="nofollow noreferrer">aggregate over subselects fails</a>:</p>
<blockquote>
<p>The following nonsensical query causes PostgreSQL to fail with ERROR: plan
should not reference subplan's variable.  (This was stripped down from an
'useful' query that triggered the same bug).  First encountered on 8.3.4,
reproduced on 8.3.7</p>
</blockquote>
<p>Patch is <a href="https://www.postgresql.org/message-id/20090425164503.269D37540A1@cvs.postgresql.org" rel="nofollow noreferrer">Aggregrate patch</a>:</p>
<blockquote>
<p>Fix the handling of sub-SELECTs appearing in the arguments of an outer-level
aggregate function.  By definition, such a sub-SELECT cannot reference any
variables of query levels between itself and the aggregate's semantic level
(else the aggregate would've been assigned to that lower level instead).
So the correct, most efficient implementation is to treat the sub-SELECT as
being a sub-select of that outer query level, not the level the aggregate
syntactically appears in.  Not doing so also confuses the heck out of our
parameter-passing logic, as illustrated in bug report from Daniel Grace.</p>
</blockquote>
<blockquote>
<p>Fortunately, we were already copying the whole Aggref expression up to the
outer query level, so all that's needed is to delay SS_process_sublinks
processing of the sub-SELECT until control returns to the outer level.</p>
</blockquote>
<blockquote>
<p>This has been broken since we introduced spec-compliant treatment of
outer aggregates in 7.4; so patch all the way back.</p>
</blockquote>
<p>With the aggregates.sql (r1.13.4.1 -&gt; r1.13.4.2) patch being:</p>
<pre><code>+ -- Test handling of sublinks within outer-level aggregates.
+ -- Per bug report from Daniel Grace.
+ select
+   (select max((select i.unique2 from tenk1 i where i.unique1 = o.unique1)))
+ from tenk1 o;
+ 
</code></pre>

### Answer ID: 78899713
<pre><code>select (select max(i.unique2) from tenk1 i where i.unique1 = o.unique1)
from tenk1 o
</code></pre>
<p>would do what you said, but the query doesn't do that. It does an inner</p>
<pre><code>select i.unique2 from tenk1 i where i.unique1 = o.unique1
</code></pre>
<p>(which is, as you say, a weird, even pointless, self-join, but this is a test case). That produces one row per row of the &quot;outer&quot; <code>tenk1</code>. Then it it uses <code>max</code> to get the single largest value of <code>unique2</code> that came out of the query (which is also the largest value in the table).</p>

