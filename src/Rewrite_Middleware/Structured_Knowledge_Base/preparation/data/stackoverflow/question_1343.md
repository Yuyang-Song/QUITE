# use Intersect into IQueryable and EfCore
[Link to question](https://stackoverflow.com/questions/71524412/use-intersect-into-iqueryable-and-efcore)
**Creation Date:** 1647593194
**Score:** 2
**Tags:** entity-framework, iqueryable
## Question Body
<p>I'm trying to use LinQ Intersect (or equivalent) into an IQueryable method but it seems like I'm doing it wrong.</p>
<p>I have some PRODUCTS that match some SPECIFITY (like colors, materials, height...), those specifications have different values, for example:</p>
<p>color : blue, red, yellow
height : 128cm, 152cm...</p>
<p>I need to get the products that match <strong>ALL</strong> the list of couple specifityId / specifityValue I provide.</p>
<p>Here what I'm trying to do:</p>
<pre><code>// The list of couple SpecifityID (color, material..) / SpecifityValue (red, yellow, wood...)
List&lt;string&gt; SpecId_SpecValue = new List&lt;string&gt;();

SpecId_SpecValue.Add(&quot;3535a444-1139-4a1e-989f-795eb9be43be_BEA&quot;);
SpecId_SpecValue.Add(&quot;35ad6162-a885-4a6a-8044-78b68f6b2c4b_Purple&quot;);

int filterCOunt = SpecId_SpecValue.Count;

var query =
            Products
                    .Include(pd =&gt; pd.ProductsSpecifity)
                .Where(z =&gt; SpecId_SpecValue
                    .Intersect(z.ProductsSpecifity.Select(x =&gt; (x.SpecifityID.ToString() + &quot;_&quot; + x.SpecifityValue)).ToList()).Count() == filterCOunt);
</code></pre>
<p>I got the error : <em>InvalidOperationException: The LINQ expression 'DbSet() could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.</em> which mean it can't be translated to SQL and I need to ToList before my filter.</p>
<p>The problem is, I don't want to call ToList() because I got huge number of products in my Database and I don't want to load them in memory before filtering them.</p>
<p>Is there an other way to achieve what I need to do?</p>

## Answers
### Answer ID: 71556592
<p>I ended up using a solution found in the link @Gert Arnold provide <a href="https://stackoverflow.com/a/70819284/1143650">here</a>.</p>
<p>I used <a href="https://github.com/yv989c/BlazarTech.QueryableValues#getting-started" rel="nofollow noreferrer">BlazarTech.QueryableValues.SqlServer</a> @yv989c's answers</p>
<p>Here's what is now working like a charm :</p>
<pre><code>// The list of couple SpecifityID (color, material..) / SpecifityValue (red, yellow, wood...)
            Dictionary&lt;Guid, string&gt; SpecId_SpecValue = new Dictionary&lt;Guid, string&gt;();

            SpecId_SpecValue.Add(new Guid(&quot;3535a444-1139-4a1e-989f-795eb9be43be&quot;), &quot;BEA&quot;);
            SpecId_SpecValue.Add(new Guid(&quot;35ad6162-a885-4a6a-8044-78b68f6b2c4b&quot;), &quot;Purple&quot;);


            // BlazarTech.QueryableValues.SqlServer
            var queryableValues = DbContext.AsQueryableValues(SpecId_SpecValue);

            var query = Products.Include(pd =&gt; pd.ProductsSpecifity)
                .Where(x =&gt; x.ProductsSpecifity
                    .Where(e =&gt; queryableValues
                        .Where(v =&gt;
                            v.Key == e.SpecifityID &amp;&amp;
                            v.Value == e.SpecifityValue
                        )
                        .Any()
                    ).Count() == dynamicFilter.Count);
</code></pre>

### Answer ID: 71530485
<p>The query expresses &quot;products of which all <code>x.SpecifityID.ToString() + &quot;_&quot; + x.SpecifityValue</code> combinations exactly match some given combinations&quot;.</p>
<p>Set combination operators like <code>Except</code> often don't play nice with EF for various reasons I'm not going into here. Fortunately, in many of these cases a work-around can be found by using <code>Contains</code>, which EF does support well. In your case:</p>
<pre class="lang-cs prettyprint-override"><code>var query = Products.Include(pd =&gt; pd.ProductsSpecifity)
    .Where(z =&gt; z.ProductsSpecifity
        .Select(x =&gt; x.SpecifityID.ToString() + &quot;_&quot; + x.SpecifityValue)
            .Count(s =&gt; SpecId_SpecValue.Contains(s)) == filterCount);
</code></pre>
<p>Please note that the comparison is not efficient. Transforming database values before comparison disables any use of indexes (is not <em>sargable</em>). But doing this more efficiently isn't trivial in EF, see <a href="https://stackoverflow.com/q/26198860/861716">this</a>.</p>

