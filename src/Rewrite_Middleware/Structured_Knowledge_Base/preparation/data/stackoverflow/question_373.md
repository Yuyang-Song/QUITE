# Sqlite, SQLAlchemy
[Link to question](https://stackoverflow.com/questions/22998984/sqlite-sqlalchemy)
**Creation Date:** 1397163852
**Score:** 1
**Tags:** python, date, sqlite, sqlalchemy
## Question Body
<p>I'm currently creating a small application with PySide to learn the basics Python and GUIs. The this is I need to store some information into a small database. The information is mostly, name of account, price, date. And I need to be able to view it in a QTableView (Exemple : total of a certain account). I've manage to do it with SQLITE3 due to the code being really ugly, I've decided to rewrite it. One thing that I coudn't get to work is to select data from the table between 2 dates chosen by the user from the QDateEdit.</p>

<p>Now my question is, since I need to do some query depending on which date the user select with QDateEdit (Or any other widget better suited for this). Which database could handle the 'date' stuff easily. I might be wrong but storing date in SQLITE3 gave me a string 'yyyy-mm-dd'.</p>

<p>What would be the "best" way to acheive this.</p>

## Answers
### Answer ID: 22999860
<p>This can be done using <a href="http://docs.sqlalchemy.org/en/latest/dialects/sqlite.html#date-and-time-types" rel="nofollow">SQLAlchemy</a>.</p>

<blockquote>
  <h1>Date and Time Types</h1>
  
  <p>SQLite does not have built-in DATE, TIME, or DATETIME types, and pysqlite does not provide out of the box functionality for translating values between Python <em>datetime</em> objects and a SQLite-supported format. SQLAlchemy’s own <a href="http://docs.sqlalchemy.org/en/latest/core/type_basics.html#sqlalchemy.types.DateTime" rel="nofollow"><code>DateTime</code></a> and related types provide date formatting and parsing functionality when SQlite is used. The implementation classes are <a href="http://docs.sqlalchemy.org/en/latest/dialects/sqlite.html#sqlalchemy.dialects.sqlite.DATETIME" rel="nofollow"><code>DATETIME</code></a>, <a href="http://docs.sqlalchemy.org/en/latest/dialects/sqlite.html#sqlalchemy.dialects.sqlite.DATE" rel="nofollow"><code>DATE</code></a> and <a href="http://docs.sqlalchemy.org/en/latest/dialects/sqlite.html#sqlalchemy.dialects.sqlite.TIME" rel="nofollow"><code>TIME</code></a>. These types represent dates and times as ISO formatted strings, which also nicely support ordering. There’s no reliance on typical “libc” internals for these functions so historical dates are fully supported.</p>
</blockquote>

