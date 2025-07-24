# EF Core compiled query fails with InvalidOperationException
[Link to question](https://stackoverflow.com/questions/76980380/ef-core-compiled-query-fails-with-invalidoperationexception)
**Creation Date:** 1692995522
**Score:** 1
**Tags:** c#, entity-framework-core
## Question Body
<p>I am using EF Core 7.0.5, with the compiled queries feature, connected to a SQL Server 2019 instance on Linux. This application is an ASP.NET Core MVC application running on Windows.</p>
<p>Compiled query (failing):</p>
<pre class="lang-cs prettyprint-override"><code>private static readonly Func&lt;ApplicationDbContext, Guid, List&lt;RelatedItem&gt;&gt; _findRelatedPrimaryItems = EF.CompileQuery(
    (ApplicationDbContext database, Guid entityID) =&gt;
        database.RelatedItems
            .AsNoTracking()
            .Where(ri =&gt; ri.PrimaryItemID == entityID)
            .ToList()
    );
</code></pre>
<p>Calling code:</p>
<pre class="lang-cs prettyprint-override"><code>public List&lt;RelatedItem&gt; FindRelatedItemsForDocument(Guid documentID) {
    //  This commented out query works fine, but it's not the compiled query I want.
    //List&lt;RelatedItem&gt; items = this.RelatedItems
    //      .AsNoTracking()
    //      .Where(ri =&gt; ri.PrimaryItemID == documentID)
    //      .ToList();

    List&lt;RelatedItem&gt; items = _findRelatedPrimaryItems(this, documentID);
    return items;
}
</code></pre>
<p>Error:</p>
<blockquote>
<p>InvalidOperationException: The LINQ expression 'DbSet()
.Where(r =&gt; r.PrimaryItemID == __entityID) .ToList()' could not be
translated. Either rewrite the query in a form that can be translated,
or switch to client evaluation explicitly by inserting a call to
'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See
<a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.</p>
</blockquote>
<p>I have defined several other compiled queries that work just fine.</p>
<p>Here is an example:</p>
<pre class="lang-cs prettyprint-override"><code>private static readonly Func&lt;ApplicationDbContext, Guid, Document?&gt; _findDocument = EF.CompileQuery(
    (ApplicationDbContext database, Guid documentID) =&gt;
        database.Documents
            .AsNoTracking()
            .Where(d =&gt; d.DocumentID == documentID)
            .FirstOrDefault()
    );
</code></pre>
<p>In case it's relevant, the table columns in question are defined as:</p>
<p>RelatedItems</p>
<div class="s-table-container">
<table class="s-table">
<thead>
<tr>
<th>Column</th>
<th>Definition</th>
</tr>
</thead>
<tbody>
<tr>
<td>RelatedItems.RelatedItemID</td>
<td>PK bigint identity not null</td>
</tr>
<tr>
<td>RelatedItems.PrimaryItemID</td>
<td>uniqueidentifier not null</td>
</tr>
<tr>
<td>RelatedItems.SecondayItemID</td>
<td>uniqueidentifier not null</td>
</tr>
</tbody>
</table>
</div>
<p>Documents</p>
<div class="s-table-container">
<table class="s-table">
<thead>
<tr>
<th>Column</th>
<th>Definition</th>
</tr>
</thead>
<tbody>
<tr>
<td>Documents.DocumentID</td>
<td>PK uniqueidentifier not null</td>
</tr>
<tr>
<td>Documents.Title</td>
<td>nvarchar(max) not null</td>
</tr>
</tbody>
</table>
</div>
<p>There is no database relationship between these two tables.</p>
<p>I don't see any difference between the working query and the failing query.  I appreciate any help.</p>

## Answers
### Answer ID: 76980455
<p>Well.  That was dumb.</p>
<p>Changing the compiled query signature to return an <code>IEnumerable&lt;&gt;</code> instead of a <code>List&lt;&gt;</code> makes it work great.</p>

