# How can I get EF Core to correctly translate complext value object queries into SQL?
[Link to question](https://stackoverflow.com/questions/79231176/how-can-i-get-ef-core-to-correctly-translate-complext-value-object-queries-into)
**Creation Date:** 1732725988
**Score:** 0
**Tags:** c#, asp.net-core, entity-framework-core, .net-9.0
## Question Body
<p>I use EF Core 8 in a .NET 9 application with a PostgreSQL database.</p>
<p>I have an entity that has a date range value object defined as a property.</p>
<p>Value object:</p>
<pre><code>public record DateRange
{
    private DateRange()
    {
    }

    public DateOnly Start { get; init; }
    public DateOnly? End { get; init; }

    public int LengthInDays =&gt; End.HasValue ? End.Value.DayNumber - Start.DayNumber : int.MaxValue;

    public static DateRange Create(DateOnly start, DateOnly? end)
    {
        if (start == default) 
            throw new ArgumentException(&quot;Start date cannot be empty.&quot;, nameof(start));

        if (end.HasValue &amp;&amp; start &gt; end.Value) 
            throw new ApplicationException(&quot;End date precedes start date&quot;);

        return new DateRange
                   {
                       Start = start,
                       End = end
                   };
    }

    public bool IsWithinRange(DateOnly date)
    {
        return date &gt;= Start &amp;&amp; (!End.HasValue || date &lt;= End);
    }
}
</code></pre>
<p>Here's how the property is defined within the entity:</p>
<pre><code>public DateRange ValidityDateRange { get; private set; }
</code></pre>
<p>Here's the entity configuration for this property:</p>
<pre><code>builder.ComplexProperty(x =&gt; x.ValidityDateRange);
</code></pre>
<p>Here's the Query that EF is having trouble with:</p>
<pre><code>var campaigns = await campaignRepository.Query()
        .Where(c =&gt; c.ValidityDateRange.Start &lt;= currentDate &amp;&amp; c.ValidityDateRange.End &gt;= currentDate)
        .WhereIf(request.Title is not null, c =&gt; c.Title.Value == request.Title)
        .WhereIf(request.Code is not null, c =&gt; c.Code.Value == request.Code)
        .WhereIf(request.CategoryName is not null, c =&gt; c.CampaignCategory.Name.Value == request.CategoryName)
        .WhereIf(request.TypeName is not null, c =&gt; c.CampaignType.Name.Value == request.TypeName)
        .Include(c =&gt; c.CampaignCategory)
        .Include(c =&gt; c.CampaignType)
        .Include(c =&gt; c.Conditions)
        .ThenInclude(cond =&gt; cond.ProductCategory)
        .Include(c =&gt; c.Rewards)
        .ThenInclude(reward =&gt; reward.ProductCategory)
        .Include(c =&gt; c.Coupons)
        .AsSplitQuery()
        .ToListAsync(cancellationToken);
</code></pre>
<p>Here's the error message I get when EF tries to evaluate my query:</p>
<blockquote>
<p>The LINQ expression 'DbSet()
.Where(c =&gt; !(c.IsDeleted))
.Where(c =&gt; c.ValidityDateRange.Start &lt;= __currentDate_0 &amp;&amp; c.ValidityDateRange.End &gt;= __currentDate_1)
.Where(c =&gt; c.Title.Value == __request_Title_2)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.</p>
</blockquote>

