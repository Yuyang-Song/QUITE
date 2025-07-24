# Werkzeug without ORM
[Link to question](https://stackoverflow.com/questions/4838528/werkzeug-without-orm)
**Creation Date:** 1296324555
**Score:** 1
**Tags:** python, orm, werkzeug
## Question Body
<p>How do I use the Werkzeug framework without any ORM like SQLAlchemy? In my case, it's a lot of effort to rewrite all the tables and columns in SQLAlchemy from existing tables &amp; data.</p>

<p>How do I query the database and make an object from the database output?</p>

<p>In my case now, I use Oracle with cx_Oracle. If you have a solution for MySQL, too, please mention it.</p>

<p>Thanks.</p>

## Answers
### Answer ID: 4881338
<p>maybe this is what i looking for <a href="http://www.sqlalchemy.org/trac/wiki/SqlSoup" rel="nofollow">http://www.sqlalchemy.org/trac/wiki/SqlSoup</a>
and ht*p://spyced.blogspot.com/2006/04/introducing-sqlsoup.html</p>

<p>so i don't have to declare the table to get the object</p>

<p>rp = db.bind.execute('select * from mupp')
a = rp.fetchall()
a[0].name</p>

<p>that's great...thanks for all inspiring response </p>

### Answer ID: 4842513
<p>SQLAlchemy supports reflection so you don't have to do that. Take a look at the <a href="http://www.sqlalchemy.org/docs/core/schema.html#sqlalchemy.schema.Table" rel="nofollow">autoload parameter of <code>Table</code></a>, <a href="http://www.sqlalchemy.org/docs/orm/extensions/declarative.html#using-a-hybrid-approach-with-table" rel="nofollow">you can even make this work with the ORM.</a></p>

### Answer ID: 4838669
<p>Is it a problem to use normal DB API, issue regular SQL queries, etc? cx_Oracle even has connection pooling biolt in to help you manage connections.</p>

