# Query exceeded resource limits in Bigquery
[Link to question](https://stackoverflow.com/questions/51961853/query-exceeded-resource-limits-in-bigquery)
**Creation Date:** 1534923170
**Score:** 6
**Tags:** sql, google-bigquery
## Question Body
<p>In order to find the country for a specific IP address, I'm using the Maxmind IP address database. I've downloaded the database and imported it into Google BigQuery, so I can query it. In a separate table, I'm capturing IP-addresses from certain events in our systems. I would now like to join those two data sources.</p>

<p>The columns in the Maxmind database are as follows:</p>

<ul>
<li>start_ip_range   STRING  NULLABLE</li>
<li>end_ip_range STRING  NULLABLE</li>
<li>start_ip_num STRING  NULLABLE</li>
<li>end_ip_num   STRING  NULLABLE</li>
<li>country_code STRING  NULLABLE</li>
<li>country_name</li>
</ul>

<p>The columns in my event table are:</p>

<ul>
<li>request_id STRING    NULLABLE</li>
<li>ip_address STRING    NULLABLE</li>
</ul>

<p>As documented here (<a href="https://dev.maxmind.com/geoip/legacy/csv/" rel="nofollow noreferrer">https://dev.maxmind.com/geoip/legacy/csv/</a>) there is a way to get an integer representation of the ip address, so I can use it to query the ip address and retrieve the country_code or country_name.</p>

<p>I have now constructed the following query:</p>

<pre><code>SELECT
  p.*,
  g.country_code AS country_code
FROM
  `dev.event_v1` p
INNER JOIN
  `dev.geo_ip_countries` g
ON
  SAFE_CAST(SPLIT(p.ip_address, ".")[OFFSET(0)] AS NUMERIC)*16777216 + 
  SAFE_CAST(SPLIT(p.ip_address, ".")[OFFSET(1)] AS NUMERIC)*65536 + 
  SAFE_CAST(SPLIT(p.ip_address, ".")[OFFSET(2)] AS NUMERIC)*256 + 
  SAFE_CAST(SPLIT(p.ip_address, ".")[OFFSET(3)] AS NUMERIC)
BETWEEN 
  SAFE_CAST(g.start_ip_num AS INT64)
AND 
  SAFE_CAST(g.end_ip_num AS INT64)
LIMIT 100
</code></pre>

<p>And however this works when using a limit, it doesn't for constructing a view.</p>

<p>Two questions:
1. Is there a way to simplify the query
2. Google BigQuery throws an error when I try to return a large result set:</p>

<pre><code>Error: Query exceeded resource limits. 28099.974050246612 CPU seconds were used, and this query must use less than 5600.0 CPU seconds.
</code></pre>

<p>Any help is appreciated!</p>

<p><strong>Solution</strong>
Rewriting the query to the following worked and solved the resource limit issue too:</p>

<pre><code>SELECT
  p.*,
  g.country_code
FROM
  `dev.event_v1` p
INNER JOIN
  `dev.geo_ip_countries` g
ON 
  NET.IP_TRUNC(NET.SAFE_IP_FROM_STRING(p.ip_address),16) = NET.IP_TRUNC(NET.SAFE_IP_FROM_STRING(g.start_ip_range),16)
WHERE 
  NET.SAFE_IP_FROM_STRING(p.ip_address) 
  BETWEEN 
    NET.SAFE_IP_FROM_STRING(g.start_ip_range) 
  AND 
    NET.SAFE_IP_FROM_STRING(g.end_ip_range)
</code></pre>

## Answers
### Answer ID: 51968591
<p>Try below (BigQuery Standard SQL)   </p>

<pre><code>#standardSQL
SELECT
  p.* EXCEPT(ip_address_num),
  g.country_code AS country_code
FROM (
  SELECT *, 
    SAFE_CAST(SPLIT(p.ip_address, ".")[OFFSET(0)] AS NUMERIC)*16777216 + 
    SAFE_CAST(SPLIT(p.ip_address, ".")[OFFSET(1)] AS NUMERIC)*65536 + 
    SAFE_CAST(SPLIT(p.ip_address, ".")[OFFSET(2)] AS NUMERIC)*256 + 
    SAFE_CAST(SPLIT(p.ip_address, ".")[OFFSET(3)] AS NUMERIC) ip_address_num
  FROM `dev.event_v1` 
) p
INNER JOIN (
  SELECT 
    SAFE_CAST(g.start_ip_num AS INT64) start_ip_num, 
    SAFE_CAST(g.end_ip_num AS INT64) end_ip_num,
    country_code
  FROM `dev.geo_ip_countries`
) g
ON ip_address_num BETWEEN g.start_ip_num AND g.end_ip_num
</code></pre>

### Answer ID: 51964066
<p>So you're joining everything in <code>dev.event_v1</code> with <code>dev.geo_ip_countries</code> to get <code>dev.geo_ip_countries.country_code</code> for each row in <code>dev.event_v1</code>. I think you'd be interested in a left join.</p>

<p>You might be interested in testing if the conversions in the <a href="https://cloud.google.com/bigquery/docs/reference/standard-sql/functions-and-operators#netip_from_string" rel="nofollow noreferrer">net functions</a> can replace your math portion.</p>

<p>I don't know much about the contents of event_v1 requests or ip_addresses which could divide it, but I'm willing to bet there's a lot more rows there than there are in the geo_ip_countries. It's likely the bulk of your query time. Lets say you need to reduce that time about 6 fold. You should probably select a 6th of it to join and insert into a staging table, and repeat for the next 6ths in sequence.</p>

<p>I think using the <a href="https://cloud.google.com/bigquery/docs/reference/standard-sql/functions-and-operators#ntile" rel="nofollow noreferrer"><code>NTILE</code></a><code>(6)</code> would help you; maybe <code>OVER (ROWS UNBOUNDED PRECEDING) as nt</code>, not sure really. Then with a <code>nt = 1</code> in the where or join on clause.</p>

