# Why am I getting error 1054 for this query ? Is there a more efficient way to write this query?
[Link to question](https://stackoverflow.com/questions/62763449/why-am-i-getting-error-1054-for-this-query-is-there-a-more-efficient-way-to-wr)
**Creation Date:** 1594064959
**Score:** 0
**Tags:** mysql, sql, subquery
## Question Body
<p>I am working with the <a href="https://i.sstatic.net/p7go2.png" rel="nofollow noreferrer">sakila database</a> and I need to write a query to find out all the films that are available in the country Canada.</p>
<pre><code>SELECT FILM_ID AS Film_id, TITLE AS Title 
FROM FILM
WHERE COUNTRY IN ( SELECT COUNTRY
                   FROM COUNTRY 
                   INNER JOIN CITY USING (COUNTRY_ID)
                   INNER JOIN ADDRESS USING (CITY_ID)
                   INNER JOIN STORE USING (ADDRESS_ID)
                   INNER JOIN INVENTORY USING (STORE_ID)
                   INNER JOIN FILM USING (FILM_ID)
                   WHERE COUNTRY = 'Canada')
ORDER BY Title ; 
</code></pre>
<p>When I try to run the above-written query, I am getting an Error 1054, unknown column 'country' in 'IN/ALL/ANY' Subquery.</p>
<p>I tried rewriting the entire query to ensure that I'm not getting this error because of invisible garbage characters (I don't know what invisible garbage characters in queries are, I read a stack overflow answer for a similar type of an error) and even after that, it doesn't work.</p>
<p>Am I getting this error because of the numerous join clauses in the subquery or is that fine? Is there a more efficient way to write this query?</p>
<p>Please let me know what is wrong with this query and do tell what are invisible garbage characters in queries.</p>

