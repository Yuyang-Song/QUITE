# LINQ Generic IQueryable&lt;T&gt; WHERE Clause
[Link to question](https://stackoverflow.com/questions/62614829/linq-generic-iqueryablet-where-clause)
**Creation Date:** 1593287289
**Score:** 3
**Tags:** linq, reflection, dbcontext
## Question Body
<p>Let's say I have a DBContext with 3 DBSets:</p>
<pre><code>public class DatabaseContext : DbContext
{
    public DbSet&lt;A&gt; As { get; set; }
    public DbSet&lt;B&gt; Bs { get; set; }
    public DbSet&lt;C&gt; Cs { get; set; }
}

class A
{
    public string Text { get; set; }
    public string Code { get; set; }
}

class B
{
    public string Name { get; set; }
    public string Code { get; set; }
}

class C
{
    public string Book { get; set; }
    public string Code { get; set; }
}
</code></pre>
<p>I want to write a <strong>generic</strong> method that:</p>
<ol>
<li>Generically takes any of the three <code>DbSet</code> as the first argument</li>
<li>Takes a string value as the second argument</li>
<li>Without casting to <code>IEnumerable</code>, returns the first record in the provided <code>DbSet</code> where the <code>Code</code> field matches the provided string</li>
</ol>
<p>So far I have this method:</p>
<pre><code>public static T GetCode&lt;T&gt;(IQueryable&lt;T&gt; set, string code) where T : class
{
    var Prop = typeof(T).GetProperty(&quot;Code&quot;);
    return set.Where(x =&gt; (string)Prop.GetValue(x) == code).FirstOrDefault();
}
</code></pre>
<p>When I try to call it using this line:</p>
<pre><code>var _A = GetCode(TheDB.As, &quot;123&quot;);
var _B = GetCode(TheDB.Bs, &quot;123&quot;);
var _C = GetCode(TheDB.Cs, &quot;123&quot;);
</code></pre>
<p>I get this error:</p>
<blockquote>
<p>InvalidOperationException:</p>
<p>The LINQ expression 'DbSet&lt;A&gt;.Where(m =&gt; (string)__Prop_0.GetValue(m) == __code_1)' could not be translated.</p>
<p>Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync().</p>
</blockquote>
<p>How can I write the <code>WHERE</code> clause on the <code>DbSet</code> that is able to translate properly for <code>IQueryable</code>? My method works if I cast the <code>IQueryable</code> to an <code>IEnumerable</code>, but I don't want to do that, since the set may potentially be very large and I want the database (not my application) to do the record searching.</p>

## Answers
### Answer ID: 62615004
<p>The easiest (and type safe) approach would be just to introduce an interface like <code>IHaveCode</code> and limit the generic parameter to it:</p>
<pre><code>interface IHaveCode
{
     string Code { get; set; }
}

class A: IHaveCode
{
    public string Text { get; set; }
    public string Code { get; set; }
}

class B: IHaveCode
{
    public string Name { get; set; }
    public string Code { get; set; }
}

class C: IHaveCode
{
    public string Book { get; set; }
    public string Code { get; set; }
}

public static T GetCode&lt;T&gt;(IQueryable&lt;T&gt; set, string code) where T : IHaveCode
{
    return set.Where(x =&gt; x.Code == code).FirstOrDefault();
}
</code></pre>
<p>If for some reason it does not suit you then you will need to construct an <a href="https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/expression-trees/" rel="nofollow noreferrer">expression tree</a> yourself.</p>

### Answer ID: 62650015
<p>You can implement the GetCode method using <a href="https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/expression-trees/" rel="nofollow noreferrer">Expression Trees</a>.</p>
<pre class="lang-cs prettyprint-override"><code>public static T GetCode&lt;T&gt;(IQueryable&lt;T&gt; set, string code) where T : class {
    PropertyInfo codeProp = typeof(T).GetProperty(&quot;Code&quot;);
    if(codeProp == null)
        throw new ArgumentException($&quot;{typeof(T).FullName} does not have the Code property&quot;);
    ParameterExpression param = Expression.Parameter(typeof(T));
    Expression getCode = Expression.MakeMemberAccess(param, codeProp);
    Expression codeVal = Expression.Constant(code);
    Expression body = Expression.Equal(getCode, codeVal);
    Expression&lt;Func&lt;T, bool&gt;&gt; predicate = Expression.Lambda&lt;Func&lt;T, bool&gt;&gt;(body, param);
    return set.FirstOrDefault(predicate);
}
</code></pre>

### Answer ID: 62633558
<p>A more Generic method than the one from Guru Stron, one that is also usable for DbSets of classes without a property <code>Code</code>, would be to provide the property that you want to use in your comparison.</p>
<pre><code>public static T GetFirstPropertyMatchOrDefault&lt;T&gt;(
    this IQueryable&lt;T&gt; source,
    Expression&lt;Func&lt;T, string&gt;&gt; propertySelector,
    string comparisonValue)
{
    return source.Where(sourceElement =&gt; propertySelector(sourceElement) == comparisonValue)
                 .FirstOrDefault();
}
</code></pre>
<p>Usage:</p>
<pre><code>string comparisonValue = ...
A fetchedA = dbContext.As.GetFirstPropertyMachOrDefault(a =&gt; a.Code, comparisonValue);
</code></pre>
<p>But now that you have made it generic, you can also use it to fetch other properties;</p>
<pre><code>// Get a C by Book title:
string bookTitle = ...
C fetchedC = dbContext.Cs.GetFirstPropertyOrDefault(c =&gt; c.Book);
</code></pre>

