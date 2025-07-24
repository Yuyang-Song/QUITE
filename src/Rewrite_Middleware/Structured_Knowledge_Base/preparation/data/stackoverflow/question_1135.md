# How to eliminate user-defined duplicate rows returned in an SQL query?
[Link to question](https://stackoverflow.com/questions/60532348/how-to-eliminate-user-defined-duplicate-rows-returned-in-an-sql-query)
**Creation Date:** 1583345765
**Score:** 0
**Tags:** sql, db2
## Question Body
<p>In my DB2 database I have some information about locations. I wrote a query for a DB2 table, called TABLEONE, to return some items I need for a report:</p>

<pre><code>SELECT LOCATION, TIMESTAMP, LASTNAME, CUSTOMER_ID, REASON, Info1, Info2, Info3 FROM TABLEONE
</code></pre>

<p>Six unique rows were returned:</p>

<pre><code> +------------+----------------------------+----------+-------------+------------+-------+--------------+-------+
| LOCATION   | TIMESTAMP                  | LASTNAME | CUSTOMER_ID | REASON     | Info1 | Info2        | Info3 |
+------------+----------------------------+----------+-------------+------------+-------+--------------+-------+
| FrontDoor  | 2020-02-18 14:00:00.000000 | Smith    | 122         | Dropoff    | 1     | Apple        | Dog   |
+------------+----------------------------+----------+-------------+------------+-------+--------------+-------+
| FrontDoor  | 2020-02-19 11:00:00.000000 | Smith    | 122         | Dropoff    | 3     | Pear         | Cat   |
+------------+----------------------------+----------+-------------+------------+-------+--------------+-------+
| Kitchen    | 2020-02-19 17:00:00.000000 | Smith    | 122         | Eat        | 3     | Grapes       | Cat   |
+------------+----------------------------+----------+-------------+------------+-------+--------------+-------+
| Bathroom   | 2020-02-19 19:00:00.000000 | Smith    | 122         | Bio        | 2     | Pear         | Cat   |
+------------+----------------------------+----------+-------------+------------+-------+--------------+-------+
| FrontDoor  | 2020-02-19 11:00:00.000000 | Jones    | 123         | Dropoff    | 1     | Tomato       | Dog   |
+------------+----------------------------+----------+-------------+------------+-------+--------------+-------+
| LivingRoom | 2020-02-19 12:00:00.000000 | Jones    | 123         | Television | 3     | Dragon Fruit | Pear  |
+------------+----------------------------+----------+-------------+------------+-------+--------------+-------+
</code></pre>

<p>I need the LOCATION, LASTNAME, CUSTOMER_ID and REASON to establish a unique row and need to return only one row with the largest timestamp. I also need all other rows: Info1, Info2 and Info3 returned in the SELECT statement.</p>

<p>In other words, how do I rewrite the query to obtain this result?:</p>

<pre><code> +------------+----------------------------+----------+-------------+------------+-------+--------------+-------+
| LOCATION   | TIMESTAMP                  | LASTNAME | CUSTOMER_ID | REASON     | Info1 | Info2        | Info3 |
+------------+----------------------------+----------+-------------+------------+-------+--------------+-------+
| FrontDoor  | 2020-02-19 13:00:00.000000 | Smith    | 122         | Dropoff    | 1     | Apple         | Dog   |
+------------+----------------------------+----------+-------------+------------+-------+--------------+-------+
| Kitchen    | 2020-02-19 17:00:00.000000 | Smith    | 122         | Eat        | 3     | Grapes       | Cat   |
+------------+----------------------------+----------+-------------+------------+-------+--------------+-------+
| Bathroom   | 2020-02-19 19:00:00.000000 | Smith    | 122         | Bio        | 2     | Pear         | Cat   |
+------------+----------------------------+----------+-------------+------------+-------+--------------+-------+
| FrontDoor  | 2020-02-19 11:00:00.000000 | Jones    | 123         | Dropoff    | 1     | Tomato       | Dog   |
+------------+----------------------------+----------+-------------+------------+-------+--------------+-------+
| LivingRoom | 2020-02-19 12:00:00.000000 | Jones    | 123         | Television | 3     | Dragon Fruit | Pear  |
+------------+----------------------------+----------+-------------+------------+-------+--------------+-------+
</code></pre>

<p>Thanks,
Matt</p>

## Answers
### Answer ID: 60533725
<p>Try this:</p>

<pre><code>/*
WITH TABLEONE (LOCATION, TIMESTAMP, LASTNAME, CUSTOMER_ID, REASON, Info1, Info2, Info3) AS 
(
VALUES
  ('FrontDoor  ', '2020-02-18 14:00:00.000000', 'Smith', 122, 'Dropoff    ', 1, 'Apple        ', 'Dog ')
, ('FrontDoor  ', '2020-02-19 11:00:00.000000', 'Smith', 122, 'Dropoff    ', 3, 'Pear         ', 'Cat ')
, ('Kitchen    ', '2020-02-19 17:00:00.000000', 'Smith', 122, 'Eat        ', 3, 'Grapes       ', 'Cat ')
, ('Bathroom   ', '2020-02-19 19:00:00.000000', 'Smith', 122, 'Bio        ', 2, 'Pear         ', 'Cat ')
, ('FrontDoor  ', '2020-02-19 11:00:00.000000', 'Jones', 123, 'Dropoff    ', 1, 'Tomato       ', 'Dog ')
, ('LivingRoom ', '2020-02-19 12:00:00.000000', 'Jones', 123, 'Television ', 3, 'Dragon Fruit ', 'Pear')
)
*/
SELECT A.LOCATION, A.TIMESTAMP, A.LASTNAME, A.CUSTOMER_ID, A.REASON, A.Info1
—-, A.Info2
, A.Info3
FROM
(
SELECT T.*, ROWNUMBER() OVER(PARTITION BY LOCATION, LASTNAME, CUSTOMER_ID, REASON ORDER BY TIMESTAMP DESC) RN_  
FROM TABLEONE T
) A
—- JOIN MYTAB B ON ...
WHERE A.RN_=1;
</code></pre>

### Answer ID: 60532400
<p>Use <code>lag()</code>:</p>

<pre><code>select timestamp, location, lastname, customerid, reason
from (select t.*,
             lag(timestamp) over (partition by location, lastname, customerid, reason) as prev_timestamp_llcr
      from t
     ) t
where date(prev_timestamp_llcr) &lt;&gt; date(timestamp) or
      prev_timestamp_llcr is null;
</code></pre>

<p>EDIT:</p>

<p>If you only wanted to keep one record per day, you could use aggregation:</p>

<pre><code>select min(timestamp) as timestamp, location, lastname, customerid, reason
from t
group by date(prev_timestamp_llcr), location, lastname, customerid, reason
</code></pre>

