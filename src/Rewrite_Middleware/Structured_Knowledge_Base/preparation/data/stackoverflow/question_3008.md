# SQLAlchemy query works on SQLite but gives error on PostgreSQL: Column must appear in the GROUP BY clause or be used in an aggregate function
[Link to question](https://stackoverflow.com/questions/62140252/sqlalchemy-query-works-on-sqlite-but-gives-error-on-postgresql-column-must-appe)
**Creation Date:** 1591042276
**Score:** 0
**Tags:** python, postgresql, flask, sqlalchemy
## Question Body
<p>I have the following SQLAlchemy query that joins two tables, selects a number of exsisting columns and calcultes two more based on sum and count functions. When testing on a local SQLite database the query works just fine, but when I run it on my Heroku server which uses a PostgreSQL database I get the following error:</p>

<p><code>Column Book.firstname_sold must appear in the GROUP BY clause or be used in an aggregate function</code></p>

<p>The query looks like this:</p>

<pre><code>book_list = db.session.query(Receipt.id,
                               Book.firstname_sold,
                               Book.lastname_sold,
                               Book.email_sold,
                               Book.sold_date,
                               Book.street_sold,
                               Book.number_sold,
                               Book.postalcode_sold,
                               Book.city_vsold,
                               func.sum(func.cast(func.replace(Book.price_sold, ",", "."), Integer)).label("price"),
                               func.count(Book.id).label("count_books"))\
    .join(Book).filter(Receipt.user_id == current_user.id).group_by(Receipt.id)
</code></pre>

<p>How would I rewrite this query so that it works both on SQLite and PostgreSQL?</p>

