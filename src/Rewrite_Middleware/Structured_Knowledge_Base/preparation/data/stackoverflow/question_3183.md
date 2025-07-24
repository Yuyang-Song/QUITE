# MySQL inner join with MAX(Date) and Grouping
[Link to question](https://stackoverflow.com/questions/70362867/mysql-inner-join-with-maxdate-and-grouping)
**Creation Date:** 1639567610
**Score:** 0
**Tags:** mysql, sql
## Question Body
<p>I have a MySQL database 8.0 that has a structure like below:</p>
<pre><code>Table1: Child
Id | Name   | EnrolmentId
1  | Nathan | 12345ABC
2  | James  | 56789BCD

Table2 : Enrolments
Id | EnrolmentId |StartDate |  Status | DateUpdated
1  | 12345ABC    |2021-12-01| PENDING | 2021-06-08T02:13:24
2  | 12345ABC    |2021-12-01| CONFIRM | 2021-12-15T04:56:45
3  | 56789BCD    |2021-12-02| CREATED | 2021-06-09T02:13:24
4  | 56789BCD    |2021-12-02| CONFIRM | 2021-12-16T04:56:45
</code></pre>
<p>I want to show only 1 row per enrolment with their latest Enrolment Status.</p>
<pre><code>EnrolmentID | Name   | StartDate |  Status | DateUpDated
12345ABC    | Nathan |2021-12-01 | CONFIRM | 2021-12-15T04:56:45
56789BCD    | James  |2021-12-02 | CONFIRM | 2021-12-16T04:56:45   
</code></pre>
<p>I am using the query below :</p>
<pre><code> SELECT e.enrolmentId,c.Name,e.startDate, e.Status,e.DateUpdated
    FROM child c INNER JOIN enrolment e ON c.EnrolmentId = e.enrolmentid
    GROUP BY e.enrolmentid ORDER BY c.Name; 
</code></pre>
<p>It works fine but because my database is in Azure MySQL 8.0xx and as per other suggestions I have set the server paramaters of sql_mode to full_group_by to off but still randomly I get this error till I restart the MySQL server. Below is the error I get.</p>
<pre><code>&quot;Expression #1 of SELECT list is not in GROUP BY clause and contains nonaggregated column
'mydatbase.c.Name' which is not functionally dependent on columns in GROUP BY clause;this is incompatible with sql_mode=only_full_group_by
</code></pre>
<p>Is there a way I can rewrite it so I can make it MySQL 8.0 friendly.</p>

## Answers
### Answer ID: 70363149
<pre class="lang-sql prettyprint-override"><code>WITH cte AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY EnrolmentId ORDER BY e.DateUpdated DESC) rn
    FROM child c 
    INNER JOIN enrolment e USING (EnrolmentId)
)
SELECT * 
FROM cte
WHERE rn = 1
ORDER BY Name;
</code></pre>
<p>Of course, replace asterisks with definite columns lists (ambiguous <code>Id</code> - assign proper aliases).</p>

