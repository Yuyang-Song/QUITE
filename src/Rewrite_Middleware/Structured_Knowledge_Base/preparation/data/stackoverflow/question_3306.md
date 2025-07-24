# Expression.Lambda returns with &quot;The LINQ expression ... could not be translated. Why?
[Link to question](https://stackoverflow.com/questions/75628142/expression-lambda-returns-with-the-linq-expression-could-not-be-translated)
**Creation Date:** 1677852628
**Score:** 0
**Tags:** c#, linq
## Question Body
<p>I have been over at Jeremy to &quot;borrow&quot; som very nice code that more or less acts as dynamic-linq. <a href="https://blog.jeremylikness.com/blog/dynamically-build-linq-expressions/" rel="nofollow noreferrer">https://blog.jeremylikness.com/blog/dynamically-build-linq-expressions/</a></p>
<p>I have made som small changes. I would like to evalute predicates based on Regex. The product of an Expression.Lambda looks like this.</p>
<pre><code>        .Where(d =&gt; new  List&lt;string&gt; { &quot;P1101&quot;, &quot;P1102&quot;}
            .Contains(d.PntName) | Regex.IsMatch(
            input: d.PntName, 
            pattern: &quot;^A.*&quot;))
</code></pre>
<p>I get the following error</p>
<pre><code>The LINQ expression 'DbSet&lt;DataTransaction&gt;
    .Where(d =&gt; List&lt;string&gt; { &quot;P1101&quot;, &quot;P1102&quot;, }
        .Contains(d.PntName) | Regex.IsMatch(
        input: d.PntName, 
        pattern: &quot;^A.*&quot;))' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync(). See https://go.microsoft.com/fwlink/?linkid=2101038 for more information.

</code></pre>
<p>*** Update ***</p>
<p>The problematic part of the query is being produced at runtime. I am setting the following MethodInfo</p>
<pre><code>typeof(Regex).GetMethods(BindingFlags.Static | BindingFlags.Public)
     .Single(m =&gt; m.Name == nameof(Regex.IsMatch)
          &amp;&amp; m.GetParameters().Length == 2); 
</code></pre>
<p>Is there somewhere to declare that the method should omit the names?</p>
<p>**** Full Code ****</p>
<pre><code>Program.cs
            using (var context = new DataTransactionContext(optionsWithLog))
            {
                var count = await context.DbDataTransactions.CountAsync();
                Console.WriteLine($&quot;Verified insert count: {count}.&quot;);
                Console.WriteLine(&quot;Parsing expression...&quot;);
                var parser = new JsonExpressionParser();
                var predicate = parser.ParseExpressionOf&lt;DataTransaction&gt;(
                    JsonDocument.Parse(
                        await File.ReadAllTextAsync(&quot;dataDatabaseRules.json&quot;)));
                Console.WriteLine(&quot;Retrieving from database...&quot;);
                var query = context.DbDataTransactions.Where(predicate);
                    //.OrderBy(t =&gt; t.PntNo);
                var results = await query.ToListAsync();
                Console.WriteLine($&quot;Retrieved {results.Count}&quot;);
                Console.WriteLine(&quot;Sample:&quot;);
                Console.WriteLine(results[0]);
            }

</code></pre>
<p>ExpressionParser</p>
<pre><code>public class JsonExpressionParser
{
    private const string StringStr = &quot;string&quot;;

    private readonly string BooleanStr = nameof(Boolean).ToLower();
    private readonly string Number = nameof(Number).ToLower();
    private readonly string In = nameof(In).ToLower();
    private readonly string And = nameof(And).ToLower();
    private readonly string Contains = nameof(Contains).ToLower();

    //Method construction
    private readonly MethodInfo MethodContains = typeof(Enumerable).GetMethods(
                    BindingFlags.Static | BindingFlags.Public)
                    .Single(m =&gt; m.Name == nameof(Enumerable.Contains)
                        &amp;&amp; m.GetParameters().Length == 2);

    private readonly MethodInfo PerformMyMeth =
    //    typeof(Regex).GetMethod(&quot;IsMatch&quot;, new Type[] { typeof(string) });
    typeof(Regex).GetMethods(BindingFlags.Static | BindingFlags.Public)
                .Single(m =&gt; m.Name == nameof(Regex.IsMatch)
                    &amp;&amp; m.GetParameters().Length == 2); //Sætter antallet af parametre for Regex


    private delegate Expression Binder(Expression left, Expression right);

    private Expression ParseTree&lt;T&gt;(
        JsonElement condition,
        ParameterExpression parm)
    {
        Expression left = null;

        //AND OR
        var gate = condition.GetProperty(nameof(condition)).GetString();
        
        JsonElement rules = condition.GetProperty(nameof(rules));

        //Binder &gt; Short hand for Binary Expression
        Binder binder = gate == And ? (Binder)Expression.And : Expression.Or;

        Expression bind(Expression left, Expression right) =&gt;
            left == null ? right : binder(left, right);

        foreach (var rule in rules.EnumerateArray())
        {
            if (rule.TryGetProperty(nameof(condition), out JsonElement check))
            {
                var right = ParseTree&lt;T&gt;(rule, parm);
                left = bind(left, right);
                continue;
            }

            string @operator = rule.GetProperty(nameof(@operator)).GetString();     //eg. IN
            string type = rule.GetProperty(nameof(type)).GetString();               //eg. string
            string field = rule.GetProperty(nameof(field)).GetString();             //eg. PntName
            
            JsonElement value = rule.GetProperty(nameof(value));                    //værdien
            
            //The expression constant has to be compared to some property. The code in the next snippet creates a property expression.
            var property = Expression.Property(parm, field);
            
            if (@operator == In)
            {

                //Contains call that we build ealier
                var contains = MethodContains.MakeGenericMethod(typeof(string));

                object val = value.EnumerateArray().Select(e =&gt; e.GetString())
                    .ToList();

                var right = Expression.Call(
                    contains,
                    Expression.Constant(val),
                    property);
                left = bind(left, right);
            }
            else if(@operator == Contains)
            {


                object val = (type == StringStr || type == BooleanStr) ?
                    (object)value.GetString() : value.GetDecimal();

                var toCompare = Expression.Constant(val);
                var right = Expression.Call(PerformMyMeth, property, toCompare);

                left = bind(left, right);
            }
            else
            {
                object val = (type == StringStr || type == BooleanStr) ?
                    (object)value.GetString() : value.GetDecimal();
                var toCompare = Expression.Constant(val);
                var right = Expression.Equal(property, toCompare);

                left = bind(left, right);
            }
        }

        return left;
    }

    public Expression&lt;Func&lt;T, bool&gt;&gt; ParseExpressionOf&lt;T&gt;(JsonDocument doc)
    {
        //En oprettelse af en Expression sker ved hjælp af static factory method kald.
        // ParameterExpression, en reference til en Lambda expression
        var itemExpression = Expression.Parameter(typeof(T));

        Console.WriteLine(&quot;Item expression: &quot; + itemExpression.ToString());

        var conditions = ParseTree&lt;T&gt;(doc.RootElement, itemExpression);

        if (conditions.CanReduce)
        {
            conditions = conditions.ReduceAndCheck();
        }

        Console.WriteLine(&quot;Conditions: &quot; + conditions.ToString());

        var query = Expression.Lambda&lt;Func&lt;T, bool&gt;&gt;(conditions, itemExpression);
        return query;
    }

    public Func&lt;T, bool&gt; ParsePredicateOf&lt;T&gt;(JsonDocument doc)
    {
        var query = ParseExpressionOf&lt;T&gt;(doc);
        return query.Compile();
    }
</code></pre>
<pre><code></code></pre>

## Answers
### Answer ID: 75628184
<p>Just call the function as non-named arguments</p>
<pre class="lang-cs prettyprint-override"><code>.Where(d =&gt; new  List&lt;string&gt; { &quot;P1101&quot;, &quot;P1102&quot;}
            .Contains(d.PntName) | Regex.IsMatch(
                d.PntName, 
                &quot;^A.*&quot;))
</code></pre>

