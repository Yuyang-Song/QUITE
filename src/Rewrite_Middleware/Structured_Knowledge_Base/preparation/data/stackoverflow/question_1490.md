# How to Query Entries with Specific Decision IDs in MS Access
[Link to question](https://stackoverflow.com/questions/78752933/how-to-query-entries-with-specific-decision-ids-in-ms-access)
**Creation Date:** 1721110852
**Score:** 1
**Tags:** sql, mysql, ms-access
## Question Body
<p>I have a table named MyTable linked from an external MS Access database (C:\Data\LinkedDatabases\ExternalData.mdb). The table structure includes GroupId, RuleId, and DecisionCode.</p>
<p>I need to create a query that lists all entries from this table where the values 10 and 42 both exist in the DecisionCode field under the same GroupId and RuleId. However, it should only return these entries if both DecisionCode values 10 and 42 exist for the same GroupId and RuleId.</p>
<p>Here is the query I initially wrote, which results in a syntax error:</p>
<pre><code>SELECT A.*
FROM (SELECT * FROM MyTable IN 'C:\Data\LinkedDatabases\ExternalData.mdb') AS A
WHERE EXISTS (
SELECT 1
FROM (
    SELECT GroupId, RuleId
    FROM MyTable IN 'C:\Data\LinkedDatabases\ExternalData.mdb'
    WHERE DecisionCode IN (10, 42)
    GROUP BY GroupId, RuleId
    HAVING COUNT(DISTINCT DecisionCode) = 2
) AS B
WHERE A.GroupId = B.GroupId
AND A.RuleId = B.RuleId
)
AND A.DecisionCode IN (10, 42);
</code></pre>
<p>I encountered a syntax error: &quot;missing operator in query expression 'COUNT(DISTINCT DecisionCode) = 2'&quot;.</p>
<p>I understand that DISTINCT is not supported in the COUNT function in MS Access. How can I rewrite this query to achieve the desired result?</p>
<p>Here’s the revised attempt, which still doesn’t return the correct results:</p>
<pre><code>SELECT A.*
FROM (SELECT * FROM MyTable IN 'C:\Data\LinkedDatabases\ExternalData.mdb') AS A
WHERE EXISTS (
    SELECT 1
    FROM (
        SELECT GroupId, RuleId
        FROM MyTable IN 'C:\Data\LinkedDatabases\ExternalData.mdb'
        WHERE DecisionCode IN (10, 42)
        GROUP BY GroupId, RuleId
        HAVING COUNT(*) = 2
    ) AS B
    WHERE A.GroupId = B.GroupId
    AND A.RuleId = B.RuleId
    AND EXISTS (
        SELECT 1
        FROM MyTable AS C
        WHERE C.GroupId = A.GroupId
        AND C.RuleId = A.RuleId
        AND C.DecisionCode = 10
    )
    AND EXISTS (
        SELECT 1
        FROM MyTable AS D
        WHERE D.GroupId = A.GroupId
        AND D.RuleId = A.RuleId
        AND D.DecisionCode = 42
    )
)
AND A.DecisionCode IN (10, 42);
</code></pre>
<p>This query includes nested subqueries to ensure that both DecisionCode 10 and 42 exist for the same GroupId and RuleId. However, it still returns entries that only contain DecisionCode 10.</p>
<p>Any advice on how to correctly structure this query in MS Access?</p>
<p>Example Data:</p>
<div class="s-table-container"><table class="s-table">
<thead>
<tr>
<th style="text-align: left;">GroupId</th>
<th style="text-align: left;">RuleId</th>
<th style="text-align: left;">DecisionCode</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;">1</td>
<td style="text-align: left;">15</td>
<td style="text-align: left;">10</td>
</tr>
<tr>
<td style="text-align: left;">1</td>
<td style="text-align: left;">15</td>
<td style="text-align: left;">42</td>
</tr>
<tr>
<td style="text-align: left;">1</td>
<td style="text-align: left;">16</td>
<td style="text-align: left;">10</td>
</tr>
<tr>
<td style="text-align: left;">1</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">10</td>
</tr>
<tr>
<td style="text-align: left;">2</td>
<td style="text-align: left;">15</td>
<td style="text-align: left;">10</td>
</tr>
<tr>
<td style="text-align: left;">2</td>
<td style="text-align: left;">16</td>
<td style="text-align: left;">10</td>
</tr>
<tr>
<td style="text-align: left;">2</td>
<td style="text-align: left;">16</td>
<td style="text-align: left;">42</td>
</tr>
<tr>
<td style="text-align: left;">2</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">42</td>
</tr>
<tr>
<td style="text-align: left;">3</td>
<td style="text-align: left;">15</td>
<td style="text-align: left;">10</td>
</tr>
<tr>
<td style="text-align: left;">3</td>
<td style="text-align: left;">16</td>
<td style="text-align: left;">10</td>
</tr>
<tr>
<td style="text-align: left;">3</td>
<td style="text-align: left;">17</td>
<td style="text-align: left;">10</td>
</tr>
</tbody>
</table></div>
<p>Desired outcome:</p>
<div class="s-table-container"><table class="s-table">
<thead>
<tr>
<th style="text-align: left;">GroupId</th>
<th style="text-align: left;">RuleId</th>
<th style="text-align: left;">DecisionCode</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;">1</td>
<td style="text-align: left;">15</td>
<td style="text-align: left;">10</td>
</tr>
<tr>
<td style="text-align: left;">1</td>
<td style="text-align: left;">15</td>
<td style="text-align: left;">42</td>
</tr>
<tr>
<td style="text-align: left;">2</td>
<td style="text-align: left;">16</td>
<td style="text-align: left;">10</td>
</tr>
<tr>
<td style="text-align: left;">2</td>
<td style="text-align: left;">16</td>
<td style="text-align: left;">42</td>
</tr>
</tbody>
</table></div>

## Answers
### Answer ID: 78753372
<p>Make sure GroupID and RuleID pair is IN set filtered for 42 AND set filtered for 10:</p>
<pre><code>SELECT MyTable.*
FROM MyTable
WHERE GroupID &amp; &quot;:&quot; &amp; RuleID IN 
    (SELECT GroupID &amp; &quot;:&quot; &amp; RuleID FROM MyTable WHERE DecisionCode = 42) 
AND GroupID &amp; &quot;:&quot; &amp; RuleID IN 
    (SELECT GroupID &amp; &quot;:&quot; &amp; RuleID FROM MyTable WHERE DecisionCode =10);
</code></pre>

### Answer ID: 78753523
<p><a href="https://i.sstatic.net/F08MCneV.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/F08MCneV.png" alt="enter image description here" /></a></p>
<pre><code>    select * from data as d 
where exists  
(select 1 from data as d2 where d2.groupid=d.groupid and d2.ruleid=d.ruleid                         and d2.decisioncode=10) 
and exists  (select 1 from data as d2 where d2.groupid=d.groupid and d2.ruleid=d.ruleid  and d2.decisioncode=42)
</code></pre>

