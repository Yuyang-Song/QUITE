# T-SQL 2000 to 2008
[Link to question](https://stackoverflow.com/questions/5208956/t-sql-2000-to-2008)
**Creation Date:** 1299390332
**Score:** 0
**Tags:** t-sql
## Question Body
<p>I have around 200-250 reports that have been developed in SQL Server 2000 and I have used <code>*=</code> , <code>=*</code> in many places. So recently we migrated to SQL Server 2008 and all reports have to be fixed for the 2008 standard.</p>

<p>So I have couple of issue in compatibility like </p>

<blockquote>
  <p>"The query uses non-ANSI outer join
  operators (<code>*=</code> or<code>=*</code>). To run this
  query without modification, please set
  the compatibility level for current
  database to 80, using the SET
  COMPATIBILITY_LEVEL option of ALTER
  DATABASE. It is strongly recommended
  to rewrite the query using ANSI outer
  join operators (LEFT OUTER JOIN, RIGHT
  OUTER JOIN). In the future versions of
  SQL Server, non-ANSI join operators
  will not be supported even in
  backward-compatibility modes."</p>
</blockquote>

<p>So it takes long time to re-query all things and fixing. Even we don't need to enable backward compatibility of 2008, we do need to fix all those queries...</p>

<p>Is there any tool that will fix all those queries easily?</p>

<p>Thanks and Best Regards,</p>

## Answers
### Answer ID: 7959068
<p>There is a tool built into SSMS that can help, but you will still need to test. See my post on SSC which describes the technique:</p>

<p><a href="http://www.sqlservercentral.com/Forums/FindPost1098339.aspx" rel="nofollow">http://www.sqlservercentral.com/Forums/FindPost1098339.aspx</a></p>

### Answer ID: 5209501
<p>There is no tool. How can any tool know what the semantics would be of this, for example?</p>

<p>You are changing</p>

<pre><code>FROM Table1 T1, Table2 T2, Table2 T3
WHERE T1.key *= T2.key AND T1.key = T3.key AND T3.foo = 'bar'
</code></pre>

<p>to</p>

<pre><code>FROM
   Table T1
   JOIN
   Table T3 ON T1.key = T3.key
   LEFT JOIN
   Table T2 ON T1.key = T3.key
WHERE
    T3.foo = 'bar'
</code></pre>

<p>You have been able to use JOIN/LEFT JOIN etc since at least SQL Server 6.5: using <code>*=</code> for SQL Server 2000 was ignorance and/or laziness</p>

### Answer ID: 5208973
<p>The <a href="http://www.microsoft.com/downloads/en/details.aspx?FamilyID=f5a6c5e9-4cd9-4e42-a21c-7291e7f0f852&amp;displaylang=en" rel="nofollow">Microsoft SQL Server 2008 Upgrade Advisor</a> should identify the offending TSQL, but it won't fix it for you.</p>

<p>It is a prudent idea to run the SQL Server 2008 Upgrade Advisor on all Databases to be upgraded.</p>

