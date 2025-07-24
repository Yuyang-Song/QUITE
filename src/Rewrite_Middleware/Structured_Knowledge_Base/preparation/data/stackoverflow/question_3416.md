# OData orderby Enum Type throws exception
[Link to question](https://stackoverflow.com/questions/78992684/odata-orderby-enum-type-throws-exception)
**Creation Date:** 1726552234
**Score:** 1
**Tags:** c#, .net, entity-framework, asp.net-core, odata
## Question Body
<p>I have an entity defined as follows, which encounters issues when trying to sort by the <code>TheType</code> property:</p>
<pre><code>[Serializable]
[Authorize]
[JsonObject(ItemNullValueHandling = NullValueHandling.Ignore)]
public class TheEntity
{
    /// &lt;summary&gt;
    /// Unique Identifier
    /// &lt;/summary&gt;
    [Key]
    public Guid Id { get; set; }

    /// &lt;summary&gt;
    /// Tenant Id. Non-configurable
    /// &lt;/summary&gt;
    public Guid TenantId { get; set; }

    [EnumDataType(typeof(TheTypeEnum))]
    [JsonConverter(typeof(StringEnumConverter))]
    public TheTypeEnum? TheType { get; set; }
}
</code></pre>
<p>In my OData query, <code>TheType</code> is represented as a <code>varchar</code> field in the database.
For eg: The OData query looks like http://localhost/odata/theEntity?$orderby=theType</p>
<p>The function handling this query is:</p>
<pre><code>public async Task&lt;ApiResponse&lt;IQueryable&lt;TheEntity&gt;&gt;&gt; QueryTheEntities(ODataQueryOptions&lt;TheEntity&gt; options)
{
    var response = new ApiResponse&lt;IQueryable&lt;TheEntity&gt;&gt;();

    try
    {
        int maxTop = options.Top?.Value ?? options.Context?.DefaultQuerySettings?.MaxTop ?? MAX_RESULTS;
        var query = await scopedRepository
            .TheEntity
            .GetQueryAsync(mapper: mapper, options, new QuerySettings());
            
        response.Data = query.Take(maxTop);
    }
    catch (ODataException ex)
    {
        logger.LogError(ex, &quot;OData query failed.&quot;);
        response.ModelState.AddModelError(&quot;OData options&quot;, &quot;One or more parameters in the OData query are invalid.&quot;);
    }

    return response;
}
</code></pre>
<p>However, when attempting to order by <code>TheType</code>, I receive the following exception:</p>
<blockquote>
<p>The LINQ expression <code>DbSet&lt;TheEntity&gt;().Where(s =&gt; s.TenantId == __scope_TenantId_0) .OrderBy(s =&gt; s.TheType == null ? null : (TheTypeEnum?)Enum.Parse&lt;TheTypeEnum&gt;(s.TheType))</code> could not be translated. Additional information: Translation of method 'System.Enum.Parse' failed. If this method can be mapped to your custom function, see <a href="https://go.microsoft.com/fwlink/?linkid=2132413" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2132413</a> for more information. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.</p>
</blockquote>
<p>Here's the LINQ expression properly formatted</p>
<pre class="lang-cs prettyprint-override"><code>DbSet&lt;TheEntity&gt;()
    .Where(s =&gt; s.TenantId == __scope_TenantId_0)
    .OrderBy(s =&gt; 
        s.TheType == null ? null : (TheTypeEnum?)Enum.Parse&lt;TheTypeEnum&gt;(s.TheType)
    )
</code></pre>
<p>From this exception, it seems that sorting by `TheType` is not supported at the database level due to the use of `Enum.Parse`. I would like to avoid loading the entire dataset into memory, as it is quite large. Is there a way to perform this sorting efficiently at the database level without resorting to client-side evaluation?</p>
<p>Tried the below, but  no luck.</p>
<pre><code>        foreach (var orderByNode in orderByClause.OrderByNodes)
        {
            if (orderByNode is OrderByPropertyNode propertyNode)
            {
                var propertyName = propertyNode.Property.Name;
                var isDescending = propertyNode.Direction == OrderByDirection.Descending;
            

                if (IsEnumProperty(propertyName))
                {
                    // Order by the underlying integer value of the enum
                    var parameter = Expression.Parameter(typeof(Simulation), &quot;sim&quot;);
                    var property = Expression.Property(parameter, propertyName);
                    var convertToInt = Expression.Convert(property, typeof(int));  // Convert enum to int

                    var orderByExpression = Expression.Lambda&lt;Func&lt;Simulation, int&gt;&gt;(convertToInt, parameter);

                    orderedQuery = orderedQuery == null
                        ? query.OrderBy(orderByExpression)
                        : isDescending ? orderedQuery.ThenByDescending(orderByExpression) : orderedQuery.ThenBy(orderByExpression);
                }
            }

        }
</code></pre>

