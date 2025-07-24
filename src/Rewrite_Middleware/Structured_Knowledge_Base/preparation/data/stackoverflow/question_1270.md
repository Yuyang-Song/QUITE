# .Net Core 5 Rest Api Entity Framework Linq Expression Translation Error While Getting Record List From Controller
[Link to question](https://stackoverflow.com/questions/67504336/net-core-5-rest-api-entity-framework-linq-expression-translation-error-while-ge)
**Creation Date:** 1620824939
**Score:** 0
**Tags:** c#, entity-framework, linq, expression, asp.net-core-5.0
## Question Body
<p>I am working on a project and I got an error while getting queried list. I will tell on code block below.</p>
<pre><code>//AT REPOSITORY SIDE THIS FUNCTION GETS FILTERED LIST OF RECORDS
        public List&lt;TEntity&gt; GetList(Expression&lt;Func&lt;TEntity, bool&gt;&gt; filter)
        {
            using (var context=new MyContext()){
                return context.Set&lt;TEntity&gt;().Where(filter).ToList();
            }
        }
//AT ENTITY SIDE THIS FUNCTION CHECKS IF ALL PROPERTIES ARE EQUAL WITH THE GIVEN OBJECT
        public bool PublicPropertiesEqual(object which) 
        {
            var type = this.GetType();
            var whichType = which.GetType();
            var whichProperties = whichType.GetProperties(BindingFlags.Public | BindingFlags.Instance);
            foreach (PropertyInfo pi in type.GetProperties(BindingFlags.Public | BindingFlags.Instance))
            {
                if(whichProperties.Any(x =&gt; x.Name == pi.Name)){
                    object selfValue = type.GetProperty(pi.Name).GetValue(this, null);
                    object whichValue = type.GetProperty(pi.Name).GetValue(which,null);
                    if (selfValue != whichValue &amp;&amp; (selfValue == null || !selfValue.Equals(whichValue)))
                    {
                        return false;
                    }
                }
            }
            return true;
        }
//AT CONTROLLER SIDE ONLY CALLED REPO GETLIST FUNCTION WITH GIVEN FILTER
        [HttpGet]
        public IActionResult GetList([FromQuery] TEntity  query)
        {
            List&lt;TEntity&gt; res = _repo.GetList(x = x.PublicPropertiesEqual(query));
            return Ok(res);
        }
</code></pre>
<h3>PROBLEM</h3>
<p>When I execute the code I get an error like that</p>
<blockquote>
<p>InvalidOperationException: The LINQ expression 'DbSet()
.Where(c =&gt; c.PublicPropertiesEqual(__query_0))' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.</p>
</blockquote>
<p>So I cant get records from database. I tried to write custom expression tree showed below at the controller side and it also doesn't work.</p>
<pre><code>        [HttpGet]
        public IActionResult GetList([FromQuery] TEntity  query)
        {
            var param = Expression.Parameter(typeof(TEntity));
            var lambda = Expression.Lambda&lt;Func&lt;TEntity,bool&gt;&gt;(
                Expression.Call(
                    param, 
                    _entityType.GetMethod(&quot;PublicPropertiesEqual&quot;),
                    Expression.Constant(query)
                ),
                param
            );
            List&lt;TEntity&gt; res = _repo.GetList(lambda);
            return Ok(res);
        }
</code></pre>
<p>And the error after executed this code</p>
<blockquote>
<p>InvalidOperationException: The LINQ expression 'DbSet()
.Where(c =&gt; c.PublicPropertiesEqual(Customer))' could not be translated. REST OF THE ERROR IS SAME ABOVE...</p>
</blockquote>
<p><strong>As a conclusion, how can I filter the query with using PublicPropertiesEqual(object) function ?</strong></p>

## Answers
### Answer ID: 67505011
<p>It is easy to write such function, but you have to filter out navigation properties by yourself:</p>
<pre class="lang-cs prettyprint-override"><code>public static Expression&lt;Func&lt;T, bool&gt;&gt; PublicPropertiesEqual&lt;T&gt;(T entity)
{
    var props = typeof(T).GetProperties();
    var entityParam = Expression.Parameter(typeof(T), &quot;e&quot;);
    var entityExpr = Expression.Constant(entity);

    var equality = props.Select(p =&gt; Expression.Equal(
        Expression.MakeMemberAccess(entityParam, p),
        Expression.MakeMemberAccess(entityExpr, p)
    ));

    var predicate = equality.Aggregate(Expression.AndAlso);
    return Expression.Lambda&lt;Func&lt;T, bool&gt;&gt;(predicate, entityParam);
}
</code></pre>
<p>Usage is simple:</p>
<pre class="lang-cs prettyprint-override"><code>List&lt;TEntity&gt; res = _repo.GetList(PublicPropertiesEqual(query));
</code></pre>
<p>Anyway if you have access to <code>DbContext</code> better to pass it to the function and reuse <code>IModel</code> information.</p>
<pre class="lang-cs prettyprint-override"><code>public static Expression&lt;Func&lt;T, bool&gt;&gt; PublicPropertiesEqual&lt;T&gt;(DbContext ctx, T entity)
{
    var et = ctx.Model.FindEntityType(typeof(T));
    if (et == null)
        throw new InvalidOperationException();

    var props = et.GetProperties();
    var entityParam = Expression.Parameter(typeof(T), &quot;e&quot;);
    var entityExpr = Expression.Constant(entity);

    var equality = props
        .Where(p =&gt; !p.IsForeignKey() &amp;&amp; !p.IsIndexerProperty())
        .Select(p =&gt; Expression.Equal(
            Expression.MakeMemberAccess(entityParam, p.PropertyInfo),
            Expression.MakeMemberAccess(entityExpr, p.PropertyInfo)
        ));

    var predicate = equality.Aggregate(Expression.AndAlso);
    return Expression.Lambda&lt;Func&lt;T, bool&gt;&gt;(predicate, entityParam);
}
</code></pre>

