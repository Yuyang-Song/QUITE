# Flask-SQLalchemy, Oracle, and pre-pending Owner to queries
[Link to question](https://stackoverflow.com/questions/60938035/flask-sqlalchemy-oracle-and-pre-pending-owner-to-queries)
**Creation Date:** 1585596339
**Score:** 0
**Tags:** python, oracle-database, flask, flask-sqlalchemy
## Question Body
<p>I've written a Flask app using flask-sqlalchemy.  My dev database username was the same as the oracle 'db owner'.  In production, they've given me a different read-only user.  The DBA has said I will need to prefix queries with the owner name in production.  </p>

<p>For example:<br>
A Flask-SQLAlchemy query might translate to <code>SELECT * from USERS;</code> in my Dev environment.<br>
In production, my queries are supposed to look like:  <code>SELECT * from &lt;owner&gt;.USERS;</code>.</p>

<p>How do I prepend the owner to all of my queries without having to rewrite everything?  or do I need to ditch the ORM queries and write them native?</p>

<p>I think this is the ultimate solution, but I don't know how to implement it with Flask-SQLAlchemy: 
<a href="https://stackoverflow.com/questions/49862366/sqlalchemy-how-to-specify-owner-in-oracle-database">Sqlalchemy - How to Specify Owner in Oracle database</a></p>

## Answers
### Answer ID: 60960318
<p>Use the <a href="https://cx-oracle.readthedocs.io/en/latest/api_manual/connection.html#Connection.current_schema" rel="nofollow noreferrer">cx_Oracle Connection.current_schema</a> setting.</p>

