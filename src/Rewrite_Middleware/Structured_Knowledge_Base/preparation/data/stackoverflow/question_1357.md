# select ... into variable from table where 1=0 leads to the replacement of the variable with null
[Link to question](https://stackoverflow.com/questions/72398016/select-into-variable-from-table-where-1-0-leads-to-the-replacement-of-the-va)
**Creation Date:** 1653599271
**Score:** 0
**Tags:** database, postgresql, stored-procedures, plpgsql
## Question Body
<p>We are migrating a lot of code from SQL Server to Postgresql. We met the following problem, a serious difference between SQL Server and Postgresql.</p>
<p>Of course, below, by the expression 1=0, I meant cases when the query conditions do not return a single record.</p>
<p>A query in SQL Server:</p>
<pre><code>select @variable = t.field 
from table t 
where 1 = 0
</code></pre>
<p>saves the previous value of the variable.</p>
<p>A query in Postgresql:</p>
<pre><code>select t.field 
into variable 
from table t 
where 1 = 0
</code></pre>
<p>replaces the previous value of the variable with null.</p>
<p>We have already rewritten a lot of code without taking this feature into account.</p>
<p>Is there an easy way in postgresql, without rewriting the code, to save the value of a variable in such cases? For example, maybe there is some kind of server's or database's or session's settings? We did not find any relevant information in the documentation. We do not understand such a pattern of behavior in postgresql, which requires the introduction of additional variables and lines of code to check the result of the every query.</p>

## Answers
### Answer ID: 72398391
<p>As far as I know there is no way to change postgresql's behavior here.<br />
I don't have access to the SQL/PSM specifications, so I couldn't tell you which one matches the standard (if any / if <code>SELECT INTO &lt;variable&gt;</code> even is in it).</p>
<p>You don't need to use additional variables though, you can use <code>INTO STRICT</code> and catch the exception when no rows were returned:</p>
<pre><code>DO $$
    DECLARE
        variable int = 1;
    BEGIN
        BEGIN
            SELECT 1
            INTO STRICT variable
            WHERE FALSE;
        EXCEPTION
            WHEN NO_DATA_FOUND THEN
        END;
        RAISE NOTICE 'kept the previous value: %', variable;
    END
$$
</code></pre>
<p>shows &quot;kept the previous value: 1&quot;.<br />
Though it is obviously more verbose than the SQL Server version.</p>

