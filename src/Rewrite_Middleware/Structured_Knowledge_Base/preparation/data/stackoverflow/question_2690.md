# How to join with sub-table using Django&#39;s ORM?
[Link to question](https://stackoverflow.com/questions/47734330/how-to-join-with-sub-table-using-djangos-orm)
**Creation Date:** 1512862119
**Score:** 0
**Tags:** django, postgresql, orm
## Question Body
<p>I've this query. Orders post records by last comment on post. This query works well with small tables. However, I've filled database with random data approximately 2M rows on comment table. Analyzed query with explain and saw that sequential scan is performed on Post table.</p>

<pre><code> Post.objects.extra(select={'last_update': 'select max(c.create_date) from comment_comment c where c.post_id = post_post.id'}).order_by('-last_update')
</code></pre>

<p>I've rewritten same query which is faster than current one. But I could not find a way to fit the query on django's orm. How can I rewrite it? If it is possible, I want to write it not using raw query as much as possible.</p>

<p>Regards. Thanks for any help. </p>

<pre><code>select
p.*,
t.last_update
from 
post_post p
join
( select c.post_id as pid, max(c.create_date) as last_update from comment_comment c group by pid) t
on p.id = t.pid
order by t.last_update desc
limit 50;
</code></pre>

## Answers
### Answer ID: 47806029
<p>If I make some assumptions about your Django model, it will look something like this:</p>

<pre><code>posts.objects
   .annotate(last_update=Max('comments__create_date'))
   .order_by('-last_update')[:50]
</code></pre>

<p>In Django, <a href="https://docs.djangoproject.com/en/2.0/ref/models/querysets/#annotate" rel="nofollow noreferrer">annotate</a> is your friend.</p>

