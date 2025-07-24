# HQL diff 2 date in days
[Link to question](https://stackoverflow.com/questions/33517167/hql-diff-2-date-in-days)
**Creation Date:** 1446626300
**Score:** 0
**Tags:** java, hibernate, postgresql, hql
## Question Body
<p>I write right SQL query:</p>

<pre><code>SELECT i, (i.sme_end - '2015-09-10') 
FROM Incidents i 
WHERE (i.sme_end - '2015-09-10') &lt;= 100 
ORDER BY ('2015-09-10' - i.sme_end)
</code></pre>

<p>But when I rewrite this query on HQL:</p>

<pre><code>java.util.Date currentDate = new java.util.Date(System.currentTimeMillis());
int days = 100;
session.createQuery("SELECT i, (i.smeEnd - :currentDate) "+
                "FROM IncidentsEntity i " +
                "WHERE (i.smeEnd - :currentDate) &lt;= :days " +
                "ORDER BY (i.smeEnd - :currentDate)")
                .setParameter("days", days)
                .setParameter("currentDate", currentDate);
</code></pre>

<p>I get ClassCastException: java.lang.Integer cannot be cast to java.util.Date</p>

<p>Where do I do mistake?
Database Postgresql 9.4</p>

## Answers
### Answer ID: 33518333
<p>tray to cast  (i.smeEnd - :currentDate) to integer in where clause</p>

<p>(i.smeEnd - :currentDate) ::integer &lt;= :days</p>

<p>or as cast ...  </p>

<p>cast ((i.smeEnd - :currentDate) as integer) &lt;= :days</p>

<p>if i'm not wrong, something similar did happen to college of mine a while ago. something with java checking passed parameter conditions, it checks ":currentDate) &lt;= :days" conversions from other data types, pre checking this condition and assuming that both parameters must be dates ignoring that bracket,   cant remember details . i rarely work with java, nor this is my homelanguage<br>
but hope this helps</p>

<p>edited 2015-11-06</p>

<p>sorry, cant comment yet not enough respect points :)
to ansver your coment</p>

<p>"What different between cast ((i.smeEnd - :currentDate) as integer) and EXTRACT(EPOCH FROM date_trunc('day', age(i.smeEnd, :currentDate))) / 60 / 60 / 24 ? Two variant are working" </p>

<p>you must understand, both are working because query syntax is different. 
problem occurs with java (hibernate?) query parser is a bit "smart" , pre checking if query is all right, it finds in the query a condition with 2 parameters ":currentDate) &lt;= :days" and fails at it, because it tries to precheck if condition is valid, dont know the details, this same problem can occur when you have some other conditions with  different parameter types next to each other which logic encapsulated with brackets.     </p>

<p>if you put anything  between ":currentDate  [here] ) or [here] &lt;= :days" that query will work for you, I bet that if you switch those two values 
 (i.smeEnd - :currentDate) &lt;= :days
to </p>

<p>(- :currentDate + i.smeEnd ) &lt;= :days</p>

<p>that query will work too</p>

### Answer ID: 33518908
<p>Unfortunately, Hibernate does not handle date/time operators well enough (it usually does not understand, what type can they return). In your case, this means it sees the <code>(i.smeEnd - :currentDate)</code> expression as a <code>timestamp</code>.</p>

<p>To overcome this limitation, you can tweak your HQL in these ways:</p>

<ul>
<li>In <code>WHERE</code>, just do some math<br>
<code>(i.smeEnd - :currentDate) &lt;= :days</code> becames <code>i.smeEnd &lt;= DATE(:currentDate) + :days</code> (note that <code>:currentDate</code> binds as <code>timestamp</code>, not <code>date</code>).</li>
<li>In <code>ORDER BY</code>, just remove the constant part (as that won't effect ordering at all)<br>
<code>(i.smeEnd - :currentDate)</code> becames <code>i.smeEnd</code></li>
<li>In <code>SELECT</code>, well that one won't be so obvious. If you use <code>PostgreSQL81Dialect</code> (or some dialect, which extends that), <code>HQL</code> will understand the <code>age</code> function, so<br>
<code>(i.smeEnd - :currentDate)</code> becames<br>
<code>EXTRACT(EPOCH FROM date_trunc('day', age(i.smeEnd, :currentDate))) / 60 / 60 / 24</code></li>
</ul>

<p>The whole query:</p>

<pre><code>SELECT i, EXTRACT(EPOCH FROM date_trunc('day', age(i.smeEnd, :currentDate))) / 60 / 60 / 24
FROM IncidentsEntity i
WHERE i.smeEnd &lt;= (DATE(:currentDate) + :days)
ORDER BY i.smeEnd
</code></pre>

