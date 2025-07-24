# MySQL &amp; Memcached for large datasets?
[Link to question](https://stackoverflow.com/questions/11809266/mysql-memcached-for-large-datasets)
**Creation Date:** 1344089273
**Score:** 0
**Tags:** mysql, sql, dataset, memcached
## Question Body
<p>For a customer I am currently investigating improvements to their database structure. </p>

<p>My customer offers holiday rentals on their website. 
On their front page they have a search function wich sends a query to a MySQL database architecture (Master-Master setup) that answers that query with all the holiday rentals that the customer is interested in. </p>

<p>Due to the growth of the company and the increasing load on their servers the search query's are currently running up to 10+ seconds. Mainly because the query's end with an ORDER BY which causes MySQL to create a temp table and sort all the data, an average search query can return up to 20k holiday homes. 
Ofcourse one of the things we are doing is investigating the query's, rewriting them and putting indexes where needed. Unfortunately we are unable to get allot more performance under these circumstances. 
That's why we are looking into implementing Memcached on top of MySQL to cache these large datasets in memory for faster retrieval. Unfortunately the datasets that the query's return are quite large wich makes Memcached not that effective at this point. The array that MySQL returns are currently about 15k rows with about 60 values per row.
The reason Memcached is interesting is because we want to drastically improve the search function, and lowering the load on the MySQL platform. This would make it more scalable. </p>

<p>I am wondering if there is anyone that is familair with (longterm) caching MySQL data in Memcached and making it more effective for large datasets?</p>

<p>Thanks a bunch!</p>

## Answers
### Answer ID: 11809555
<p>Memcache is for storing key-value pairs, not for large sets of data. Will it work? Yes. Of course it will. But with how much data you guys are going to throw at it, you're going to run out of memory very soon and end up hitting the database anyway with how often your search results may change. And remember that just because it's memcache doesn't mean it doesn't have to go through web sockets to a (most likely) different machine. Your problem seems to be that you're using MySQL for something it was never designed well for, which is its use as a search engine. No matter how many things you optimize, all you're doing is raising the ceiling an inch at a time.</p>

<p>I could take this post in a "you need to optimize MySQL parameters so that it doesn't have to create those temp tables" direction, but I'm going to assume you've already looked into that and keep going.</p>

<p>My recommendation is that you implement something on top of MySQL to handle the searching. In my own quest for fast searching, these are the solutions I gave the most weight to:</p>

<p>Sphinx: <a href="http://sphinxsearch.com" rel="nofollow">http://sphinxsearch.com</a><br>
Solr: <a href="http://lucene.apache.org/solr" rel="nofollow">http://lucene.apache.org/solr</a><br>
Elasticsearch: <a href="http://www.elasticsearch.org" rel="nofollow">http://www.elasticsearch.org</a></p>

<p>You'll find plenty of resources here on StackOverflow for which of those is better and faster and what not. For our purposes, we picked Elasticsearch for one of our projects and Solr for another.</p>

