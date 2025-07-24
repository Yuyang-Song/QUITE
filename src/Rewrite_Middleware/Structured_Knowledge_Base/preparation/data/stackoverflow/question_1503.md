# How to migrate and process queries (not just tables) in SQL Server instead of Access?
[Link to question](https://stackoverflow.com/questions/79186625/how-to-migrate-and-process-queries-not-just-tables-in-sql-server-instead-of-ac)
**Creation Date:** 1731530904
**Score:** 0
**Tags:** sql-server, ms-access, database-migration
## Question Body
<p>My aging Access 2010 database is quite slow and unstable now. All tables, queries and forms were stored in Access, and it can't handle the load of my department (20+ users). I thought of using SQL Server as a back-end, and migrated the database using Migration Assistant.</p>
<p>Now, my tables are linked and stored in the SQL Server, but when using the forms in Access as front end, the queries take much longer to load than before. (I assume since queries are still executed in Access, plus network connection latency to take data from tables)</p>
<p>Is there an easy/automated way to move queries to SQL Server so that forms in Access use them, and the actual processing is done by SQL Server so that the front end just receives the final data? Would that reduce my overall query and processing times?</p>
<p>Tried migrating data from Access to SQL Server to reduce loading times and instability. Querying now takes even longer since queries are still processed in Access instead of SQL Server. Queries are too many, and complex to rewrite in SQL Server easily.</p>

## Answers
### Answer ID: 79187105
<p>The general solution in near all cases is to simply take the existing query, and paste it into SQL (SSMS). Get the query working.</p>
<p>You then create a new SQL server view, and paste in that now working SQL. You then save the view with the same name as the client side query. Now, link the view from Access, and give it the same name as what the existing query was.</p>
<p>The above will thus result in great performance.</p>
<p>Of course, you want to adopt a hospital like triage approach here. In other words, you don't need to convert all such queries, but attack the most used and slow queries that are used most often.</p>
<p>Also, for a form that edits data, you can continue to keep the form bound to a table (now a linked table), and converting such forms to use a linked view when such forms are based on one table will not help performance.</p>
<p>In fact, any linked query or linked view based on a single table tends to NOT see performance improvements anyway. Only those client-side queries that involve multiple tables and joins need be converted to server-side SQL views.</p>
<p>Also, keep in mind the following:</p>
<pre><code>docmd.OpenForm &quot;frmInvoices&quot;,,,&quot;InvoiceNum = 134343&quot;
</code></pre>
<p>In the above, Access is smart, and will ONLY pull the one record down the network pipe. This includes when the form is bound directly to a linked table.</p>
<p>However, if you are opening forms without a where clause, then that's the issue and problem in the first place. In other words, if your designs from day 1 don't try to limit data pulled into a form (or report), then using SQL server not going to help you. As noted, in above, that invoice table can have 1 million rows, and EVEN with a form bound to a linked table, then ONLY one record travels down the network pipe.</p>
<p>In other words, most queries don't pull all the data down to access, but will ONLY pull what you tell it to pull from SQL server.</p>
<p>If your forms don't restrict data pulled from the table, then of course some view, a pass-though query, and even a using SQL stored procedures WILL HELP ZERO for performance!</p>
<p>So, it is a general urban myth that Access pulls all the data from SQL server. It does not, and in fact in most cases pulls only what the developer told Access to pull in the first place!</p>
<p>In other words, good performance is that of having good designs. So, one should avoid at all costs to open a form bound directly to some linked table without a where clause.  However, as noted, even existing forms bound to a linked table on SQL server will ONLY pull the rows you tell the form to pull. This of course assumes you ARE telling that form to ONLY pull the data that the user requires (and you do this by using the &quot;where&quot; clause of the openform command from VBA).</p>
<p>So, the low hanging fruit should be to address the slowest queries, and 9 out of 10 times, such queries are complex queries, and ones with multiple table joins. So, those are the first areas you can deal with in terms of fixing performance. And as noted, create a view with the same name as the current client-side query, and then link to that view (you have to delete or often just re-name the existing client-side query).</p>
<p>As noted, simple client side queries that involve only one table in general will not benefit from the above advice, and hence you can same time by not spending efforts to convert &quot;any&quot; and &quot;all&quot; queries you have now to views, but only thus convert queries that are running slow, and are most often used.</p>

