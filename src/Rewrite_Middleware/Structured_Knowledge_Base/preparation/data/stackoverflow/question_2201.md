# two servers, unlinked, with sub select involving both
[Link to question](https://stackoverflow.com/questions/23408636/two-servers-unlinked-with-sub-select-involving-both)
**Creation Date:** 1398950742
**Score:** 0
**Tags:** sql, sql-server-2008, vb6
## Question Body
<p>We have two database servers, db1 and db2, unlinked. I cannot link them.</p>

<p>I have a query that goes something like:</p>

<pre><code>    SELECT name, modify_date
    FROM sys.objects
    where col = value and datecol &gt;= datevalue and
          not exists(select ObjectName
                     from table2
                     where ObjectName = sys.objects.name and
                           DateTime &gt; sys.objects.modify_date and
                           ObjectType = Type
                    )
    order by xxxx
</code></pre>

<p>Originally that would work just fine because we were looking at DB1 for changes. Now that I'm modifying the program to look at the two database servers for new objects created, the table on DB1 does not exist on DB2, and I need to find a way to rewrite the query in some way that will allow me to retrieve the info from the table on DB1, and then use it in a comparison on db2.</p>

<p>I've been trying to something like         </p>

<pre><code>    SELECT name, modify_date
    FROM sys.objects
    where col = value and datecol &gt;= datevalue and
          not exists('Value1', 'Value2', 'Value3')
    order by xxxx
</code></pre>

<p>So that I can just return the sub query, build a string, and drop it back in. However, the syntax to do the SQL portion is eluding me. I would prefer to stay away from "col &lt;> 'value1' and col &lt;> 'value2' and col &lt;> 'value3'.</p>

<p>Does anyone have any suggestions?</p>

<p>Using SQL Server 2008 and modifying an old vb6 application that is not ready for a rewrite into .net yet..</p>

## Answers
### Answer ID: 23408715
<p>The correct syntax is <code>not in</code>:</p>

<pre><code>SELECT name, modify_date
FROM sys.objects
where col = value and datecol &gt;= datevalue and
      col not in ('Value1', 'Value2', 'Value3')
order by xxxx;
</code></pre>

