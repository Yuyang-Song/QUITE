# Inserting large number of records into SQL Server
[Link to question](https://stackoverflow.com/questions/48263205/inserting-large-number-of-records-into-sql-server)
**Creation Date:** 1516019876
**Score:** 0
**Tags:** batch-file, sql-server-2014, multiple-records
## Question Body
<p>I have a very large number of records that must be inserted into a SQL Server database. It is about 1 million record that must be inserted. </p>

<p>I do so by running this simple bat script: </p>

<pre><code>ECHO %TIME%
sqlcmd -S "SQLSERVER" -i "C:\Users\name\Desktop\OutPut\Result 
tblAccount.sql"
ECHO %TIME%
Pause
</code></pre>

<p>But once I run the script I get the following error: </p>

<blockquote>
  <p>some part of your SQL statement is nested too deeply. Rewrite the query or break it up into smaller queries</p>
</blockquote>

<p>Is there any solution to how to insert that many records?</p>

<p>I have SQL Server 2014 Developer edition. </p>

<p>Edit the question by adding the query I'm running </p>

<pre><code>IF NOT EXISTS (SELECT * FROM [dbo].[tblAccount] 
               WHERE [AccountID] = 117242 
                 AND [TimeStamp] = CAST(N'2013-01-16 05:53:50.490' AS DateTime)) 
BEGIN
    INSERT INTO [dbo].[tblAccount] ([AccountID], [Name], [Comment],[IsMachine],
                                    [UserID], [Prefix], [Action], [Initials],
                                    [Name], [TimeStamp], [Reason], [Iscal]) 
    VALUES (117242, 'blabla', 'The users project)', 1, 
            'val', 39, 'val', 'blabla',
            'blabla', CAST(N'2013-01-16 05:53:50.490' AS DateTime), 'NORMAL', '0')
END
</code></pre>

## Answers
### Answer ID: 48264907
<p>It seems this is related to a bug in 2012 (fixed in SP2) and 2014 (fixed in SP1) according to this connect item, 
<a href="https://connect.microsoft.com/sqlserver/feedback/details/805659/sql-statement-is-nested-too-deeply" rel="nofollow noreferrer">https://connect.microsoft.com/sqlserver/feedback/details/805659/sql-statement-is-nested-too-deeply</a> -</p>

