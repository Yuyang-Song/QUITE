# Using text SQL with LINQ
[Link to question](https://stackoverflow.com/questions/13249220/using-text-sql-with-linq)
**Creation Date:** 1352198292
**Score:** 10
**Tags:** c#, sql, sql-server, linq, linq-to-sql
## Question Body
<p>I'm currently having issues with using LINQ to SQL for my project. This is because most of the lengthy SQL queries (or <em>views</em>, rather) are hard-coded into C#, and what we've been doing all along is to use <code>context.Database.SqlQuery&lt;ClassName&gt;(sql, sqlParams)</code>.</p>

<p>It's been generally very effective, but right now we need something more dynamic. We need to plug in stuff like <code>.Where(x =&gt; x.Name.Contains("Anonymous")).Take(20)</code> or something else along the lines. However, plugging in directly to the previously mentioned line of code would result in the following:</p>

<p><code>context.Database.SqlQuery&lt;ClassName&gt;(sql, sqlParams).Where(x =&gt; x.Name.Contains("Anonymous")).Take(20);</code></p>

<p>While it actually works and pulls the top 20 records where the name contains "Anonymous", the performance is pretty bad. What it does behind the scenes is to take all the records from that table and then finally filtering them after having loaded them to memory.</p>

<p>I would then like to ask, is there any way to translate the text SQL to LINQ, or translate the LINQ to SQL, such that I can execute both my text SQL and LINQ in one single statement. If you don't actually have a solution, I'd gladly appreciate suggestions too...!</p>

<p><strong>EDIT:</strong> I've considered using Expression Trees, but I'm not sure how they can actually fit into the picture. Also, I've considered using database views. But there are so many views (quite a number per table) it would definitely be a hassle to port everything over to MS SQL and then rewriting all the querying logic.</p>

## Answers
### Answer ID: 13375417
<p>You can't really do that as expression trees generate SQL from an expression that's built dynamically i.e. from the expressions you can "compile" a SQL, what you're asking is akin to asking for a "SQL-to-LINQ dissasembler".</p>

<p>My suggestion for your problem is - take your SQL queries and save them as views in the database, then map your views in the LINQ-To-SQL .dbml files and add your LINQ queries on top of that.</p>

<pre><code>context.viewSavedFromYourSql.Where(x =&gt; x.Name.Contains("Anonymous")).Take(20);
</code></pre>

<p>This way LINQ will query from your view, and return only the data you need.</p>

<p><em>(you can also use table-valued functions instead of views)</em></p>

### Answer ID: 13444964
<p>To view SQL generated in visual studio, set breakpoint and move the mouse cursor to the variable (the linq query don't should ends with .ToList() or ToArray()) or use this method <a href="https://stackoverflow.com/questions/4899974/how-to-view-linq-generated-sql-statements">How to view LINQ Generated SQL statements?</a>. To convert sql to linq look here: <a href="http://www.sqltolinq.com/" rel="nofollow noreferrer">http://www.sqltolinq.com/</a></p>

<p>You can create fast and quality stored procedure and add it to data context for using in linq queries.</p>

### Answer ID: 13375539
<p>Can't you store your queries into Stored procedures and call those with your search text as a param? Procedures can be called through your LINQ-To-SQL. That should save you some time..</p>

<p>Link for more info on calling Simple/Complex procedures: <a href="http://www.codeproject.com/Articles/230380/LINQ-to-SQL-Advanced-Concepts-and-Features" rel="nofollow">http://www.codeproject.com/Articles/230380/LINQ-to-SQL-Advanced-Concepts-and-Features</a></p>

### Answer ID: 13374766
<p>You may want to take a look at <a href="http://www.sqltolinq.com/" rel="nofollow">Linker</a>.</p>

<p>It translate SQL statements to LINQ statements. Obviously it can't convert all kind of SQL queries, but it helps you a lot if you want to convert all hard coded SQL queries to LINQ statements.</p>

<p>Sorry if it is not free!</p>

### Answer ID: 13249997
<p>[Opinion]</p>

<p>Not likely without a significant amount of effort.</p>

<p>What you seem to be asking for is either a sql -> sql model tokeniser or a full blown sql -> IQueryable tokeniser, both which would be significant effort to implement.</p>

<p>My suggestion is either write a rough sql parser to then just put in the required statement, or to rewrite your views as LinqToDatabase queries.</p>

<p>As explanation when you create an IQueryable expression its expression tree is the object logic of the query, your provider then takes that logic and tries to map it into a series of sql statements to execute and a mapper for the results. You seem to be asking for the opposite so you would want to translate a series of sql statements back into an expression tree.</p>

<p>This to me seems like a bit of double work, in that you would map into an expression tree, append onto it, then map back. Not least because a perfect map is probably not possible so you would find that you would get equivalent but not what you expected sql back out.</p>

