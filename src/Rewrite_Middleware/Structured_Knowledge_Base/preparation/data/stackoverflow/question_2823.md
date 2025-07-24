# Handle nested SQL statements in SQL Server
[Link to question](https://stackoverflow.com/questions/53993788/handle-nested-sql-statements-in-sql-server)
**Creation Date:** 1546327926
**Score:** 1
**Tags:** sql, sql-server, sql-server-2014, database-administration, sqlperformance
## Question Body
<p>My procedure has large query syntax, many "nested if else" when I create it on one SQL Server I get this error:</p>

<blockquote>
  <p>Some part of your SQL statement is nested too deeply. Rewrite the query or break it up into smaller queries.</p>
</blockquote>

<p>but when I create that on another server, it is created without error. I know the procedure has poor performance but why that is created correctly on another server</p>

<p>Does it depend on server config or database feature ?</p>

## Answers
### Answer ID: 53993808
<p><strong>when i create that on another server,that is created without error</strong></p>

<p>Reason is that the two version is not same . I think you 1st server is older than 2012sp1 that's why you got that error. you can check this <a href="https://support.microsoft.com/en-us/help/2958429/bugs-that-are-fixed-in-sql-server-2012-service-pack-2" rel="nofollow noreferrer">link</a></p>

