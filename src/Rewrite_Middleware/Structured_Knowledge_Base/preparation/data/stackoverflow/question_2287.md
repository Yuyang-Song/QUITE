# SQL Server 2008 Error 4147 when querying a view, but not when executing the content of the view
[Link to question](https://stackoverflow.com/questions/27776772/sql-server-2008-error-4147-when-querying-a-view-but-not-when-executing-the-cont)
**Creation Date:** 1420450782
**Score:** 2
**Tags:** sql-server-2008
## Question Body
<p><strong>In summary, I can't figure out why a Select on a View will give an error, but not when executing the View's Select statement itself.</strong></p>

<p>When I run the query below:</p>

<pre><code>SELECT * 
  FROM vAccountBalance
</code></pre>

<p>I get the following error:</p>

<p><em>Msg 4147, Level 15, State 1, Procedure vAccountBalance, Line 13
The query uses non-ANSI outer join operators ("</em>=" or "=<em>"). To run this query without modification, please set the compatibility level for current database to 80, using the SET COMPATIBILITY_LEVEL option of ALTER DATABASE. It is strongly recommended to rewrite the query using ANSI outer join operators (LEFT OUTER JOIN, RIGHT OUTER JOIN). In the future versions of SQL Server, non-ANSI join operators will not be supported even in backward-compatibility modes.
Msg 4413, Level 16, State 1, Line 2
Could not use view or function 'vAccountBalance' because of binding errors.</em></p>

<p>When I execute vAccountBalance's Select statement (below), it executes without error.
Also, the statement below does not contain non-ANSI operators (* = or = *) that the error and most solutions refer to.  Compatibility level is set to 100.</p>

<pre><code>SELECT T1.ACCOUNTCODE, 
COALESCE (T2.CreditTotal, 0) AS CreditTotal, 
COALESCE (T3.DebitTotal, 0) AS DebitTotal, 
COALESCE (T2.CreditTotal, 0) - COALESCE (T3.DebitTotal, 0) AS AccountBalance
FROM dbo.ACCOUNT AS T1         
LEFT OUTER JOIN dbo.vCreditTotals AS T2 ON T1.ACCOUNTCODE = T2.Account 
LEFT OUTER JOIN dbo.vDebitTotals AS T3 ON T1.ACCOUNTCODE = T3.Account
</code></pre>

## Answers
### Answer ID: 27814213
<p>The issue relates to the option used to view the content of the View.</p>

<p>When using "Design" (as I did) to see the View's statement, the non-ANSI operators (* =) are automatically converted to the LEFT OUTER JOIN format.</p>

<p>When using "Script View as > Alter to > New Query Editor Window" to see the View's statement, the non-ANSI operator (* =) is displayed.</p>

<p>When executing the View it gave an error, since the View does contain a non-ANSI operator.</p>

<p>When executing the content of the View after opening it by using "Design", it does not give an error since the Non-ANSI operator has been converted.</p>

### Answer ID: 27776944
<p>Try executing <code>sp_refreshview 'vAccountBalance'</code> and then running the SELECT on view.</p>

