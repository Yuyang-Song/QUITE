# SQL Union All is too slow
[Link to question](https://stackoverflow.com/questions/15547139/sql-union-all-is-too-slow)
**Creation Date:** 1363867802
**Score:** 2
**Tags:** sql, sql-server, performance, union
## Question Body
<p>I am rewriting an old legacy system. It has a function called <code>checkExisting()</code>. The old system was using queries for extracting objects from the MSSQL database like this (with ADO DB):</p>

<pre><code>SELECT ObjectId, Name..... 
FROM tblRegisteredIncludes   
WHERE UPPER("Name") IN ('PROGA.H', 'PROGB.H'...............  list)
</code></pre>

<p>There are many tables like <code>tblRegisteredIncludes</code> but SQLs are grouped by the tablename and are using the IN clause with list of object names. </p>

<p>This is executing properly fast because SQL Server collects all objects in one scan and there was an index over the <code>Name</code> column in the table.</p>

<p>However, in the new system, I can not use the same SQL because the <code>WHERE</code> condition is more complex. It is also using a Source field and sometimes and other fields in the condition. I have a larger number of single SQL queries:</p>

<pre><code>SELECT ObjectId, Name..... FROM tblRegisteredIncludes   
WHERE UPPER("Name") = 'PROGA.H' AND UPPER("Source") = "..."

SELECT ObjectId, Name..... FROM tblRegisteredIncludes   
WHERE UPPER("Name") = ('PROGB.H') AND UPPER("Source") = "..."
</code></pre>

<p>I have replaced the Name-Index in <code>tblRegisteredIncludes</code> table with a composite index over <code>(Name,Source)</code>. </p>

<p>I have expected even so the total SQLs execution to be a little slower but with no more than 15-20%. Instead it is much, much slower, sometimes up to 100%. I tried to combine the SQLs in a single large SQL query using UNION ALL:</p>

<pre><code>SELECT ObjectId, Name..... FROM tblRegisteredIncludes   
WHERE UPPER("Name") = 'PROGA.H' AND UPPER("Source") = "..."
UNION ALL
SELECT ObjectId, Name..... FROM tblRegisteredIncludes   
WHERE UPPER("Name") = ('PROGB.H') AND UPPER("Source") = "..."
</code></pre>

<p>and then pocessing the resulting ADO DB recordset later but it is even slower! </p>

<p>I need to know whether there is some efficient way to execute these queries faster? I need to reach performance similar to the old case when using IN clause and a list of names. I can provide the execution plan.</p>

## Answers
### Answer ID: 15548538
<p>In the <code>union all</code> version, each subquery is resulting in a separate scan of the table.</p>

<p>You should be bringing in all the rows using <code>or</code> conditions:</p>

<pre><code>SELECT ObjectId, Name.....
FROM tblRegisteredIncludes   
WHERE (UPPER("Name") = 'PROGA.H' AND UPPER("Source") = "...") or
      (UPPER("Name") = ('PROGB.H') AND UPPER("Source") = "...") or
      . . .
</code></pre>

<p>If you have a situation where all the comparisons are on <code>Name</code> and <code>Source</code>, I would suggest creating a table-on-the-fly using a CTE:</p>

<pre><code>with toinclude as (
   select 'PROGA.H' as name, 'SOURCE' as source union all
   select . . .
)
select ri.ObjectId, ri.Name
from tblRegisteredIncludes join
     toinclude
     on ri.name = toinclude.name and ri.source = toinclude.source
</code></pre>

<p>You can leave out the <code>toupper()</code> unless you are specifically concerned that your implementation or fields have overridden the default of case-insensitive behavior.  The use of a function in a <code>where</code> clause generally prevents the use of indexes.</p>

### Answer ID: 15548039
<p>From what you describe I assume the table has a very large number of rows in which case it is almost certainly the UPPER which is causing the speed issue because that means it can't properly use the indexes which you appeaar to have correctly set. Is the data stored really case-sensitive? - check db setting, by default it usually isn't in which case you can remove the UPPER.</p>

<p>If it IS case-sensitive then if the case of the stored names is consistent you can still remove the Upper and just use whatever the consistent upper/lower case name is e.g. Name = 'ProgB.H'</p>

