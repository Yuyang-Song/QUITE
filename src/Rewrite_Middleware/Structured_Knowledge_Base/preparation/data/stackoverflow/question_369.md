# Doing a join across two databases with different collations on SQL Server and getting an error
[Link to question](https://stackoverflow.com/questions/2290753/doing-a-join-across-two-databases-with-different-collations-on-sql-server-and-ge)
**Creation Date:** 1266514406
**Score:** 69
**Tags:** sql-server, t-sql, collation
## Question Body
<p>I know, I know with what I wrote in the question I shouldn't be surprised.  But my situation is slowly working on an inherited POS system and my predecessor apparently wasn't aware of JOINs so when I looked into one of the internal pages that loads for 60 seconds I see that it's a fairly quick, rewrite these 8 queries as one query with JOINs situation.  Problem is that besides not knowing about JOINs he also seems to have had a fetish for multiple databases and surprise, surprise they use different collations.  Fact of the matter is we use all "normal" latin characters that English speaking people would consider the entire alphabet and this whole thing will be out of use in a few months so a bandaid is all I need.</p>

<p>Long story short is I need some kind of method to cast to a single collation so I can compare two fields from two databases.</p>

<p>Exact error is:</p>

<blockquote>
  <p>Cannot resolve the collation conflict
  between
  "SQL_Latin1_General_CP850_CI_AI" and
  "SQL_Latin1_General_CP1_CI_AS" in the
  equal to operation.</p>
</blockquote>

## Answers
### Answer ID: 2291116
<p>A general purpose way is to coerce the collation to DATABASE_DEFAULT. This removes hardcoding the collation name which could change.</p>

<p>It's also useful for temp table and table variables, and where you may not know the server collation (eg you are a vendor placing your system on the customer's server)</p>

<pre><code>select
    sone_field collate DATABASE_DEFAULT
from
    table_1
    inner join
    table_2 on table_1.field collate DATABASE_DEFAULT = table_2.field
where whatever
</code></pre>

### Answer ID: 2290796
<p>You can use the collate clause in a query (I can't find my example right now, so my syntax is probably wrong - I hope it points you in the right direction)</p>

<pre><code>select sone_field collate SQL_Latin1_General_CP850_CI_AI
  from table_1
    inner join table_2
      on (table_1.field collate SQL_Latin1_General_CP850_CI_AI = table_2.field)
  where whatever
</code></pre>

