# Translate Generic Query of Business Layer to Data Access Layer
[Link to question](https://stackoverflow.com/questions/19813228/translate-generic-query-of-business-layer-to-data-access-layer)
**Creation Date:** 1383744083
**Score:** 2
**Tags:** c#, architecture, layer
## Question Body
<p>I am in the middle of rewriting legacy software to .Net and have created a Data Access Layer using Linq 2 SQL that is working pretty well. The database I am working with has over 230 tables and is not something I can really change. The problem I am running into is with the Business Layer. I would like for the developers to be able to query the business objects and have those queries map to the data layer. So something like <code>Customers.Query(c=&gt;c.ID=="MyID")</code>
and have that be able to be passed to my DAL, <code>context.CUSTOMERS.Query(c=&gt;c.UID == "MyID")</code>
I have generic Query methods in my DAL that will allow me to pass in the DAL query.</p>

<p>This is where I am stuck. I can create a method that uses an Expression but how do I get and then map those fields to the corresponding DAL fields and get the value that is trying to be matched. What I don't want is to have to expose the DAL objects to the end developers who are doing presentation layer stuff. I am open to ideas and suggestions.</p>

## Answers
### Answer ID: 19938701
<p>So I think I have been able to find a solution to this. Using <a href="http://msdn.microsoft.com/en-us/library/bb882521.aspx" rel="nofollow noreferrer">ExpressionVisitor</a> and help from <a href="https://stackoverflow.com/questions/14007101/how-can-i-convert-a-lambda-expression-between-different-but-compatible-models">this post</a></p>

<p>I modified the VisitMember method:</p>

<pre><code>    protected override Expression VisitMember(MemberExpression node)
    {
        string sDbField = ((SFWBusinessAttributes)node.Expression.Type.GetProperty(node.Member.Name).GetCustomAttribu`tes(typeof(SFWBusinessAttributes), true)[0]).DBColumn;
        var expr = Visit(node.Expression);
        if (expr.Type != node.Type)
        {
            MemberInfo newMember = expr.Type.GetMember(sDbField).Single();
            return Expression.MakeMemberAccess(expr, newMember);
        }
        return base.VisitMember(node);
    }
</code></pre>

<p>To pull the Attribute off of the Property of the Business Object.</p>

<p>To call everything I can do from the app:</p>

<pre><code>    BusObj.Query(a =&gt; a.IsDeleted != true &amp;&amp; a.Company.Contains("Demo"))
</code></pre>

<p>Which calls a method in the business object</p>

<pre><code>    public List&lt;Account&gt; Query(Expression&lt;Func&lt;Account, bool&gt;&gt; expression)
    {
        using (Data.CustomerData data = new Data.CustomerData(_connstring))
        {
             return MapList(data.Query&lt;Data.Database.ACCOUNT&gt;(expression.Convert&lt;Account, Data.Database.ACCOUNT&gt;()).ToList());
        }
</code></pre>

<p>Performance seems pretty good, I know there is going to be a hit with the mapping but it is something I can live with for now.</p>

### Answer ID: 19825554
<p>Do the developers need to query the business objects using an expression? The reason I ask is because mapping expressions may be complicated. At some point, some mapping has to be done. The DAL is usually the mapping layer that turns DB objects into domain objects, and vice-versa.</p>

<p>Two other approaches to consider:</p>

<ol>
<li><p>Use the repository pattern, where the caller passes in a query object. The DAL would be responsible for turning that query object into an expression. An example of the repository pattern is shown in a <a href="https://stackoverflow.com/q/14092234/279516">question that I asked</a>.</p></li>
<li><p>Expose more specific methods, like:</p>

<p>public Customer GetCustomersById(int id) { ... }</p></li>
</ol>

<p>I believe either of those two approaches would make things easier to query.</p>

