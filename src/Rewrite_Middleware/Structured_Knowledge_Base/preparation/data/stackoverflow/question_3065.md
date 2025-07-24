# Optimize query to retreive calling clients information
[Link to question](https://stackoverflow.com/questions/64776164/optimize-query-to-retreive-calling-clients-information)
**Creation Date:** 1605039429
**Score:** 0
**Tags:** mysql, sql
## Question Body
<p>I have the following query which taking ages in mysql even while it's limited to 7 records.</p>
<pre><code>SELECT b.lastname, b.firstname, b.photo, b.id, b.phone_home, a.number, a.calldate 
FROM phonecalls as a 
LEFT JOIN  clients b ON instr(b.phone_home, a.number) 
OR instr(b.phone_work, a.number)
OR instr(b.phone_prive, a.number) 
GROUP BY a.call_id DESC
LIMIT 7
</code></pre>
<p><strong>phonecalls table:</strong></p>
<pre><code>call_id        int(11)  
number         varchar(50)
calldate       datetime
</code></pre>
<p>The phonecalls table contains more than 50.000 records.</p>
<p><strong>clients table:</strong></p>
<pre><code>id             bigint(20)   
lastname       varchar(200)
firstname      varchar(200)
photo          varchar(255)
phone_home     varchar(50)
phone_work     varchar(50)
phone_prive    varchar(50)
</code></pre>
<p>The clients table contains more than 2.500 records.</p>
<p>This query is used for call detection of the number calling the data center. When someone is calling, I am searching the clients database, to find if the calling number detected by the system, exists even as part of the 3 phone columns I have in the clients table.
This means if the number 123456 is calling and we have a client with phone_home 0035123456, we need to find it.</p>
<p>Even while limiting only to the last 7 phone calls, it's still super slow.</p>
<p>Any ideas how can I rewrite it to run faster?</p>

