# Postgresql - Query running a lot faster with enable_nestloop=false. Why is the planner not doing the right thing?
[Link to question](https://stackoverflow.com/questions/7885129/postgresql-query-running-a-lot-faster-with-enable-nestloop-false-why-is-the-p)
**Creation Date:** 1319521283
**Score:** 5
**Tags:** postgresql
## Question Body
<p>I have a query that runs a lot slower (~5 minutes) when I run it with the default enable_nestloop=true and enable_nestloop=false (~10 secs). </p>

<p>Explain analyse result for both cases: </p>

<p>Machine A nestloop=true - <a href="http://explain.depesz.com/s/nkj0">http://explain.depesz.com/s/nkj0</a> (~5 minutes)
Machine A nestloop=false - <a href="http://explain.depesz.com/s/wBM">http://explain.depesz.com/s/wBM</a> (~10 secs)</p>

<p>On a different slightly slower machine, copying the database over and leaving the default enable_nestloop=true it takes ~20 secs.</p>

<p>Machine B nestloop=true -  (~ 20secs)</p>

<p>For all the cases above I ensured that I did an ANALYZE before running the queries. There were no other queries running in parallel.</p>

<p>Both machines are running Postgres 8.4. Machine A is running Ubuntu 10.04 32 bit while Machine B is running Ubuntu 8.04 32 bit.</p>

<p>The actual query is available here . It is a reporting query with many joins as the database is mainly used for transaction processing.</p>

<ol>
<li><p>Without  resorting to putting in something like materialized views what can I do to make the planner do what I achieved by setting enable_nestloop=false ?</p></li>
<li><p>From the research I have done it seems to be that the reason the planner is choosing the seemingly unoptimal query is because of the huge difference between the estimated and actual rows. How can I get this figure closer ?</p></li>
<li><p>If I should rewrite the query, what should I change ?</p></li>
<li><p>Why is it that the planner seems to be doing the right thing for Machine B. What should I be comparing in both the machines ?</p></li>
</ol>

## Answers
### Answer ID: 8665541
<p>This might be useful reading: 
<a href="http://www.postgresql.org/docs/9.1/static/explicit-joins.html" rel="nofollow" title="PostgreSQL tutorial about explicit JOINs">PostgreSQL tutorial about explicit JOINs</a>.</p>

<p>Query planner tries to analyze the JOIN order to find the best order for JOINing.</p>

<p>I saw Your query had at least 15 JOINs. The number of possible JOIN orders goes up as factorial (n!). So it is not reasonable for query planner to try to find the best JOIN order if there are 15 JOINs - it would have to look at 15! = 1307674368000 different plans.</p>

<p>So it uses Genetic Query Optimizer instead. See <a href="http://www.postgresql.org/docs/9.1/static/runtime-config-query.html#RUNTIME-CONFIG-QUERY-GEQO" rel="nofollow" title="test2">Query Planning: Genetic Query Optimizer parameters</a>. The parameter "geqo_threshold" determines how many JOINs must be present for query planner to use Genetic Query Optimizer.</p>

<p>This way the PostgreSQL planner looks at only small part of possible variants and tries to find the best one (randomly). So each time You run the ANALYZE, it might come up with better plan.</p>

<p>I think that generally, if You have so many tables to JOIN, You are better off doing as You did: rewriting the query to optimal JOIN order.</p>

### Answer ID: 8047151
<p>Turns out rewriting the query was the best fix. The query was written in a way that it relied heavily on left joins and had many joins. I flattened it out and reduced the left joins by using my knowledge of the join nature of the data in the tables the query was joining. I guess the rule of thumb is if the planner is coming out with real crappy estimates, there might be a better way of writing the query.</p>

### Answer ID: 7892728
<p>There are usually only one reason for different plan for same data and same queries on two servers with same PostgreSQL. This is different configuration - mainly value of work_mem. Hash join is usually faster, but needs a lot of available memory.</p>

### Answer ID: 7886075
<p>If the query planner chooses suboptimal query plans, then chances are it has incomplete or misleading information to work with.</p>

<p>See this <a href="http://wiki.postgresql.org/wiki/Tuning_Your_PostgreSQL_Server" rel="nofollow">PostgreSQL Wiki page</a> on server tuning. Especially pay attention to the chapters on <strong>random_page_cost</strong> and <strong>default_statistics_target</strong>.<br>
Also read the corresponding chapters in the manual on <a href="http://www.postgresql.org/docs/current/interactive/planner-stats.html" rel="nofollow">Statistics Used by the Planner</a> and <a href="http://www.postgresql.org/docs/current/interactive/runtime-config-query.html#RUNTIME-CONFIG-QUERY-CONSTANTS" rel="nofollow">Planner Cost Constants</a>.</p>

<p>More specifically, it might help to increase the <code>statistics target</code> for the following columns:</p>

<pre><code>ALTER TABLE postgres.products ALTER COLUMN id SET STATISTICS 1000;
ALTER TABLE postgres.sales_orders ALTER COLUMN retailer_id SET STATISTICS 1000;
ALTER TABLE postgres.sales_orders ALTER COLUMN company_id SET STATISTICS 1000;

ALTER TABLE goods_return_notes ALTER COLUMN retailer_id SET STATISTICS 1000;
ALTER TABLE goods_return_notes ALTER COLUMN company_id SET STATISTICS 1000;

ALTER TABLE retailer_category_leaf_nodes ALTER COLUMN tree_left SET STATISTICS 1000;
ALTER TABLE channels ALTER COLUMN principal_id SET STATISTICS 1000;
</code></pre>

<p>These are involved in the filters resulting in the </p>

<blockquote>
  <p>huge difference between the estimated and actual rows.</p>
</blockquote>

<p>There are <strong>more</strong>. Check every column where the planer deviates a lot from the estimate. Default is just 100. Makes only sense for tables with >> 1000 rows. Experiment with the setting. Run <code>ANALYZE</code> on the tables afterwards for the changes to take effect.</p>

<p>It might also help to create a <em>partial index</em> on <code>postgres(sales_orders.retailer_id) WHERE retailer_id IS NOT NULL</code> (depending on how common NULL values are).</p>

<hr>

<p>Another thing that may help you is to <strong>upgrade</strong> to the latest version 9.1. There have been a number of substantial improvements in this area.</p>

