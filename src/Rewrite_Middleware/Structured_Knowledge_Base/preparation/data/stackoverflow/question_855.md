# Building dynamic query in a loop using Expression trees
[Link to question](https://stackoverflow.com/questions/46105811/building-dynamic-query-in-a-loop-using-expression-trees)
**Creation Date:** 1504822173
**Score:** 1
**Tags:** c#, entity-framework, linq, expression-trees
## Question Body
<p>I have a system that allows different criteria pertaining to Sales to be stored in the database. When the criteria are loaded, they are used to build a query and return all applicable Sales. The criteria objects look like this:</p>

<p>ReferenceColumn (The column in the Sale table they apply to)</p>

<p>MinValue (Minimum value the reference column must be)</p>

<p>MaxValue (Maximum value the reference column must be)</p>

<p>A search for Sales is done using a collection of the aforementioned criteria. ReferenceColumns of the same type are OR'd together, and ReferenceColumns of different types are AND'd together. So for example if I had three criteria:</p>

<p>ReferenceColumn: 'Price', MinValue: '10', MaxValue: '20'</p>

<p>ReferenceColumn: 'Price', MinValue: '80', MaxValue: '100'</p>

<p>ReferenceColumn: 'Age', MinValue: '2', MaxValue: '3'</p>

<p>The query should return all Sales where the price was between 10-20 or between 80-100, but only if those Sales's Age is between 2 and 3 years old.</p>

<p>I have it implemented using a SQL query string and executing using .FromSql:</p>

<pre><code>public IEnumerable&lt;Sale&gt; GetByCriteria(ICollection&lt;SaleCriteria&gt; criteria)
{
StringBuilder sb = new StringBuilder("SELECT * FROM Sale");

var referenceFields = criteria.GroupBy(c =&gt; c.ReferenceColumn);

// Adding this at the start so we can always append " AND..." to each outer iteration
if (referenceFields.Count() &gt; 0)
{
    sb.Append(" WHERE 1 = 1");
}

// AND all iterations here together
foreach (IGrouping&lt;string, SaleCriteria&gt; criteriaGrouping in referenceFields)
{
    // So we can always use " OR..."
    sb.Append(" AND (1 = 0");

    // OR all iterations here together
    foreach (SaleCriteria sc in criteriaGrouping)
    {
        sb.Append($" OR {sc.ReferenceColumn} BETWEEN '{sc.MinValue}' AND '{sc.MaxValue}'");
    }

    sb.Append(")");
}

return _context.Sale.FromSql(sb.ToString();
}
</code></pre>

<p>And this is fact works just fine with our database, but it doesn't play nice with other collections, particulary the InMemory database we use for UnitTesting, so I'm trying to rewrite it using Expression trees, which I've never used before. So far I've gotten this:</p>

<pre><code>public IEnumerable&lt;Sale&gt; GetByCriteria(ICollection&lt;SaleCriteria&gt; criteria)
{
var referenceFields = criteria.GroupBy(c =&gt; c.ReferenceColumn);

Expression masterExpression = Expression.Equal(Expression.Constant(1), Expression.Constant(1));
List&lt;ParameterExpression&gt; parameters = new List&lt;ParameterExpression&gt;();

// AND these...
foreach (IGrouping&lt;string, SaleCriteria&gt; criteriaGrouping in referenceFields)
{
    Expression innerExpression = Expression.Equal(Expression.Constant(1), Expression.Constant(0));
    ParameterExpression referenceColumn = Expression.Parameter(typeof(Decimal), criteriaGrouping.Key);
    parameters.Add(referenceColumn);

    // OR these...
    foreach (SaleCriteria sc in criteriaGrouping)
    {
        Expression low = Expression.Constant(Decimal.Parse(sc.MinValue));
        Expression high = Expression.Constant(Decimal.Parse(sc.MaxValue));
        Expression rangeExpression = Expression.GreaterThanOrEqual(referenceColumn, low);
        rangeExpression = Expression.AndAlso(rangeExpression, Expression.LessThanOrEqual(referenceColumn, high));
        innerExpression = Expression.OrElse(masterExpression, rangeExpression);
    }

    masterExpression = Expression.AndAlso(masterExpression, innerExpression);
}

var lamda = Expression.Lambda&lt;Func&lt;Sale, bool&gt;&gt;(masterExpression, parameters);

return _context.Sale.Where(lamda.Compile());
}
</code></pre>

<p>It's currently throwing an ArgumentException when I call Expression.Lamda. Decimal cannot be used there and it says it wants type Sale, but I don't know what to put there for Sales, and I'm not sure I'm even on the right track here. I'm also concerned that my masterExpression is duplicating with itself each time instead of appending like I did with the string builder, but maybe that will work anyway.</p>

<p>I'm looking for help on how to convert this dynamic query to an Expression tree, and I'm open to an entirely different approach if I'm off base here.</p>

## Answers
### Answer ID: 46106541
<p>I think this will work for you </p>

<pre><code> public class Sale
            {
                public int A { get; set; }

                public int B { get; set; }

                public int C { get; set; }
            }

            //I used a similar condition structure but my guess is you simplified the code to show in example anyway
            public class Condition
            {
                public string ColumnName { get; set; }

                public ConditionType Type { get; set; }

                public object[] Values { get; set; }

                public enum ConditionType
                {
                    Range
                }

                //This method creates the expression for the query
                public static Expression&lt;Func&lt;T, bool&gt;&gt; CreateExpression&lt;T&gt;(IEnumerable&lt;Condition&gt; query)
                {
                    var groups = query.GroupBy(c =&gt; c.ColumnName);

                    Expression exp = null;
                    //This is the parametar that will be used in you lambda function
                    var param = Expression.Parameter(typeof(T));

                    foreach (var group in groups)
                    {
                        // I start from a null expression so you don't use the silly 1 = 1 if this is a requirement for some reason you can make the 1 = 1 expression instead of null
                        Expression groupExp = null;

                        foreach (var condition in group)
                        {
                            Expression con;
                            //Just a simple type selector and remember switch is evil so you can do it another way
                            switch (condition.Type)
                            {
//this creates the between NOTE if data types are not the same this can throw exceptions
                                case ConditionType.Range:
                                    con = Expression.AndAlso(
                                        Expression.GreaterThanOrEqual(Expression.Property(param, condition.ColumnName), Expression.Constant(condition.Values[0])),
                                        Expression.LessThanOrEqual(Expression.Property(param, condition.ColumnName), Expression.Constant(condition.Values[1])));
                                    break;
                                default:
                                    con = Expression.Constant(true);
                                    break;
                            }
                            // Builds an or if you need one so you dont use the 1 = 1
                            groupExp = groupExp == null ? con : Expression.OrElse(groupExp, con);
                        }

                        exp = exp == null ? groupExp : Expression.AndAlso(groupExp, exp);
                    }

                    return Expression.Lambda&lt;Func&lt;T, bool&gt;&gt;(exp,param);
                }
            }

            static void Main(string[] args)
            {
                //Simple test data as an IQueriable same as EF or any ORM that supports linq.
                var sales = new[] 
                {
                    new Sale{ A = 1,  B = 2 , C = 1 },
                    new Sale{ A = 4,  B = 2 , C = 1 },
                    new Sale{ A = 8,  B = 4 , C = 1 },
                    new Sale{ A = 16, B = 4 , C = 1 },
                    new Sale{ A = 32, B = 2 , C = 1 },
                    new Sale{ A = 64, B = 2 , C = 1 },
                }.AsQueryable();

                var conditions = new[]
                {
                    new Condition { ColumnName = "A", Type = Condition.ConditionType.Range, Values= new object[]{ 0, 2 } },
                    new Condition { ColumnName = "A", Type = Condition.ConditionType.Range, Values= new object[]{ 5, 60 } },
                    new Condition { ColumnName = "B", Type = Condition.ConditionType.Range, Values= new object[]{ 1, 3 } },
                    new Condition { ColumnName = "C", Type = Condition.ConditionType.Range, Values= new object[]{ 0, 3 } },
                };

                var exp = Condition.CreateExpression&lt;Sale&gt;(conditions);
                //Under no circumstances compile the expression if you do you start using the IEnumerable and they are not converted to SQL but done in memory
                var items = sales.Where(exp).ToArray();

                foreach (var sale in items)
                {
                    Console.WriteLine($"new Sale{{ A = {sale.A},  B =  {sale.B} , C =  {sale.C} }}");
                }

                Console.ReadLine();
            }
</code></pre>

