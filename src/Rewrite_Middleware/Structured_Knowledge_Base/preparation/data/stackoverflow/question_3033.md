# mariadb/mysql Nested `WITH` statement causes table-not-found error
[Link to question](https://stackoverflow.com/questions/63111934/mariadb-mysql-nested-with-statement-causes-table-not-found-error)
**Creation Date:** 1595840278
**Score:** 0
**Tags:** mysql, sql, mariadb
## Question Body
<p>I am not sure if this is a documented limit in mariadb or a bug in its query parsing. We are porting some enormous queries from vertica to mariadb, and I have encountered cases where queries with nested <code>WITH</code> clauses is throwing a bogus table-not-found error.</p>
<p>Running mariadb version: 10.3.14</p>
<p>The actual sql is monstrous, but I have been able to reduce it to a simple case which fails.
<strong>with-bad.sql</strong></p>
<pre><code>WITH v1 AS
(   SELECT  'fred' AS name
),
v2 AS
(   WITH v21 AS
    (   SELECT  alias11.name
        FROM    v1 alias11
        JOIN    v1 alias12
        ON      alias11.name = alias12.name
    )
    SELECT  name FROM v21
),
v3 AS
(   WITH v31 AS
    (   SELECT  alias21.name
        FROM    v2 alias21
        JOIN    v2 alias22
        ON      alias21.name = alias22.name
    )
    SELECT  name FROM v31
)
SELECT * FROM v3
</code></pre>
<p>Fails with error:</p>
<pre><code>MariaDB [MYSCHEMA]&gt; \. with-bad.sql
ERROR 1146 (42S02) at line 1 in file: 'with-bad.sql': Table 'MYSCHEMA.v1' doesn't exist
</code></pre>
<p>But, it does work if I have one less <code>WITH</code>.
<strong>with-good.sql</strong></p>
<pre><code>WITH v1 AS
(   SELECT  'fred' AS name
),
v2 AS
(   WITH v21 AS
    (   SELECT  alias11.name
        FROM    v1 alias11
        JOIN    v1 alias12
        ON      alias11.name = alias12.name
    )
    SELECT  name FROM v21
)
SELECT * FROM v2
</code></pre>
<p>And also works if there is no join in the 3rd <code>WITH</code>.
<strong>with-nojoin.sql</strong></p>
<pre><code>WITH v1 AS
(   SELECT  'fred' AS name
),
v2 AS
(   WITH v21 AS
    (   SELECT  alias11.name
        FROM    v1 alias11
        JOIN    v1 alias12
        ON      alias11.name = alias12.name
    )
    SELECT  name FROM v21
),
v3 AS
(   WITH v31 AS
    (   SELECT  alias21.name
        FROM    v2 alias21
    )
    SELECT  name FROM v31
)
SELECT * FROM v3
</code></pre>
<p>The <strong>with-bad.sql</strong> example does work in other database engines (e.g. vertica) so not a stupid typo by me (the cause of most of my errors).</p>
<p>Does anyone know if this is a known mariadb/mysql limit, or known bug? Feels like a bug (i.e. the extra code which causes it does not even reference <code>v1</code> directly).</p>
<p>Any suggested &quot;mechanical&quot; workarounds would be very much appreciated. Actual SQL is very complex, so hoping to avoid a complete rewrite/restructure it if possible.</p>
<p>Thanks</p>

## Answers
### Answer ID: 63112141
<p>Do NOT use nested WITH, use chained one.</p>
<p>For example, your <strong>with-bad.sql</strong> should be</p>
<pre><code>WITH 
v1 AS
(   SELECT  'fred' AS name
),
v21 AS
(   SELECT  alias11.name
    FROM    v1 alias11
    JOIN    v1 alias12
    ON      alias11.name = alias12.name
),
v2 AS
(   SELECT  name FROM v21
),
v31 AS
(   SELECT  alias21.name
    FROM    v2 alias21
    JOIN    v2 alias22
    ON      alias21.name = alias22.name
),
v3 AS
(   SELECT  name FROM v31
)
SELECT * FROM v3
</code></pre>

