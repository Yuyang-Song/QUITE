# LINQ expression could not be translated
[Link to question](https://stackoverflow.com/questions/61732702/linq-expression-could-not-be-translated)
**Creation Date:** 1589208922
**Score:** 1
**Tags:** c#, linq
## Question Body
<p>I have the following database query where I am trying to check if there exists an item with a particular barcode that is linked to a particular mailbag. The query is as follows:</p>

<pre><code>var exists = await dbcontext.Items
                .Include(t =&gt; t.MailBagItems)
                .ThenInclude(mt =&gt; mt.MailBag)
                .AnyAsync(t =&gt; t.Barcode.Equals(barcode) &amp;&amp;
                t.MailBagItems.FirstOrDefault() != null &amp;&amp; 
t.MailBagItems.FirstOrDefault().MailBag.Number.ToLower().Equals(mailbagNumber.ToLower()));
</code></pre>

<p>For some reason, I'm getting the following exception:</p>

<blockquote>
  <p>System.InvalidOperationException: The LINQ expression could not be
  translated. Either rewrite the query in a form that can be translated,
  or switch to client evaluation explicitly by inserting a call to
  either AsEnumerable(), AsAsyncEnumerable(), ToList(), or
  ToListAsync().</p>
</blockquote>

<p>I know for a fact from removing parts of the boolean expression that the issue is in the last boolean condition where I'm checking the mailbag number. However, I get the same error if I remove the calls to ToLower(). Can someone indicate what is wrong with my expression and how to fix it? Please note I'm using .NET core 3 and SQL Server.</p>

## Answers
### Answer ID: 61733610
<p>Managed to make the query work by changing it to the following:</p>

<pre><code>var exists = dbcontext.Items
                .AnyAsync(t =&gt; t.Barcode.Equals(barcode) &amp;&amp;
                            t.MailBagItems.Any(t =&gt; t.MailBag.Number.ToLower().Equals(mailbagNumber.ToLower())));
</code></pre>

<p>Seems it wasn't enjoying the .FirstOrDefault().MailBag before.</p>

### Answer ID: 61733580
<p>Your <code>AnyAsync</code> is to complex for EF to transform to SQL, if you want to still use that query you will have to materialize the entities first, like this:</p>

<pre><code>var exists = dbcontext.Items
                .Include(t =&gt; t.MailBagItems)
                .ThenInclude(mt =&gt; mt.MailBag)
                .ToListAsync()
                .AnyAsync(t =&gt; t.Barcode.Equals(barcode) &amp;&amp;
                t.MailBagItems.FirstOrDefault() != null &amp;&amp; 
t.MailBagItems.FirstOrDefault().MailBag.Number.ToLower().Equals(mailbagNumber.ToLower()));
</code></pre>

<p>Also you are missing the <code>await</code> keyword,  or was that intended?</p>

