# How do I kill/abort/terminate/exit a running query when specific if condition is fullfilled?
[Link to question](https://stackoverflow.com/questions/66256507/how-do-i-kill-abort-terminate-exit-a-running-query-when-specific-if-condition-is)
**Creation Date:** 1613638099
**Score:** 0
**Tags:** sql, sql-server, t-sql
## Question Body
<p>I have a script in Msn SQL Server Management Studio 17 (I belive running a Msn SQL Server 14) that are supposed to create tables in a specific database. There are posibilities that some of the tables is not created. If that happens I have a if statement that checks for that. When the tables are created the script are supposed to do a print, go forward and keep running. This works fine. But, when the table is not created. I want the script to do a print, saying the tables is not created and then stop.</p>
<p>I've set it upp with an if statement like below. @sid is declared as int and given the value from @@spid. Since I can't copy my code from the environment due to security, I've rewritten it. So if there are some misspellings in code I say works above, it's because I've misspelled it in my rewriting because everything works exept for the query termination part. :)</p>
<pre><code>if object_id(@database + '.dbo.' + @table, 'U') is not null
begin
/* print and some actions, this works absolutely correct. */
end
else
begin
print 'Saying the table don't exists in the database.' --This works fine.
kill spid @sid --This doesn't work. I've also tried kill spid = @sid, kill @@spid, kill @sid, kill spid spid @@spid
end
</code></pre>
<p>How should I put this to get the print out and then exit the query?</p>

