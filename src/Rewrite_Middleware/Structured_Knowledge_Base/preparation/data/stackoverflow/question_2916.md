# Looking for an alternative for WITH SQL statement, having interdependent temporary tables
[Link to question](https://stackoverflow.com/questions/58408471/looking-for-an-alternative-for-with-sql-statement-having-interdependent-tempora)
**Creation Date:** 1571212865
**Score:** 0
**Tags:** sql, sql-server
## Question Body
<p>I am working on a huge DB with many tables. I have a kind of working version with the ";WITH" statement but it have side effects on the whole database (it sometimes stops or slows down the ETL job)so I am looking for an alternative. </p>

<p>I tried to rewrite the query but then I get the</p>

<blockquote>
  <p>multi-part identifier x could not be bound</p>
</blockquote>

<p>because the tables build upon each other.</p>

<p>The kind of working version is:</p>

<pre class="lang-sql prettyprint-override"><code>USE[database]
;WITH[table1] AS 
(
  SELECT [RegionList].[Cluster]
         ,[RegionList].[Region]
         ,[Customer]
         ,[Key1]
         ,[Key2]
         ,MAX(..[TimeK].) AS [Time]
  FROM [table3]
  JOIN [RegionList] ON [RegionList].[Region] = [DRegion].[Region]
  JOIN [DTime] ON [table3].[TimeK] = [DTime].[TimeK]
  JOIN [PKey]  ON [table3].[Key2] = [PKey].[Key2]

  GROUP BY [RegionList].[Cluster]
         ,[RegionList].[Region]
         ,[Customer]
         ,[Key1]
         ,[Key2]

)
,[table2] AS
(
 SELECT [table3].[Name]
        ,[DProduct].[Product]
        ,[PKey].[Key2]
        ,CASE
             WHEN [table1].[time] IS NULL THEN [DProduct].[Product]
             WHEN ...
             ELSE NULL
        END AS [NotActive]
 FROM [table1]
 JOIN [DProduct] ON [table1].[Key1] = [DProduct].[Key1]
 JOIN [PKey]  ON [table3].[Key2] = [PKey].[Key2]
 JOIN [Name] ON [table3].[Name] = [DName].[Name]

)
SELECT [table2].[NotActive]
       ,[table2].[Name]
       ,[tabel1].[Time]
       ,[table1].[Region]   
FROM [table2]
JOIN [table1] ON [table1].[Key2] = [table2].[Key2]
WHERE [NotActive] IS NOT NULL

</code></pre>

<p>(needed to alter the names from the data, so if there is an error it is because of the transcript)</p>

<p>I wanted to rewrite it so I have:</p>

<pre class="lang-sql prettyprint-override"><code>USE[database]

SELECT [table2].[NotActive]
       ,[table2].[Name]
       ,[tabel1].[Time]
       ,[table1].[Region]   
FROM (
      SELECT [RegionList].[Cluster]
         ,[RegionList].[Region]
         ,[Customer]
         ,[Key1]
         ,[Key2]
         ,MAX(..[TimeK].) AS [Time]
      FROM [table3]
      JOIN [RegionList] ON [RegionList].[Region] = [DRegion].[Region]
      JOIN [DTime] ON [table3].[TimeK] = [DTime].[TimeK]
      JOIN [PKey]  ON [table3].[Key2] = [PKey].[Key2]

      GROUP BY [RegionList].[Cluster]
         ,[RegionList].[Region]
         ,[Customer]
         ,[Key1]
         ,[Key2]
      ) AS [table1],
    (
      SELECT [table3].[Name]
        ,[DProduct].[Product]
        ,[PKey].[Key2]
        ,CASE
             WHEN [table1].[time] IS NULL THEN [DProduct].[Product]
             WHEN ...
             ELSE NULL
        END AS [NotActive]
      FROM [table1]
      JOIN [DProduct] ON [table1].[Key1] = [DProduct].[Key1]
      JOIN [PKey]  ON [table3].[Key2] = [PKey].[Key2]
      JOIN [Name] ON [table3].[Name] = [DName].[Name]
    ) AS [table2]

WHERE [NotActive] IS NOT NULL


</code></pre>

<p>But now in the second part of the statement there is the "multi-part identifier [table1] could not be bound" error. I know that at this part it doesn't "see" [table1] but what do I do? Is there an easy fix? Or am I on the wrong way?</p>

