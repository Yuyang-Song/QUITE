# Django ORM annotate performance
[Link to question](https://stackoverflow.com/questions/65506731/django-orm-annotate-performance)
**Creation Date:** 1609330216
**Score:** 4
**Tags:** python, django, django-rest-framework
## Question Body
<p>I'm using Django and Django REST Framework at work and we've been having some performance issues with couple endpoints lately. We started by making sure that the SQL part is optimized, no unnesecary N+1 queries, indexes where possible, etc.</p>
<p>Looking at the database part itself, it seems to be very fast (3 SQL queries total, under a second), even with larger datasets, but the API endpoint still took &gt;5 seconds to return. I started profiling the Python code using couple different tools and the majority of time is always spent inside the <code>annotate</code> and <code>set_group_by</code> functions in Django.</p>
<p><a href="https://i.sstatic.net/le0oG.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/le0oG.png" alt="debug_toolbar_screenshot" /></a></p>
<p>I tried Googling about <code>annotate</code> and performance, looking at Django docs, but there's no mention of it being a 'costly' operation, especially when used with the <code>F</code> function.</p>
<p>The <code>annotate</code> part of the code looks something like this:</p>
<pre><code>qs = qs.annotate(
    foo_name=models.F(&quot;foo__core__name&quot;),
    foo_birth_date=models.F(&quot;foo__core__birth_date&quot;),
    bar_name=models.F(&quot;bar__core__name&quot;),
    spam_id=models.F(&quot;baz__spam_id&quot;),
    spam_name=models.F(&quot;baz__spam__core__name&quot;),
    spam_start_date=models.F(&quot;baz__spam__core__start_date&quot;),
    eggs_id=models.F(&quot;baz__spam__core___eggs_id&quot;),
    eggs_name=models.F(&quot;baz__spam__eggs__core___name&quot;),
)

qs = (
    qs.order_by(&quot;foo_id&quot;, &quot;eggs_id&quot;, &quot;-spam_start_date&quot;, &quot;bar_name&quot;)
    .values(
        &quot;foo_name&quot;,
        &quot;foo_birth_date&quot;,
        &quot;bar_name&quot;,
        &quot;spam_id&quot;,
        &quot;spam_name&quot;,
        &quot;eggs_id&quot;,
        &quot;eggs_name&quot;,
    )
    .distinct()
)
</code></pre>
<p>The query is quite big, spans multiple relatonships, so I was sure that the problem is database related, but it doesn't seem to be. All the <code>select_related</code> and <code>prefetch_related</code> are there, indexes too.</p>
<p>I tried rewriting the code without <code>annotate</code> at all, but it didn't seem to help. I started wondering wether the time spent in <code>annotate</code> is really a red herring and it's only how the profiler sees it, but all profilers I tried showed the same thing.</p>
<p>While I feel like I know Django quite well and had success optimizing API endoints before, I'm not sure what 'thread' to pull in this case. I tried looking at Django internals, especially around <code>annotate</code> and <code>set_group_by</code> but couldn't pin point the time spent there. My last ditch effort will be trying to rewrite those couple endpoints with raw SQL, but I'd very much like to avoid that.</p>
<p>All help will be much appriciated : )</p>

