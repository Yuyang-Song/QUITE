# LINQ - Get records from one table, with second table multi record matching
[Link to question](https://stackoverflow.com/questions/69465604/linq-get-records-from-one-table-with-second-table-multi-record-matching)
**Creation Date:** 1633522778
**Score:** 1
**Tags:** c#, linq, entity-framework-core
## Question Body
<p>I am working on a system where I am given a SQL database where there are no relationships (please dont get me started on this).</p>
<p>A table that I have is bank accounts, id, sort code, account number, name.
A second table that I have is a payments table, this has 6 fields, for account number and sort code, but I only need to match on one pair (sort code and account number)</p>
<p>So, I have a query that gets all the bank accounts like this</p>
<pre><code>var bankAccounts =
            _databaseContext.BankAccounts
                .Where(accounts =&gt; model.BankAccountIds
                    .Any(x =&gt; x == accounts.Id))
                .ToList();
</code></pre>
<p>I am building a query and</p>
<pre><code>_databaseContext.Payments.Where(x =&gt; bankAccounts.Any(b =&gt; b.AccountNumber == x.AccountNumber) 
                                  &amp;&amp; bankAccounts.Any(b =&gt; b.SortCode == x.SortCode));
</code></pre>
<p>However, when I run this I get the error</p>
<blockquote>
<p>ystem.InvalidOperationException: The LINQ expression 'DbSet()
.Where(p =&gt; bankAccounts_0
.Any(b =&gt; b.AccountNumber == p.AccountNumber) &amp;&amp; bankAccounts_0
.Any(b =&gt; b.SortCode == p.SortCode))' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.</p>
</blockquote>
<p>So, what I need is to be able to write the query in such a way it gets me all the payments that are made where the sort code and account number match in the payments table to the bank accounts table</p>
<p>And I do realise that if we had the relationship between the tables this would be much simpler, however as contractor, I have little clout as to how they architect things</p>
<p>-- Edit</p>
<p>In Datacontext in <code>OnModelCreating</code> I was also doing this, but when seeding the data this dies - just building now to get the exception it throws</p>
<pre><code> modelBuilder.Entity&lt;BankAccount&gt;()
            .HasMany(payment =&gt; payment.Payments)
            .WithOne(bankAccount =&gt; bankAccount.BankAccountDetails)
            .HasPrincipalKey(x =&gt; new {x.AccountNumber, x.SortCode});
</code></pre>
<p>Then when running the code I get this</p>
<blockquote>
<p>System.InvalidOperationException: Unable to track an entity of type 'BankAccount' because alternate key property 'AccountNumber' is null. If the alternate key is not used in a relationship, then consider using a unique index instead. Unique indexes may contain nulls, while alternate keys may not.</p>
</blockquote>

## Answers
### Answer ID: 69469483
<p>Realistically, you're looking for an SQL like:</p>
<pre><code>SELECT *
FROM Payments p
WHERE 
  EXISTS(
    SELECT null 
    FROM BankAccounts ba
    WHERE  
      ba.BankAccountId IN (some,list,of,guids,from,your,model) AND 
      ba.AccountNumber = p.AccountNumber AND
      ba.SortCode = p.SortCode
  )
</code></pre>
<p>Your having downloaded the bank acounts (<code>ToList()</code>ed them) first actually actively cripples EF's ability to do this; it can't see a way to create the coordinated subquery any more, as it's no longer a database-based collection but a collection from the client side. As far as I know, EF supports no notion of building a value set from complex client-provided data and joining to it.</p>
<p>If you keep your &quot;these certain bank accounts&quot; operation as a database-based enumerable your EF might be able to translate it to something like the above :</p>
<pre><code>_databaseContext.Payments.Where(pay =&gt; 
    _databaseContext.BankAccounts.Where(
      ba =&gt; model.BankAccountIds.Any(mba =&gt; mba == ba.Id)
    ).Any(ba =&gt; 
        ba.AccountNumber == pay.AccountNumber &amp;&amp;
        ba.SortCode == pay.SortCode
    )
);
</code></pre>
<p>The <code>.Any(mba =&gt; mba == ba.Id)</code> will translate to IN so long as it's truly a simple prop; you could also use <code>model.BankAccountIds.Contains(ba.Id)</code> but in either case the model literally needs a list of bank account guids for this restriction to translate. The <code>.Any(ba =&gt; </code> can translate to a coordinated <code>EXISTS</code>.</p>
<p>Even if it does work, I'd say you have some data modelling issues to work out - having to write a full client app like this is a headache..</p>
<hr />
<p>You noted that &quot;it doesn't work&quot;, but in my tests (which are as close as I can get them to the scenario you posted) there wasn't any problem at all:</p>
<p><a href="https://i.sstatic.net/W5ePG.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/W5ePG.png" alt="enter image description here" /></a></p>
<p>On the left you can see my tables: BankAccounts and Payments. They both have AccountNumber and SortCode which are never the PK, they have no FKs, the payments Ac/Sort may be null. In the middle is the query I recommended you, with the only fudge above it being me making something like what I assume your model is: a root object that holds a property called BankAccountIds that is a collection of guids. On the right, you can see the generated query; it's come out fairly identically to the SQL posted initially. I use EF Core 5</p>
<p>Examine what is different between what I've set up, and what you have. Post your models. Post the exact query that doesn't work</p>

### Answer ID: 69466114
<p>what you try to do is equivalent to <code>ID in (1,2,3,6,..)</code>,. To get that the code must use<code>Contains</code>, not <code>Any</code>.</p>
<p>There's no way to convert that <code>List.Any(x.id)</code> to SQL.</p>
<ul>
<li>First, there are no lists or arrays in T-SQL, so EF Core couldn't send that array to the server.</li>
<li>Second, <code>bankAccounts</code> contains complex objects, not values. EF Core would have to generate a table type with all relevant fields and send it to the server for use in a subquery.</li>
</ul>
<p>In T-SQL we'd write:</p>
<pre><code>Select * 
From Payments
Where AccountNumber in (....) AND SortCode in (...)
</code></pre>
<p>To do the same in LINQ we need <code>Contains</code>. To use it the list of values should contain individual simple values:</p>
<pre><code>var accNumbers=bankAccounts.Select(b =&gt; b.AccountNumber).ToList();
var sortCodes=bankAccounts.Select(b =&gt; b.SortCode).ToList();

var payments = _databaseContext.Payments.Where(x =&gt;
        accNumbers.Contains(x.AccountNumber) 
        &amp;&amp; sortCodes.Contains(x.SortCode));
</code></pre>

### Answer ID: 69465825
<p>New version, after clarificaiton in comments:
I think you could do it as one query instead of materialize the bankAccounts -list first, maybe try some like this:</p>
<pre><code>_databaseContext.Payments
    .Where(p=&gt;_databaseContext.BankAccounts.Where(accounts =&gt; model.BankAccountIds.Contains(accounts.Id) &amp;&amp; accounts.AccountNumber==p.AccountNumber  &amp;&amp; accounts.SortCode==p.SortCode ))
</code></pre>
<hr />
<p>I think the problem is that LINQ cannot translate the list of bankAccounts to SQL, try to make a list of the AccountNumbers and SortCode as <code>List&lt;string&gt;</code> and do something like this:</p>
<pre><code>var bankAccounts =
            _databaseContext.BankAccounts
                .Where(accounts =&gt; model.BankAccountIds.Contains(accounts.Id))
                .ToList();

var accountNumbers=bankAccounts.Select(x=&gt;x.AccountNumber).ToList();
var sortCodes=bankAccounts.Select(x=&gt;x.SortCode).ToList();

_databaseContext.Payments.Where(x =&gt; accountNumbers.Contains(x.AccountNumber) &amp;&amp; sortCodes.Contains(x.SortCode));
</code></pre>

