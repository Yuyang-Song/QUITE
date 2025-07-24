# How can I capture SQL Query that is hitting my SQL database?
[Link to question](https://stackoverflow.com/questions/43002128/how-can-i-capture-sql-query-that-is-hitting-my-sql-database)
**Creation Date:** 1490365818
**Score:** 0
**Tags:** visual-studio-2012, sql-server-2012
## Question Body
<p>I've recently lost all files on a web project that contained over 200 reports written in Visual Studio.  The internal web server is still running the reports that were published but I cannot make any changes now that the project files are gone.  In an effort to save time and not have to rewrite all of the queries I'd like to know if there is a way to capture the queries as they hit my database.
Thanks in advance.</p>

## Answers
### Answer ID: 43002305
<p>If you have Sql Server Management Studio, then you can simply go to Tools --> Sql Server Profiler.  Connect to your Database Instance, and it will begin showing you all the activity between your DB and anything that is interacting with it.  </p>

<p><a href="https://learn.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms" rel="nofollow noreferrer">https://learn.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms</a></p>

<p>Hope this helps.  </p>

