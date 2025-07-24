# Rewriting this database access query to circumvent &#39;DISTINCT ON&#39; error, in Django
[Link to question](https://stackoverflow.com/questions/33324742/rewriting-this-database-access-query-to-circumvent-distinct-on-error-in-djang)
**Creation Date:** 1445731995
**Score:** 1
**Tags:** python, django, performance, postgresql, sqlite
## Question Body
<p>I have two very simple models:</p>

<pre><code>class Link(models.Model):
    description = models.TextField(validators=[MaxLengthValidator(500)])
    submitter = models.ForeignKey(User)
    submitted_on = models.DateTimeField(auto_now_add=True)

class Publicreply(models.Model):
    submitted_by = models.ForeignKey(User)
    answer_to = models.ForeignKey(Link)
    submitted_on = models.DateTimeField(auto_now_add=True)
    description = models.TextField(validators=[MaxLengthValidator(250)])
</code></pre>

<p>In the bid to get the latest <code>publicreply</code> for each <code>link</code> object, I tried this: <code>latest_replies = Publicreply.objects.filter(answer_to_id__in=link_ids).order_by('answer_to', 'submitted_on').distinct('answer_to')</code> where <code>link_ids</code> is a list of all <code>link</code> objects I needed in this particular case.</p>

<p>Problem is, I get a <strong>DISTINCT ON fields is not supported by this database backend</strong>. I'm on SQLite locally, Postgres in production. What's a way to re-write this query such that I get the same result? Note that I don't want to run a database query under a FOR loop - I've profiled that and the results are very unsavory. Is there a single query to get the job done?</p>

## Answers
### Answer ID: 33324882
<p>You could just take care of the <code>distinct</code> in memory.</p>

<pre><code>replies_by_link = {}
replies = Publicreply.objects.filter(answer_to_id__in=link_ids).order_by('answer_to', 'submitted_on')

for reply in replies:
    if reply.answer_to_id not in replies_by_link:
        replies_by_link[reply.answer_to_id] = reply
</code></pre>

<p>and then you can access all the replies via <code>replies_by_link.values()</code>.</p>

