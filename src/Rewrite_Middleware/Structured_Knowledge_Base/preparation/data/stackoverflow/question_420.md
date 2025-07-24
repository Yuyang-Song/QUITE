# Mysql query/subquery
[Link to question](https://stackoverflow.com/questions/25515906/mysql-query-subquery)
**Creation Date:** 1409090660
**Score:** 3
**Tags:** php, mysql
## Question Body
<p>I'm trying to conform an existing database and system to data we are now receiving from a manufacturer.  Its format can't/won't be changed.  It is a table with product numbers (item_id) from a single manufacturer that cross reference parts from multiple manufacturers (oem_code).  </p>

<p>Table: xref</p>

<pre><code>item_id   | oem_code
   A      |    123
   A      |    234
   B      |    234
   B      |    345
   C      |    456  
</code></pre>

<p>Table: parts  (only showing relevant partNum column)</p>

<pre><code>partNum  
  S.A  
  S.B  
  S.C  
  123  
  234  
  345  
  456  
</code></pre>

<p>Both xref columns contain part numbers in the parts table.  I need to enter a part number <code>($fielddata)</code> and then retrieve all data from parts where <code>parts.partNum = $fielddata</code>, as well as all cross referenced numbers from xref that match <code>parts.partNum</code>.  Unfortunately, the part numbers from the manufacturer have <code>S</code>. preceding them in our system but not in the table they are sending.  Our system won't recognize them without the <code>S</code>.</p>

<p>MySQL query is  </p>

<pre><code>SELECT * 
FROM parts
WHERE partNum
IN (    
    SELECT oem_code
    FROM xref
    WHERE item_id = ( 
        SELECT item_id
        FROM xref 
        WHERE oem_code = '$fielddata' 
    )
)
</code></pre>

<p><code>123</code> returns all data from parts where parts.partNum = 123, 234 (needs also S.A)<br>
<code>234</code> errors out, #1242 - Subquery returns more than 1 row (needs 234, S.A, S.B)<br>
<code>A</code> returns nothing (needs 123, 234, S.A)<br>
<code>S.A</code> also returns nothing (needs 123, 234, S.A)</p>

<p>I understand the limitations of my sql statement and subquery and why I'm not getting the full result set desired, but I don't know how to expand it to get what I want.  I was happy to get as far as I did with it.  When I try to expand it, I get undesired results or errors, so I'm pretty much at the end of my ability.</p>

<p>I'm also aware that running subqueries aren't efficient on large databases.  So I'm up for a total rewrite of the sql or a modification of what I've got so far.  xref has <code>&gt;27k</code> rows and parts has <code>&gt;550k</code> rows with 10 columns (if anyone cares).</p>

<p>Any help would be greatly appreciated.</p>

## Answers
### Answer ID: 25516277
<p>A query using <code>exists</code></p>

<pre><code>SELECT *
FROM parts
WHERE EXISTS (
    SELECT 1 FROM xref x1
    JOIN xref x2 ON x1.item_id = x2.item_id
    WHERE (x2.oem_code = '$fielddata' OR x2.item_id = RIGHT('$fielddata',1))
    AND (x1.oem_code = partNum OR CONCAT('S.',x1.item_id) = partNum)
)
</code></pre>

<p><strong>Update</strong></p>

<p>It may be faster to join against a derived table for a given <code>$fielddata</code>. This is essentially @JohnRuddell's query but modified to use a derived table.</p>

<pre><code>SELECT p.* FROM parts p
JOIN (
    SELECT x.oem_code partNum
        FROM xref x
        JOIN xref x1 
          ON x1.item_id = x.item_id 
         AND x1.oem_code = '$fielddata'
          OR x.item_id = RIGHT('$fielddata', 1)
    UNION
    SELECT CONCAT('S.', x.item_id) partNum
        FROM xref x
        WHERE x.oem_code = '$fieldata' 
           OR x.item_id = RIGHT('$fielddata', 1)
) t1 ON t1.partNum = p.partNum
</code></pre>

### Answer ID: 25516023
<p>I think this should do what you want</p>

<pre><code>SELECT * 
FROM parts
WHERE partNum IN 
(   SELECT x.oem_code
    FROM xref x
    JOIN xref x1 
      ON x1.item_id = x.item_id 
     AND x1.oem_code = '$fielddata'
      OR x.item_id = RIGHT('$fielddata', 1)
)
OR partNum IN 
(   SELECT CONCAT('S.', x.item_id)
    FROM xref x
    WHERE x.oem_code = '$fieldata' 
       OR x.item_id = RIGHT('$fielddata', 1)
)
</code></pre>

<p><a href="http://sqlfiddle.com/#!2/670723/23" rel="nofollow">DEMO</a></p>

<p>just use a join so you aren't doing a third subquery</p>

