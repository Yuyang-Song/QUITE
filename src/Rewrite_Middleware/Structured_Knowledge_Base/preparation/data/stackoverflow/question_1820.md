# A database system for stat counting
[Link to question](https://stackoverflow.com/questions/9160616/a-database-system-for-stat-counting)
**Creation Date:** 1328534040
**Score:** 0
**Tags:** mysql, database, nosql, aggregation, counting
## Question Body
<p>My server generates huge amounts of transaction logs. Each record contains information about the referer URL, the user, the manufacturer and the related product. An example record might be as follows:</p>

<pre><code>{transaction_id: 1, url: "http://example.com/", user_agent: "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.77 Safari/535.7", manufacturer_id: 2, product_id: 3}
</code></pre>

<p>I store these logs only for a month, then I discard the old ones to make room for the new ones.</p>

<p>What I need is to answer questions like "How many times was Product-3 displayed on URL <a href="http://example.com/" rel="nofollow">http://example.com/</a> each day?" or "How many times did a user with Firefox 10 requested a product of Manufacturer-2 each day?". All reports are daily, but the ways of grouping may increase in time. Also, I should be able to store the data for years.</p>

<p><strong>What database system do you recommend to aggregate logs in flexible ways?</strong></p>

<p>I considered,</p>

<ul>
<li><strong>MySQL</strong>: Storage friendly and easy to archive, but requires altering tables and rewriting queries each time an aggregation was changed.</li>
<li><strong>CouchDB</strong>: Map-reduce approach is nice, but its revision system is not suitable for counting(isn't it?).</li>
<li><strong>Redis</strong>: Perfect for in-memory counting, but is hard to query and needs to fit all data to the memory.</li>
<li><strong>MongoDB</strong>: Easy to create new types of aggregations and perfect for on-disk counting, but it doesn't seem that much storage friendly and it doesn't seem as stable as MySQL and CouchDB either.</li>
</ul>

<p>I am inclined towards MongoDB. What do you think?</p>

## Answers
### Answer ID: 9161505
<p>You should look into Bigtable-like databases. Currently, there are two open-source implementations: HBase and Hypertable. (Disclaimer: i work for Hypertable). Analytics is a typical usage scenario.</p>

<p>In case of Hypertable, you get</p>

<ul>
<li>automatic timestamps for each inserted row</li>
<li>rows with a certain configurable age (i.e. 1 month) will be deleted automatically</li>
<li>a query language (similar to SQL)</li>
</ul>

<p>I'm sure HBase offers similar functionality.</p>

<p>Have a look at this tutorial - it shows how to query logs of web visitors by specifying time intervals and other predicates.
<a href="http://code.google.com/p/hypertable/wiki/HQLTutorial" rel="nofollow">http://code.google.com/p/hypertable/wiki/HQLTutorial</a></p>

