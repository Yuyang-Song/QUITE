# How to rewrite SQL joins into window functions?
[Link to question](https://stackoverflow.com/questions/44956175/how-to-rewrite-sql-joins-into-window-functions)
**Creation Date:** 1499364800
**Score:** 1
**Tags:** postgresql, join, window-functions, vertica
## Question Body
<p>Database is HP Vertica 7 or PostgreSQL 9.</p>

<pre><code>create table test (
id int,
card_id int,
tran_dt date,
amount int
);

insert into test values (1, 1, '2017-07-06', 10);
insert into test values (2, 1, '2017-06-01', 20);
insert into test values (3, 1, '2017-05-01', 30);
insert into test values (4, 1, '2017-04-01', 40);
insert into test values (5, 2, '2017-07-04', 10);
</code></pre>

<p>Of the payment cards used in the last 1 day, what is the maximum amount charged on that card in the last 90 days.</p>

<pre><code>select t.card_id, max(t2.amount) max
from test t
join test t2 on t2.card_id=t.card_id and t2.tran_dt&gt;='2017-04-06'
where t.tran_dt&gt;='2017-07-06'
group by t.card_id
order by t.card_id;
</code></pre>

<p>Results are correct</p>

<pre><code>card_id    max
-------    ---
1          30
</code></pre>

<p>I want to rewrite the query into sql window functions.</p>

<pre><code>select card_id, max(amount) over(partition by card_id order by tran_dt range between '60 days' preceding and current row) max
from test
where card_id in (select card_id from test where tran_dt&gt;='2017-07-06')
order by card_id;
</code></pre>

<p>But result set does not match, how can this be done?</p>

<p>Test data here:
<a href="http://sqlfiddle.com/#!17/db317/1" rel="nofollow noreferrer">http://sqlfiddle.com/#!17/db317/1</a></p>

## Answers
### Answer ID: 44960132
<p>I can't try PostgreSQL, but in Vertica, you can apply the ANSI standard OLAP window function. </p>

<p>But you'll need to nest two queries: The window function only returns sensible results if it has all rows that need to be evaluated in the result set. </p>

<p>But you only want the row from '2017-07-06' to be displayed. </p>

<p>So you'll have to filter for that date in an outer query:</p>

<pre><code>WITH olap_output AS (
  SELECT 
    card_id
  , tran_dt
  , MAX(amount) OVER (
      PARTITION BY card_id
      ORDER BY tran_dt
      RANGE BETWEEN '90 DAYS' PRECEDING AND CURRENT ROW
    ) AS the_max
  FROM test
)
SELECT
  card_id
, the_max
FROM olap_output
WHERE tran_dt='2017-07-06'
;

card_id|the_max
      1|     30
</code></pre>

### Answer ID: 44959890
<p>As far as I know, PostgreSQL Window function doesn't support bounded <code>range preceding</code> thus <code>range between '90 days' preceding</code> won't work.  It does support bounded <code>rows preceding</code> such as <code>rows between 90 preceding</code>, but then you would need to assemble a time-series query similar to the following for the Window function to operate on the time-based rows:</p>

<pre><code>SELECT c.card_id, t.amount, g.d as d_series
FROM generate_series(
  '2017-04-06'::timestamp, '2017-07-06'::timestamp, '1 day'::interval
) g(d)
CROSS JOIN ( SELECT distinct card_id from test ) c
LEFT JOIN test t ON t.card_id = c.card_id and t.tran_dt = g.d
ORDER BY c.card_id, d_series
</code></pre>

<p>For what you need (based on your question description), I would stick to using <code>group by</code>.</p>

