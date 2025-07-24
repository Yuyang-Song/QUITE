# EF Core 3.1 doesn&#39;t translate with a helper class on querying
[Link to question](https://stackoverflow.com/questions/60797350/ef-core-3-1-doesnt-translate-with-a-helper-class-on-querying)
**Creation Date:** 1584866384
**Score:** 0
**Tags:** c#, entity-framework-core
## Question Body
<p>In .NET Core 2.2, I used to use a helper class that decrypts the data from the database and retrieves the user information, but now I can't. I get an exception saying that it can't' be translated.</p>

<p>That's the same logic used in .NET Core 2.2</p>

<pre><code>var cp = await Context.Company
                      .Where(a =&gt; Encrypt.Decry(a.Email, a.Em) == login.Email 
                                  &amp;&amp; login.Password == Hash.get(a.Password))
                      .SingleOrDefaultAsync();
</code></pre>

<p>The exception :</p>

<blockquote>
  <p>The LINQ expression 'DbSet.Where(c => Encrypt.Decry(value: c.Email, sec: c.Em) == __login_Email_0 &amp;&amp; __login_Password_1 == Hash.get(c.Password))' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync(). See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information."}</p>
</blockquote>

<p>I don't get why I should explicitly used <code>AsEnumerable()</code>, <code>AsAsyncEnumerable()</code>, <code>ToList()</code>, or <code>ToListAsync()</code> ?</p>

<p>Update : So I tried to follow the example by adding <code>AsEnumerable</code> but it must be with await and I get an error on <code>where</code></p>

<pre><code> var cp = await Context.Company.AsAsyncEnumerable().Where(a =&gt; Encrypt.Decry(a.Email, a.Em) == login.Email &amp;&amp; login.Password == Hash.get(a.Password)).SingleOrDefaultAsync();
</code></pre>

## Answers
### Answer ID: 60797530
<p>EF Core can't translate <code>Encrypt.Decry</code> to SQL query. That's why you see the error. You can load all data into memory and then execute <code>Encrypt.Decry</code>.</p>

<p>From <a href="https://learn.microsoft.com/en-us/ef/core/querying/client-eval" rel="nofollow noreferrer">https://learn.microsoft.com/en-us/ef/core/querying/client-eval</a>:</p>

<blockquote>
  <p>Prior to version 3.0, Entity Framework Core supported client
  evaluation anywhere in the query. For more information, see the
  previous versions section.</p>
</blockquote>

<p>Most likely now it's implemented like this to avoid unintentional client evaluation where a lot of data can be loaded into memory. Now you should explicitly configure client evaluation.</p>

