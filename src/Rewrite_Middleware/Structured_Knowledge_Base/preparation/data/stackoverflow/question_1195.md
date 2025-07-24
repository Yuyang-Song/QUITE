# Joining Tables between Multiple Foreign Servers with Foreign Data Wrapper Causes Performance Issue
[Link to question](https://stackoverflow.com/questions/62922815/joining-tables-between-multiple-foreign-servers-with-foreign-data-wrapper-causes)
**Creation Date:** 1594842895
**Score:** 0
**Tags:** postgresql, foreign-data-wrapper
## Question Body
<p>One of my legacy PHP applications is using a PostgreSQL database with Foreign Data Wrapper. This database has a local table and two foreign servers set up (one pointing to database A, another pointing to database B).</p>
<p>The application uses ORM to construct SQL queries. One of the complex queries is actually joining 6 tables across the two foreign servers and also the local table. And the query just hangs forever because the those 6 tables have on average millions of records.</p>
<p>There are many more queries like this in the legacy app. I have configured the foreign servers to <code>use_remote_estimate 'true'</code> and increase the <code>fetch_size</code> but still see no drastic improvements.</p>
<p>I'm wondering if there are some configurations that can be done on the foreign server to optimise the query speed. Before I start rewriting the whole application to not use PHP and ORM.</p>

## Answers
### Answer ID: 62924687
<p>Selectivity estimation problems in FDW are very common, and can lead to plans with atrocious performance.  Since you are looking for magic bullet, have you tried running ANALYZE on the foreign tables in the local server, so it can use local statistics to some come up with plans?  You might want to set up a clone to test this in.  ANALYZE can also make things worse, and there is no easy way to undo it once done.</p>
<p>Another step might be setting cursor_tuple_fraction to 1 (or at least much higher than the defaults) on the servers on the foreign sides.  This could help if the overall query plan is sound on the local side, but the execution on the foreign sides is bad.</p>
<p>Barring those, you need to look at EXPLAIN (VERBOSE) and EXPLAIN (ANALYZE) of an archetypical bad query to figure out what is going on.</p>
<blockquote>
<p>Before I start rewriting the whole application to not use PHP and ORM.</p>
</blockquote>
<p>Why would that help?  Do you already know how rewrite the queries to make them faster, you just can't get the ORM to cooperate?</p>

