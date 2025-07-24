# How to convert SUBSELECT with TOP and ORDER BY to JOIN
[Link to question](https://stackoverflow.com/questions/28882443/how-to-convert-subselect-with-top-and-order-by-to-join)
**Creation Date:** 1425571850
**Score:** 1
**Tags:** sql, sql-server, performance
## Question Body
<p>I have a working sql select, which looks like this</p>

<p>[Edited: Im sorry i did one mistake in the question, i edited alias of Table1 but im trying the answers]</p>

<pre><code>SELECT 
m.Column1
,t2.Column2
,COALESCE
    (
        (
            SELECT TOP 1 Vat
            FROM LinkedDBServer.DatabaseName.dbo.TableName t3 
            WHERE 
                m.MaterialNumber = t3.MaterialNumber COLLATE Czech_CI_AS
                and t3.Currency = …
                and ...
            ORDER BY [Date] DESC
        ), m.Vat
    ) as Vat
FROM Table1 m
JOIN Table2 t2 on (m.Column1 = t2.Column1)
</code></pre>

<p>It works but the problem is that it takes too long and LinkedServer cut my connection because it takes more than 10 minutes. The purpose of the query is to get newer data from a different database if it exists (i get newest data by top and ordering it by date and precondition is that every data in that database is newer than in mine, thats why im using COALESCE).</p>

<p>But my though is if I was able to rewrite it to JOIN it could be faster. But another problem could be I dont have an primary key (and cant change that).</p>

<p>How can I speed that query up ? (Im using SQL Server 2008 R2) 
Thank you</p>

<p>Here i attached Estimated Query Plan: (Its readable in browser ZOOM :) Estimation is for 2 Coalesce columns.
<img src="https://i.sstatic.net/RKAIS.png" alt="enter image description here"></p>

## Answers
### Answer ID: 28882770
<p>Another option:</p>

<pre><code>; WITH vat AS (
  SELECT MaterialNumber COLLATE Czech_CI_AS As MaterialNumber
       , Vat
       , Row_Number() OVER (PARTITION BY MaterialNumber ORDER BY "Date" DESC) As sequence
  FROM   LinkedDBServer.DatabaseName.dbo.TableName
  WHERE  Currency = ...
  AND    ...
)
SELECT t1.Column1
     , m.Column2
     , Coalesce(vat.Vat, m.Vat) As Vat
FROM   Table1 As t1
 INNER
  JOIN Table2 As m
    ON m.Column1 = t1.Column1
 LEFT
  JOIN vat
    ON vat.MaterialNumber = m.MaterialNumber
   AND vat.sequence = 1
;
</code></pre>

### Answer ID: 28882656
<p>Try rewriting query using <code>outer apply</code></p>

<pre><code>SELECT 
t1.Column1
,t2.Column2
,COALESCE(ou.vat, m.Vat) as Vat
FROM Table1 t1
JOIN Table2 m on (m.Column1 = t1.Column1)
outer apply
        (
            SELECT TOP 1 Vat
            FROM LinkedDBServer.DatabaseName.dbo.TableName t3 
            WHERE 
                m.MaterialNumber = t3.MaterialNumber COLLATE Czech_CI_AS
                and t3.Currency = …
                and ...
            ORDER BY [Date] DESC
        ) ou
</code></pre>

