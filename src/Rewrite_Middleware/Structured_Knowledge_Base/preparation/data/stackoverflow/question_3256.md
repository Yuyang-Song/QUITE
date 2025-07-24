# Avoid full table scan under window function run with use of join condition
[Link to question](https://stackoverflow.com/questions/73869060/avoid-full-table-scan-under-window-function-run-with-use-of-join-condition)
**Creation Date:** 1664287853
**Score:** 1
**Tags:** sql, postgresql, optimization, query-optimization
## Question Body
<p>Given a database table <code>events</code> with columns: <code>event_id</code>, <code>correlation_id</code>, <code>username</code>, <code>create_timestamp</code>. It contains more than 1M records.</p>
<p>There is a problem I am trying to solve: <strong>for each event of a particular user display its latest sibling event</strong>. Sibling events are the events which has same <code>correlation_id</code>. The query I use for that is the following:</p>
<pre><code>SELECT 
  &quot;events&quot;.&quot;event_id&quot; AS &quot;event_id&quot;, 
  &quot;latest&quot;.&quot;event_id&quot; AS &quot;latest_event_id&quot; 
FROM 
  events &quot;events&quot; 
  JOIN (
    SELECT 
      &quot;latest&quot;.&quot;correlation_id&quot; AS &quot;correlation_id&quot;, 
      &quot;latest&quot;.&quot;event_id&quot; AS &quot;event_id&quot;, 
      ROW_NUMBER () OVER (
        PARTITION BY &quot;latest&quot;.&quot;correlation_id&quot; 
        ORDER BY 
          &quot;latest&quot;.&quot;create_timestamp&quot; ASC
      ) AS &quot;rn&quot; 
    FROM 
      events &quot;latest&quot;
  ) &quot;latest&quot; ON (
    &quot;latest&quot;.&quot;correlation_id&quot; = &quot;events&quot;.&quot;correlation_id&quot; 
    AND &quot;latest&quot;.&quot;rn&quot; = 1
  ) 
WHERE 
  &quot;events&quot;.&quot;username&quot; = 'user1'
</code></pre>
<p>It gets correct list of results but causes performance problems which must be fixed. Here is an execution plan of the query:</p>
<pre><code>Hash Right Join  (cost=13538.03..15522.72 rows=1612 width=64)
  Hash Cond: ((&quot;latest&quot;.correlation_id)::text = (&quot;events&quot;.correlation_id)::text)
  -&gt;  Subquery Scan on &quot;latest&quot;  (cost=12031.35..13981.87 rows=300 width=70)
        Filter: (&quot;latest&quot;.rn = 1)
        -&gt;  WindowAgg  (cost=12031.35..13231.67 rows=60016 width=86)
              -&gt;  Sort  (cost=12031.35..12181.39 rows=60016 width=78)
                    Sort Key: &quot;latest_1&quot;.correlation_id, &quot;latest_1&quot;.create_timestamp
                    -&gt;  Seq Scan on events &quot;latest_1&quot;  (cost=0.00..7268.16 rows=60016 width=78)
  -&gt;  Hash  (cost=1486.53..1486.53 rows=1612 width=70)
        -&gt;  Index Scan using events_username on events &quot;events&quot; (cost=0.41..1486.53 rows=1612 width=70)
              Index Cond: ((username)::text = 'user1'::text)
</code></pre>
<p>From the plan, I can conclude that the performance problem <strong>mainly caused by calculation of latest events for ALL events in the table which takes ~80% of cost</strong>. Also it performs the calculations even if there are no events for a user at all. Ideally, I would like the query to do these steps which seem more efficient for me:</p>
<ol>
<li>find all events by a user</li>
<li>for each event from Step 1, find all siblings, sort them and get the 1st</li>
</ol>
<p>To simplify the discussion, let's consider all required indexes as already created for needed columns. It doesn't seem to me that the problem can be solved purely by index creation.</p>
<p><strong>Any ideas what can be done to improve the performance?</strong> Probably, there are options to rewrite the query or adjust a configuration of the table.</p>
<p>Note that this question is significantly obfuscated in terms of business meaning to clearly demonstrate the technical problem I face.</p>

## Answers
### Answer ID: 73893024
<p>Although I like the <code>LATERAL JOIN</code> approach suggested by others, when it comes to fetching just 1 field I'm 50/50 about using that and using a subquery as below.(If you need to fetch multiple fields using the same logic than by all means LATERAL is the way to go!)</p>
<p>I wonder if either would perform better, presumably they are executed in a very similar way by the SQL engine.</p>
<pre><code>SELECT e.event_id, 
       (SELECT l.event_id
          FROM events AS l
         WHERE l.correlation_id = e.correlation_id 
         ORDER BY l.create_timestamp ASC -- shouldn't this be DESC?
         FETCH FIRST 1 ROWS ONLY) as latest_event_id
FROM events AS e
WHERE e.username = 'user1';
</code></pre>
<p>Note: You're currently asking for the OLDEST correlated record. In your  post you say you're looking for the &quot;latest sibling event&quot;. &quot;Latest&quot; IMHO implies the most recent one, so it would have the biggest <code>create_timestamp</code>, meaning you need to ORDER BY that field from <em>high</em> to <em>low</em> and then take the first one.</p>
<p>Edit: identical as suggested above, for this approach you also want the index on <code>correlation_id</code> and <code>create_timestamp</code></p>
<pre><code>CREATE INDEX ON event (correlation_id, create_timestamp);
</code></pre>
<p>You might even want to include the <code>event_id</code> to avoid a bookmark lookup although these pages are likely to be in cache anyway so not sure if it will really help all that much.</p>
<pre><code>CREATE INDEX ON event (correlation_id, create_timestamp, event_id);
</code></pre>
<p>PS: same is true about adding <code>correlation_id</code> to your <code>events_username</code> index... but that's all quite geared towards this (probably simplified) query and do keep in mind that more (and bigger) indexes will bring some overhead elsewhere even when they might bring big benefits elsewhere... it's always a compromise.</p>

### Answer ID: 73869899
<p>The window function has to scan the whole table. It has no idea that really you are only interested in the first value. A lateral join could perform better and is more readable anyway:</p>
<pre><code>SELECT 
  e.event_id, 
  latest.latest_event_id
FROM 
  events AS e
  CROSS JOIN LATERAL
     (SELECT
        l.event_id AS latest_event_id
      FROM
        events AS l
      WHERE
        l.correlation_id = e.correlation_id 
      ORDER BY l.create_timestamp
      FETCH FIRST 1 ROWS ONLY
     ) AS latest
WHERE e.username = 'user1';
</code></pre>
<p>The perfect index to support that would be</p>
<pre><code>CREATE INDEX ON event (correlation_id, create_timestamp);
</code></pre>

### Answer ID: 73869996
<p>All those needless double quotes are making my eyes bleed.</p>
<p>This should very fast with a lateral join, provided the number of returned rows is rather low, i.e. 'user1' is rather specific.</p>
<pre><code>explain analyze SELECT 
  events.event_id AS event_id, 
  latest.event_id AS latest_event_id 
FROM 
  events &quot;events&quot; 
  cross JOIN lateral (
    SELECT 
      latest.event_id AS event_id 
      FROM events latest
      WHERE latest.correlation_id=events.correlation_id 
      ORDER by create_timestamp ASC limit 1
  ) latest 
WHERE 
  events.username = 'user1';
</code></pre>
<p>You will want an index on <code>username</code>, and one on <code>(correlation_id, create_timestamp)</code></p>
<p>If the number of rows returned is large, then your current query, which precomputes in bulk, is probably better. But would be faster if you used DISTINCT ON rather than the window function to pull out just the latest for each correlation_id.  Unfortunately the planner does not understand these queries to be equivalent, and so will not interconvert between them based on what it thinks will be faster.</p>

### Answer ID: 73869884
<p>Without having access to the data, I'm really just throwing out ideas...</p>
<ol>
<li><p>Instead of a subquery, it's worth trying a materialized CTE</p>
</li>
<li><p>Rather than the row_number analytic, you can try a <code>distinct on</code>.  Honestly, I don't predict any gains.  It's basically the same thing at the database level</p>
</li>
</ol>
<p>Sample of both:</p>
<pre><code>with latest as materialized (
    SELECT distinct on (&quot;correlation_id&quot;)
      &quot;correlation_id&quot;, &quot;event_id&quot; 
    FROM events
    order by
      &quot;correlation_id&quot;, &quot;create_timestamp&quot; desc
)
SELECT 
  e.&quot;event_id&quot;, 
  l.&quot;event_id&quot; AS &quot;latest_event_id&quot; 
FROM 
  events &quot;events&quot; e
  join latest l ON
    l.&quot;correlation_id&quot; = e.&quot;correlation_id&quot; 
WHERE 
  e.&quot;username&quot; = 'user1'
</code></pre>
<p>Additional suggestion -- if you are doing this over and over, I'd consider creating a temp table or materialized view for &quot;latest,&quot; including an index by coorelation_id rather than re-running the subquery (or CTE) every single time.  This will be a one-time pain followed my repeated gain.</p>
<p>Yet one more suggestion -- if at all possible, drop the double quotes from your object names.  Maybe it's just me, but I find them brutal.  Unless you have spaces, reserved words or mandatory uppercase in your field names (please don't do that), then these create more problems than they solve.  I kept them in the query I listed above, but it pained me.</p>
<p>And this last comment goes back to knowing your data...  since row_number and distinct on are relatively expensive operations, it may make sense to make your subquery/cte more selective by introducing the &quot;user1&quot; constraint.  This is completely untested, but something like this:</p>
<pre><code>SELECT distinct on (e1.correlation_id)
  e1.correlation_id, e1.event_id
FROM events e1
join events e2 on
  e1.correlation_id = e2.correlation_id and
  e2.username = 'user1'
order by
  e1.correlation_id, e1.create_timestamp desc
</code></pre>

### Answer ID: 73869752
<p>One option that may improve efficiency is to rewrite the query filtering &quot;rn&quot; = 1 beforehand to reduce resulting rows when joining tables:</p>
<pre><code>WITH &quot;latestCte&quot;(&quot;correlation_id&quot;, &quot;event_id&quot;) as (SELECT 
  &quot;correlation_id&quot;, 
  &quot;event_id&quot;, 
  ROW_NUMBER () OVER (
    PARTITION BY &quot;correlation_id&quot; 
    ORDER BY 
      &quot;create_timestamp&quot; ASC
  ) AS &quot;rn&quot; 
FROM 
  events)
SELECT 
  &quot;events&quot;.&quot;event_id&quot; AS &quot;event_id&quot;, 
  &quot;latest&quot;.&quot;event_id&quot; AS &quot;latest_event_id&quot; 
FROM 
  events &quot;events&quot; 
  JOIN (
    SELECT &quot;correlation_id&quot;, &quot;event_id&quot; FROM &quot;latestCte&quot; WHERE &quot;rn&quot; = 1
  ) &quot;latest&quot; ON (
    &quot;latest&quot;.&quot;correlation_id&quot; = &quot;events&quot;.&quot;correlation_id&quot; 
  ) 
WHERE 
  &quot;events&quot;.&quot;username&quot; = 'user1'
</code></pre>
<p>Hope it helps, also I am curious to see the resulting execution plan of this query. Best regards.</p>

