# SQL Server EnumParameters Method on StoredProcedure object in SQL Server 2008 SQL-DMO
[Link to question](https://stackoverflow.com/questions/1876251/sql-server-enumparameters-method-on-storedprocedure-object-in-sql-server-2008-sq)
**Creation Date:** 1260387135
**Score:** 0
**Tags:** sql, sql-server, sqldmo
## Question Body
<p>Hello all you wonderfully helpful people,</p>

<p>What is the alternative to EnumParameters in SQL Server 2008? This MSDN article mentions that this method is going away, so what should be used instead?</p>

<p><a href="http://msdn.microsoft.com/en-us/library/ms133474(SQL.90).aspx" rel="nofollow noreferrer">http://msdn.microsoft.com/en-us/library/ms133474(SQL.90).aspx</a></p>

<p>Here is the error we receive when attempting to use this method:</p>

<blockquote>
  <p>Microsoft SQL-DMO (ODBC SQLState:
  42000) error '800a1033'</p>
  
  <p>[Microsoft][ODBC SQL Server
  Driver][SQL Server]The query uses
  non-ANSI outer join operators ("<em>=" or
  "=</em>"). To run this query without
  modification, please set the
  compatibility level for current
  database to 80, using the SET
  COMPATIBILITY_LEVEL option of ALTER
  DATABASE. It is strongly recommended
  to rewrite the query using ANSI outer
  join operators (LEFT OUTER JOIN, RIGHT
  OUTER JOIN). In the future versions of
  SQL Server, non-ANSI join operators
  will not be supported even in
  backward-compatibility modes.</p>
</blockquote>

<p>Thanks!</p>

<p>Paul</p>

## Answers
### Answer ID: 1876324
<p>Not only this method, but everything DMO that is deprecated since 2005. Use <a href="http://msdn.microsoft.com/en-us/library/ms162169.aspx" rel="nofollow noreferrer">SMO</a> instead:<a href="http://msdn.microsoft.com/en-us/library/microsoft.sqlserver.management.smo.storedprocedure.parameters.aspx" rel="nofollow noreferrer">StoredProcedure.Parameters</a>.</p>

### Answer ID: 1876294
<p>Swap from using DMO to SMO, the object model exposes the stored procedure parameter collection.</p>

<p><a href="http://msdn.microsoft.com/en-us/library/ms162209(SQL.90).aspx" rel="nofollow noreferrer">http://msdn.microsoft.com/en-us/library/ms162209(SQL.90).aspx</a></p>

