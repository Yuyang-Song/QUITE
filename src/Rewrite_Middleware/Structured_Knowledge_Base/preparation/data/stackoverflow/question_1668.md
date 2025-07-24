# SQL - Getting the max effective date less than a date in another table
[Link to question](https://stackoverflow.com/questions/3284885/sql-getting-the-max-effective-date-less-than-a-date-in-another-table)
**Creation Date:** 1279571948
**Score:** 1
**Tags:** sql
## Question Body
<p>I'm currently working on a conversion script to transfer a bunch of old data out of an SQL Server 2000 database and onto a SQL Server 2008.  One of thing things I'm trying to accomplish during this conversion is to eliminate all of the composite keys and replace them with a "proper" primary key.  Obviously, when I transfer the data I need to inject the foreign key values into the new table structures.</p>

<p>I'm currently stuck with one data set though and I can't seem to get my head around it in a set-based fashion.  The two tables with which I am working are called Charge and Law.  They have a 1:1 relationship and "link" on three columns.  The first two are an equal link on the LawSource and LawStatue columns, but the third column is causing me problems.  The ChargeDate column should link to the LawDate column where LawDate &lt;= ChargeDate.</p>

<p>My current query is returning more than one row (in some cases) for a given Charge because the Law may have more than one LawDate that is less than or equal to the ChargeDate.</p>

<p>Here's what I currently have:</p>

<pre><code>select LawId
from Law a
join Charge b on b.LawSource = a.LawSource 
                 and b.LawStatute = a.LawStatute 
                 and b.ChargeDate &gt;= a.LawDate
</code></pre>

<p>Any way I can rewrite this to get the most recent entry in the Law table that is the same (or earlier) date at the ChargeDate?</p>

## Answers
### Answer ID: 3285094
<p>This would be easier in SQL 2008 with the partitioning functions (so, it should be easier in the future for you).</p>

<p>The usual caveats of "I don't have your schema, so this isn't tested" apply, but I think it should do what you need.</p>

<pre><code>select
  l.LawID
from
  law l
  join (
    select 
      a.LawSource,
      a.LawStatue,
      max(a.LawDate) LawDate
    from 
      Law a
      join Charge b on b.LawSource = a.LawSource 
                     and b.LawStatute = a.LawStatute 
                     and b.ChargeDate &gt;= a.LawDate
    group by
      a.LawSource, a.LawStatue
  ) d on l.LawSource = d.LawSource and l.LawStatue = d.LawStatue and l.LawDate = d.LawDate
</code></pre>

### Answer ID: 3285090
<p>If performance is not an issue, <code>cross apply</code> provides a very readable way:</p>

<pre><code>select  *
from    Law l
cross apply
        (
        select  top 1 *
        from    Charge
        where   LawSource = l.LawSource 
                and LawStatute = l.LawStatute 
                and ChargeDate &gt;= l.LawDate
        order by
                ChargeDate
        ) c
</code></pre>

<p>For each row, this looks up the row in the Charge table with the smallest ChargeDate.</p>

<p>To include rows from <code>Law</code> without a matching <code>Charge</code>, change <code>cross apply</code> to <code>outer apply</code>.</p>

