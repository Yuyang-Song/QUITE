# EF Core: Linq, Where with object list does work
[Link to question](https://stackoverflow.com/questions/72814414/ef-core-linq-where-with-object-list-does-work)
**Creation Date:** 1656585806
**Score:** 0
**Tags:** c#, linq, .net-6.0, ef-core-6.0
## Question Body
<p>I have Database Table with a composite primary key, so want to check if both key pairs are matching</p>
<pre><code>  
public async Task&lt;IList&lt;AccountingAccountCategoryMap&gt;&gt; GetList(IEnumerable&lt;AccountingAccountCategoryKey&gt; keys)
        {
            return await Query.Where(item =&gt; keys.Any(x =&gt;
                x.CategoryId == item.CategoryId &amp;&amp; x.AccountingAccountId == 
                item.AccountingAccountId)).ToListAsync();
        }
</code></pre>
<p>I get this error:</p>
<blockquote>
<p>{   &quot;Message&quot;: &quot;The LINQ expression 'x =&gt; x.CategoryId ==
EntityShaperExpression: \r\n<br />
Orderlyze.Service.DL.Contract.Entity.AccountingAccountCategoryMap\r\n
ValueBufferExpression: \r\n        ProjectionBindingExpression:
EmptyProjectionMember\r\n    IsNullable: False\r\n.CategoryId &amp;&amp;
x.AccountingAccountId == EntityShaperExpression: \r\n<br />
Orderlyze.Service.DL.Contract.Entity.AccountingAccountCategoryMap\r\n
ValueBufferExpression: \r\n        ProjectionBindingExpression:
EmptyProjectionMember\r\n    IsNullable:
False\r\n.AccountingAccountId' could not be translated. Either rewrite
the query in a form that can be translated, or switch to client
evaluation explicitly by inserting a call to 'AsEnumerable',
'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See
<a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more
information.&quot;,   &quot;Inner&quot;: &quot;&quot; }</p>
</blockquote>
<p><strong>The Question is why does work? And is there way to fix it without Client Evaluation?</strong></p>

## Answers
### Answer ID: 72814836
<p>What is happening here is EF cannot execute the query fully in the server. That’s probably because of the keys.</p>
<p>If the keys are stored in the database then you could try referring to the table in the database instead. Or if there are a limited number of keys you could try specifying them explicitly (or possibly using ToList on them).</p>

