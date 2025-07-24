# Group by clientId and date in SQL
[Link to question](https://stackoverflow.com/questions/67354678/group-by-clientid-and-date-in-sql)
**Creation Date:** 1619946973
**Score:** -1
**Tags:** sql, sql-server
## Question Body
<p>I have the following table:</p>
<p><a href="https://i.sstatic.net/VOG9H.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/VOG9H.png" alt="Table" /></a></p>
<p>I want to do groupBy date and by specific client where <code>IsDeleted = 0</code>.</p>
<p>More precisely, I want to do this:</p>
<p><a href="https://i.sstatic.net/sfaLa.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/sfaLa.png" alt="Result" /></a></p>
<p>Data in this screenshot doesn't reflect data in the table.</p>
<p>So, for example, client Anne Marie is ClientId = 12 in my database.</p>
<p>I need to group by for each month and then another group by? I mean, I can have multiple records in one month..</p>
<p>I hope I posted clear question, if not, please write to put more details on.</p>
<p>Update:</p>
<p>I need something like this:</p>
<pre><code>select 
    Convert([date], [Date]) as [Date], 
    TotalAttendants as Total,
    FemaleAttendants as Women, 
    MaleAttendants
from
    dbo.Events
where 
    EventTypeId = 1 
    and IsDeleted = 0
group by 
    Convert([date], date)
order by 
    Convert([date], date)
</code></pre>
<p>Only I need to wrap those dates into Months (T-SQL or something similar).</p>
<p>At the, end I need to rewrite this query to linq for C#</p>

## Answers
### Answer ID: 67354890
<p>It appears, from your example picture of desired output, you just need to use the <code>sum</code> aggregate function and group by the <code>date</code> in each case, however it's not clear what you mean by &quot;another group by&quot;, so clarify if you need to.</p>
<pre><code>select concat(Left(DateName(month,[date]),3), ' ', Year([date])), 
    sum(TotalAttendants) as Total,
    Sum(FemaleAttemdants) as Women,
    Sum(MaleAttendants) as Men
from table
where IsDeleted=0
group by concat(Left(DateName(month,[date]),3), ' ', Year([date]))
</code></pre>

