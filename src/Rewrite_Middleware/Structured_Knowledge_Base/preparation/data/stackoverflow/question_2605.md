# Materialized View Query Rewrite Usage?
[Link to question](https://stackoverflow.com/questions/42371086/materialized-view-query-rewrite-usage)
**Creation Date:** 1487689939
**Score:** 0
**Tags:** oracle-database, oracle11g, materialized-views
## Question Body
<p>So I have been working with Oracle support over an Materialized view compile issue with our dataguard standby database and they recommended turning off query rewrite (setting <code>query_rewrite_enabled=false</code>). We have many MV's that have "enable query rewrite" in them, so I am a little hesitant to turn it off and cause potential performance problems..</p>

<p>Is there any way to tell if the MV's are in fact using query rewrite (perhaps a V$ view or something?)? When I tested querying one of the base tables it did not use the materialized view and an explain plan showed a full table scan. I am thinking that most our the queries wouldn't be rewritten, but I wanted to be sure before making a change.</p>

<p>Also, are there any other big impacts I should be aware off if I turn off <code>query_rewrite_enabled</code>?</p>

