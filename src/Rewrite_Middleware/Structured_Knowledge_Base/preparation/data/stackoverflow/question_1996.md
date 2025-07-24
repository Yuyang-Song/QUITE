# How to ensure all Postgres queries have WHERE clause?
[Link to question](https://stackoverflow.com/questions/15034582/how-to-ensure-all-postgres-queries-have-where-clause)
**Creation Date:** 1361573715
**Score:** 4
**Tags:** postgresql
## Question Body
<p>I am building a multi tenant system in which many clients data will be in the same database.</p>

<p>I am paranoid about some developer forgetting to put the appropriate "WHERE clientid = " onto every query.</p>

<p>Is there a way to, at the database level, ensure that every query has the correct WHERE = clause, thereby ensuring that no query will ever be executed without also specifying which client the query is for?</p>

<p>I was wondering if maybe the query rewrite rules could do this but it's not clear to me if they can do so.</p>

<p>thanks</p>

## Answers
### Answer ID: 15039512
<p>Another way is to create a <code>VIEW</code> for:</p>

<pre><code>SELECT * 
FROM t
WHERE t.client_id = current_setting('session_vars.client_id');
</code></pre>

<p>And use <code>SET session_vars.client_id = 1234</code> at the start of the session.</p>

<p>Deny acces to the tables, and leave only permissins for views.</p>

<p>You may need to create rewrite rules for <code>UPDATE</code>, <code>DELETE</code>, <code>INSERT</code> for the views (it depends on your PostgreSQL version).</p>

<p>Performance penalty will be small (if any) because PostgreSQL will rewrite the queries before execution.</p>

### Answer ID: 15035319
<p>Deny permissions on the table <code>t</code> for all users. Then give them permission on a function <code>f</code> that returns the table and accepts the parameter client_id:</p>

<pre><code>create or replace function f(_client_id integer)
returns setof t as
$$
    select *
    from t
    where client_id = _client_id
$$ language sql
;

select * from f(1);
 client_id | v 
-----------+---
         1 | 2
</code></pre>

