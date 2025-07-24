# how to provide False in raw SQL query
[Link to question](https://stackoverflow.com/questions/37016186/how-to-provide-false-in-raw-sql-query)
**Creation Date:** 1462319301
**Score:** 0
**Tags:** python, django, database, django-database
## Question Body
<p>I have inherited Django code that does a migration with a raw SQL query:</p>

<pre><code>INSERT INTO karaage_projectmembership ( ..., is_project_supervisor, ...) SELECT DISTINCT ..., '0', ...
</code></pre>

<p><code>is_project_supervisor</code> is a boolean. The full code is on <a href="https://github.com/Karaage-Cluster/karaage/blob/31aac391ea4824ff8a6e32e0b88345c8acc4aabb/karaage/migrations/0006_auto_karage4.py#L594" rel="nofollow noreferrer">github</a>.</p>

<p>This works for mysql and sqlite, but <a href="https://travis-ci.org/Karaage-Cluster/karaage/jobs/127420207#L852" rel="nofollow noreferrer">breaks with postgresql</a>:</p>

<pre><code>django.db.utils.ProgrammingError: column "is_project_supervisor" is of type boolean but expression is of type text
</code></pre>

<p>Looking in the git history, looks like in the past other values were tried but without success on <em>all</em> databases, such as <code>FALSE</code>, <code>0::bool</code>, <code>0</code>, <code>'f'</code>, <code>'0'</code>.</p>

<p>Is there any easy way of fixing this? Or do I need to rewrite the SQL to use the Django ORM (suspect this might be less efficient)?</p>

<p>This also has a <a href="https://github.com/Karaage-Cluster/karaage/issues/279" rel="nofollow noreferrer">ticket on github</a>.</p>

<p>Thanks</p>

