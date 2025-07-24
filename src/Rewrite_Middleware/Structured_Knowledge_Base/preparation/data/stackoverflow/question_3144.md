# Calculate distance with LINQ, problem &quot;could not be translated.&quot;
[Link to question](https://stackoverflow.com/questions/68536244/calculate-distance-with-linq-problem-could-not-be-translated)
**Creation Date:** 1627333032
**Score:** 1
**Tags:** c#, linq
## Question Body
<p>I am writing a query to compare a given coordinate with coordinates from the database and return only those at a given distance.
Unfortunately, an error like the one below is displayed.<br />
I used different libraries like GeoCoordniate, Coordinate, and it was always the same error.<br />
What am I doing wrong? Can it be done in some other way?</p>
<pre><code>[HttpGet(&quot;search&quot;)]
public async Task&lt;ActionResult&lt;IEnumerable&gt;&gt; GetSearched(
    [FromQuery] decimal? latitude,
    [FromQuery] decimal? longitude,
    [FromQuery] int? radius)
{
    var punkt = new Point((double)latitude, (double)longitude) { SRID = 4326 };
    var _term = from l in _context.Locations
        let punkt2 = new Point((double)l.Latitude, (double)l.Longitude) { SRID = 4326 }
        let dystans = punkt.Distance(punkt2)
        where dystans &lt;= radius
        select l;
    return await _term.ToListAsync();
}
</code></pre>
<p>Error description:</p>
<pre><code>System.InvalidOperationException: The LINQ expression 'DbSet&lt;Location&gt;()
    .Where(l =&gt; (Nullable&lt;double&gt;)__punkt_1.Distance(__p_0) &lt;= __p_2)' could not be translated.
</code></pre>
<p>Additional information: Translation of method 'NetTopologySuite.Geometries.Geometry.Distance' failed. If this method can be mapped to your custom function, see <a href="https://go.microsoft.com/fwlink/?linkid=2132413" rel="nofollow noreferrer">New feature topic: custom function mapping</a> for more information. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to <code>AsEnumerable</code>, <code>AsAsyncEnumerable</code>, <code>ToList</code>, or <code>ToListAsync</code>. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">Client vs. Server Evaluation</a> for more information.</p>

