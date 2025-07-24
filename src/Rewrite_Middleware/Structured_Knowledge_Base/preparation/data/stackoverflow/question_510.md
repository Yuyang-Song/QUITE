# Django queries are 40 times slower than identical Postgres queries?
[Link to question](https://stackoverflow.com/questions/29164393/django-queries-are-40-times-slower-than-identical-postgres-queries)
**Creation Date:** 1426847345
**Score:** 6
**Tags:** django, postgresql, django-debug-toolbar
## Question Body
<p>I am running Django 1.7 with Postgres 9.3, running with <code>runserver</code>. My database has about 200m rows in it or about 80GB of data. I'm trying to debug why the same queries are reasonably fast in Postgres, but slow in Django. </p>

<p>The data structure is like this:</p>

<pre><code>class Chemical(models.Model):
    code = models.CharField(max_length=9, primary_key=True)
    name = models.CharField(max_length=200)

class Prescription(models.Models):
    chemical = models.ForeignKey(Chemical)
    ... other fields
</code></pre>

<p>The database is set up with C collation and suitable indexes:</p>

<pre><code>                                   Table "public.frontend_prescription"
  Column       |          Type           |                             Modifiers
 id                | integer                 | not null default nextval('frontend_prescription_id_seq'::regclass)
 chemical_id       | character varying(9)    | not null
 Indexes:
    "frontend_prescription_pkey" PRIMARY KEY, btree (id)
    "frontend_prescription_a69d813a" btree (chemical_id)
    "frontend_prescription_chemical_id_4619f68f65c49a8_like" btree (chemical_id varchar_pattern_ops)
</code></pre>

<p>This is is my view:</p>

<pre><code>def chemical(request, bnf_code):
    c = get_object_or_404(Chemical, bnf_code=bnf_code)
    num_prescriptions = Prescription.objects.filter(chemical=c).count()
    context = {
        'num_prescriptions': num_prescriptions
    }
    return render(request, 'chemical.html', context)
</code></pre>

<p>The bottleneck is the <code>.count()</code>. call. The Django debug toolbar shows that the time taken on this is 2647ms (under the "Time" heading below), but the EXPLAIN section suggests the time taken should be 621ms (at the bottom):</p>

<p><img src="https://i.sstatic.net/nV94k.png" alt="screenshot of debug toolbar"></p>

<p>Even stranger, if I run the same query directly in Postgres it seems to take only 200-300ms:</p>

<pre><code># explain analyze select count(*) from frontend_prescription where chemical_id='0212000AA';

QUERY PLAN
-------------------------------------------------------------------------------------------------------------------------------------------------------------
 Aggregate  (cost=279495.79..279495.80 rows=1 width=0) (actual time=296.318..296.318 rows=1 loops=1)
   -&gt;  Bitmap Heap Scan on frontend_prescription  (cost=2104.44..279295.83 rows=79983 width=0) (actual time=162.872..276.439 rows=302389 loops=1)
         Recheck Cond: ((chemical_id)::text = '0212000AA'::text)
         -&gt;  Bitmap Index Scan on frontend_prescription_a69d813a  (cost=0.00..2084.44 rows=79983 width=0) (actual time=126.235..126.235 rows=322252 loops=1)
               Index Cond: ((chemical_id)::text = '0212000AA'::text)
 Total runtime: 296.591 ms 
</code></pre>

<p>So my question: in the debug toolbar, the EXPLAIN statement differs from actual performance in Django. And it is slower still than a raw query in Postgres. </p>

<p>Why is there this discrepancy? And how should I debug this / improve the performance of my Django app?</p>

<p>UPDATE: Here's another random example: 350ms for EXPLAIN, more than 10,000 to render! Help, this is making my Django app almost unusable. </p>

<p><img src="https://i.sstatic.net/i0jZI.png" alt="enter image description here"></p>

<p><strong>UPDATE 2:</strong> Here's the Profiling panel for another slow (40 seconds in Django, 600ms in EXPLAIN...) query. If I'm reading it right, it suggests that each SQL call from my view is taking 13 seconds... is this the bottleneck?</p>

<p><img src="https://i.sstatic.net/QSNLe.png" alt="enter image description here"></p>

<p>What's odd is that the profiled calls are only slow for queries that return lots of results, so I don't think the delay is some Django connection overhead that applies to every call.</p>

<p><strong>UPDATE 3:</strong> I tried rewriting the view in raw SQL and the performance is now better some of the time, although I'm still seeing slow queries about half the time. (I do have to create and re-create the cursor each time, otherwise I get <code>InterfaceError</code> and a message about the cursor being dead - not sure if this is useful for debugging. I've set <code>CONN_MAX_AGE=1200</code>.) Anyway, this performs OK, though obviously it's vulnerable to injection etc as written:</p>

<pre><code>cursor = connection.cursor()
query = "SELECT * from frontend_chemical WHERE code='%s'" % code
c = cursor.execute(query)
c = cursor.fetchone()
cursor.close()

cursor = connection.cursor()
query = "SELECT count(*) FROM frontend_prescription WHERE chemical_id="
query += "'" + code + "';"
cursor.execute(query)
num_prescriptions = cursor.fetchone()[0]
cursor.close()

context = {
    'chemical': c,
    'num_prescriptions': num_prescriptions
}
return render(request, 'chemical.html', context)
</code></pre>

## Answers
### Answer ID: 32890200
<p>It's not reliable profiling code on your development machine (revealed in comments, all sorts of things are running on your desktop that might be interfering).  It's also not going to show you real-world performance to examine runtimes with django-debug-toolbar active.  If you are interested in how this thing will perform in the wild you have to run it on your intended infrastructure and measure it with a light touch.</p>

<pre><code>def some_view(request):
    search = get_query_parameters(request)
    before = datetime.datetime.now()
    result = ComplexQuery.objects.filter(**search)
    print "ComplexQuery took",datetime.datetime.now() - before
    return render(request, "template.html", {'result':result})
</code></pre>

<p>Then you need to run this several times to warm up caches before you can do any sort of measuring.  Results will vary wildly with setups.  You could be using connection pooling that takes warming up, postgres is quicker on subsequent queries of the same sort, django might also be set up the have some local cache, all of which need spinup before you can say for sure it's <em>that</em> query.</p>

<p>All the profiling tools report times without factoring in their own introspection slow-down, you have to take a relative approach and use DDT (or my favorite for these problems: <a href="https://github.com/dcramer/django-devserver" rel="nofollow">django-devserver</a>) to identify hotspots in request handlers that consistently perform badly.  One other tool worthy of note: <a href="https://pypi.python.org/pypi/linesman" rel="nofollow">linesman</a>.  It's a bit of a hassle to set up and maintain but really really useful.</p>

<p>I have been responsible for fairly large setups (DB size in tens of GB) and haven't seen a simple query like that run aground that badly.  First find out if you really have a problem (that it's not just runserver ruining your day), then use the tools to find that hotspot, then optimize.</p>

### Answer ID: 29175062
<p>It is very likely that when Django runs the query, the data needs to be read from disk. But when you check why the query was slow, the data is already in memory due to the earlier query.</p>

<p>The easiest solutions are to buy more memory, or a faster io system.</p>

