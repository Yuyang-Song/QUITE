# Call JSON-functions on PostgreSQL 9.1
[Link to question](https://stackoverflow.com/questions/24653550/call-json-functions-on-postgresql-9-1)
**Creation Date:** 1404908425
**Score:** 0
**Tags:** sql, json, postgresql, postgresql-9.1
## Question Body
<p>I've got a query which works on PostgreSQL 9.3, due to the fact that it supports JSON types etc.</p>

<p>I would like to call this query on a remote API, which only runs PostgreSQL 9.1, with no such support.</p>

<p>These are the needed things:</p>

<pre><code>ROW_TO_JSON, ARRAY_TO_JSON, ::json 
</code></pre>

<p>Are is it somehow possible to rewrite a query to support such in PostgreSQL 9.1?</p>

<p>I have no control over the API and the remote database behind.</p>

