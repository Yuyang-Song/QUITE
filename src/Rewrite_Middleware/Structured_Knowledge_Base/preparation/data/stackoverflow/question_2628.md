# SQL between date with dd.mm.yyyy only matches on day
[Link to question](https://stackoverflow.com/questions/43496406/sql-between-date-with-dd-mm-yyyy-only-matches-on-day)
**Creation Date:** 1492606532
**Score:** 0
**Tags:** mysql, sql
## Question Body
<p>I want to use a Datepicker to select specific entries in my Database.</p>

<p>The Problem i face is that the entries i get as a reposnse from my query are only sorted for the day part of the date. </p>

<p>I use the date format (varchar field in database): </p>

<pre><code>*dd.mm.yyyy hh:mm ($date = date("Y-m-d") . ' ' . date("H:i");)* 
</code></pre>

<p>For example:</p>

<pre><code> 01.04.2016
 10.04.2016
 11.04.2016
 01.04.2017
 10.04.2017
 11.04.2017
</code></pre>

<p>The Query to get the entries:</p>

<pre><code>SELECT *
FROM order_date
WHERE date &gt;= '10.04.2017' AND date &lt;= '10.04.2017'
</code></pre>

<p>Now i expected to get only the to matching entries but
the result of the Query are all four table entries which start with day 10 or 11. Even two of them are in the year 2016.</p>

<p>As i saw in other posts the <em>between XX and YY</em> work if the date is set with yyyy-mm-dd or yyyymmdd but the problem is that i got a database with around 20k entries on which i need a datepicker so i would prefer to use the givin format of the date without rewriting all entries.</p>

<p>Is there a possibilty to get a datepicker between with dd.mm.yyyy format aswell?</p>

<p>Any help highly appriciated</p>

## Answers
### Answer ID: 43496735
<p>How about something around this idea ?</p>

<pre><code>SELECT * 
FROM Mytable WHERE date
                 BETWEEN CONVERT(datetime,'10.04.2017',104 ) 
                     AND CONVERT(datetime,'10.04.2017',104 )
</code></pre>

### Answer ID: 43496574
<p>Use <a href="https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_str-to-date" rel="nofollow noreferrer">STR_TO_DATE</a> function may help.</p>

<pre><code>STR_TO_DATE('10.04.2017','%d.%m.%Y')
</code></pre>

### Answer ID: 43496546
<p>Try something like this,</p>

<pre><code>STR_TO_DATE('10.04.2017', '%d.%m.%Y')

SELECT *
FROM order_date
WHERE date &gt;= STR_TO_DATE('10.04.2017', '%d.%m.%Y') AND date &lt;= STR_TO_DATE('10.04.2017', '%d.%m.%Y')
</code></pre>

### Answer ID: 43496474
<p>You can typecast the column as DATE, and use the ORDER BY clause.</p>

