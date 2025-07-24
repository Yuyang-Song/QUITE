# c# linq generated query length over the limit. Is there any way we could up lift this limit?
[Link to question](https://stackoverflow.com/questions/13933801/c-linq-generated-query-length-over-the-limit-is-there-any-way-we-could-up-lift)
**Creation Date:** 1355836305
**Score:** 4
**Tags:** c#, sql, linq, entity-framework
## Question Body
<p>Hi I'm building an MVC 4 report, and using EF5. Database is on SQL 2005.</p>

<p>The report has a large amount of long string filters, when there are a lot of them selected, I got this error:"Some part of your SQL statement is nested too deeply. Rewrite the query or break it up into smaller queries."</p>

<p>Filters are selected and return a List, and in the LINQ query I use:</p>

<pre><code>DataContext.Entity.Where(list.Contains(column));
return IQueryable&lt;Entity&gt;;
</code></pre>

<p>I guess it's the LINQ-generated SQL query that gets over the limit, and I don't know what is the limit. </p>

<p>Is there any way we could control this limit? or please point out if my guess was wrong. </p>

<p>Thanks a lot. </p>

<p>Thanks for the link below, provided by @AdrianFaciu , and it's really helpful, I think it's similar issue. (I guess my each string filter's length is too long, and there are a lot of them.)
<a href="https://stackoverflow.com/questions/656167/hitting-the-2100-parameter-limit-sql-server-when-using-contains">Hitting the 2100 parameter limit (SQL Server) when using Contains()</a></p>

<p>I have read a few workarounds, but still looking for a proper solution, not by generating string queries. It seems at least for now, I have to load data step by step to reduce the length of the query.</p>

## Answers
### Answer ID: 17472919
<p>I had a similar problem on EF and Firebird – When linq query in where clause had two contains.
Solution Was simple but not elegant – LoadAll, and filter them in memory.</p>

<p>Foundedlist.RemoveAll(x=> !RolesList.contains(x.id));</p>

### Answer ID: 13951663
<p>The proper solution is using SQL directly. EF and Linq are not tools for writing report queries. It is ORM - you use it to get objects from database work with them and maybe also modify them and store them back to database. </p>

<p>If you need complex query just to pull data from database to build a report or some complex search engine you should simply pass the complexity of ORM and go to low level SQL - and if you reached size limit of the query or parameters you really need it. It will make your query much simpler, smaller and faster and it will allow you using some advanced features like table valued parameters to avoid large contains calls.</p>

<p>Changing all your reports from SProcs to Linq was really stupid ... You are wasting your time to produce much worse solution. </p>

