# Azure SQL Server database query suddenly exhausting DTUs
[Link to question](https://stackoverflow.com/questions/79220447/azure-sql-server-database-query-suddenly-exhausting-dtus)
**Creation Date:** 1732462673
**Score:** 1
**Tags:** sql-server, azure, resources
## Question Body
<p>I have a Microsoft SQL Server database on Azure. Recently a query that has worked in the past started to max out DTUs and never returns. While attempting to diagnose the problem, I rewrote the query as a sequence of <code>SELECT ... INTO #temp_table</code> statements and these run in a fraction of a second.</p>
<p>My question is, why did the original query start failing? Should I rewrite all the other join queries to avoid this issue reoccurring?</p>
<p>Here's the query (table names have been changed).</p>
<pre><code>SELECT      T_Primary.Id
FROM        T_Primary
INNER JOIN  T_Secondary ON T_Secondary.Id = T_Primary.T_Secondary_Id
WHERE       (T_Secondary.Path = @path OR T_Secondary.Path Like concat(@path, '\%'))
AND         T_Primary.Probability &lt; 1
AND         T_Primary.Ignore = 0
</code></pre>
<p>Neither table is very big. <code>T_Primary</code> has 251464 rows and <code>T_Secondary</code> has 180032 rows.</p>
<p>There is a foreign key on <code>T_Primary.T_Secondary_Id</code> referencing <code>T_Secondary.Id</code> and an index supporting the foreign key.</p>
<p>The column definitions are as follows.</p>
<pre><code>T_Primary.T_Secondary_Id  int            not null
T_Primary.Probability     float          not null
T_Primary.Ignore          bit            not null
T_Secondary.Id            int            not null  identity
T_Secondary.Path          nvarchar(255)  not null
</code></pre>
<p>Here's the stored procedure.</p>
<pre><code>CREATE PROCEDURE dbo.sp_0001 (@path nvarchar(255) = NULL)
AS
BEGIN
    SET NOCOUNT ON

    SELECT      T_Secondary.id, 
                T_Secondary.path, 
                T_Secondary.name
    INTO        #temp1
    FROM        T_Secondary 
    WHERE       (T_Secondary.Path = @path OR T_Secondary.Path Like concat(@path, '\%'))
    ;

    SELECT      T_Primary.Id,
                T_Primary.[Probability],
                T_Primary.[Ignore]
    INTO        #temp2
    FROM        T_Primary 
    Inner JOIN  #temp1
    on          #temp1.Id = T_Primary.T_Secondary_Id
    ;

    SELECT      Id,
                Probability,
                Ignore
    FROM        #temp2
    WHERE       Probability &lt; 1
    AND         Ignore = 0
    ;

END
GO
</code></pre>
<p>This stored procedure runs in a fraction of a second.</p>
<p>Here's a link to the query plan of the original query.</p>
<p><a href="https://www.brentozar.com/pastetheplan/?id=S1gC3bfmke" rel="nofollow noreferrer">https://www.brentozar.com/pastetheplan/?id=S1gC3bfmke</a></p>
<p>and here's a link to the query rewritten as a stored procedure</p>
<p><a href="https://www.brentozar.com/pastetheplan/?id=ryLnTZGQJl" rel="nofollow noreferrer">https://www.brentozar.com/pastetheplan/?id=ryLnTZGQJl</a></p>

