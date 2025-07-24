# How can I implement Query Interception in a LINQ to Entities query? (c#)
[Link to question](https://stackoverflow.com/questions/5249473/how-can-i-implement-query-interception-in-a-linq-to-entities-query-c)
**Creation Date:** 1299690574
**Score:** 4
**Tags:** c#, linq, entity-framework-4, iqueryable, ef-code-first
## Question Body
<p>I'm trying to implement encrypted columns in EF4 and using the CTP5 features to allow simple use of POCO's to query the database. Sorry that this is a lot of words, but I hope the below gives enough to explain the need and the problem!</p>

<p>So, bit of background, and my progress so far:</p>

<p>The intention is that if you query the tables without using our DAL then the data is rubbish, but I don't want the developers to worry about if/when/how the data is encrypted.</p>

<p>For simplicity, at this stage I'm working on the assumption any string column will be encrypted.</p>

<p>Now, I have successfully implemented this for returning the data using the Objectmaterialized event, and for data commits using the SavingChanges event.</p>

<p>So given the following class:</p>

<pre><code>public class Thing
{

    public int ID { get; set; }
    [Required]
    public string Name { get; set; }
    public DateTime Date { get; set; }
    public string OtherString { get; set; }
}
</code></pre>

<p>The below query returns all the required values and the POCO materialized has clear data in it.</p>

<pre><code>var things = from t in myDbContext.Things
             select t;
</code></pre>

<p>where myDbContext.Things is a <code>DbSet&lt;Thing&gt;</code> </p>

<p>Likewise, passing an instance of <code>Thing</code> to <code>Things.Add()</code><br>
<em>(with clear string data in the Name and/or OtherString values)</em><br>
and then calling <code>myDbContext.SaveChanges()</code> encrypts the strings before it gets to the data store. </p>

<p>Now, the problem I have is in this query:</p>

<pre><code>var things = from t in myDbContext.Things
             where t.Name == "Hairbrush"
             select t;
</code></pre>

<p>This results in the unencrypted value being compared to the encrypted value in the DB. Obviously I don't want to get all the records from the database, materialize them, and then filter the results based on any supplied Where clause... so what I need to do is: <em>intercept that query and rewrite it by encrypting any strings in the Where clause.</em>
So I've looked at:</p>

<ul>
<li>writing a query provider, but that doesn't seem like the right solution... <em>(is it?)</em></li>
<li>writing my own IQueryable wrapper for the DbSet which will capture the expression, run over it using an expression tree visitor and then forward the new expression to the DbSet...</li>
</ul>

<p>Attempts at both have left me somewhat lost! I prefer the second solution i think since it feels a bit neater, and is probably clearer to other developers in future. But I'm happy to go with either or another <strong>better</strong> option!!</p>

<p>The main thing I am struggling with is when/how the LINQ expression is applied to the object... I think i've got myself a bit confused as to where the expression executes in the IQueryable object thus I'm not sure which method I need to implement in my wrapper to then grab and manipulate the expression being passed in... </p>

<p>I'm sure I'm missing something fairly obvious here and I'm waiting for that light bulb moment... but its not coming!!</p>

<p>Any help will be very gratefully received! </p>

## Answers
### Answer ID: 11483412
<p>You can use David Fowler's Query Interceptor:</p>

<p><a href="https://github.com/davidfowl/QueryInterceptor" rel="nofollow">https://github.com/davidfowl/QueryInterceptor</a></p>

<p>One example of its use:</p>

<p>IQueryable q = ...;
IQueryable modifed = q.InterceptWith(new MyInterceptor());</p>

<p>And on class MyInterceptor:</p>

<p>protected override Expression VisitBinary(BinaryExpression node) {
        if (node.NodeType == ExpressionType.Equal) {
            // Change == to !=
            return Expression.NotEqual(node.Left, node.Right);
        }
        return base.VisitBinary(node);
    }</p>

### Answer ID: 5422463
<p>Thought I'd let you know what my final solution was. 
In the end I have gone a wrapper class which implements a Where method, but without going to the extent of implementing IQueryable entirely. LINQ will still execute against the class (at least to the extent that I want/need it to) and will call the Where method with the expression from the LINQ. </p>

<p>I then traverse this ExpressionTree and replace my strings with encrypted values before forwarding the new expressiontree to the internal DbSet. and then returning the result.</p>

<p>Its pretty crude, and has its limitation, but works for our particular circumstance without problem. </p>

<p>Thanks,
Ben</p>

### Answer ID: 5249590
<p>you should use the <code>QueryInterceptor</code> attribute, search here in SO or in google and you find examples on how to use it.</p>

<p>a snippet:</p>

<pre><code>[QueryInterceptor("Orders")]
public Expression&lt;Func&lt;Order, bool&gt;&gt; FilterOrders() 
{
    return o =&gt; o.Customer.Name == /* Current principal name. */;
} 

// Insures that the user accessing the customer(s) has the appropriate
// rights as defined in the QueryRules object to access the customer
// resource(s).

[QueryInterceptor ("Customers")]
public Expression&lt;Func&lt;Customer, bool&gt;&gt; FilterCustomers() 
{
  return c =&gt; c.Name == /* Current principal name. */ &amp;&amp;
              this.CurrentDataSource.QueryRules.Contains(
                rule =&gt; rule.Name == c.Name &amp;&amp;
                        rule.CustomerAllowedToQuery == true
              );
}
</code></pre>

