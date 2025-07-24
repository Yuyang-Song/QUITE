# SQL statement is nested too deeply when adding more subqueries to projection
[Link to question](https://stackoverflow.com/questions/52421483/sql-statement-is-nested-too-deeply-when-adding-more-subqueries-to-projection)
**Creation Date:** 1537434635
**Score:** 1
**Tags:** sql-server, entity-framework, entity-framework-6
## Question Body
<p>Reproduction project available on github, using <code>AdventureWorks2016</code> database. <a href="https://github.com/pako1337/EntityFrameworkNestedQueries" rel="nofollow noreferrer">GitHub Reproduction</a></p>

<p>We have custom filtering mechanism to accomodate for our needs. What it does is - it takes input data, builds expression tree with full query and passes it to <code>EntityFramework</code> to execute. We have two parts of the query - getting basic entity and getting some extra data values, represented as sub queries inside final projection.</p>

<p>Problem:<br>
When getting more than ~20 subqueries, <code>SqlServer</code> throws an error:</p>

<blockquote>
  <p>Some part of your SQL statement is nested too deeply. Rewrite the query or break it up into smaller queries.</p>
</blockquote>

<p>Upon closer investigation it turns out queries similar to this:</p>

<pre><code>var products = db.Products.Where(p =&gt; productIds.Contains(p.ProductID))
                .Select(p =&gt; new
                {
                    Entity = p,
                    Extras = new
                    {
                        TotalTransactions = p.TransactionHistories.Count(),
                        TotalCostChanges = p.ProductCostHistories.Count(),
                        AverageTransactionCost = p.TransactionHistories.Average(t =&gt; t.Quantity * t.ActualCost),
                        MaxQuantity = (int?)p.TransactionHistories.Max(t =&gt; t.Quantity)
                    }
                });
</code></pre>

<p>Are resulting in SQL query generated like this:</p>

<pre><code>SELECT 
    [Project3].[ProductID] AS [ProductID], 
    [Project3].[Name] AS [Name], 
    [Project3].[C1] AS [C1], 
    [Project3].[C2] AS [C2], 
    [Project3].[C3] AS [C3], 
    (SELECT 
        MAX([Extent5].[Quantity]) AS [A1]
        FROM [Production].[TransactionHistory] AS [Extent5]
        WHERE [Project3].[ProductID] = [Extent5].[ProductID]) AS [C4]
    FROM ( SELECT 
        [Project2].[ProductID] AS [ProductID], 
        [Project2].[Name] AS [Name], 
        [Project2].[C1] AS [C1], 
        [Project2].[C2] AS [C2], 
        (SELECT 
            AVG([Filter4].[A1]) AS [A1]
            FROM ( SELECT 
                 CAST( [Extent4].[Quantity] AS decimal(19,0)) * [Extent4].[ActualCost] AS [A1]
                FROM [Production].[TransactionHistory] AS [Extent4]
                WHERE [Project2].[ProductID] = [Extent4].[ProductID]
            )  AS [Filter4]) AS [C3]
        FROM ( SELECT 
            [Project1].[ProductID] AS [ProductID], 
            [Project1].[Name] AS [Name], 
            [Project1].[C1] AS [C1], 
            (SELECT 
                COUNT(1) AS [A1]
                FROM [Production].[ProductCostHistory] AS [Extent3]
                WHERE [Project1].[ProductID] = [Extent3].[ProductID]) AS [C2]
            FROM ( SELECT 
                [Extent1].[ProductID] AS [ProductID], 
                [Extent1].[Name] AS [Name], 
                (SELECT 
                    COUNT(1) AS [A1]
                    FROM [Production].[TransactionHistory] AS [Extent2]
                    WHERE [Extent1].[ProductID] = [Extent2].[ProductID]) AS [C1]
                FROM [Production].[Product] AS [Extent1]
                WHERE [Extent1].[ProductID] IN (707, 708, 709, 711)
            )  AS [Project1]
        )  AS [Project2]
    )  AS [Project3]
</code></pre>

<p>With each property added to Extras, one more nested query is created.</p>

<p>Is there any way in which <code>EntityFramework</code> will generate better query (see: all those nested queries for values C1, C2... can be represented as simple sub-queries in main select) or should this kind of query be created in some completely different way?</p>

