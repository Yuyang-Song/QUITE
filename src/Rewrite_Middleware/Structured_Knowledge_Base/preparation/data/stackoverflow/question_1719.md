# What are the drawbacks of using a method which calls a delegate for every row in SqlDataReader?
[Link to question](https://stackoverflow.com/questions/4910333/what-are-the-drawbacks-of-using-a-method-which-calls-a-delegate-for-every-row-in)
**Creation Date:** 1296947552
**Score:** 3
**Tags:** c#, generics, readability, sqlconnection, maintainability
## Question Body
<p>When I find a new idea, I always stick with it, and am unable to see any weak sides of it. Bad things happen when I start to use the new idea in a large project, and discover some moths later that the idea was extremely bad and I shouldn't use it in any project.</p>

<p>That's why, having a new idea and being ready to use it in a new large project, <strong>I need your opinion on it, especially negative one</strong>.</p>

<hr>

<p>For a long time, I was bored to type again and again or copy-paste the following blocks in projects where database must be accessed directly:</p>

<pre><code>string connectionString = Settings.RetrieveConnectionString(Database.MainSqlDatabase);
using (SqlConnection sqlConnection = new SqlConnection(connectionString))
{
    sqlConnection.Open();

    using (SqlCommand getProductQuantities = new SqlCommand("select ProductId, AvailableQuantity from Shop.Product where ShopId = @shopId", sqlConnection))
    {
        getProductQuantities.Parameters.AddWithValue("@shopId", this.Shop.Id);
        using (SqlDataReader dataReader = getProductQuantities.ExecuteReader())
        {
            while (dataReader.Read())
            {
                yield return new Tuple&lt;int, int&gt;((int)dataReader["ProductId"], Convert.ToInt32(dataReader["AvailableQuantity"]));
            }
        }
    }
}
</code></pre>

<p>So I've done a small class which allows to write something like that to do the same thing as above:</p>

<pre><code>IEnumerable&lt;Tuple&lt;int, int&gt;&gt; quantities = DataAccess&lt;Tuple&lt;int, int&gt;&gt;.ReadManyRows(
    "select ProductId, AvailableQuantity from Shop.Product where ShopId = @shopId",
    new Dictionary&lt;string, object&gt; { { "@shopId", this.Shop.Id } },
    new DataAccess&lt;string&gt;.Yield(
        dataReader =&gt;
        {
            return new Tuple&lt;int, int&gt;(
                (int)dataReader["ProductId"],
                Convert.ToInt32(dataReader["AvailableQuantity"]);
        }));
</code></pre>

<p>The second approach is:</p>

<ul>
<li><p>Shorter to write,</p></li>
<li><p>Easier to read (at least for me; some people may say that actually, it's much less readable),</p></li>
<li><p>Harder to make errors (for example in first case, I often forget to open the connection before using it, or I forget <code>while</code> block, etc.),</p></li>
<li><p>Faster with the help of Intellisense,</p></li>
<li><p>Much more condensed, especially for simple requests.</p></li>
</ul>

<p>Example:</p>

<pre><code>IEnumerable&lt;string&gt; productNames = DataAccess&lt;string&gt;.ReadManyRows(
    "select distinct ProductName from Shop.Product",
    new DataAccess&lt;string&gt;.Yield(dataReader =&gt; { return (string)dataReader["ProductName"]; }));
</code></pre>

<p>After implementing such thing with simple <code>ExecuteNonQuery</code>, <code>ExecuteScalar</code> and <code>ReadManyRows</code> and a generic <code>DataAccess&lt;T&gt;.ReadManyRows</code> in a small project, I was happy to see that the code is much shorter and easier to maintain.</p>

<p>I found only two drawbacks:</p>

<ul>
<li><p>Some modifications in requirements will require heavy code changes. For example, if there is a need to add transactions, it will be very easy to do with ordinary <code>SqlCommand</code> approach. If my approach is used instead, it will require to rewrite the whole project to use <code>SqlCommand</code>s and transactions.</p></li>
<li><p>Slight modifications on command level will require to move from my approach to standard <code>SqlCommand</code>s. For example, when querying one row only, either <code>DataAccess</code> class must be extended to include this case, or the code must use directly <code>SqlCommand</code> with <code>ExecuteReader(CommandBehavior.SingleRow)</code> instead.</p></li>
<li><p>There might be a small performance loss (I don't have precise metrics yet).</p></li>
</ul>

<p>What are the other weak points of this approach, especially for <code>DataAccess&lt;T&gt;.ReadManyRows</code>?</p>

## Answers
### Answer ID: 4911277
<p>What you're trying to accomplish is nice, I actually like this kind of syntax and I think it's pretty flexible. However I believe you need to design you APIs better.</p>

<p>The code is readable and nearly beautiful but it is hard to understand, primarily due to lots of generics that don't make much sense unless you know exactly what each type means. I'd use generic type inference wherever possible to eliminate some of them. To do so, consider using generic methods instead of generic types.</p>

<p>Some syntax suggestions (I don't have compiler now so they are basically ideas):</p>

<p><strong>Use anonymous types instead of dictionaries</strong></p>

<p>It's trivial to write a helper that converts anonymous type to a dictionary but I think it improves the notation greatly and you wouldn't need to write <code>new Dictionary&lt;string, object&gt;</code>.</p>

<p><strong>Use Tuple.Create</strong></p>

<p>This static method was created to avoid specifying types explicitly.</p>

<p><strong>Create a strong-typed wrapper around DataReader</strong></p>

<p>This would remove those ugly conversions all around the place—and actually, do you really need access to <code>DataReader</code> in that lambda?</p>

<p>I will illustrate this by code for your examples.<br>
Kudos to <a href="https://stackoverflow.com/users/285873/david-harkness">David Harkness</a> for chaining idea.</p>

<pre><code>var tuples = new DataAccess ("select ProductId, AvailableQuantity from Shop.Product where ShopId = @shopId")
    .With (new { shopId = this.Shop.Id }) // map parameters to values
    .ReadMany (row =&gt;
         Tuple.Create (row.Value&lt;int&gt; ("ProductId"), row.Value&lt;int&gt; ("AvailableQuantity"))); 

var strings = new DataAccess ("select distinct ProductName from Shop.Product")
    .ReadMany (row =&gt; row.Value&lt;string&gt; ("ProductName")); 
</code></pre>

<p>I can also see it being extended for handling single row selection:</p>

<pre><code>var productName = new DataAccess ("select ProductName from Shop.Product where ProductId = @productId")
    .With (new { productId = this.SelectedProductId }) // whatever
    .ReadOne (row =&gt; row.Value&lt;string&gt; ("ProductName")); 
</code></pre>

<p>This is a rough draft for <code>Row</code> class:</p>

<pre><code>class Row {
    DataReader reader;

    public Row (DataReader reader)
    {
        this.reader = reader;
    }

    public T Value&lt;T&gt; (string column)
    {
        return (T) Convert.ChangeType (reader [column], typeof (T));
    }
}
</code></pre>

<p>It is to be instantiated inside <code>ReadOne</code> and <code>ReadMany</code> calls and provides convenient (and limited) access to underlying <code>DataReader</code> for selector lambdas.</p>

### Answer ID: 4911178
<p>The delegate does make it a bit harder to read/understand immediately for someone new to this approach but it should be easy enough to pick up eventually.</p>

<p>From a maintainability point of view it may be harder to understand the stack trace when errors eventually creep in. Primarily if an error occurs in this section:</p>

<pre><code>new DataAccess&lt;string&gt;.Yield(
    dataReader =&gt;
    {
        return new Tuple&lt;int, int&gt;(
            (int)dataReader["ProductId"],
            Convert.ToInt32(dataReader["AvailableQuantity"]);
    }));
</code></pre>

<p>The use of yield puts some limitations on where you can try/catch (<a href="https://stackoverflow.com/questions/346365/why-cant-yield-return-appear-inside-a-try-block-with-a-catch">Why can&#39;t yield return appear inside a try block with a catch?</a>) but that is an issue in the previous approach as well and may not be relevant in your scenario.</p>

### Answer ID: 4910971
<p>First of all, never apologize for not copy-pasting code.</p>

<p>Your abstraction looks fine, however what troubles me a little more is the fact that the first example you gave keeps the <code>SqlConnection</code> open longer than it needs to be.</p>

<p>Using an <code>IEnumerable&lt;T&gt;</code> is great, since you defer execution to when and if it is consumed.
However, as long as you have not reached the end of your enumeration, the connection stays open.</p>

<p>The implementation of your method could consume the entire enumeration via a <code>ToList()</code>, and then return the list instead. You could even still support the deferred execution by implementing a small custom enumerator.</p>

<p>But I need to put a caveat around this, verify that there isn't any old code doing some magic while enumerating.  </p>

### Answer ID: 4910459
<p>Your abstraction approach looks sound. Any performance hit due to extra method calls will be trivial, and developer time is far more expensive than CPU time. When you need to add transactions or single-row selects, you can expand your library classes. You're making good use of <a href="http://www.c2.com/cgi/wiki?DontRepeatYourself" rel="nofollow">Don't Repeat Yourself</a> here.</p>

<p>The Spring Framework for Java makes heavy use of these types of template classes and helpers such as <code>JdbcTemplate</code> and <code>HibernateTemplate</code> to remove the need for developers to write boilerplate code. The idea is to write and test it well once and reuse it many times over.</p>

### Answer ID: 4910440
<p>My thoughts: you're embedding SQL in code, in a string (as opposed to using LINQ, which is at least syntax-checked, which helps provided you keep your DBML or EDMX mapping file synched with your database structure). Embedding SQL in non-syntax checked code in this way could easily lead to unmaintainable code, where you (or someone else) later changes the database structure or the embedded SQL string in a way that breaks the application. Embedding SQL in strings is particularly prone to producing hard-to-find bugs, because code with logical errors will still compile correctly; this makes it more likely that developers who are less familiar with the code base will obtain a false sense of security that changes they've made have not had any adverse or unintended effects.</p>

