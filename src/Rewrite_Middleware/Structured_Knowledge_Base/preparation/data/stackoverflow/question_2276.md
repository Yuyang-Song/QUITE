# How to work around EF generating SQL statement nested too deeply
[Link to question](https://stackoverflow.com/questions/27129899/how-to-work-around-ef-generating-sql-statement-nested-too-deeply)
**Creation Date:** 1416927385
**Score:** 2
**Tags:** c#, sql-server, linq, entity-framework
## Question Body
<p>I am using a self-referencing model in Entity Framework 6, from which I need to select instances, based on a selection by the user. 
For larger selections, I get an exception: "Some part of your SQL statement is nested too deeply. Rewrite the query or break it up into smaller queries."</p>

<p>This is a simplified version of my model:</p>

<pre class="lang-cs prettyprint-override"><code>public class Hierarchy
{
    public int Id { get; set; }
    public string Name { get; set; }
    public int? ParentId { get; set; }
    public virtual Hierarchy Parent { get; set; }
    public virtual ICollection&lt;Hierarchy&gt; Children { get; set; }
}
</code></pre>

<p>The selection by the user contains a number of id's.</p>

<p>My database is seeded with</p>

<pre class="lang-none prettyprint-override"><code>Id  Name        ParentId
1   Root        NULL
2   parent-1    1
3   item-1-1    2
4   item-1-2    2
5   parent-2    1
6   item-2-1    2
7   item-2-2    2
8   child-1-1-1 3
9   child-1-1-2 3
10  child-1-2-1 4
11  child-1-2-2 4
12  child-2-1-1 3
13  child-2-1-2 3
14  child-2-2-1 4
15  child-2-2-2 4
</code></pre>

<p>I need to retrieve the selected instances themselves, as well as, the parents and the children of selected instances. The problem is in selecting the parents. This is a Linq query, which does that:</p>

<pre class="lang-cs prettyprint-override"><code>public static List&lt;Hierarchy&gt; Select(List&lt;int&gt; selection)
{
        var result = context.Hierarchy
            .Where(sub =&gt; sub.Children.Select(csub =&gt; csub.Id).Intersect(selection).Any());
}
</code></pre>

<p>Unfortunately, it gets converted to an ugly SQL statement. When calling </p>

<pre class="lang-cs prettyprint-override"><code>var test = Hierarchy.Select(new List&lt;int&gt;() { 2, 6, 11 });
</code></pre>

<p>this gets converted to:</p>

<pre class="lang-sql prettyprint-override"><code>SELECT 
    [Extent1].[Id] AS [Id], 
    [Extent1].[Name] AS [Name], 
    [Extent1].[ParentId] AS [ParentId]
    FROM [dbo].[Hierarchy] AS [Extent1]
    WHERE  EXISTS (SELECT 
        1 AS [C1]
        FROM  (SELECT 
            [Extent2].[Id] AS [Id]
            FROM [dbo].[Hierarchy] AS [Extent2]
            WHERE [Extent1].[Id] = [Extent2].[ParentId]
        INTERSECT
            SELECT 
            [UnionAll2].[C1] AS [C1]
            FROM  (SELECT 
                [UnionAll1].[C1] AS [C1]
                FROM  (SELECT 
                    2 AS [C1]
                    FROM  ( SELECT 1 AS X ) AS [SingleRowTable1]
                UNION ALL
                    SELECT 
                    6 AS [C1]
                    FROM  ( SELECT 1 AS X ) AS [SingleRowTable2]) AS [UnionAll1]
            UNION ALL
                SELECT 
                11 AS [C1]
                FROM  ( SELECT 1 AS X ) AS [SingleRowTable3]) AS [UnionAll2]) AS [Intersect1]
    )
</code></pre>

<p>A level of <code>UnionAll&lt;n&gt;</code> subqueries is added for each id in the selection. In practice, the user may select many id's. When there are more than some 40 id's, I bump into a leaky abstraction and get the exception. In any case, it looks like a sub-optimal query.</p>

<p>Essentially, my query needs to find all instances that have any of the selected items as a child. This involves determining, for each instance, the intersection of two lists: a local list of selected id's and the list of children of each instance in the database.</p>

<p>Can anybody think of a way to do this with Linq to entities, without emitting a query for each select item?</p>

## Answers
### Answer ID: 27130244
<p>may be</p>

<pre><code>public static List&lt;Hierarchy&gt; Select(List&lt;int&gt; selection)
{
    var result = context.Hierarchy
        .Where(sub =&gt; sub.Children.Any(csub =&gt; selection.Contains(csub.Id)));
}
</code></pre>

