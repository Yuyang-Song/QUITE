# Mysql vs Oracle XE vs Postgresql . Scalability and performance, which to chose?
[Link to question](https://stackoverflow.com/questions/13952182/mysql-vs-oracle-xe-vs-postgresql-scalability-and-performance-which-to-chose)
**Creation Date:** 1355918901
**Score:** 10
**Tags:** mysql, oracle-database, postgresql, database-performance
## Question Body
<p>I understand that this is very broad so let me give you the setting and be specific about my focus points.</p>

<p><strong>Setting:</strong></p>

<p>I am working with an existing PHP application using MYSQL. Tables almost all use the MYISAM engine and contain millions of rows for the most part. One of the largest tables uses an EAV design which is necessary but impacts on performance. The application was written to best leverage MYSQL cache. It requests a fair amount of requests per page load (partialy because of this) and is complex enough to have to go through most tables of the whole DB on each page load.</p>

<p>Pros: </p>

<ul>
<li>it's free </li>
<li>MYISAM tables support full text indexes which are important to the application</li>
</ul>

<p>Cons: </p>

<ul>
<li>With the way things are set up, MYSQL is limited to one CPU for the whole of the application. If one very demanding query is run (or server is under a lot of load) it will queue all others making the site unresponsive</li>
<li>MYSQL caching and lack of "WITH" or "INTERSECT" means we have to break our queries down to better use cache. Thus multiplying the number of queries made. For instance, using subqueries over multiple tables with millions of rows (even with decent indexing) turns out to be a big issue with the current/upcomming load and the constraint layed out in the point above (CPU usage)</li>
</ul>

<p>Feeling the need to scale up in the upcomming year, but not necessarily ready to pay for licensing right away, I've been thinking about rewriting the application and switching DBs.</p>

<p>The three options being considered are to either continue using mysql but with the INNODB engine, this way we can leverage more CPU power. Adapt to Oracle XE and get a license when we need to scale upwards of 4Gb database, 1Gb RAM or the 1 CPU limit (all of which we haven't hit yet). Or adapt to PostgreSQL</p>

<p><strong>So the questions are :</strong></p>

<ul>
<li>How would losing full text indexing impact performance in the three cases (does oracle or postgreSQL have an equivalent?)</li>
<li>How do oracle and postgreSQL leverage cache on subqueries, WITH, and UNION/INTERSECT statements</li>
<li>How do Oracle and PostgreSQL leverage multicore/cpu power (if/when we get an oracle license)</li>
</ul>

<p>I think that's already a lot to answer so I'll stop here. I don't mind simple/incomplete answers if there are links to compliment.</p>

<p>If you need any more information just let me know</p>

<p>Thanks in advance guys, the help is appreciated.</p>

## Answers
### Answer ID: 13953550
<p>PostgreSQL supports full text search and indexes. Details <a href="http://www.postgresql.org/docs/current/static/textsearch.html">here</a>.</p>

<p>And it can use any number of CPU cores. It creates separate process for every session + some additional support processes. Details <a href="http://www.postgresql.org/docs/current/static/tutorial-arch.html">here</a>.</p>

<p>PostgreSQL doesn't have built in query caching, but there are lots of open source utilities for this purpose.</p>

