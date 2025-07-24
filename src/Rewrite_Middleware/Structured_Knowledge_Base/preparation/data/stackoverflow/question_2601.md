# Availability tracking with Algolia
[Link to question](https://stackoverflow.com/questions/42138629/availability-tracking-with-algolia)
**Creation Date:** 1486648650
**Score:** 13
**Tags:** search, algolia
## Question Body
<p>I am working on an Airbnb-like website and I am in the process of rewriting our in-house, SQL-based search system with Algolia. It's been a really pleasant journey so far, as I have managed to remove a lot of legacy code and outsource it, with awesome results. However, there is one critical piece of our search system which I am not sure can be implemented with Algolia.</p>

<p>Internally, we store the availability/unavailability (and price) of each date for each asset as a single row in the database. This means our <code>availabilities</code> table looks like this:</p>

<pre><code>asset_id | date       | status      | price_cents
-------- | ---------- | ----------- | -----------
1        | 2017-02-09 | available   | 15000
1        | 2017-02-10 | available   | 15000
1        | 2017-02-11 | unavailable | NULL
1        | 2017-02-12 | available   | 20000
</code></pre>

<p>When a user searches for available properties, they enter a date range and, optionally, a price range.</p>

<p>What we're doing now is simply querying the <code>availabilities</code> table and making sure that all dates in the date range are available for that asset (i.e. the count of available dates is equal to the number of days in the range). If the user enters a price range, we also make sure that the average price for those dates is within the requested range. The SQL query is fairly complex, but this is what it does at the end of the day.</p>

<p>I have been trying to replicate this with Algolia, but couldn't find any documentation about a similar feature. In fact, I am facing two separate issues right now:</p>

<ul>
<li>I have no way to ensure all dates in the provided date range are available, because Algolia has little to no knowledge about associations, and</li>
<li>I have no way to calculate (and query) the average price for the provided date range, because it depends on user input (i.e. the date range).</li>
</ul>

<p>Is there a way to achieve this with Algolia? If not, is it feasible to use SQL or another tool in combination with Algolia to achieve the desired result? Of course, I could do all of this with Elasticsearch, but Algolia is so fast and easy that I'd hate to step away from it because of these issues.</p>

## Answers
### Answer ID: 42141753
<p>This use-case is definitely complex, and Algolia needs precomputed data in order to work.</p>

<hr>

<p><strong>Edit 2020 (better solution)</strong></p>

<p>In each item, you could simply store the list of days where the location is available, e.g.</p>

<pre class="lang-js prettyprint-override"><code>{
  name: "2 bedroom appartment",
  location: "Paris",
  availabilities: ['2020-04-27', '2020-04-28', '2020-04-30']
  price_cents: 30000
}
</code></pre>

<p>You could then, at search time, generate the list of all the availabilities you require your items to have, e.g. (available from April 28th to April 30th):</p>

<pre class="lang-js prettyprint-override"><code>index.search('', {
  filters: '' +
    'availabilities:2020-04-28 AND availabilities:2020-04-29 AND availabilities:2020-04-30 AND ' +
    'price_cents &gt;= ' + lowPriceRange + ' AND price_cents &lt;= ' + highPriceRange 
}) 
</code></pre>

<p>In this example, the record wouldn't match as it lacks <code>2020-04-29</code>.</p>

<hr>

<p>Another solution, which works more generically, but requires way more records:</p>

<p>I'm assuming there is a cap of the amount of days in advance you can book, I'll assume here it's 90 days.<br>
You could generate every date range possible inside those 90 days.<br>
This would mean generating <code>90 + 89 + ...</code> = <code>90 * 91 / 2</code> = <code>4095</code> date ranges.<br>
Then for each of those ranges, and each of the flats you're offering on your service, you could generate an object like this:</p>

<pre class="lang-coffee prettyprint-override"><code>{
  name: "2 bedroom appartment",
  location: "Paris",
  availability_range: "2017-02-09 -&gt; 2017-02-10",
  availability_start_timestamp: 10001000,
  availability_end_timestamp: 10002000,
  price_cents: 30000
}
</code></pre>

<p>With those objects, then searching for an date range would be as easy as:</p>

<pre class="lang-js prettyprint-override"><code>index.search('', {
  filters: '' +
    'availability_range:"' + startDate + ' -&gt; ' + endDate + '" AND ' +
    'price_cents &gt;= ' + lowPriceRange + ' AND price_cents &lt;= ' + highPriceRange 
}) 
</code></pre>

<p>You would only be indexing available time ranges, so this should greatly reduce the amount of objects, but it would still be probably huge.</p>

<p>Finally, the timestamps in the object would be here to know which ones to delete when a booking is made.
The call would be something like:</p>

<pre class="lang-js prettyprint-override"><code>index.deleteByQuery('', {
  filters: 'availability_start_timestamp &lt; ' + booking_end_timestamp + ' AND availability_end_timestamp &gt; ' + booking_start_timestamp
})
</code></pre>

