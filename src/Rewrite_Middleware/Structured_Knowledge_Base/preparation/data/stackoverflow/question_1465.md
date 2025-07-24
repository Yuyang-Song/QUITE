# SQL Server Recursive CTE to shred JSON: Types don&#39;t match between the anchor and the recursive part
[Link to question](https://stackoverflow.com/questions/77237030/sql-server-recursive-cte-to-shred-json-types-dont-match-between-the-anchor-and)
**Creation Date:** 1696508270
**Score:** 0
**Tags:** json, sql-server, recursion, common-table-expression
## Question Body
<p>I am trying to rewrite a function to an inline Table Valued Fuction.
Database is SQL Server 2022.
Please have a look at the following <a href="http://sqlfiddle.com/#!18/089b0/2" rel="nofollow noreferrer">SQL Fiddle</a>. I tried multiple rewrites with explicit CASTs but it still wouldn't work for the key from the OPENJSON function. Running the query without that column however works as expected.</p>
<p>Can you please give any insight why this error occurs and how to fix it?</p>
<p>Thanks to @siggemannen for the solution: The collation of the key has to be changed as well.Here's a <a href="http://sqlfiddle.com/#!18/089b0/11/0" rel="nofollow noreferrer">SQL Fiddle</a> to show the working solution.</p>
<p>Here's the example as code:</p>
<pre><code>  DECLARE @json NVARCHAR(MAX) =N'{&quot;menu&quot;: {  
  &quot;id&quot;: &quot;file&quot;,  
  &quot;value&quot;: &quot;File&quot;,  
  &quot;popup&quot;: {  
    &quot;menuitem&quot;: [  
      {&quot;value&quot;: &quot;New&quot;, &quot;onclick&quot;: &quot;CreateDoc()&quot;},  
      {&quot;value&quot;: &quot;Open&quot;, &quot;onclick&quot;: &quot;OpenDoc()&quot;},  
      {&quot;value&quot;: &quot;Save&quot;, &quot;onclick&quot;: &quot;SaveDoc()&quot;}  
    ]  
  }  
}}  '
;
/* code adapted from Phil Factor 
https://www.red-gate.com/simple-talk/databases/sql-server/t-sql-programming-sql-server/importing-json-web-services-applications-sql-server/
*/
WITH cteRecurseJSON AS
(
    SELECT 
        CAST(1 AS INTEGER) AS Depth, 
        --CAST('$' AS NVARCHAR(4000)) AS ThePath,
        CAST(N'' AS NVARCHAR(4000)) AS ThePath,
        CAST(@json  AS NVARCHAR(MAX)) AS TheValue, 
        CAST('object' AS VARCHAR(10)) AS ValueType
    UNION ALL
    SELECT 
        r.Depth+1 AS Depth,
            CAST(v.[Key] AS NVARCHAR(4000)) AS ThePath,
        Coalesce(Value,'') AS TheValue,
        CAST(CASE Type WHEN 1 THEN 'string'
                WHEN 0 THEN 'null'
                WHEN 2 THEN 'int'
                WHEN 3 THEN 'boolean'
                WHEN 4 THEN 'array' ELSE 'object' END AS VARCHAR(10)) AS ValueType
    FROM cteRecurseJSON r
    CROSS APPLY OPENJSON(r.TheValue) v
    WHERE r.ValueType IN ('array','object')

)
SELECT *
FROM cteRecurseJSON
</code></pre>

## Answers
### Answer ID: 77241301
<p>The value <code>ThePath</code> in the anchor part needs to be <code>nvarchar(max)</code> and you need to change the collation <a href="https://stackoverflow.com/questions/77237030/sql-server-recursive-cte-to-shred-json-types-dont-match-between-the-anchor-and#comment136163799_77237030">as noted by @siggemanen</a>.</p>
<p>You should also use <code>STRING_ESCAPE</code> for correct escaping of paths. And you can simplify the <code>CASE</code> by just checking for an array.</p>
<pre class="lang-sql prettyprint-override"><code>WITH cteRecurseJSON AS
(
    SELECT 
        CAST(1 AS INTEGER) AS Depth, 
        CAST(N'$' AS NVARCHAR(max))  COLLATE database_default AS ThePath,
        CAST(jsonValue  AS NVARCHAR(MAX)) AS TheValue, 
        CAST('object' AS VARCHAR(10)) AS ValueType
    FROM test
    UNION ALL
    SELECT 
        r.Depth+1 AS Depth,
        CAST(
          r.ThePath +
          CASE WHEN r.ValueType = 'array' THEN '[' + v.[key] + ']'
               WHEN STRING_ESCAPE(v.[key], 'json') &lt;&gt; v.[key] THEN '.&quot;' + STRING_ESCAPE(v.[key], 'json') + '&quot;' --got a space in it
               ELSE '.' + v.[Key]
            END
          AS  NVARCHAR(MAX)) AS ThePath,
        Coalesce(Value,'') AS TheValue,
        CAST(CASE Type
                WHEN 1 THEN 'string'
                WHEN 0 THEN 'null'
                WHEN 2 THEN 'int'
                WHEN 3 THEN 'boolean'
                WHEN 4 THEN 'array'
                ELSE 'object' END AS VARCHAR(10)) AS ValueType
    FROM cteRecurseJSON r
    CROSS APPLY OPENJSON(r.TheValue) v
    WHERE r.ValueType IN ('array', 'object')
)
SELECT *
FROM cteRecurseJSON;
</code></pre>
<p><a href="https://dbfiddle.uk/DYNd2sE9" rel="nofollow noreferrer"><strong>db&lt;&gt;fiddle</strong></a></p>

