# Performance issues with internal query from MS Access against SQL Server
[Link to question](https://stackoverflow.com/questions/10124547/performance-issues-with-internal-query-from-ms-access-against-sql-server)
**Creation Date:** 1334237208
**Score:** 2
**Tags:** sql-server, performance, ms-access, database-performance, sqlperformance
## Question Body
<p>We have an application that runs in MSAccess but utilizes SQL Server as the backend database. This generates a query to check which views it's got access to, and for normal users this takes up to 18 seconds. For all users that's member of the db_owner role, it takes 0.2 seconds. Is there any way I can tune this for normal users? Maybe something I can do in Access? I don't want to give them db_owner, and rewriting the application to not use Access is out of the question.</p>

<p>Here's the query:</p>

<pre><code>select 
  object_name(id), 
  user_name(uid), type, 
  ObjectProperty(id, N'IsMSShipped'), 
  ObjectProperty(id, N'IsSchemaBound') 
    from sysobjects 
    where type = N'V' 
      and permissions(id) &amp; 4096 &lt;&gt; 0
</code></pre>

<p>Using MS Access 2003, SQL Server 2008 R2</p>

## Answers
### Answer ID: 26062006
<p>Let me guess: You have an Access-ADP application that does this at startup. We had exactly the same. This query is used to get metadata that Access uses later. The root cause of the problem is the deprecated PERMISSIONS function:</p>

<p><a href="http://msdn.microsoft.com/en-us/library/ms186915.aspx" rel="nofollow">http://msdn.microsoft.com/en-us/library/ms186915.aspx</a></p>

<p>Quote: "Continued use of the PERMISSIONS function may result in slower performance."</p>

<p>Since you cannot change either the query or the function, you are out of luck.</p>

<p>I suggest you consider moving to an ACCDB with linked tables, as ADP-support was cancelled in Access 2013 anyway.</p>

### Answer ID: 26061628
<p>Bit late to the party but try this:</p>

<pre><code>select
  [name], 
  schema_name(schema_id), 
  [type], 
  Is_MS_Shipped,
  Is_Schema_published
from 
    sys.all_views
where 
    not permissions(object_id) &amp; 4096 = 0
</code></pre>

<p>Using the view specific object and inverting the comparison may give you slight improvement</p>

### Answer ID: 10159701
<p>Short of figuring out the root cause of issue, maybe a work around might help? Just an idea: you could encapsulate your SQL statement in a proc owned by a db_owner and give it an  <a href="http://msdn.microsoft.com/en-us/library/ms188354.aspx" rel="nofollow">EXECUTE AS</a> clause.  That way when a non db_owner called the proc the SQL in the proc would get executed under the impersonation of db_owner just for the duration and scope of the proc.  Hopefully then your non db_owner users would benefit from the performance you're seeing when db_owner's run that SQL.</p>

