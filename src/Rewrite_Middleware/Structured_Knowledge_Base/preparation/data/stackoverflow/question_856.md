# The &quot;*&quot; is not working in SQL Server 2016
[Link to question](https://stackoverflow.com/questions/46138316/the-is-not-working-in-sql-server-2016)
**Creation Date:** 1505028554
**Score:** 1
**Tags:** sql, sql-server, join
## Question Body
<p>I have a SQL query written in SQL Server version 2000. The query is not running in SQL Server 2016. The query is like below.</p>

<pre><code>Select *
from ProjPace2 P, ProjPace2 P2
where P.DivCode *= P2.DivCode
  and P.ProjGrp *= P2.ProjGrp
  and P.ProjYr *= P2.ProjYr
  and P.T_D *= P2.T_D
  and P.Qtr *= P2.Qtr
  and P.SRA_LRA *= P2.SRA_LRA
  and P.District *= P2.District
  and P.PICompany *= P2.PICompany
  and P.ContCode *= P2.ContCode
  and P.dtWkEnding &gt; dateadd(dd,-1,'1/1/2015')
  and P2.dtWkEnding between dateadd(dd,-10,'1/1/2015') and dateadd(dd,-3,'1/1/2015')
</code></pre>

<p>I am getting the following error:</p>

<blockquote>
  <p>Msg 4147, Level 15, State 1, Line 20<br>
  The query uses non-ANSI outer join operators ("&ast;=" or "=&ast;"). To run this query without modification, please set the compatibility level for current database to 80, using the SET COMPATIBILITY_LEVEL option of ALTER DATABASE. It is strongly recommended to rewrite the query using ANSI outer join operators (LEFT OUTER JOIN, RIGHT OUTER JOIN). In the future versions of SQL Server, non-ANSI join operators will not be supported even in backward-compatibility modes.</p>
</blockquote>

<p>I can understand the error is occurring due to "*" and I want to replace it with Left outer join so I can get the same result.</p>

<p>Any help will be thankfully accepted.</p>

<p>Partha </p>

## Answers
### Answer ID: 46138813
<p>All conditions that are specified with <code>*=</code> operator denote <code>ON</code> clause for <code>LEFT OUTER JOIN.</code> So equivalent query would become:</p>

<pre><code>Select *
from ProjPace2 P
  left outer join ProjPace2 P2 on 
    P.DivCode = P2.DivCode
    and P.ProjGrp = P2.ProjGrp
    and P.ProjYr = P2.ProjYr
    and P.T_D = P2.T_D
    and P.Qtr = P2.Qtr
    and P.SRA_LRA = P2.SRA_LRA
    and P.District = P2.District
    and P.PICompany = P2.PICompany
    and P.ContCode = P2.ContCode
where P.dtWkEnding &gt; dateadd(dd,-1,'1/1/2015')
  and P2.dtWkEnding between dateadd(dd,-10,'1/1/2015') and dateadd(dd,-3,'1/1/2015')
</code></pre>

<p>One note though: Since you have condition where returned rows must have <code>P2.dtWkEnding between dateadd(dd,-10,'1/1/2015') and dateadd(dd,-3,'1/1/2015')</code> there is no need for <code>LEFT OUTER JOIN</code> since rows without matching <code>P2</code> record will never be returned. So for this query you should use <code>INNER JOIN</code>.</p>

