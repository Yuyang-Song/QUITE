# Rewrite SQL query using joins (or make it more efficient some other way)
[Link to question](https://stackoverflow.com/questions/32430963/rewrite-sql-query-using-joins-or-make-it-more-efficient-some-other-way)
**Creation Date:** 1441598906
**Score:** 0
**Tags:** sql, sqlite, join
## Question Body
<p>Is it possible to rewrite the following SQL query using JOIN(s) or make it in other way more efficient ?
I may be using SQLite (I can connect to few different databases), which means I cannot use RIGHT JOIN(s). The ellipsis (...) in the query below means that I can have many UNION(s) there.</p>

<p>I construct this query programmatically, because there is no other way in my case. I'm just trying to get the idea how I could rewrite it to make it more efficient. Any ideas ?
Thanks in advance.</p>

<pre><code>SELECT serial_nr, name, cert_type FROM certificates WHERE (cert_type&lt;3 AND
serial_nr IN
(
    SELECT DISTINCT serial_nr FROM certificates WHERE (cert_type&lt;3 AND (name LIKE 'george%' ))
    UNION
    SELECT DISTINCT serial_nr FROM ip_addresses WHERE ((address LIKE '192.168%' ))
    ....
));
</code></pre>

## Answers
### Answer ID: 32433310
<p>Try something like this;</p>

<pre><code>SELECT serial_nr, name, cert_type FROM certificates A 
inner join certificates B on A.serial_nr=B.serial_nr and B.name like'george%'
inner join ip_address C on A.serial_nr=C.serial_nr and C.Address like '192.168%'
...
WHERE A.cert_type&lt;3 
</code></pre>

