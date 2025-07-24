# Postgresql Offset Behavior with json column
[Link to question](https://stackoverflow.com/questions/27415340/postgresql-offset-behavior-with-json-column)
**Creation Date:** 1418271765
**Score:** 7
**Tags:** postgresql
## Question Body
<p>Using postgresql 9.4 we have a simple contacts table with (id text not null (as pk), blob json) to experiment with porting a couchdb crm database. We will eventually split out to more columns etc, and handle the data more idomatically for a rdbms, but that's besides the point for the time being.</p>

<p>There are approximately 100k rows. </p>

<p>I am aware that hardcore postgresql performance experts advise against using offset however I can accept a small performance penalty (happy with anything under 100msec)</p>

<pre><code>SELECT id FROM couchcontacts OFFSET 10000 LIMIT 10 
</code></pre>

<p>As expected takes &lt;10ms </p>

<pre><code>SELECT blob-&gt;&gt;'firstName' FROM couchcontacts LIMIT 10 
</code></pre>

<p>Also takes &lt; 10ms (presume 10 json decode ops on blob column here)</p>

<pre><code>SELECT blob-&gt;&gt;'firstName' FROM couchcontacts OFFSET 10000 LIMIT 10 
</code></pre>

<p>Takes upwards of 10 seconds!!  Noted inefficiencies of offset aside why is this presumably causing 10,010 json decode ops? As the projection has no side-effects I don't understand the reason this can't be fast? </p>

<p>Is this a limitation of json functionality being relatively new to postgres? and thus unable to determine <code>-&gt;&gt;</code> opereator isnt yielding side-effects?</p>

<p>Interesting rewriting the query to this bring it back under 10milliseconds</p>

<pre><code>SELECT jsonblob-&gt;&gt;'firstName' FROM couchdbcontacts WHERE id IN (SELECT id FROM couchcontacts OFFSET 10000 LIMIT 10)
</code></pre>

<p>Is there a way to ensure offset doesnt json decode the offsetted records? (i.e. don't execute the select projection)</p>

<pre><code>"Limit  (cost=1680.31..1681.99 rows=10 width=32) (actual time=12634.674..12634.842 rows=10 loops=1)"
"  -&gt;  Seq Scan on couchcontacts  (cost=0.00..17186.53 rows=102282 width=32) (actual time=0.088..12629.401 rows=10010 loops=1)"
"Planning time: 0.194 ms"
"Execution time: 12634.895 ms"
</code></pre>

## Answers
### Answer ID: 27417806
<p>I ran a few tests, and I'm seeing similar behaviors. Each of these have immaterial differences in performance:</p>

<ul>
<li><code>select id</code> ...</li>
<li><code>select indexed_field</code> ...</li>
<li><code>select unindexed_field</code> ...</li>
<li><code>select json_field</code> ...</li>
<li><code>select *</code> ...</li>
</ul>

<p>This one, however, does show a difference in performance:</p>

<ul>
<li><code>select json_field-&gt;&gt;'key'</code> ...</li>
</ul>

<p>When the json_field is null, the performance impact is negligible. When it's empty, it degrades things very slightly. When it's filled in, it degrades noticeably. And when the field is loaded with larger data, it degrades materially.</p>

<p>In other words, Postgres seems to want to unserialize the json data for every row it's visiting. (Which is probably a bug, and one that's massively affecting RoR developers seeing how they use json.)</p>

<p>Fwiw, I noted that re-arranging the query so it uses a CTE will work around the problem:</p>

<pre><code>with data as (
  select * from table offset 10000 limit 10
)
select json_field-&gt;&gt;'key' from data;
</code></pre>

<p>(It might get an only-very-slightly better plan than the <code>id IN (...)</code> query that you highlighted.)</p>

