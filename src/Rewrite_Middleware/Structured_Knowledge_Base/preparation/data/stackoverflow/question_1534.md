# Is it better to use stored procedures instead of SQL statements in a C application?
[Link to question](https://stackoverflow.com/questions/8745732/is-it-better-to-use-stored-procedures-instead-of-sql-statements-in-a-c-applicati)
**Creation Date:** 1325779878
**Score:** 4
**Tags:** sql, c, sql-server, t-sql
## Question Body
<p>I'm developing an application which queries data from the host, and then inserts them into an SQL database. My application runs in random times on our PC's ( we have 600-700 PCs ) from a server location, so my application isn't located at all PC. It is only located at the server. So it is possible that sometimes it runs on 50 PCs. </p>

<p>I keep getting two types of SQL error messages. The first is time out, and the other is SSL security error. Right now my application executes about 5-10 SQL commands. So i'm thinking to rewrite my code to call stored procedures which could reduce the number of SQL calls. The only question is that is it worth it? I mean of course, it has its advantages, because if i have to change something then it is enough to change the stored procedure, and i don't have to recompile my application. But won't that cause trouble for the SQL server? I mean isn't that a problem when the same stored procedure will be executed 50 times at the same time?</p>

<p>So what way is better? Using stored procedures, or using SQL commands in my code?</p>

<p>Thanks!</p>

## Answers
### Answer ID: 8745806
<p>If you often call several identical SQL statements in a row, the answer is clear-cut: use SPs to reduce the number of round trips. The load on your SQL server is not going to change, but the network latency will go down due to reduced number of round-trips. As an added bonus, your system architecture <em>may</em> become easier to understand and maintain, because the complex SQL logic would be encapsulated in your data access layer.</p>

<p>This may not have anything to do with your SSL errors, but the situation with timeouts has a decent <em>chance</em> of improving.</p>

