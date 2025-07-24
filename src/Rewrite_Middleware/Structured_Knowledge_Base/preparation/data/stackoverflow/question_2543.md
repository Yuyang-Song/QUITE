# Translating query from Firebird to PostgreSQL # 2
[Link to question](https://stackoverflow.com/questions/39099903/translating-query-from-firebird-to-postgresql-2)
**Creation Date:** 1471951660
**Score:** 0
**Tags:** sql, postgresql, firebird
## Question Body
<p>I have a SQL query :</p>

<pre><code>SELECT TRIM(RL.RDB$RELATION_NAME), TRIM(FR.RDB$FIELD_NAME), FS.RDB$FIELD_TYPE, TRIM(RC.RDB$CONSTRAINT_TYPE)
    FROM RDB$RELATIONS RL
        LEFT OUTER JOIN RDB$RELATION_FIELDS FR ON FR.RDB$RELATION_NAME = RL.RDB$RELATION_NAME
        LEFT OUTER JOIN RDB$FIELDS FS ON FS.RDB$FIELD_NAME = FR.RDB$FIELD_SOURCE
        LEFT OUTER JOIN RDB$INDEX_SEGMENTS ISS ON ISS.RDB$FIELD_NAME = FR.RDB$FIELD_NAME
            INNER JOIN RDB$RELATION_CONSTRAINTS RC ON RC.RDB$CONSTRAINT_NAME = ISS.RDB$INDEX_NAME
            WHERE (RL.RDB$VIEW_BLR IS NULL)
                ORDER BY RL.RDB$RELATION_NAME, FR.RDB$FIELD_NAME
</code></pre>

<p>Yesterday i asked how correctly translate a query from Firebird to PostgreSQL and I'm asking once again :) . (But I'd just started working with databases and got really hard task (rewrite a big part of code, because RDBMS had been changed) ). A big part is done, but I have a problems with this translation. So, can u help me? <a href="http://pastebin.com/z03gGjy2" rel="nofollow">There is some code</a> which i've translated by myself.</p>

