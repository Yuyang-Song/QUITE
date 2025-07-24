# Grouping result set in infobright
[Link to question](https://stackoverflow.com/questions/19001287/grouping-result-set-in-infobright)
**Creation Date:** 1380101789
**Score:** 1
**Tags:** mysql, sql, infobright
## Question Body
<p>I am writing a program in java to fetch records from infobright database. Here are the table structure, query and the format of output I require.</p>

<p>Table structure:</p>

<pre><code>column name             type
------------          ----------
id                    integer
date                  integer
product_id            integer
search_engine_id      integer
visitor               integer
</code></pre>

<p>example query:</p>

<pre><code>select   date,
         product_id, 
         search_engine_id, 
         sum(visitor)
from     report
where    date in (201300910, 20130919)
group by search_engine_id, 
         product_id, 
         date
order by product_id, 
         date
</code></pre>

<p>The result set of the above query would be in the following format:</p>

<pre><code>+----------+-------------+----------------+------------------+
| date     | product_id | search_engine_id | sum(visitor)    |
+----------+-------------+----------------+------------------+
| 20130910 |      108   |              2 |                7  |
| 20130910 |      108   |              1 |                15 |
| 20130919 |      108   |              1 |                2  |
| 20130919 |      108   |              2 |                3  |
| 20130910 |      107   |              1 |                3  |
| 20130910 |      107   |              2 |                2  |
| 20130919 |      107   |              1 |                2  |
| 20130919 |      107   |              2 |                3  |
| 20130919 |      106   |              1 |                10 |
</code></pre>

<p>There are two types of search_engine_id, that is 1 and 2. </p>

<p>For a given day, one product_id can exist two times at max, i.e., one record for search_engine_id 1 and other record for search_engine_id 2. What I want is to group the result with respect to product_id. So it would look something like:</p>

<pre><code>+-------------------+-------------+----------------+------------------+
| date              | product_id | search_engine_id | sum(visitor)    |
+-------------------+-------------+----------------+------------------+
| 20130910,20130919 |      108   |        2,1,1,2 |      7,15,2,3     |
</code></pre>

<p>The main reason of doing this in the sql side is to make the data prepared for every product_id so that it will have less memory usage in java side. I have tried <code>group_contact</code> function but that seems to be not supported by infobright. Is there a way I can rewrite the query/make use of some other function to achieve this?  </p>

