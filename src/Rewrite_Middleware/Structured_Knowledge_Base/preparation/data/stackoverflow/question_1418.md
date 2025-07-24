# string.Contains could not be translated
[Link to question](https://stackoverflow.com/questions/75406009/string-contains-could-not-be-translated)
**Creation Date:** 1675991055
**Score:** -2
**Tags:** c#
## Question Body
<p>This is my first post in this site.</p>
<p>I have a list of vehicles in my database and every vehicle has a Vin (License Plate Number, in example &quot;6TRJ244&quot;, it is a string value).</p>
<p>I receive a list of search values, in example &quot;A&quot;, &quot;B&quot;,&quot;J&quot;</p>
<p>I need to filter the vehicles which Vin Contains one of the search values.
In example if I have three vehicles with Vin: Vehicle1_Vin = &quot;123AJ&quot;, Vehicle2_Vin = &quot;123BJ&quot;, Vehicle3_Vin = &quot;777CR&quot;</p>
<p>If I receive as search values &quot;X&quot;, &quot;A&quot;,&quot;C&quot; I should return Vehicles 1 and 3</p>
<p>With LINQ I am trying to do something like this</p>
<pre><code>var searchParams = new List&lt;string&gt;() { &quot;A&quot;, &quot;B&quot;, &quot;C&quot;};

vehicles = vehicles.Where((vehicle) =&gt; searchParams.Any((searchParam) =&gt; vehicle.Vin.Contains(searchParam)));
</code></pre>
<p>But I receive this error message</p>
<p>&quot;System.InvalidOperationException: The LINQ expression 'searchParam =&gt; EntityShaperExpression:
ProjectAlpha.BusinessObjects.Models.Vehicle
ValueBufferExpression:
ProjectionBindingExpression: EmptyProjectionMember
IsNullable: False
.Vin.Contains(searchParam)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.&quot;</p>
<p>Thanks ins advance!</p>

## Answers
### Answer ID: 75438114
<p>It is not clear what collection type vehicles variable is so better introduce new variable or transfer IEnumerable to same type as source collection (ToArray/ToList etc):</p>
<pre><code>var searchParams = new List&lt;string&gt;() { &quot;A&quot;, &quot;B&quot;, &quot;C&quot;};
var filtered = vehicles.Where(vehicle =&gt; searchParams.Any(vehicle.Vin.Contains));
</code></pre>

### Answer ID: 75406857
<p>You could try use functions if you are using net core try with something like this</p>
<pre><code>IQueryable&lt;T&gt; nightClub = nightClub.Where(nc =&gt; EF.Functions.Like(nc.Name, &quot;%Dfox%&quot;);
</code></pre>

