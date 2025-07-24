# EF CORE 5 + MySql 5.7 group then select top 1 LINQ
[Link to question](https://stackoverflow.com/questions/77785793/ef-core-5-mysql-5-7-group-then-select-top-1-linq)
**Creation Date:** 1704793874
**Score:** 0
**Tags:** c#, entity-framework-core
## Question Body
<p>I'm using <strong>EF Core 5</strong> to rewrite some sql statements from an older system, My DataBase is <strong>MySql 5.7</strong>, here is a quite simple SQL query:</p>
<pre><code>SELECT 
    MAX(CreateTime) AS LatestRecordTime,MemberId,TotalAmount,CostAmount,BonusAmount
FROM 
    CashFlowRecord
WHERE 
    CreateTime &lt;= '2023-12-31'
    And TotalAmount&gt;0
GROUP BY 
    MemberId;
</code></pre>
<p>A <code>CashFlowRecord</code> table stores all the users' flow records, I just need to fetch the latest cash flow record for each member/ user, so using <code>MAX(CreateTime)</code> works well for me.</p>
<p><strong>Problem</strong>: how to properly rewrite this sql query to EF core LINQ query? Notion: I'm using <strong>MySql 5.7</strong> so the window function like <strong>row_number()</strong> is not supported and I can not upgrade the mysql to 8.0.
First I tried this:</p>
<pre><code>var qry = DbContext.Set&lt;CashFlowRecord&gt;()
        .WHERE(t=&gt;t.CreateTime &lt;= '2023-12-31' &amp;&amp; t.TotalAmount &gt; 0)
        .GroupBy(t =&gt; t.MemberId)
        .Select(t=&gt;new { MemId = t.Key, Latest = t.OrderByDescending(e=&gt;e.CreateTime).First()});

var lst = (await qry.ToDictionaryAsync(t =&gt; t.MemId, t =&gt; t.Latest)).Select(t=&gt;t.Value).ToList(); 
</code></pre>
<p>A <strong>MySql.Data.MySqlClient.MySqlException</strong> exception thrown because MySql 5.7 has no Row_Number() function but the EF translate the <code>.OrderByDescending(t=&gt; t.CreateTime).Take(1) </code> to Row_Number().</p>
<p>The Error Message:
<strong>You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '(PARTITION BY <code>c0</code>.<code>MemberId</code> ORDER BY <code>c0</code>.<code>CreateTime</code> DESC) AS <code>row</code></strong></p>
<p><strong>I dont konw how to fix this issue, I got no idea and I could not upgrade either one.</strong></p>
<hr />
<p>updated: there seems no better solutions for this issue than using <code>FromSqlRaw</code>. So I suggest upgrading MySql and EF core at the same time.</p>

