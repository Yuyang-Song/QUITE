# Is SQLAlchemy efficient when using it with raw SQL?
[Link to question](https://stackoverflow.com/questions/76502021/is-sqlalchemy-efficient-when-using-it-with-raw-sql)
**Creation Date:** 1687112971
**Score:** -2
**Tags:** python, postgresql, flask, sqlalchemy, flask-sqlalchemy
## Question Body
<p>I have a Flask web application with a Postgres database (&lt;10 million rows). I used SQLAlchemy to connect with Postgres, but queries that I have written in native SQLAlchemy are compiled to SQL that is too slow. The <a href="https://stackoverflow.com/questions/14754994/why-is-sqlalchemy-count-much-slower-than-the-raw-query">.count() method</a> is one of the main offenders here. I am planning to rewrite my queries. Pseudocode examples:</p>
<p>From <code>db.session.query(Table).filter(Table.column==condition).count()</code></p>
<p>To <code>db.session.execute(sqlalchemy.text(&quot;SELECT count(Table.id) from Table WHERE Table.column=condition&quot;)</code></p>
<p>My question is: can I do better than the execute-text construct? Will this still get wrapped in slow SQLAlchemy logic? Or is this as close to running raw SQL as it gets? How much faster can I tune my Flask-Postgres interaction? (I'm not interested in answers that involve additional third-party services.)</p>

## Answers
### Answer ID: 76502348
<p>I think in that case you might be better off using <code>func.count</code> like this: <code>db.session.query(func.count(OrmClass.id)).filter(OrmClass.column==condition).scalar()</code>.</p>
<p>The <code>.query()</code> interface has a lot of quirks because it was kept mostly backwards compatible.  I didn't even know it generates a subquery to perform count.  I'm sure there was/is a reason.</p>
<p>If you are using 1.4 with <code>future=True</code> or using 2+ then you can start using <code>select()</code> which I find way more consistent for everything.</p>
<p>You could write it with <code>select()</code> and <code>func.count()</code> like this, which is closer to actual <code>SQL</code>:</p>
<pre class="lang-py prettyprint-override"><code>from sqlalchemy.sql import select, func

count = db.session.execute(select(func.count(OrmClass.id)).where(OrmClass.column==condition)).scalar()
</code></pre>

