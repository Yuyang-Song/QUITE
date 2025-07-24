# LINQ GroupBy with SQLite.EF6 results in &#39;APPLY joins are not supported&#39; exception
[Link to question](https://stackoverflow.com/questions/45207172/linq-groupby-with-sqlite-ef6-results-in-apply-joins-are-not-supported-exceptio)
**Creation Date:** 1500533173
**Score:** 4
**Tags:** c#, entity-framework, linq, sqlite, group-by
## Question Body
<p>I have the table <code>VersionedEntities</code> that looks like this:</p>

<pre><code>+----+--------------+---------+
| Id | Name         | Version |
+----+--------------+---------+
| 1  | FirstEntity  | 1       |
+----+--------------+---------+
| 2  | SecondEntity | 2       |
+----+--------------+---------+
| 1  | ThirdEntity  | 3       |
+----+--------------+---------+
</code></pre>

<p><code>Version</code> is the primary key.</p>

<p><code>VersionedEntity</code> class:</p>

<pre><code>[Table("VersionedEntities")]
public class VersionedEntity
{
    public int Id { get; set; }
    public string Name { get; set; }
    [Key]
    public long Version { get; set; }
}
</code></pre>

<p>I want to select the latest version of each <code>Id</code>, resulting in this:</p>

<pre><code>+----+--------------+---------+
| Id | Name         | Version |
+----+--------------+---------+
| 2  | SecondEntity | 2       |
+----+--------------+---------+
| 1  | ThirdEntity  | 3       |
+----+--------------+---------+
</code></pre>

<p>I already have a working query when using <code>Microsoft SQL Server</code> as database:</p>

<pre><code>List&lt;VersionedEntity&gt; versionedEntities;

using (var dbContext = _createDbContext())
{
    versionedEntities = dbContext.VersionedEntity
        .GroupBy(versionedEntity =&gt; versionedEntity.Id)
        .Select(group =&gt; group.OrderByDescending(versionedEntity =&gt; versionedEntity.Version).FirstOrDefault()).ToList());
}
</code></pre>

<p>I want to use SQLite as database instead, but when using SQLite the above query results in an <code>NotSupportedException</code> with the message: <code>APPLY joins are not supported</code>.</p>

<p>What I have found out is that only <code>LEFT OUTER JOIN</code> is implemented in SQLite (<a href="https://sqlite.org/omitted.html" rel="nofollow noreferrer">source</a>). I guess that LINQ <code>GroupBy()</code> is using one of the not implemented joins.</p>

<p>I would like to know if there is a workaround to this, or if I could rewrite my query to something that is SQLite compatible.</p>

## Answers
### Answer ID: 45208325
<p>I could suggest the following alternative query which should translate to <code>NOT EXISTS</code> criteria based SQL query:</p>

<pre><code>var result = db.VersionedEntity
    .Where(e =&gt; !db.VersionedEntity.Any(e2 =&gt; e2.Id == e.Id &amp;&amp; e2.Version &gt; e.Version))
    .ToList();
</code></pre>

<p>It's just a different interpretation of the requirement - select the record if there is no other record with the same <code>Id</code> and bigger <code>Version</code>.</p>

