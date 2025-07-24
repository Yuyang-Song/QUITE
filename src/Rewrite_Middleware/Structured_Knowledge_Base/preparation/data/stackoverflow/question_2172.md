# Replacing a large WHERE column IN clause
[Link to question](https://stackoverflow.com/questions/21712548/replacing-a-large-where-column-in-clause)
**Creation Date:** 1392151224
**Score:** 0
**Tags:** sql, sql-server, sql-server-2008-r2
## Question Body
<p><strong>Background</strong></p>

<p>I find myself stuck in a situation with some very odd constraints. The .NET project I'm working on has a series of convoluted controls layered upon one another. At the lowest level, a SQL query is being constructed, the results of which will ultimately populate a custom data grid.</p>

<p>The pieces of this query are passed into a stored procedure, which ends up constructing executing dynamic SQL under the hood. The sproc is called as follows:</p>

<pre><code>GetPagedResults @columnList, @fromClause, @whereClause, @pageNumber, @pageSize...
</code></pre>

<p><strong>The Problem</strong></p>

<p>My problem arises from the fact that some of my predecessors wrote some really poor filtering logic. In the most drastic example, they retrieve a list of IDs from the database, whittle them down with some complex filtering logic, and then construct the WHERE clause as follows:</p>

<pre><code>WHERE PrimaryKeyColumn IN (list of 1,500 uniqueidentifiers)
</code></pre>

<p>This has resulted in our app's performance taking a serious nosedive. I've been trying to find ways to rectify the issue while still working within the confines of the stored procedure listed above, since it's fragile and deeply ingrained in the codebase.</p>

<p><strong>What I've Tried</strong></p>

<p><strong>1. Performing a JOIN, and doing all the filtering logic in SQL</strong></p>

<p>The code that they  use to whittle down the list of IDs is hundreds of lines long. Rewriting in with SQL could take days, and I don't have the confidence in our test suite to ensure that what I wrote would be functionally equivalent to the current solution.</p>

<p><strong>2. Using a user-defined function in the FROM clause</strong></p>

<p>To replace the massive <code>WHERE [column] IN</code>, I tried creating a user-defined function that would join on the list of IDs, which I formatted as XML, since it's a relatively easy way to represent a list. The result made the FROM clause of my query appear like this:</p>

<p><code>FROM MyUdf('&lt;root&gt;&lt;item id="00000000-0000-0000-0000-000000000000"/&gt;...&lt;/root&gt;')</code></p>

<p>And my function looked like this:</p>

<pre><code>ALTER FUNCTION [dbo].[MyUdf] (@idList XML)
RETURNS TABLE
AS RETURN
(
    SELECT s.* FROM SomeTable s
    JOIN @idList.nodes('/root/item') R (nref) 
        ON s.[PrimaryKeyColumn] = nref.value('@id','[uniqueidentifier]')
)
</code></pre>

<p>While this ensured that I was creating something functionally equivalent, the performance was abysmal. On average, it was 3x slower than the existing solution for a set of 1,000  uniqueidentifiers. Ouch.</p>

<p><strong>3. Doing a straight-up JOIN on the input</strong></p>

<p>When the UDF failed, I thought that maybe I could simply convert a string of uniqueidentifiers to XML within the SELECT statement, and then join on that. That would give me a FROM clause that looked like:</p>

<pre><code>FROM SomeTable s 
JOIN (CONVERT(XML, '&lt;uuids here&gt;')).nodes(/root/item) r(nref)
    ON s.PrimaryKeyColumn = nref.value('@id',[uniqueidentifier])
</code></pre>

<p>Unfortunately, it doesn't appear as though you can perform a CONVERT between the keywords JOIN and ON.</p>

<p><strong>4. Using a table variable</strong></p>

<p>I feel like this would be the ideal route, I don't think I can make it work given the constraints. The stored procedure I have to call into will only give me control over the @fromClause and @whereClause. So I can't include any SQL statements before the SELECT begins to create a table variable and populate it with the IDs to filter on.</p>

<p>If it's possible to create and populate such a table <em>within</em> a SELECT statement, then it might work. But from the reading I've done, I don't think this is a possibility.</p>

<p><strong>So...</strong></p>

<p>I'm sure there's a way to do this, but given the constraints I have to work under, I'm short on ideas. Is there anything I can manipulate in the FROM or WHERE clauses that would allow me to avoid the use of an enormous <code>WHERE [column] IN</code> clause?</p>

