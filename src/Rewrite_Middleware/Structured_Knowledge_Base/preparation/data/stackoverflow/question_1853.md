# Similar UTF-8 strings for autocomplete field
[Link to question](https://stackoverflow.com/questions/10237366/similar-utf-8-strings-for-autocomplete-field)
**Creation Date:** 1334872354
**Score:** 2
**Tags:** postgresql, utf-8, plpgsql, string-comparison, similarity
## Question Body
<h2>Background</h2>

<p>Users can type in a name and the system should match the text, even if the either the user input or the database field contains accented (UTF-8) characters. This is using the <code>pg_trgm</code> module.</p>

<h2>Problem</h2>

<p>The code resembles the following:</p>

<pre><code>  SELECT
    t.label
  FROM
    the_table t
  WHERE
    label % 'fil'
  ORDER BY
    similarity( t.label, 'fil' ) DESC
</code></pre>

<p>When the user types <code>fil</code>, the query matches <code>filbert</code> but not <code>filé powder</code>. (Because of the accented character?)</p>

<h3>Failed Solution #1</h3>

<p>I tried to implement an <a href="https://stackoverflow.com/a/3051845/59087">unaccent</a> function and rewrite the query as:</p>

<pre><code>  SELECT
    t.label
  FROM
    the_table t
  WHERE
    unaccent( label ) % unaccent( 'fil' )
  ORDER BY
    similarity( unaccent( t.label ), unaccent( 'fil' ) ) DESC
</code></pre>

<p>This returns only <code>filbert</code>.</p>

<h3>Failed Solution #2</h3>

<p>As suggested:</p>

<pre><code>CREATE EXTENSION pg_trgm;
CREATE EXTENSION unaccent;

CREATE OR REPLACE FUNCTION unaccent_text(text)
  RETURNS text AS
$BODY$
  SELECT unaccent($1); 
$BODY$
  LANGUAGE sql IMMUTABLE
  COST 1;
</code></pre>

<p>All other indexes on the table have been dropped. Then:</p>

<pre><code>CREATE INDEX label_unaccent_idx 
ON the_table( lower( unaccent_text( label ) ) );
</code></pre>

<p>This returns only one result:</p>

<pre><code>  SELECT
    t.label
  FROM
    the_table t
  WHERE
    label % 'fil'
  ORDER BY
    similarity( t.label, 'fil' ) DESC
</code></pre>

<h2>Question</h2>

<p>What is the best way to rewrite the query to ensure that both results are returned?</p>

<p>Thank you!</p>

<h2>Related</h2>

<p><a href="http://wiki.postgresql.org/wiki/What%27s_new_in_PostgreSQL_9.0#Unaccent_filtering_dictionary" rel="nofollow noreferrer">http://wiki.postgresql.org/wiki/What%27s_new_in_PostgreSQL_9.0#Unaccent_filtering_dictionary</a></p>

<p><a href="http://postgresql.1045698.n5.nabble.com/index-refuses-to-build-td5108810.html" rel="nofollow noreferrer">http://postgresql.1045698.n5.nabble.com/index-refuses-to-build-td5108810.html</a></p>

## Answers
### Answer ID: 10238113
<p>You are not using the operator class provided by the <code>pg_trgm</code> module. Create an index like this:</p>
<pre class="lang-sql prettyprint-override"><code>CREATE INDEX label_Lower_unaccent_trgm_idx
ON test_trgm USING gist (lower(unaccent_text(label)) gist_trgm_ops);
</code></pre>
<p>Originally, I had a GIN index here, but a GiST is typically better suited for this kind of query because it can return values sorted by similarity. See:</p>
<ul>
<li><a href="https://stackoverflow.com/questions/11281103/postgresql-matching-patterns-between-two-columns/11282358#11282358">Matching patterns between multiple columns</a></li>
<li><a href="https://stackoverflow.com/questions/11249635/finding-similar-strings-with-postgresql-quickly/11250001#11250001">Finding similar strings with PostgreSQL quickly</a></li>
</ul>
<p>Your query has to match the index expression to be able to use it.</p>
<pre class="lang-sql prettyprint-override"><code>SELECT label
FROM   the_table
WHERE  lower(unaccent_text(label)) % 'fil'
ORDER  BY similarity(label, 'fil') DESC;  -- ok to use original string here
</code></pre>
<p>However, &quot;filbert&quot; and &quot;filé powder&quot; are not actually very similar to &quot;fil&quot; according to the <code>%</code> operator. I suspect you really want:</p>
<pre class="lang-sql prettyprint-override"><code>SELECT label
FROM   the_table
WHERE  lower(unaccent_text(label)) LIKE 'fil%'  -- !
ORDER  BY similarity(label, 'fil') DESC;  -- ok to use original string here
</code></pre>
<p>This finds all strings starting with the search string, and sorts the best matches according to the <code>%</code> operator first.</p>
<p>The expression can use a GIN or GiST index since PostgreSQL <strong>9.1</strong>! <a href="https://www.postgresql.org/docs/current/pgtrgm.html#PGTRGM-FUNC-TABLE" rel="nofollow noreferrer">The manual</a>:</p>
<blockquote>
<p>Beginning in PostgreSQL 9.1, these index types also support index
searches for <code>LIKE</code> and <code>ILIKE</code>, for example</p>
</blockquote>
<p><strong>If</strong> you actually meant to use the <code>%</code> operator:</p>
<p>Try <a href="https://www.postgresql.org/docs/current/pgtrgm.html#PGTRGM-FUNC-TABLE" rel="nofollow noreferrer"><strong>adapting the threshold</strong></a> for the similarity operator <code>%</code>:</p>
<pre><code>SET pg_trgm.similarity_threshold = 0.1;  -- Postgres 9.6 or later
SELECT set_limit(0.1);  -- Postgres 9.5 or older
</code></pre>
<p>Or even lower? The default is 0.3. Just to see whether the threshold filters additional matches.</p>

### Answer ID: 10238184
<p>A solution for PostgreSQL 9.1:</p>

<pre><code>-- Install the requisite extensions.
CREATE EXTENSION pg_trgm;
CREATE EXTENSION unaccent;

-- Function fixes STABLE vs. IMMUTABLE problem of the unaccent function.
CREATE OR REPLACE FUNCTION unaccent_text(text)
  RETURNS text AS
$BODY$
  -- unaccent is STABLE, but indexes must use IMMUTABLE functions.
  SELECT unaccent($1); 
$BODY$
  LANGUAGE sql IMMUTABLE
  COST 1;

-- Create an unaccented index.
CREATE INDEX the_table_label_unaccent_idx
ON the_table USING gin (lower(unaccent_text(label)) gin_trgm_ops);

-- Define the matching threshold.
SELECT set_limit(0.175);

-- Test the query (matching against the index expression).
SELECT
  label
FROM
  the_table
WHERE
  lower(unaccent_text(label)) % 'fil'
ORDER BY
  similarity(label, 'fil') DESC 
</code></pre>

<p>Returns "filbert", "fish fillet", and "filé powder".</p>

<p>Without calling <code>SELECT set_limit(0.175);</code>, you can use the double tilde (<code>~~</code>) operator:</p>

<pre><code>-- Test the query (matching against the index expression).
SELECT
  label
FROM
  the_table
WHERE
  lower(unaccent_text(label)) ~~ 'fil'
ORDER BY
  similarity(label, 'fil') DESC 
</code></pre>

<p>Also returns "filbert", "fish fillet", and "filé powder".</p>

