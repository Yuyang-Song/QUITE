# Implementing a NoSQL backend
[Link to question](https://stackoverflow.com/questions/30335432/implementing-a-nosql-backend)
**Creation Date:** 1432066969
**Score:** 2
**Tags:** python, django, nosql
## Question Body
<p>We have our own custom NoSQL storage system (sort of a document database), and we want a Django app above it.</p>

<p>I want to write a backend that will allow me to connect to our database. I don't care about the Django ORM because we have our own library for querying our database.</p>

<ol>
<li>What would be the simplest &amp; quickest way of doing this?   Rewriting
&amp; overriding the <code>django.db.backends.base</code> classes seems too much of
a hassle since we don't care about Django's ORM. What we basically
need is a way to keep a connection alive, and have the queries run
against the database from our <code>views.py</code> file</li>
<li>If we want to keep the Django auth system, should we rewrite that part so that  Django creates the User model etc. in our DB? Perhaps we should have two databases, a simple RDBMS for the authentication part, and the rest of the data in our custom database?</li>
</ol>

<p>Thanks in advance!</p>

