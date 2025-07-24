# How to store/query co-ordiantes for calculating the distance between in meters?
[Link to question](https://stackoverflow.com/questions/66351937/how-to-store-query-co-ordiantes-for-calculating-the-distance-between-in-meters)
**Creation Date:** 1614173477
**Score:** 0
**Tags:** c#, spatial, nettopologysuite
## Question Body
<p>I am storing co-ordinates in my database like this</p>
<pre><code>var geometryFactory = NtsGeometryServices.Instance.CreateGeometryFactory(srid: 4326);

var point = geometryFactory.CreatePoint(new NetTopologySuite.Geometries.Coordinate(
    command.GeoCoordinate!.Longitude,
    command.GeoCoordinate!.Latitude));
</code></pre>
<p>I then need to query the db for any points within a certain distance of some co-ordinate, so I pass in an expression like this</p>
<pre><code>x =&gt; x.Location.Distance(inputPoint) &lt; distance
</code></pre>
<p>However, the distance returned just uses a normal pythagarus calculation, giving me a result in degrees rather than meters or miles.</p>
<p>I can manually calculate the distance in meters using haversine formula, but passing that in to my expression reults in a linq error:</p>
<blockquote>
<p>The LINQ expression  could not be translated. Either rewrite the query in a form that can be translated, or switch to ..</p>
</blockquote>
<p>How can I store/query this data such that I can pass a filter to ef core and get back a list of results within the given distance?</p>

## Answers
### Answer ID: 66365412
<p>Do you really need to work with EPSG:4326 (Lat/lon coordinate pairs, rather than projected coordinates like <a href="https://en.wikipedia.org/wiki/Universal_Transverse_Mercator_coordinate_system" rel="nofollow noreferrer">UTM</a>)?</p>
<p>If you could switch to UTM coordinates you would have meters directly in the database and wouldn't need to worry about conversion.</p>

