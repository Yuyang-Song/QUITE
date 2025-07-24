# Entity Framework Core with linq does not translate enum in a in query
[Link to question](https://stackoverflow.com/questions/74966356/entity-framework-core-with-linq-does-not-translate-enum-in-a-in-query)
**Creation Date:** 1672440168
**Score:** 1
**Tags:** c#, linq, enums, entity-framework-core, .net-6.0
## Question Body
<p>I try to do a in query in a where clause with enum type <code>TypeDocument</code> and it's not working because it looks like linq expression cannot be translated to a SQL query. Linq cannot convert the enum in int for the comparison if I understand correctly:</p>
<pre><code>documents.Where(doc =&gt; query.TypesExclus.Any(type =&gt; type != doc.TypeDocument))
</code></pre>
<p>I know I can do a <code>.ToListAsync()</code> before and than the where after but I prefer to let the database server handler the filter for better performance.</p>
<p>I have tried to add value conversion but this doesn't change the result.
<a href="https://learn.microsoft.com/en-us/ef/core/modeling/value-conversions?tabs=data-annotations" rel="nofollow noreferrer">https://learn.microsoft.com/en-us/ef/core/modeling/value-conversions?tabs=data-annotations</a></p>
<p>I get the following error:</p>
<blockquote>
<p>System.InvalidOperationException : The LINQ expression 'type =&gt; (int)type == (int)EntityShaperExpression:<br />
Sp.Domain.Entities.Document
ValueBufferExpression:
ProjectionBindingExpression: Outer
IsNullable: False
.TypeDocument' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'.</p>
</blockquote>
<p>Code:</p>
<pre><code>public async Task&lt;GetDocumentsResult&gt; RetrieveAsync(GetDocumentRegimeQuery query)
{
    var documents = context.Documents
        .AsNoTracking()
        .Where(doc =&gt; doc.Regime.Id == query.RegimeId
                      &amp;&amp; doc.AfficherSiteParticipant == true)
        .Select(d =&gt; new DocumentDto { Id = d.Id, Nom = d.Nom, TypeDocument = d.TypeDocument, DateSauvegarde = d.DateSauvegarde, Extension = d.Extension });

    if (query.TypesExclus.Any())
    {
        documents = documents.Where(doc =&gt; query.TypesExclus.Any(type =&gt; type != doc.TypeDocument));
    }

    return new GetDocumentsResult { Documents = await documents.ToListAsync() };
}
</code></pre>

## Answers
### Answer ID: 74967806
<p>Entity Framework Core does not support translating enum types to SQL.</p>
<p>You can try to convert the enum to an integer before performing the comparison.</p>
<pre><code>documents = documents.Where(doc =&gt; query.TypesExclus.Any(type =&gt; (int)type != (int)doc.TypeDocument));
</code></pre>

