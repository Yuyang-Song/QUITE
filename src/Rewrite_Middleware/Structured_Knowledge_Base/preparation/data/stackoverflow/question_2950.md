# Writing a LINQ query to fetch entities with a rolling calculation: The LINQ expression could not be translated
[Link to question](https://stackoverflow.com/questions/59924288/writing-a-linq-query-to-fetch-entities-with-a-rolling-calculation-the-linq-expr)
**Creation Date:** 1580088140
**Score:** 0
**Tags:** c#, linq, asp.net-core
## Question Body
<p>I am trying to grab all of the products in my database if they are within a certain distance of the user. For each row in my database, I want to calculate the distance between the user and the product, and return the product if and only if that value is less than the maximum distance allowed from the user.</p>

<pre><code> const double PIx = Math.PI;
        const double earth = 6378000.16;
        const double distanceFromUser = 50; // Change this later.

        double dLat = Convert.ToDouble(lat + (distanceFromUser / earth) * (180 / PIx));
        double dLng = Convert.ToDouble(lng + (distanceFromUser / earth) * (180 / PIx) / Math.Cos(Convert.ToDouble(lat) * PIx / 180));
        var maximumDistance = _calculator.DistanceBetweenPlaces(lat, lng, dLat, dLng);
        var paginatedProducts = products.Where(x =&gt; _calculator.DistanceBetweenPlaces(Convert.ToDouble(lng), Convert.ToDouble(lat), x.Longitude, x.Latitude) &lt; maximumDistance )
</code></pre>

<p>The idea is that I:</p>

<ol>
<li><p>Have the user's location (lat, lng)</p></li>
<li><p>Have the location of the product in a row in my table <code>(x.Longitude, x.Latitude)</code></p></li>
<li><p>I use <code>distanceBetweenPlaces</code> to determine if the distance between the user's location and the product's location is less than the <code>maximumDistance</code> allowed.</p></li>
</ol>

<p>Right now, the LINQ query says</p>

<blockquote>
  <p>could not be translated. Either rewrite the query in a form that can
  be translated, or switch to client evaluation explicitly by inserting
  a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or
  ToListAsync().</p>
</blockquote>

<p>How else can I write this?</p>

<p>Edit:</p>

<p>Here's the error if I try to turn it into a list:</p>

<pre><code>System.InvalidOperationException: The LINQ expression 'DbSet&lt;Product&gt;
.Where(p =&gt; ___calculator_0.DistanceBetweenPlaces(
    lon1: __ToDouble_1, 
    lat1: __ToDouble_2, 
    lon2: p.Longitude, 
    lat2: p.Latitude) &lt; __calc_3)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync(). See https://go.microsoft.com/fwlink/?linkid=2101038 for more information.
</code></pre>

<p>edit 2: </p>

<p>Here's the code for <code>DistanceBetweenPlaces</code> and the utility function it uses:</p>

<pre><code>/// &lt;summary&gt;
    /// cos(d) = sin(φА)·sin(φB) + cos(φА)·cos(φB)·cos(λА − λB), where φА, φB are latitudes and λА, λB are longitudes  Distance = d * R
    /// &lt;/summary&gt;
    /// &lt;param name="lon1"&gt;&lt;/param&gt;
    /// &lt;param name="lat1"&gt;&lt;/param&gt;
    /// &lt;param name="lon2"&gt;&lt;/param&gt;
    /// &lt;param name="lat2"&gt;&lt;/param&gt;
    /// &lt;returns&gt;&lt;/returns&gt;
    public double DistanceBetweenPlaces(double lon1, double lat1, double lon2, double lat2)
    {
        double R = 6371; // km

        double sLat1 = Math.Sin(ConvertToRadians(lat1));
        double sLat2 = Math.Sin(ConvertToRadians(lat2));
        double cLat1 = Math.Cos(ConvertToRadians(lat1));
        double cLat2 = Math.Cos(ConvertToRadians(lat2));
        double cLon = Math.Cos(ConvertToRadians(lon1) - ConvertToRadians(lon2));

        double cosD = sLat1 * sLat2 + cLat1 * cLat2 * cLon;

        double d = Math.Acos(cosD);

        double dist = R * d;

        return dist;
    }


    const double PIx = Math.PI;
    /// &lt;summary&gt;
    /// Convert degrees to Radians
    /// &lt;/summary&gt;
    /// &lt;param name="x"&gt;Degrees&lt;/param&gt;
    /// &lt;returns&gt;The equivalent in radians&lt;/returns&gt;
    public double ConvertToRadians(double x)
    {
        return x * PIx / 180;
    }
</code></pre>

<p>I ended up taking another approach for anyone this might help later - </p>

<pre><code>const double PIx = Math.PI;
        const double earth = 6378000.16;
        const double distanceFromUser = 80467.2;
        const double distanceFromUserHalved = distanceFromUser / 2; // Change this later.

        // This new approach adds half the distance of the radius to find a latitude upper and lower bound, and a longitude upper and lower bound.
        var TopLatBound = Convert.ToDouble(lat + (distanceFromUserHalved / earth) * (180 / PIx));
        var BottomLatBound = Convert.ToDouble(lat - (distanceFromUserHalved / earth) * (180 / PIx));
        var topLngBound = Convert.ToDouble(lng + (distanceFromUserHalved / earth) * (180 / PIx) / Math.Cos(Convert.ToDouble(lat) * PIx / 180));
        var bottomLngBound = Convert.ToDouble(lng - (distanceFromUserHalved / earth) * (180 / PIx) / Math.Cos(Convert.ToDouble(lat) * PIx / 180));

        var paginatedProducts = await PaginatedList&lt;Product&gt;.CreateAsync(products.Where(x =&gt; (x.Latitude &lt; TopLatBound &amp;&amp; x.Latitude &gt; BottomLatBound) &amp;&amp; (x.Longitude &lt; topLngBound &amp;&amp; x.Longitude&gt; bottomLngBound) &amp;&amp; x.IsArchived == false &amp;&amp; x.Decay &gt; 0)
            .OrderByDescending(x =&gt; x.DateTime), offset ?? 1, pageSize).ConfigureAwait(false);
</code></pre>

