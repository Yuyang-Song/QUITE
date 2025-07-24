# How to do general maths in sql query in django?
[Link to question](https://stackoverflow.com/questions/31346071/how-to-do-general-maths-in-sql-query-in-django)
**Creation Date:** 1436546418
**Score:** 3
**Tags:** python, mysql, django
## Question Body
<p>The following query I'd love to do in django, ideally without using iteration. I just want the database call to return the result denoted by the query below. Unfortunately according to <a href="https://docs.djangoproject.com/en/1.8/ref/models/querysets/#aggregation-functions" rel="nofollow">the docs</a> this doesn't seem to be possible; only the general functions like <code>Avg</code>, <code>Max</code> and <code>Min</code> etc are available. Currently I'm using django 1.4 but I'm happy to rewrite stuff from django 1.8 (hence the docs page; I've heard that 1.8 does a lot of these things much better than 1.4)</p>

<pre><code>select sum(c.attr1 * fs.attr2)/ sum(c.attr1) from fancyStatistics as fs
left join superData s on fs.super_id=s.id
left join crazyData c on s.crazy_id=c.id;
</code></pre>

<p><strong>Note:</strong></p>

<p>The main reason for doing this in django directly is that if we ever want to change our database from MySQL to something more appropriate for django, it would be good not to have to rewrite all the queries.</p>

## Answers
### Answer ID: 31348900
<p>You should be able to get aggregates with F expressions to do most of what you want without dropping into SQL. </p>

<p><a href="https://docs.djangoproject.com/en/1.8/topics/db/aggregation/#joins-and-aggregates" rel="nofollow">https://docs.djangoproject.com/en/1.8/topics/db/aggregation/#joins-and-aggregates</a></p>

<pre><code>aggregate_dict = FancyStatistics.objects.all()\
    .aggregate( 
        sum1=Sum(
             F('superdata__crazydata__attr1') * F('attr2'), output_field=FloatField()
         ) ,
        sum2=Sum('superdata__crazydata__attr1')
    )  
) 
result = aggregate_dict['sum1'] / aggregate_dict['sum2']
</code></pre>

<p>You need to specify the output fields if the data types used are different.</p>

### Answer ID: 31346168
<p>You can do that query in Django directly using your SQL expression. Check <a href="https://docs.djangoproject.com/en/1.8/topics/db/sql/" rel="nofollow">the docs concerning performing raw SQL queries</a>.</p>

