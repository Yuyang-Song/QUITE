# Sqlalchemy from sql using subqueries
[Link to question](https://stackoverflow.com/questions/55309068/sqlalchemy-from-sql-using-subqueries)
**Creation Date:** 1553297502
**Score:** 0
**Tags:** python, sqlalchemy
## Question Body
<p>I have folowing sql code:</p>

<pre><code>SELECT t1.* 
FROM table1 t1 
INNER JOIN table2 t2
ON t1.id = t2.sample_id
GROUP BY t1.id
HAVING NOW() &gt; (SELECT end FROM table2 WHERE start = 
  max(t2.start)) + (t1.time::text||' minute')::interval
</code></pre>

<p>I need to rewrite this code in sqlalchemy like this:</p>

<pre><code>Table1.query
   .join(Table2, Table1.id == Table2.sample_id)
   .group_by(Table1.id)
   .having(
      datetime.datetime.now() &gt; ((Table2.query.filter_by(
         start= 
         (database.session.query(func.max(Table2.start)))
      )).first().end + 
         datetime.timedelta(minutes=Table1.query.filter_by(
            id=Table1.id
         ).first().frequency))).all()
</code></pre>

<p>This SQL query returns one line of data from the database, but my query in sqlalchemy returns empty dict. Can someone help me with my recreation of my SQL query?</p>

