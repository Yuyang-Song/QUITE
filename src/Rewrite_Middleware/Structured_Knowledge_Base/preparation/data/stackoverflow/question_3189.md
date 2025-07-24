# PostgreSQL Default Result Limit
[Link to question](https://stackoverflow.com/questions/70549256/postgresql-default-result-limit)
**Creation Date:** 1641044639
**Score:** 2
**Tags:** postgresql, pgpool
## Question Body
<p>I'm using Grafana and PostgreSQL 13 for visualizing. There are many users in the Grafana and they could send queries to their own databases.</p>
<p>I need to set a default result limit for sent queries. (Like 1000) But I couldn't find a solution. I analyzed the PgPool to rewrite the query but I think it couldn't do that.</p>
<p>Is there any solution for that? I'm not sure but maybe I need a TCP Proxy which can do.</p>

## Answers
### Answer ID: 70549865
<p>The most popular solution, as far as I know, is <a href="https://www.pgbouncer.org/" rel="nofollow noreferrer">PgBouncer</a>. PgBouncer is a lightweight connection pooler for PostgreSQL. It acts as a Postgres server, so simply point your Grafana and other clients to the PgBouncer port.</p>
<p>Here are some installation guides for Linux (Ubuntu, Debian, CentOS):</p>
<ul>
<li><a href="https://severalnines.com/blog/guide-using-pgbouncer" rel="nofollow noreferrer">A Guide to Using pgBouncer for PostgreSQL</a>.</li>
<li><a href="https://pgdash.io/blog/pgbouncer-connection-pool.html" rel="nofollow noreferrer">PostgreSQL Connection Pooling with PgBouncer</a>.</li>
</ul>

