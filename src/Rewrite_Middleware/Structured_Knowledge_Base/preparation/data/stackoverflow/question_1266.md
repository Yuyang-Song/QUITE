# How to improve poor performance of EF Core SQL query that sorts on a child collection
[Link to question](https://stackoverflow.com/questions/67322954/how-to-improve-poor-performance-of-ef-core-sql-query-that-sorts-on-a-child-colle)
**Creation Date:** 1619719995
**Score:** 2
**Tags:** sql-server, entity-framework-core, query-optimization, ef-core-3.1
## Question Body
<p>My issue is with the queries that EF Core generates for fetching ordered items from a child collection of a parent.</p>
<p>I have a parent class which has a collection of child objects. I'm using Entity Framework Core 5.0.5 (code first) against a SQL Server database. I've tried to boil down the scenario, so let's call it an Owner with a collection of Pets.
I often want a list of owners with their oldest pet, so I'll do something like</p>
<pre><code>Context.Owners
.Select(owner =&gt;
    new {
       Owner = owner,
       OldPet = owner.Pets.OrderBy(pet =&gt; pet.Age).LastOrDefault()   
    })
.Where(owner.Id == 1);
</code></pre>
<p>This worked fine before (on ef6) and works functionally now. However, the issue I have is that now EF Core translates these sub collection queries into something apparently cleverer, something like</p>
<pre><code> SELECT *
  FROM [Owners] AS [c]
  LEFT JOIN (
      SELECT *
      FROM (
          SELECT [c0].[Id] ... , ROW_NUMBER() OVER(PARTITION BY [c0].[OwnerId] ORDER BY [c0].[Age] DESC) AS [row]
          FROM [Pets] AS [c0]
      ) AS [t]
      WHERE [t].[row] &lt;= 1
  ) AS [t0] ON [c].[Id] = [t0].[OwnerId]
</code></pre>
<p>The problem I'm having is that it seems to perform terribly. Looking at the execution plan it's doing a clustered index seek on the pets table, then sorting them. The 'number of rows read' is massive and the 'sorting' takes tens or hundreds of milliseconds.</p>
<p>The way EF6 does the same functionality seemed way more performant in this sort of scenario.</p>
<p>Is there a way to change the behaviour so I can choose? Or a way to rewrite this type of query such that I don't have this problem? I've tried many variations of using GroupBy etc and still have the same result.</p>

## Answers
### Answer ID: 67323643
<p>If you are doing <code>FirstOrDefault</code> in projection, EF Core has to create such join, which uses Window Function <code>ROW_NUMBER</code>. To get desired SQL it is better to rewrite your query to be more predictable for LINQ translator:</p>
<pre class="lang-cs prettyprint-override"><code>var query =
    from owner in Context.Owners
    from pet in owner.Pets
    where owner.Id == 1
    orderby pet.Age descending
    select new 
    {
        Owner = owner,
        OldPet = pet
    }

var result = query.FirstOrDefault();
</code></pre>

