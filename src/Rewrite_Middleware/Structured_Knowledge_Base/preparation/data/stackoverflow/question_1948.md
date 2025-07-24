# Improving query performance/rewriting query to be faster on MySQL
[Link to question](https://stackoverflow.com/questions/13127216/improving-query-performance-rewriting-query-to-be-faster-on-mysql)
**Creation Date:** 1351533853
**Score:** 2
**Tags:** mysql, sql
## Question Body
<p>I have a couple of queries that run very slowly (several minutes) with the data currently in my database, and I'd like to improve their performance. Unfortunately they're kind of complex so the info I'm getting via google isn't enough for me to figure out what indexes to add or if I need to rewrite my queries or what... I'm hoping someone can help. I don't <em>think</em> they should be this slow, if things were set up properly.</p>

<p>The first query is: </p>

<pre><code>SELECT i.name, i.id, COUNT(c.id) 
FROM cert_certificates c 
JOIN cert_histories h ON h.cert_certificate_id = c.id 
LEFT OUTER JOIN inspectors i ON h.inspector_id = i.id
LEFT OUTER JOIN cert_histories h2 
  ON (h2.cert_certificate_id = c.id AND h.date_changed &lt; h2.date_changed)
WHERE (h.cert_status_ref_id = ? OR h.cert_status_ref_id = ?) 
  AND h2.id IS NULL
GROUP BY i.id, i.name
ORDER BY i.name</code></pre>

<p>The second query is:</p>

<pre><code>SELECT l.letter, c.number
FROM cert_certificates c 
JOIN cert_type_letter_refs l ON c.cert_type_letter_ref_id = l.id
JOIN cert_histories h ON h.cert_certificate_id = c.id
LEFT OUTER JOIN cert_histories h2 
  ON (h2.cert_certificate_id = c.id AND h.date_changed &lt; h2.date_changed)
WHERE h.cert_status_ref_id = ? 
  AND h2.id IS NULL 
  AND h.inspector_id = ?
ORDER BY l.letter, c.number
</code></pre>

<p>The cert_certificates table contains nearly 19k records as does the cert_histories table (although in the future this table is expected to grow to approximately 2-3x the size of the cert_certificates table). The other tables are all quite small; less than 10 records each.</p>

<p>The only indexes right now are on id for each table and on cert_certificates.number. I read in a couple of places (e.g. <a href="https://stackoverflow.com/questions/3658859/when-to-add-what-indexes-in-a-table-in-rails">here</a>) to add indices for foreign keys, but in the case of the cert_histories table that'd be nearly all the columns (cert_certificate_id, inspector_id, cert_status_ref_id) which is also <a href="https://stackoverflow.com/questions/5447987/why-cant-i-simply-add-an-index-that-includes-all-columns">not advisable</a> (according to some of the answers on that question e.g. Markus Winand's), so I'm kinda lost.</p>

<p>Any help would be greatly appreciated.</p>

<p>ETA: The results from EXPLAIN on the first query are (sorry for the hideous formatting; I'm using SQLyog which presents it in a nice table but it seems StackOverflow doesn't support tables?):</p>

<pre>id select_type table   type    possible_keys   key key_len ref rows    Extra
1   SIMPLE  h   ALL NULL    NULL    NULL    NULL    19740   Using where; Using temporary; Using filesort
1   SIMPLE  i   ref index_inspectors_on_id  index_inspectors_on_id  768 marketing_development.h.inspector_id    1   
1   SIMPLE  c   ref index_cert_certificates_on_id   index_cert_certificates_on_id   768 marketing_development.h.cert_certificate_id 91  Using where; Using index
1   SIMPLE  h2  ALL NULL    NULL    NULL    NULL    19740   Using where</pre>

<p>Second query:</p>

<pre>id select_type table   type    possible_keys   key key_len ref rows    Extra
1   SIMPLE  h   ALL NULL    NULL    NULL    NULL    19795   Using where; Using temporary; Using filesort
1   SIMPLE  c   ref index_cert_certificates_on_id   index_cert_certificates_on_id   768 marketing_development.h.cert_certificate_id 91  Using where
1   SIMPLE  l   ALL index_cert_type_letter_refs_on_id   NULL    NULL    NULL    5   Using where; Using join buffer
1   SIMPLE  h2  ALL NULL    NULL    NULL    NULL    19795   Using where</pre>

## Answers
### Answer ID: 13127310
<p>You should create indices on your join fields:</p>

<pre><code>cert_certificates.cert_type_letter_ref_id
cert_histories.cert_certificate_id
cert_histories.date_changed
cert_histories.inspector_id
</code></pre>

