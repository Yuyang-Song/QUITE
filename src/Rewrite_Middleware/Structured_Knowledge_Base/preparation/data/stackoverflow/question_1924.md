# Multicolumn keys in Entity Framework Code First with eager loading
[Link to question](https://stackoverflow.com/questions/12339999/multicolumn-keys-in-entity-framework-code-first-with-eager-loading)
**Creation Date:** 1347201532
**Score:** 0
**Tags:** .net, entity-framework, ef-code-first, many-to-many, dbcontext
## Question Body
<p>I use Entity Framework, and I have a many-to-many relationship in the database between Users and Boxes, like this:</p>

<pre><code>public class HistoryEntry
{
    public int BoxId { get; set; }
    public virtual Box Box { get; set; }

    public int UserId { get; set; }
    public virtual User User { get; set; }

    public int ResultBoxId { get; set; }
    public virtual Box ResultBox { get; set; }
}
</code></pre>

<p>The key of this "HistoryEntries" table would be a multicolumn key: it consists the BoxId and the UserId:</p>

<pre><code>        modelBuilder.Entity&lt;HistoryEntry&gt;().HasKey(entry =&gt;
            new
            {
                BoxId = entry.BoxId,
                UserId = entry.UserId
            });
</code></pre>

<p>However, I want to turn off the lazy loading and the proxy creation because I would use every query with eager loading.</p>

<p>How to rewrite my code in an "eager loading" style?</p>

## Answers
### Answer ID: 12340518
<p>Use the <code>Include</code> method to eager load the navigational properties.</p>

<pre><code>var users = context.User.Include(u =&gt; u.HistoryEntries.Select(h =&gt; h.Box))
      .Where(/* */);
</code></pre>

