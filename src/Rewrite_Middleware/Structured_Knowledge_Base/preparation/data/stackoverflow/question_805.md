# Linked Server strangeness - Performance from Joins
[Link to question](https://stackoverflow.com/questions/43265338/linked-server-strangeness-performance-from-joins)
**Creation Date:** 1491511133
**Score:** 0
**Tags:** sql-server, join, linked-server
## Question Body
<p>I have an odd situation.  We have an AS400 with a Prod side and a Dev side (same machine, 2 nic cards)  From a production SQL Server, we run a query from a MS-SQL server that is using a linked Server, I'll call 'as400'   The query does 3 joins, and the execution plan looks roughly like [Remote Query] => Got Results.   It does the joins on the remote server (the Production AS400)   This will execute in no more than 0:00:02   (2 seconds)  One of the joined tables has 391 MILLION rows.  It is pulling 100 rows - joined to the other table.</p>

<p>Now, it gets weird.   On the Dev side of the same machine, running on a different SQL Server, coming in the other NIC card, executing the same query with a different database (the dev one) the execution plan is quite different!  It is:</p>

<p>[Query 1]  hash match (inner join) with [Query2]  Hash with [Query3] Hash with [Query4]</p>

<p>Expecting that each query returns 10,000 rows (I'm sure it is just using that as a guess as it doesn't know the actual rows as it is remote).   What it appears to be doing is pulling 391 million rows back on query2 and it takes > 23 HOURS before I give up and kill the query.  (Running in SSMS)</p>

<p>Clearly, the MS SQL Server is making the decision to not pass this off to the AS400 as a single query.  Why?</p>

<p>I can 'solve' the problem by using a OpenQuery (as400, cmd) instead, but then it will open us up to SQL Injection, can't do simple syntax checking on the query, and other things I don't like.  It takes 6 seconds to do the query using OpenQuery, and returns the correct data.</p>

<p>If we solve this by rewriting all our (working, fast) queries that we use in production so they can also run against dev - it involves a LOT of effort and there is down-side to it in actual production.</p>

<p>I tried using the 'remote' hint on the join, but that isn't supported by the AS400 :-(</p>

<p>Tried looking at the configuration/versions of the SQL Servers and that didn't seem to offer a clue either.  (SQL Servers are nearly the same version/are same, 10.50.6000 for the one that works, and 10.50.6220 for one that fails (newer), and also 10.50.6000 for the other one that is failing.)</p>

<p>Any clues anyone?  Would like to figure this out, we have had several people looking at this for a couple of weeks - including the Database Architect and the IBM AS400 guru, and me. (So far, my OpenQuery is the only thing that has worked)</p>

<p>One other point, the MS Servers seem to be opening connections 5 per second to the AS400 from the machines that are not working (while the query runs for 23 hours) - I don't understand that, and I'm not 100% sure it is related to this issue, but it was brought up by the AS400 guy.</p>

## Answers
### Answer ID: 43268537
<p>Without seeing the queries and execution plans it sounds like this is a problem with permissions when accessing statistics on the remote server. For the query engine to make use of all available statistics and build a plan properly, make sure the db user that is used to connect to the linked server is one of the following on the linked server:</p>

<ol>
<li>The owner of the table(s).</li>
<li>A member of the sysadmin fixed SERVER role.</li>
<li>A member of the db_owner fixed DATABASE role.</li>
<li>A member of the db_ddladmin fixed DATABASE role.</li>
</ol>

<p>To check what db user you're using to connect to the linked server use Object Explorer...</p>

<p>Expand the Server\Instance > Server Objects > Linked Servers > right click your linked server and select properties, then go to the Security page. </p>

<p>If you're not mapping logins in the top section (which I wouldn't suggest) then select the last radio button at the bottom to make connections using a specific security context and enter the username and password for the appropriate db user. Rather than using 'sa' create a new db user on the linked server that is #2 or #3 from above and use that. Then every time the linked server is used it will connect with the necessary permissions.</p>

<p>Check the below article for more detail. Hope this helps!</p>

<p><a href="http://www.benjaminnevarez.com/2011/05/optimizer-statistics-on-linked-servers/" rel="nofollow noreferrer">http://www.benjaminnevarez.com/2011/05/optimizer-statistics-on-linked-servers/</a></p>

### Answer ID: 43265494
<p>I despise linked servers for this reason (among many others). I have always had good luck with openquery() and using sp_executesql to help prevent SQL injection.</p>

<p>There is mention of this here:  <a href="https://stackoverflow.com/questions/3378496/including-parameters-in-openquery">including parameters in OPENQUERY</a></p>

