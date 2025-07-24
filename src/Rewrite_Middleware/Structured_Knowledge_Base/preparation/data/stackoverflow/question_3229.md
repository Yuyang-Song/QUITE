# With PostgREST, convert a column to and from an external encoding in the API
[Link to question](https://stackoverflow.com/questions/72537716/with-postgrest-convert-a-column-to-and-from-an-external-encoding-in-the-api)
**Creation Date:** 1654637036
**Score:** 1
**Tags:** postgresql, postgrest
## Question Body
<p>We are using PostgREST to automatically generate a REST API for a Postgres database. Our primary keys have an external representation that's different from how we store them internally. For simplicity's sake lets pretend the ids are stored as integers but we represent them as hexadecimal strings outwardly.</p>
<p>It's simple enough to get PostgREST to convert to the external representation for read operations:</p>
<pre><code>CREATE DOMAIN hexid AS bigint;

CREATE TABLE fruits (
    fruit_id hexid PRIMARY KEY,
    name text
);
CREATE OR REPLACE VIEW api_fruits AS
SELECT to_hex(fruit_id) as fruit_id, name FROM fruits;
INSERT INTO fruits(fruit_id, name) VALUES('51955', 'avocado');
</code></pre>
<p>PostgREST generates the expected representation when we <code>GET api_fruits</code>:</p>
<pre><code>[
    {
        &quot;fruit_id&quot;: &quot;caf3&quot;,
        &quot;name&quot;: &quot;avocado&quot;
    }
]
</code></pre>
<p>But that's about as far as we get with this solution. It's a one way transformation so we won't be able to POST/PATCH records this way. The way PostgREST works is to transform such requests into equivalent <code>INSERT</code> and <code>UPDATE</code> statements. But this view with its custom formatting is not updatable. This is what would happen if we tried:</p>
<pre><code>ERROR:  cannot insert into column &quot;fruit_id&quot; of view &quot;api_fruits&quot;
DETAIL:  View columns that are not columns of their base relation are not updatable.
STATEMENT:  WITH pgrst_source AS (WITH pgrst_payload AS (SELECT $1::json AS json_data), pgrst_body AS ( SELECT CASE WHEN json_typeof(json_data) = 'array' THEN json_data ELSE json_build_array(json_data) END AS val FROM pgrst_payload) INSERT INTO &quot;api_x&quot;.&quot;api_fruits&quot;(&quot;fruit_id&quot;, &quot;name&quot;) SELECT &quot;fruit_id&quot;, &quot;name&quot; FROM json_populate_recordset (null::&quot;api_x&quot;.&quot;api_fruits&quot;, (SELECT val FROM pgrst_body)) _  RETURNING &quot;api_x&quot;.&quot;api_fruits&quot;.*) SELECT '' AS total_result_set, pg_catalog.count(_postgrest_t) AS page_total, CASE WHEN pg_catalog.count(_postgrest_t) = 1 THEN coalesce((
WITH data AS (SELECT row_to_json(_) AS row FROM pgrst_source AS _ LIMIT 1)
SELECT array_agg(json_data.key || '=eq.' || json_data.value)
FROM data CROSS JOIN json_each_text(data.row) AS json_data
      WHERE json_data.key IN ('')
    ), array[]::text[]) ELSE array[]::text[] END AS header, '' AS body, nullif(current_setting('response.headers', true), '') AS response_headers, nullif(current_setting('response.status', true), '') AS response_status FROM (SELECT * FROM pgrst_source) _postgrest_t
</code></pre>
<p>We can't INSERT into &quot;View columns that are not columns of their base relation&quot;.</p>
<p>The obvious workaround is to serve <code>fruit_id</code> as a straight column, just an integer. With some post and preprocessing at the nginx level we can hex encode it there (and hex decode incoming ids). I'm wondering if we can do better than that though. For large API operations, re-encoding the JSON will use a lot of memory and CPU time and it seems so unnecessary.</p>
<p>It would have been great to be able to use a custom <code>CREATE CAST</code> to take the incoming hexadecimal strings and turn them back into integers, something like this:</p>
<pre><code>CREATE CAST (json AS hexid) WITH FUNCTION json_to_hexid AS ASSIGNMENT;
</code></pre>
<p>But alas custom casts are ignored on <code>CREATE DOMAIN</code> types. And we can't make a true custom column type because our cloud Postgres host (Google Cloud SQL) doesn't allow custom extensions.</p>
<p>It feels like some combination of <code>INSTEAD OF</code> triggers or rules could work. But when using query parameters to filter results using query parameters (e.g. select a fruit by id), I don't think there's an appropriate trigger to use. <code>INSTEAD OF</code> doesn't work for straight <code>SELECT</code> does it?</p>
<p>For example I've tested doing something like this to take care of <code>INSERT</code> and allow <code>POST</code> with PostgREST. It works:</p>
<pre><code>CREATE OR REPLACE FUNCTION api_fruits_insert()
RETURNS trigger AS
$$
BEGIN
  INSERT INTO fruits(fruit_id, name) VALUES (('x' || lpad(NEW.fruit_id, 16, '0'))::bit(64)::bigint::hexid, NEW.name);
  RETURN NEW;
END
$$ LANGUAGE 'plpgsql';

CREATE TRIGGER api_fruits_insert
INSTEAD OF INSERT
ON api_fruits
FOR EACH ROW
EXECUTE PROCEDURE api_fruits_insert();
</code></pre>
<p>The trouble is in the WHERE clause. Let's <code>PATCH api_fruits?fruit_id=in.(7b,caf3)</code> with <code>{&quot;name&quot;: &quot;pear&quot;}</code>. This works out of the box since the name column is updatable but look at the query:</p>
<pre><code>WITH pgrst_source AS (WITH pgrst_payload AS (SELECT $1::json AS json_data), pgrst_body AS ( SELECT CASE WHEN json_typeof(json_data) = 'array' THEN json_data ELSE json_build_array(json_data) END AS val FROM pgrst_payload) UPDATE &quot;api_x&quot;.&quot;api_fruits&quot; SET &quot;name&quot; = _.&quot;name&quot; FROM (SELECT * FROM json_populate_recordset (null::&quot;api_x&quot;.&quot;api_fruits&quot; , (SELECT val FROM pgrst_body) )) _ WHERE  &quot;api_x&quot;.&quot;api_fruits&quot;.&quot;fruit_id&quot; = ANY ($2) RETURNING 1) SELECT '' AS total_result_set, pg_catalog.count(_postgrest_t) AS page_total, array[]::text[] AS header, '' AS body, nullif(current_setting('response.headers', true), '') AS response_headers, nullif(current_setting('response.status', true), '') AS response_status FROM (SELECT * FROM pgrst_source) _postgrest_t
DETAIL:  parameters: $1 = '{
        &quot;name&quot;: &quot;pear&quot;
    }', $2 = '{7b,caf3}'
</code></pre>
<p>So we have essentially <code>UPDATE api_fruits SET name='berry' WHERE fruit_id IN ('7b', 'caf3');</code>. Surprisingly this works but it's a full table scan so Postgres can evaluate <code>to_hex(fruit_id)</code> for each row looking for matches. The same happens if we try to <code>GET</code> a record by fruit_id. How would we rewrite the <code>WHERE</code> clauses?</p>
<p>It really feels like some combination of just the right Postgres and PostgREST features should be able to get us to a point where it's all happening in Postgres without nginx's help and without excessive complexity. Any ideas?</p>

