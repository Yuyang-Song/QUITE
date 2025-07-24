# .net working with list stored in one column give me error
[Link to question](https://stackoverflow.com/questions/78159931/net-working-with-list-stored-in-one-column-give-me-error)
**Creation Date:** 1710413418
**Score:** 0
**Tags:** json, .net, linq, entity-framework-core, ef-core-8.0
## Question Body
<p>I have Cards in databse, in cards table:</p>
<pre class="lang-cs prettyprint-override"><code>List&lt;CardItem&gt; Items
</code></pre>
<p>in CardItem:</p>
<pre class="lang-cs prettyprint-override"><code>List&lt;CardItemContent&gt; ContentItems
</code></pre>
<p>in CardItemContent:</p>
<pre class="lang-cs prettyprint-override"><code>string ItemKey
</code></pre>
<p>in the database configuration, I have:</p>
<pre class="lang-cs prettyprint-override"><code>builder.ToTable(
    &quot;Cards&quot;
);

builder.Property(e =&gt; e.Items)
    .HasConversion(
        o =&gt;
            JsonConvert
            .SerializeObject(
            o,
            new JsonSerializerSettings()
            ),
        o =&gt;
            JsonConvert
            .DeserializeObject&lt;List&lt;CardItem&gt;&gt;(
            o,
            new JsonSerializerSettings()
            )!
    )
</code></pre>
<p>This will store the list as json in database in one column</p>
<p>now I tried the following code:</p>
<pre class="lang-cs prettyprint-override"><code>var query =
    from card in dbContext.Cards
    where
    card.Items
        .Exists(
            c =&gt; c.ContentItems.Exists(ci =&gt; ci.ItemKey != null)
        )
    select card;
</code></pre>
<p>I got error:</p>
<blockquote>
<p>The LINQ expression 'c =&gt; c.ContentItems.Exists(ci =&gt; ci.ItemKey != null)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'</p>
</blockquote>

