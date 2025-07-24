# This query doesn&#39;t work. What am I doing wrong?
[Link to question](https://stackoverflow.com/questions/22199168/this-query-doesnt-work-what-am-i-doing-wrong)
**Creation Date:** 1394026102
**Score:** -1
**Tags:** sql, sql-server
## Question Body
<p>I'm writing an update to an automated task that is used to sync data from two different tables in the same database from different applications.  The original version of the script was written in ColdFusion and works absolutely fine, but I want to rewrite a portion of the code in SQL for improved performance.  The original code script is in ColdFusion and looks like this:</p>

<pre><code>&lt;cfquery name="getIMSIToUpdate" datasource="mydsn"&gt;
SELECT DISTINCT a.imsi, b.esn, b.parentId
FROM table_a a
INNER JOIN table_b b ON a.imsi = b.termPhone
WHERE (a.parentID IS NULL OR a.parentID = '')
&lt;/cfquery&gt;

&lt;cfloop query="getIMSIToUpdate"&gt;
&lt;cfquery name="updtIMSIParentIdEsn" datasource="mydsn"&gt;
    UPDATE table_a
    SET esn = &lt;cfqueryparam cfsqltype="cf_sql_varchar" value="#Trim(getIMSIToUpdate.esn)#" null="#NOT Len(Trim(getIMSIToUpdate.esn))#" /&gt;
        ,parentId = &lt;cfqueryparam cfsqltype="cf_sql_integer" value="#Trim(getIMSIToUpdate.parentId)#" null="#NOT Len(Trim(getIMSIToUpdate.parentId))#" /&gt;
    WHERE imsi = &lt;cfqueryparam cfsqltype="cf_sql_varchar" value="#Trim(getIMSIToUpdate.imsi)#" /&gt;
&lt;/cfquery&gt;
</code></pre>

<p></p>

<p>So I'm querying records from table A, then looping through each record returned and performing an update to table A's values based on what was retrieved from table B in the original query.  This is the SQL query I wrote to replace this code:</p>

<pre><code>BEGIN
    DECLARE @update_table TABLE (imsi VARCHAR(25), esn VARCHAR(25), parentId INT);
    DECLARE @localimsi VARCHAR(25);
    DECLARE @localesn VARCHAR(25);
    DECLARE @localparentid INT;
    SELECT a.imsi, b.esn, b.parentId
    INTO "dbo"."@update_table"
    FROM dbo.table_a A
    INNER JOIN table_b B ON A.imsi = B.termPhone
    WHERE (A.parentID IS NULL OR A.parentID = '');
    WHILE (SELECT COUNT(*) FROM @update_table) &lt;&gt; 0
        SELECT TOP 1 
        @localimsi = imsi,
        @localesn = esn,
        @localparentid = parentid
        FROM @update_table;

        UPDATE table_a A
        SET esn = @localesn,
        parentId = @localparentid
        WHERE imsi = @localimsi;

        DELETE FROM @update_table WHERE imsi = @localimsi;
END
DROP TABLE "dbo"."@update_table";
</code></pre>

<p>I'm sure there is a way that I can troubleshoot this on my own, but I'm not familiar with how the SQL Server debugger works so I'm not 100% sure what is actually happening, only what I think is supposed to be happening.  The query does select the appropriate rows and values and inserts them into the temp table, but it isn't updating any of the selected records.  Additional input on how to write this SQL script to be even more efficient would be appreciated, but won't earn an answer award by itself.</p>

## Answers
### Answer ID: 22200818
<p>This is kinda hard without a schema, but what I think you're doing is updating table A to have the ESN and parentID from table B where a.IMSI = b.termPhone and the parentid on table a is null or empty.</p>

<p>You can do this using a single query:</p>

<pre><code>update table_a
set esn = b.esn, 
    parentid = b.termphone
from table_a a, 
     table_b b
where a.imsi = b.termphone
and (a.parentid is null
     or a.parentid = '')
</code></pre>

