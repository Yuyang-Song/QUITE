# EntityFramework query manipulation, db provider wrapping, db expression trees
[Link to question](https://stackoverflow.com/questions/6369605/entityframework-query-manipulation-db-provider-wrapping-db-expression-trees)
**Creation Date:** 1308216059
**Score:** 14
**Tags:** c#, entity-framework-4, localization, expression, expression-trees
## Question Body
<p>I'm trying to implement data localization logic for Entity Framework. So that if for example a query selects <code>Title</code> property, behind the scenes it should reference the column <code>Title_enGB</code> or <code>Title_deCH</code> depending on the current user culture . </p>

<p>To achieve this, I'd like to rewrite the DbExpression CommandTrees from Entity Framework. I thought these <a href="http://msdn.microsoft.com/en-us/library/bb358416.aspx" rel="noreferrer">trees</a> are a new common .NET way for building cross database insert/update/select queries.. But now all relevant constructors/factories in the namespaces <code>System.Data.Metadata</code> and <code>System.Data.Common.CommandTrees</code> in <code>System.Data.Entity.dll</code> are internal!! (In msdn documentated as public, like: <a href="http://msdn.microsoft.com/en-us/library/system.data.common.commandtrees.expressionbuilder.dbexpressionbuilder.aspx" rel="noreferrer"><code>DbExpressionBuilder</code></a>).</p>

<p>Does anyone have an idea to achieve this query manipulation with or without query tree rewrite?</p>

<p>my desired code: (<code>public class DbProviderServicesWrapper : DbProviderServices</code>)</p>

<pre><code>/// &lt;summary&gt;
/// Creates a command definition object for the specified provider manifest and command tree.
/// &lt;/summary&gt;
/// &lt;param name="providerManifest"&gt;Provider manifest previously retrieved from the store provider.&lt;/param&gt;
/// &lt;param name="commandTree"&gt;Command tree for the statement.&lt;/param&gt;
/// &lt;returns&gt;
/// An exectable command definition object.
/// &lt;/returns&gt;
protected override DbCommandDefinition CreateDbCommandDefinition(DbProviderManifest providerManifest, DbCommandTree commandTree)
{
    var originalCommandTree = commandTree as DbQueryCommandTree;
    if (originalCommandTree != null)
    {
        var expression = new MyCustomQueryRewriter(originalTree.MetadataWorkspace).Visit(originalCommandTree.Query);
        commandTree = DbQueryCommandTree.FromValidExpression(originalCommandTree.MetadataWorkspace, originalCommandTree.DataSpace, expression);
    }

    // TODO: UpdateCommand/InsertCommand

    var inner = this.Inner.CreateCommandDefinition(providerManifest, commandTree);
    var def = new DbCommandDefinitionWrapper(inner, (c, cd) =&gt; new DbCommandWrapper(c));

    return def;
}
</code></pre>

<p><br />
<br /></p>

<h1>Update</h1>

<p>Having two title columns on one table isn't cool but its easier to implement in a first step. Later I'll join an other table with the localized fields, so the main table will only contain invariant data. </p>

<p><img src="https://i.sstatic.net/9jBdh.jpg" alt="Multilanguage"></p>

## Answers
### Answer ID: 6465685
<p>Instead I will propose one more design...</p>

<pre><code>Products
   ProductID 
   ProductName
   Price
   Description
   ParentID (Nullable, FK on ProductID)
   LangCode
</code></pre>

<p>Now in this case you have,</p>

<pre><code>1, Milk, $1 , EnglishDesc  , NULL, en-us 
2. M*^*, ^*&amp;, OtherLangDesc, 1   , @$#$$
</code></pre>

<p>Your record 2 is actually another language description of entire product in different language identified by LanguageCode. </p>

<p>This way you can only manage one Table and writing some Generics based or Reflection based Querying solution will be lot easier.</p>

<pre><code>// Get Active Products
q = context.Products.Where( x=&gt; x.ParentID == null);

// Get Product's Language Code Description
IQueryable&lt;Product&gt; GetProductDesc(int productID, string langCode){
    return context.Products.Where( x=&gt;x.ParentID == productID &amp;&amp;
              x.LangCode == langCode);
}
</code></pre>

<p>You can create an interface as follow,</p>

<pre><code>interface IMultiLangObject{
    int? ParentID {get;set;}
    string LangCode {get;set;}
}
</code></pre>

<p>And you can write a generic solution based on this.</p>

### Answer ID: 6428861
<p>I agree with the answer of Shiraz that this shouldn't be what you want if you are still capable of changing the design, but I'll be assuming that this is an existing application that you are converting to Entity Framework. </p>

<p>If so, it matters if the Title_enGB/etc columns are mapped in the EDMX file / POCOs. If they are, I suppose this is possible. What you could do here, is use an Expression visitor that visits MemberExpressions, checks if they access a property named "Title" (you could create a whitelist of properties that needed to be treated like this) and then return a new MemberExpression that insteads accesses Title_enGB if the logged in user has that language set.</p>

<p>A quick example:</p>

<pre><code>public class MemberVisitor : ExpressionVisitor
{
  protected override Expression VisitMember(MemberExpression node)
  {
    if(node.Member.Name == "Title")
    {
        return Expression.Property(node.Expression, "Title_" + User.LanguageCode)
    }

    return base.VisitMember(node);
  }
}
</code></pre>

<p>And then before you execute the query:</p>

<pre><code>var visitor = new MemberVisitor();
visitor.Visit(query);
</code></pre>

<p>Again, this is only a good idea if you don't have any control over the database any more. </p>

<p>This solution may or may not be practical to you, depending on your exact situation, but rewriting queries using Expressions is definitely possible.</p>

<p>It's a much higher level solution than modifying how Entity Framework generates the actual SQL queries. That's indeed hidden from you, probably with good reason. Instead, you just modify the expression tree that describes the query and let Entity Framework worry about converting it to SQL.</p>

### Answer ID: 6379088
<p>In .net you have resx files for handling localization. See: <a href="https://stackoverflow.com/questions/1134018/what-are-the-benefits-of-resource-resx-files/1134057#1134057">What are the benefits of resource(.resx) files?</a></p>

<p>There are a couple of problems with your approach:</p>

<ul>
<li>Adding an extra language requires a database change</li>
<li>There is more data traffic from the database than is required</li>
</ul>

<p>I know that this is not a direct answer to your question but I think you should look at resx files.</p>

<p>If you must store it in the database you could redesign the database:</p>

<ul>
<li>Table 1: id, Text</li>
<li>Table 2: id, Table1_id, language_code, text</li>
</ul>

<p>This way a new language does not require a database change, and the EF code becomes much simpler.</p>

