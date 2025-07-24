# Mysql Left outer join in my Query for optimize
[Link to question](https://stackoverflow.com/questions/30816229/mysql-left-outer-join-in-my-query-for-optimize)
**Creation Date:** 1434180774
**Score:** 0
**Tags:** mysql, sql
## Question Body
<p>I have two database table name called "tablestr table" and "restbookingtable":</p>

<p><strong>tablestr:</strong></p>

<p>str_id is primary key</p>

<p><img src="https://i.sstatic.net/h4uFL.png" alt="enter image description here"></p>

<p><strong>restbooking:</strong>
bookingsection_id is foreign key </p>

<p><img src="https://i.sstatic.net/2u8Pq.png" alt="enter image description here"></p>

<p>in booking table i storing str_id multiple values with comma separated and My query is </p>

<pre><code>SELECT `str_id` FROM (`rest_tablestr`) WHERE str_id NOT IN (
SELECT SUBSTRING_INDEX(SUBSTRING_INDEX(t.bookingsection_id, ",", n.n), ",", -1) value FROM rest_restaurantbooking t 
CROSS JOIN (
SELECT a.N + b.N * 10 + 1 n FROM (
SELECT 0 AS N
UNION ALL
SELECT 1
UNION ALL
SELECT 2
UNION ALL
SELECT 3
UNION ALL
SELECT 4
UNION ALL
SELECT 5 
UNION ALL 
SELECT 6 
UNION ALL
SELECT 7 
UNION ALL 
SELECT 8 
UNION ALL 
SELECT 9) a , (
SELECT 0 AS N
UNION ALL 
SELECT 1 
UNION ALL 
SELECT 2 
UNION ALL 
SELECT 3 
UNION ALL 
SELECT 4 
UNION ALL 
SELECT 5 
UNION ALL 
SELECT 6 
UNION ALL 
SELECT 7 
UNION ALL 
SELECT 8 
UNION ALL SELECT 9) 
b ORDER BY n ) n 
WHERE n.n &lt;= 1 + (LENGTH(t.bookingsection_id) -
LENGTH(REPLACE(t.bookingsection_id, ",", ""))) AND
t.res_id = 21 AND
t.booking_status not in ("cancelled","departed","noshow") AND
((t.bookingstart_time &lt;= "2015-06-12 19:45:00" AND t.bookingend_time &gt;= "2015-06-12 22:15:00") OR 
(t.bookingend_time &gt;= "2015-06-12 19:45:00" AND t.bookingend_time &lt;= "2015-06-12 22:15:00") OR
(t.bookingstart_time &gt;= "2015-06-12 19:45:00" AND t.bookingstart_time &lt;= "2015-06-12 22:15:00") OR 
(t.bookingstart_time &gt;= "2015-06-12 19:45:00" AND t.bookingend_time &lt;= "2015-06-12 22:15:00")) ) AND
`res_id` = '21' AND
`area_id` = '28' AND 
`wait_table` = 'no' AND
`availability` = 'yes';
</code></pre>

<p><strong>Result Set:</strong></p>

<p><img src="https://i.sstatic.net/Inhlh.png" alt="enter image description here"></p>

<p>Can any body help me to rewrite query with left outer join or can be optimize query. </p>

