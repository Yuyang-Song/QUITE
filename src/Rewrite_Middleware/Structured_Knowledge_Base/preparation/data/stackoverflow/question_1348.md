# C# linq to sql - selecting tables dynamically
[Link to question](https://stackoverflow.com/questions/7179436/c-linq-to-sql-selecting-tables-dynamically)
**Creation Date:** 1314205528
**Score:** 7
**Tags:** c#, linq-to-sql, dynamic
## Question Body
<p>I have the following scenario: there are a database that generates a new logTable every year. It started on 2001 and now has 11 tables. They all have the same structure, thus the same fields, indexes,pk's, etc.</p>

<p>I have some classes called managers that - as the name says - manages every operation on this DB. For each different table i have a manager, except for this logTable which i have only one manager.</p>

<p>I've read a lot and tried different things like using ITable to get tables dynamically or an interface that all my tables implements. Unfortunately, i lose strong-typed properties and with that i can't do any searches or updates or anything, since i can't use <code>logTable.Where(q=&gt; q.ID == paramId)</code>.</p>

<p>Considering that those tables have the same structure, a query that searches logs from 2010 can be the exact one that searches logs from 2011 and on.</p>

<p>I'm only asking this because i wouldn't like to rewrite the same code for each table, since they are equal on it's structure.</p>

<p><strong>EDIT</strong></p>

<p>I'm using Linq to SQL as my ORM. And these tables uses all DB operations, not just select.</p>

## Answers
### Answer ID: 7206076
<p>As long as each of your queries return the same shape, you can use ExecuteQuery&lt;Log&gt;("Select cols From LogTable" + instance). Just be aware that ExecuteQuery is one case where LINQ to SQL allows for SQL Injection. I discuss how to parameterize ExecuteQuery at <a href="http://www.thinqlinq.com/Post.aspx/Title/Does-LINQ-to-SQL-eliminate-the-possibility-of-SQL-Injection" rel="nofollow">http://www.thinqlinq.com/Post.aspx/Title/Does-LINQ-to-SQL-eliminate-the-possibility-of-SQL-Injection</a>. </p>

### Answer ID: 7179533
<p>Consider putting all your logs in one table and using <a href="http://msdn.microsoft.com/en-us/library/dd578580%28v=sql.100%29.aspx" rel="nofollow">partitioning</a> to maintain performance.  If that is not feasible you could create a view that unions all the log tables together and use that when selecting log data.  That way when you added a new log table you just update the view to include the new table.  </p>

<p><strong>EDIT</strong> Further to the most recent comment:</p>

<p>Sounds like you need a new DBA if he won't let you create new SPs. Yes I think could define an ILogTable interface and then make your log table classes implement it, but that would not allow you do <code>GetTable&lt;ILogTable&gt;()</code>.  You would have to have some kind of DAL class with a method that created a union query, e.g.</p>

<pre><code>public IEnumerable&lt;ILogTable&gt; GetLogs()
{
    var Log2010 = from log in DBContext.2010Logs
                  select (ILogTable)log;
    var Log2011 = from log in DBContext.2011Logs
                  select (ILogTable)log;
    return Log2010.Concat(Log2011);
}
</code></pre>

<p>Above code is completely untested and may fail horribly ;-)</p>

<p>Edited to keep @AS-CII happy ;-)</p>

### Answer ID: 7179529
<p>You might want to look into the <a href="http://fluentlinqtosql.codeplex.com/" rel="nofollow">Codeplex Fluent Linq to SQL project</a>.  I've never used it, but I'm familiar with the ideas from using similar mapping techniques in EF4.  YOu could create a single object and map it dynamically to different tables using syntax such as:</p>

<pre><code>public class LogMapping : Mapping&lt;Log&gt; {
    public LogMapping(int year) {
        Named("Logs" + year);
        //Column mappings...
    }
}
</code></pre>

