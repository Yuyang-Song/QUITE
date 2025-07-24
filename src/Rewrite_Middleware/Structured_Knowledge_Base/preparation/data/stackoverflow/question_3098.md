# MYSQL selecting records adjacent/ records that share a key with records that are easy to select
[Link to question](https://stackoverflow.com/questions/66280856/mysql-selecting-records-adjacent-records-that-share-a-key-with-records-that-are)
**Creation Date:** 1613750243
**Score:** -1
**Tags:** wordpress
## Question Body
<p>I've got a database of historical records that I'm working on.</p>
<p>In this db, I have a table of officers, a table of service records, a table of report-lines (each reports has many lines, which are transcribed individually).</p>
<p>When a report-line is put into a database, it creates rows in secondary tables for the ship, each officer mentioned, and the locations mentioned.</p>
<p>What I'm trying to do is find out how many other individual officers an officer worked with directly over say 15 years.</p>
<p>I'm pretty new to this, and I'm struggling with self joins. This is going to be in Wordpress, with php/wpdb, and I'm going to be feeding in a key. I would like the self join to:</p>
<p>find all the service records associated with the key I feed in, then find all the service records that have the same record_line_f_key as the first group, and then return those- but not including the ones that have the original officer's key.</p>
<p>I've looked at a couple of tutorials and I just can't get my head around the query structure.</p>
<p>UP to now I've been using nested for loops and I want to rewrite all my code to use joins instead to make the site more efficient.</p>
<p><a href="https://i.sstatic.net/x8J6V.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/x8J6V.png" alt="This is the structure of the table." /></a></p>

## Answers
### Answer ID: 66282108
<p>I managed to solve this with a bit of help from a friend and w3school</p>
<pre><code>SELECT DISTINCT t2.*,t3.report_date 
FROM officer_service_records t1, officer_service_records t2, reports_list t3
WHERE t1.officer_key = 'sample data'
AND t2.record_line_f_key = t1.record_line_f_key
AND t2.officer_key &lt;&gt; 'sample data'
AND t3.report_key = t2.report_key
</code></pre>
<p>I've actually modified this to also pull something from yet another table (and only return the unique records</p>

