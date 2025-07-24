# EF Core sum on nested collection&#39;s properties does not work
[Link to question](https://stackoverflow.com/questions/60916103/ef-core-sum-on-nested-collections-properties-does-not-work)
**Creation Date:** 1585494104
**Score:** 2
**Tags:** c#, entity-framework-core
## Question Body
<p>My database has the following structure: One User can have many Accounts. One Account can have many Transfers.</p>

<p>This is the map configuration. I want to store in my DTO information about each user and his total savings in every account. (the code below represents one part of the whole configuration).</p>

<pre><code>this.CreateMap&lt;User, UserTestModel&gt;()
    .ForMember(
        utm =&gt; utm.AccountsSavings, 
        options =&gt; options.MapFrom(u =&gt; u.Accounts
            .Select(a =&gt; a.Transfers.Sum(t =&gt; t.Amount))
            .ToList()));
</code></pre>

<p>My query to the database (I am using EF Core 3.1.3 with Sqlite database) looks like this:</p>

<pre><code>var resultSet = await this._dbContext.Users
    .ProjectTo&lt;UserTestModel&gt;(this.Mapper.ConfigurationProvider)
    .ToListAsync(cancellationToken)
    .ConfigureAwait(false);
</code></pre>

<p>However the following exception is thrown.</p>

<p>*</p>

<blockquote>
  <blockquote>
    <p>System.InvalidOperationException : The LINQ expression 'DbSet
            .Where(t => EF.Property>((EntityShaperExpression: 
                EntityType: Account
                ValueBufferExpression: 
                    (ProjectionBindingExpression: EmptyProjectionMember)
                IsNullable: False
            ), "Id") != null &amp;&amp; EF.Property>((EntityShaperExpression: 
                EntityType: Account
                ValueBufferExpression: 
                    (ProjectionBindingExpression: EmptyProjectionMember)
                IsNullable: False
            ), "Id") == EF.Property>(t, "AccountId"))
            .Sum(t => t.Amount)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client
    evaluation explicitly by inserting a call to either AsEnumerable(),
    AsAsyncEnumerable(), ToList(), or ToListAsync().</p>
  </blockquote>
</blockquote>

<p>*</p>

<p>Is this a problem with my code, or rather with some of the frameworks I am using at the moment (AutoMapper or EF Core)?</p>

<p><strong>Edit 1:</strong></p>

<p>I decided to try to manually gather that information from the <code>User</code> entities but that code leads to the same exception which means that it is not Automapper's fault:</p>

<pre><code>var resultSet = await this._dbContext.Users
    .Select(u =&gt; u.Accounts.Select(a =&gt; a.Transfers.Sum(t =&gt; t.Amount)).ToList())
    .ToListAsync(cancellationToken)
    .ConfigureAwait(false);
</code></pre>

<p><strong>Edit 2:</strong></p>

<p>Created issue at EntityFrameworkCore's GitHub: <a href="https://github.com/dotnet/efcore/issues/20455" rel="nofollow noreferrer">https://github.com/dotnet/efcore/issues/20455</a></p>

## Answers
### Answer ID: 60917256
<p>I was able to reproduce it with SQLite provider and <code>Amount</code> type being <code>decimal</code> (works fine with SqlServer provider).</p>
<p>So you seem to be hitting the following SQLite <a href="https://learn.microsoft.com/en-us/ef/core/providers/sqlite/limitations#query-limitations" rel="nofollow noreferrer">Query Limitations</a> from EF Core documentation:</p>
<blockquote>
<p>SQLite doesn't natively support the following data types. EF Core can read and write values of these types, and querying for equality (where e.Property == value) is also supported. Other operations, however, like comparison and ordering will require <strong>evaluation on the client</strong>.</p>
<ul>
<li>DateTimeOffset</li>
<li><strong>Decimal</strong></li>
<li>TimeSpan</li>
<li>UInt64</li>
</ul>
</blockquote>
<p>As workaround, consider taking the advice from the docs:</p>
<blockquote>
<p>The <code>Decimal</code> type provides a high level of precision. If you don't need that level of precision, however, we recommend using double instead. You can use a value converter to continue using decimal in your classes.</p>
</blockquote>
<p>with sample</p>
<pre><code>modelBuilder.Entity&lt;MyEntity&gt;()
    .Property(e =&gt; e.DecimalProperty)
    .HasConversion&lt;double&gt;();           
</code></pre>

