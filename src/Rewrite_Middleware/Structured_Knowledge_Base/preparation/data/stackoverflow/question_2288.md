# Use sqlite3 for prototyping in a flask app
[Link to question](https://stackoverflow.com/questions/27787667/use-sqlite3-for-prototyping-in-a-flask-app)
**Creation Date:** 1420491043
**Score:** 0
**Tags:** python, sqlite, flask, sqlalchemy
## Question Body
<p>I am creating the prototype for a webapp using flask,
flask-sqlalchemy and some toy sqlite3 database.</p>

<p>I am using sqlite3 databases just for development purposes, but ideally
I would like to use some different SQL database in production.</p>

<p>What I am finding hard to understand is how to use SQLalchemy and sqlite3 in a way that I won't have to rewrite my queries once I use the production database.</p>

<p>A silly example: in mysql I can get a list of all the databases available (whose names I use to populate a "drop menu") using "SHOW DATABASES ", but in sqlite I have to do this by listing all the files in a directory.</p>

<p>What is the best way to prototype a webapp using sqlite3, without having to rewrite all the queries after?</p>

