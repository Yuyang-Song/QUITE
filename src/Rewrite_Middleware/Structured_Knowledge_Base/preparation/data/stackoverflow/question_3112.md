# EF Core, one to many relationships, multiple tables with single foreign table
[Link to question](https://stackoverflow.com/questions/66994841/ef-core-one-to-many-relationships-multiple-tables-with-single-foreign-table)
**Creation Date:** 1617833791
**Score:** 1
**Tags:** c#, entity-framework-core, .net-5, ef-core-5.0
## Question Body
<p>In attempt to reduce the number of tables in a database, I'd like to use a single table to store the same type of data for multiple reference tables: a one to many relationship several times over with a single foreign table.</p>
<pre><code>public class Note
{
    public int Id { get; set; }

    public int TargetId { get; set; }
    public TargetType TargetType { get; set; }
}

public enum TargetType
{
    Article,
    Order,
    Task,
    Ticket
}

public class Article
{
    public int Id { get; set; }

    public ICollection&lt;Note&gt; Notes { get; set; }
}

public class Order
{
    public int Id { get; set; }

    public ICollection&lt;Note&gt; Notes { get; set; }
}

public class Task
{
    public int Id { get; set; }

    public ICollection&lt;Note&gt; Notes { get; set; }
}

public class Ticket
{
    public int Id { get; set; }

    public ICollection&lt;Note&gt; Notes { get; set; }
}
</code></pre>
<p>Using Code First, I've attempted OnModelCreating:</p>
<pre><code>modelBuilder.Entity&lt;Transfer&gt;().HasMany(x =&gt;
    x.LineItems.Where(y =&gt; y.TargetId == x.Id &amp;&amp; y.TargetType == LineItemTarget.Transfer)).WithOne();
</code></pre>
<p>This produces:</p>
<blockquote>
<p>System.ArgumentException: 'The expression 'x =&gt; x.Notes.Where(y =&gt; ((y.TargetId == x.Id) AndAlso (Convert(y.TargetType, Int32) == 1)))' is not a valid member access expression. The expression should represent a simple property or field access: 't =&gt; t.MyProperty'. (Parameter 'memberAccessExpression')'</p>
</blockquote>
<p>At the time of the query, I've attempted essentially the same approach:</p>
<pre><code>return await _dbContext.Transfers.Include(x =&gt; x.LineItems.Where(y =&gt; y.TargetId == x.Id))
    .ToListAsync(cancellationToken);
</code></pre>
<p>Which produces:</p>
<blockquote>
<pre><code>System.InvalidOperationException: The LINQ expression 'DbSet&lt;Note&gt;()
   .Where(l =&gt; EF.Property&lt;Nullable&lt;int&gt;&gt;(EntityShaperExpression: 
       EntityType: Article
       ValueBufferExpression: 
           ProjectionBindingExpression: EmptyProjectionMember
       IsNullable: False
   , &quot;Id&quot;) != null &amp;&amp; object.Equals(
       objA: (object)EF.Property&lt;Nullable&lt;int&gt;&gt;(EntityShaperExpression: 
           EntityType: Article
           ValueBufferExpression: 
               ProjectionBindingExpression: EmptyProjectionMember
           IsNullable: False
       , &quot;Id&quot;), 
       objB: (object)EF.Property&lt;Nullable&lt;int&gt;&gt;(l, &quot;ArticleId&quot;)))
   .Where(l =&gt; l.TargetId == x.Id &amp;&amp; (int)l.TargetType == 3)'
</code></pre>
<p>could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.</p>
</blockquote>
<p>I understand this method is recommending I bring the results back to the application and attempt to filter further application side as it's unable to automatically map the relationship because &quot;ArticleId&quot; doesn't exist on Note.</p>
<p>I have also attempted to use Query Filters which I quickly learned is the same tactic as the previous option, simply applied to all queries on that table. The last thing I am currently aware of is using raw SQL which I cannot seem to map to the Note objects and would greatly prefer to avoid raw SQL altogether.</p>
<p>Essentially I am attempting to write this SQL query in LINQ, using Articles and TargetType.Article, then the same for Order, Task, Ticket, and any other tables:</p>
<pre><code>SELECT * FROM Articles JOIN Notes ON Articles.Id = Notes.TargetId AND Notes.TargetType = 1
</code></pre>
<p>How does one perform that query on the database using LINQ?</p>

