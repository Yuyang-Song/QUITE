# How to fill a Tuple whit the out of a query select
[Link to question](https://stackoverflow.com/questions/63830839/how-to-fill-a-tuple-whit-the-out-of-a-query-select)
**Creation Date:** 1599744839
**Score:** -1
**Tags:** c#, sql, linq, tuples
## Question Body
<pre><code>    public List&lt;Tuple&lt;int, int&gt;&gt; GetTupleDetailedLog()
    {
        var query = (from c in _context.Lk_business_rules
                     join v in _context.Business_rules_detailed_log on c.User_story_number equals v.User_story_number
                     where c.Status_id_fk == 3
                     group new { c, v } by new { c.Rule_description, c.User_story_number } into cv
                     select new
                     {
                         us = cv.Select(cv =&gt; cv.v.User_story_number), //this should be the first int on tuple
                         count = cv.Select(cv =&gt; cv.v.Row_id.Count()), //this should be the second int on tuple
                     });
        var TupleList = new List&lt;Tuple&lt;int, int&gt;&gt;();
        foreach (var item in query)
        {
            TupleList.Add(new Tuple&lt;int, int&gt;(Convert.ToInt32(item.us), Convert.ToInt32(item.count)));
        }
        return TupleList;
    }
</code></pre>
<p>I have a NEW problem here, I have a list of tuples and I want to fill it with the output of the select of a query. This code is helping me out, but now i have a runtime error:</p>
<p>InvalidOperationException: The LINQ expression '(GroupByShaperExpression: KeySelector: new { Rule_description = (l.Rule_description), User_story_number = (l.User_story_number) }, ElementSelector:new { c = (EntityShaperExpression: EntityType: Lk_business_rules ValueBufferExpression: (ProjectionBindingExpression: c) IsNullable: False ), v = (EntityShaperExpression: EntityType: Business_rules_detailed_log ValueBufferExpression: (ProjectionBindingExpression: v) IsNullable: False ) } ) .Select(cv =&gt; cv.v.User_story_number)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync(). See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.</p>
<p>And:</p>
<p>An unhandled exception occurred while processing the request.
InvalidOperationException: The LINQ expression '(GroupByShaperExpression:</p>
<p>Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync(). See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.
Microsoft.EntityFrameworkCore.Query.RelationalSqlTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)</p>
<p>Data involved:</p>
<p>The issue lies in obtaining a tuple with two values ​​to add to an entity that is not mapped with the database.</p>
<p>So, we have on the one hand business rules, which contain their state (we have to filter by state 3) and contain a Rows_id, we have to cross it with the same field in Detailed_log and after grouping by that same field, count how many rows each Row_id has, in detailed_log (What would give us the error that we have to put in the second field of the tuple)</p>
<p>That's why I need the join and group by, and the filter by state in the where.</p>

## Answers
### Answer ID: 63837276
<p>I'm using .net Core.  Here's a few ways you can manipulate tuples.  As @kalu93 said, you should be able to create the tuples easily in a select.  In fact in your query you could use the tuple instead of the anonymous type.  Here's some examples of tuples, value tuples, and creating and decomposing both:</p>
<pre><code>    static void Main(string[] _)
    {
        (int, int)[] intPairs = new (int, int)[] {
            (1,1),(2,2),(3,3),(4,4),(5,5)
            };

        List&lt;(int, int)&gt; valueTuples = intPairs.ToList();
        List&lt;(int, int)&gt; valueTuples2 = intPairs.Select(x =&gt; (x.Item1, x.Item2)).ToList();
        List&lt;Tuple&lt;int, int&gt;&gt; tuples = intPairs.Select(x =&gt; new Tuple&lt;int, int&gt;(x.Item2, x.Item2)).ToList();

        List&lt;Tuple&lt;int, int&gt;&gt; tuples2 = new List&lt;Tuple&lt;int, int&gt;&gt;();
        foreach (var(first,second) in intPairs)
        {
            tuples2.Add(new Tuple&lt;int, int&gt;(first, second));
        }

        List&lt;Tuple&lt;int, int&gt;&gt; tuples3 = new List&lt;Tuple&lt;int, int&gt;&gt;();
        foreach (var (first, second) in tuples)
        {
            tuples3.Add(new Tuple&lt;int, int&gt;(first, second));
        }

        List&lt;(int, int)&gt; valueTuples3 = new List&lt;(int, int)&gt;();

        foreach (var (first, second) in tuples)
        {
            valueTuples3.Add((first, second));
        }

        Console.WriteLine(Enumerable.SequenceEqual(valueTuples, valueTuples2));
        Console.WriteLine(Enumerable.SequenceEqual(valueTuples, valueTuples3));
        Console.WriteLine(Enumerable.SequenceEqual(tuples, tuples2));
        Console.WriteLine(Enumerable.SequenceEqual(tuples, tuples3));
    }
</code></pre>

### Answer ID: 63836937
<p>Can you not just Select the result of your query into <code>Tuple&lt;int, int&gt;</code> instances?</p>
<pre><code>return query.Select(x =&gt; new Tuple&lt;int, int&gt;(x.number, x.count)).ToList();
</code></pre>

