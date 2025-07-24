# Performing a Django raw SQL (using &quot;WHERE col IN&quot; syntax) or translating raw SQL to .raw() or .extra()
[Link to question](https://stackoverflow.com/questions/4257850/performing-a-django-raw-sql-using-where-col-in-syntax-or-translating-raw-sql)
**Creation Date:** 1290526978
**Score:** 1
**Tags:** sql, mysql, django, django-models, query-optimization
## Question Body
<p>Django 1.3-dev provides several ways to query the database using raw SQL. They are covered <a href="http://docs.djangoproject.com/en/dev/topics/db/sql/" rel="nofollow">here</a> and <a href="http://docs.djangoproject.com/en/dev/ref/models/querysets/#extra-select-none-where-none-params-none-tables-none-order-by-none-select-params-none" rel="nofollow">here</a>. The recommended ways are to use the <code>.raw()</code> or the <code>.extra()</code> methods. The advantage is that if the retrieved data fits the <em>Model</em> you can still use some of it's features directly.</p>

<p>The page I'm trying to display is somewhat complex because it uses lots of information which is spread across multiple tables with different relationships (one2one, one2many). With the current approach the server has to do about 4K queries per page. This is obviously slow due to database to webserver communication.</p>

<p>A possible solution is to use raw SQL to retrieve the relevant data but due to the complexity of the query I couldn't translate this to an equivalent in Django.</p>

<p>The query is:</p>

<pre><code>SELECT clin.iso as iso,
   (SELECT COUNT(*)
       FROM clin AS a
       LEFT JOIN clin AS b
           ON a.pat_id = b.pat_id
       WHERE a.iso = clin.iso
   ) AS multiple_iso,
   (SELECT COUNT(*)
       FROM samptopat
       WHERE samptopat.iso_id = clin.iso
   ) AS multiple_samp,
   (SELECT GROUP_CONCAT(value ORDER BY snp_id ASC)
       FROM samptopat
       RIGHT JOIN samptosnp
           USING(samp_id)
       WHERE iso_id = clin.iso
       GROUP BY samp_id
       LIMIT 1 -- Return 1st samp only
   ) AS snp
FROM clin
WHERE iso IN (...)
</code></pre>

<p>or alternatively <code>WHERE iso = ...</code>.</p>

<p>Sample output looks like:</p>

<pre><code>+-------+--------------+---------------+-------------+
| iso   | multiple_iso | multiple_samp | snp         |
+-------+--------------+---------------+-------------+
|     7 |        19883 |             0 | NULL        |
|     8 |        19883 |             0 | NULL        |
| 21092 |            1 |             2 | G,T,C,G,T,G |
| 31548 |            1 |             0 | NULL        |
+-------+--------------+---------------+-------------+
4 rows in set (0.00 sec)
</code></pre>

<p>The <a href="http://docs.djangoproject.com/en/dev/topics/db/sql/" rel="nofollow">documentation</a> explains how one can do a query using <code>WHERE col = %s</code> but not the <code>IN</code> syntax.
One part of this question is <strong>How do I perform raw SQL queries using Django and the <code>IN</code> statement?</strong></p>

<p>The other part is, considering the following models:</p>

<pre><code>class Clin(models.Model):
    iso = models.IntegerField(primary_key=True)
    pat = models.IntegerField(db_column='pat_id')
    class Meta:
        db_table = u'clin'

class SampToPat(models.Model):
    samptopat_id = models.IntegerField(primary_key=True)
    samp = models.OneToOneField(Samp, db_column='samp_id')
    pat = models.IntegerField(db_column='pat_id')
    iso = models.ForeignKey(Clin, db_column='iso_id')
    class Meta:
        db_table = u'samptopat'

class Samp(models.Model):
    samp_id = models.IntegerField(primary_key=True)
    samp = models.CharField(max_length=8)
    class Meta:
        db_table = u'samp'

class SampToSnp(models.Model):
    samptosnp_id = models.IntegerField(primary_key=True)
    samp = models.ForeignKey(Samp, db_column='samp_id')
    snp = models.IntegerField(db_column='snp_id')
    value = models.CharField(max_length=2)
    class Meta:
        db_table = u'samptosnp'
</code></pre>

<p><strong>Is it possible to rewrite the above query into something more ORM oriented?</strong></p>

## Answers
### Answer ID: 4261400
<p>Could you explain exactly what you're trying to extract w/ the snp subquery? I see you're joining over the two tables, but it looks like what you <em>really</em> want is <code>Snp</code> objects which have an associated <code>Clin</code> which has the given id. If so, this becomes <em>almost</em> as straightforward to do as a separate query as the other 2:</p>

<pre><code>Snp.objects.filter(samp__pat__clin__pk=given_clin)
</code></pre>

<p>or some such thing ought to do the trick. You may have to rewrite that a bit due to all the ways you're violating the conventions, unfortunately.</p>

<p>The others are something like:</p>

<pre><code>Pat.objects.filter(clin__pk=given_clin).count()
</code></pre>

<p>and</p>

<pre><code>Samp.objects.filter(clin__pk=given_clin).count()
</code></pre>

<p>if @Evgeny's reading is correct (which is how I read it as well).</p>

<p>Often, with Django's ORM, I find I get better results if I try to think about directly what I want in terms of the ORM, instead of trying to translate to or from the SQL I might use if I wasn't using the ORM.</p>

### Answer ID: 4258543
<p>For a problem like this one, I'd split the query into a small number of simpler ones, I think it's quite possible. Also, I found that MySQL actually may return results faster with this approach.</p>

<p><strong>edit</strong> ...Actually after thinking a bit I see that you need to "annotate on subqueries", which is not possible in Django ORM (not in 1.2 at least). Maybe you have to do plain sql here or use some other tool to build the query.</p>

<p>Tried to rewrite your models in more default django pattern, maybe it will help to understand the problem better. Models Pat and Snp are missing though...</p>

<pre><code>class Clin(models.Model):
    pat = models.ForeignKey(Pat)
    class Meta:
        db_table = u'clin'

class SampToPat(models.Model):
    samp = models.ForeignKey(Samp)
    pat = models.ForeignKey(Pat)
    iso = models.ForeignKey(Clin)
    class Meta:
        db_table = u'samptopat'
        unique_together = ['samp', 'pat']

class Samp(models.Model):
    samp = models.CharField(max_length=8)
    snp_set = models.ManyToManyField(Snp, through='SampToSnp')
    pat_set = models.ManyToManyField(Pat, through='SaptToPat')
    class Meta:
        db_table = u'samp'

class SampToSnp(models.Model):
    samp = models.ForeignKey(Samp)
    snp = models.ForeignKey(Snp)
    value = models.CharField(max_length=2)
    class Meta:
        db_table = u'samptosnp'
</code></pre>

<p>The following seems to mean - get count of unique patients per clinic ...</p>

<pre><code>(SELECT COUNT(*)
   FROM clin AS a
   LEFT JOIN clin AS b
       ON a.pat_id = b.pat_id
   WHERE a.iso = clin.iso
) AS multiple_iso,
</code></pre>

<p>Sample count per clinic:</p>

<pre><code>(SELECT COUNT(*)
   FROM samptopat
   WHERE samptopat.iso_id = clin.iso
) AS multiple_samp,
</code></pre>

<p>This part is harder to understand, but in Django there is no way to do GROUP_CONCAT in plain ORM.</p>

<pre><code>(SELECT GROUP_CONCAT(value ORDER BY snp_id ASC)
   FROM samptopat
   RIGHT JOIN samptosnp
       USING(samp_id)
   WHERE iso_id = clin.iso
   GROUP BY samp_id
   LIMIT 1 -- Return 1st samp only
) AS snp
</code></pre>

