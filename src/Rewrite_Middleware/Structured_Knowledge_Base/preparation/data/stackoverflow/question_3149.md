# View with union all locking tables?
[Link to question](https://stackoverflow.com/questions/68808122/view-with-union-all-locking-tables)
**Creation Date:** 1629141288
**Score:** 0
**Tags:** sql, sql-server, t-sql, view
## Question Body
<p>In my SQL Server 12.0.5000.0 database I have a view similar to this that my application uses to read data:</p>
<pre><code> create view myview as  
SELECT [id], [another_id], [textdata], [datastamp] FROM [dbo].[table_0] UNION ALL   
SELECT [id], [another_id], [textdata], [datastamp] FROM [dbo].[table_1] UNION ALL   
SELECT [id], [another_id], [textdata], [datastamp] FROM [dbo].[table_2] UNION ALL   
SELECT [id], [another_id], [textdata], [datastamp] FROM [dbo].[table_3] UNION ALL   
SELECT [id], [another_id], [textdata], [datastamp] FROM [dbo].[table_4] UNION ALL   
SELECT [id], [another_id], [textdata], [datastamp] FROM [dbo].[table_5] UNION ALL   
SELECT [id], [another_id], [textdata], [datastamp] FROM [dbo].[table_6] UNION ALL   
SELECT [id], [another_id], [textdata], [datastamp] FROM [dbo].[table_7] UNION ALL   
SELECT [id], [another_id], [textdata], [datastamp] FROM [dbo].[table_8] UNION ALL   
SELECT [id], [another_id], [textdata], [datastamp] FROM [dbo].[table_9] UNION ALL   
</code></pre>
<p>If I'm running a reindex on table 3 while I'm querying table 8 via this view, would this reindex cause locking?  I'm seeing some behavior that makes me think this might be happening.  I'm wondering about rewriting it like so:</p>
<pre><code> create view myview as  
SELECT [id], [another_id], [textdata], [datastamp] FROM [dbo].[table_0] with (nolock) UNION ALL   
SELECT [id], [another_id], [textdata], [datastamp] FROM [dbo].[table_1] with (nolock) UNION ALL   
SELECT [id], [another_id], [textdata], [datastamp] FROM [dbo].[table_2] with (nolock) UNION ALL   
SELECT [id], [another_id], [textdata], [datastamp] FROM [dbo].[table_3] with (nolock) UNION ALL   
SELECT [id], [another_id], [textdata], [datastamp] FROM [dbo].[table_4] with (nolock) UNION ALL   
SELECT [id], [another_id], [textdata], [datastamp] FROM [dbo].[table_5] with (nolock) UNION ALL   
SELECT [id], [another_id], [textdata], [datastamp] FROM [dbo].[table_6] with (nolock) UNION ALL   
SELECT [id], [another_id], [textdata], [datastamp] FROM [dbo].[table_7] with (nolock) UNION ALL   
SELECT [id], [another_id], [textdata], [datastamp] FROM [dbo].[table_8] with (nolock) UNION ALL   
SELECT [id], [another_id], [textdata], [datastamp] FROM [dbo].[table_9] with (nolock) UNION ALL   
</code></pre>
<p>If I don't care about dirty reads I would think this would be okay.</p>

