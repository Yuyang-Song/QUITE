# Way to get the CREATE statement of global temporary table?
[Link to question](https://stackoverflow.com/questions/75214082/way-to-get-the-create-statement-of-global-temporary-table)
**Creation Date:** 1674501591
**Score:** 0
**Tags:** sql-server, sql-server-2019
## Question Body
<p>I have stored procedures I need to rewrite that used global temporary tables but now must use local temporary tables so that there is no cross over between users/the prod and dev db which are on the same SQL Server instances or any other new databases this database will be share the instance with.</p>
<p>I have to convert a lot of code that is like this</p>
<pre><code>EXEC sp_executesql 
     N'SELECT manyDynamicallyCreatedColumns INTO ##someTempTable
</code></pre>
<p>I now for this to work for local tables I must instead create the table first and then <code>INSERT INTO</code> like</p>
<pre><code>CREATE TABLE #tempTable (manyColumns);

EXEC sp_executesql 
     N'INSERT INTO #tempTable SELECT manyColumns FROM somewhere'
</code></pre>
<p>The issue I face is that this stored procedure has 8 different scenarios that lead to the global temp table. The select statement of the SQL is dynamically generated via a number of other queries. I think what would be the easiest way for me to figure out what my <code>CREATE TABLE #tempTable</code> should look like is if I could print/select what global temporary table looks like after it is made, for each of these 8 scenarios. Then I would just need a If/Else If statement that creates the local table appropriately before proceeding. But I don't know how or if this is possible.</p>
<p>For real tables I can right click -&gt; Script to...-&gt; Create.  I don't know if there is an analogous way to do this via scripting that works for global temporary tables. Is there?</p>

