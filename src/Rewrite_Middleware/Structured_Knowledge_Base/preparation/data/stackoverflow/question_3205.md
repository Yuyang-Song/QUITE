# MYSQL Temporary table space
[Link to question](https://stackoverflow.com/questions/71353936/mysql-temporary-table-space)
**Creation Date:** 1646409276
**Score:** 0
**Tags:** mysql
## Question Body
<p>I am running this query:</p>
<pre><code>select CONCAT(&quot;2000&quot;,page_hits.email_id) as campaign_code ,
       page_hits.url,
       count(page_hits.url) as clicks, 
       count(page_hits.url) / ( SELECT read_count 
                                FROM emails 
                                WHERE emails.id = page_hits.email_id ) as clicks_percent
from page_hits 
where page_hits.email_id
group by page_hits.email_id,
      page_hits.url
</code></pre>
<p>and have recently started getting the error</p>
<pre><code>Error Code: 1114. The table '/rdsdbdata/tmp/#sql6061_11566_91' is full
</code></pre>
<p>MYSQL 8.0.25
Database size is 248GB total and the space on the server is 1TB.
8cpu with 64GB ram</p>
<p>Can I rewrite this to be better?  I can't see why it fails now when it worked before.</p>

