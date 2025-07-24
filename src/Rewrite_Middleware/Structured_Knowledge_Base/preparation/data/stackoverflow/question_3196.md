# LINQ to PostgreSQL: query varchar[] column with ilike condition
[Link to question](https://stackoverflow.com/questions/70806220/linq-to-postgresql-query-varchar-column-with-ilike-condition)
**Creation Date:** 1642790782
**Score:** 0
**Tags:** c#, postgresql, .net-core, entity-framework-core
## Question Body
<p>I has a table in PostgreSQL 9.6.6 database with a column of array type:</p>
<pre><code>create table public.account (
  user_name character varying(120), -- login
  emails character varying(200)[] -- array of emails of account
)
</code></pre>
<p>I need to query that table on emails, where at least one email contains given string: if where is a record with <strong>emails = '{admin@mail.com,su@mail.com,owner@mail.com}'</strong> and I'm searching for <strong>'admin'</strong>, this record should be selected.</p>
<p>It can be done for PostgreSQL using query</p>
<pre><code>select * from public.account
where 0 &lt; (select count(1) from unnest(emails) as e where upper(e) like '%ADMIN%');
</code></pre>
<p>In a C# (.NET Core 6) project a have a class for Microsoft.EntityFrameworkCore 6</p>
<pre><code>internal class Account
{
        public string UserName { get; set; }
        public string[] Emails { get; set; }
}
</code></pre>
<p>and corresponding dataset in DataContext:</p>
<pre><code>internal class DataContext : DbContext
{
    public DbSet&lt;Account&gt; Accounts { get; set; }
}
</code></pre>
<p>But there is no equivalent for such query in LINQ. I've tried</p>
<pre><code>var email = &quot;admin&quot;.ToUpper();
var accounts = dataContext.Accounts.Where(a =&gt; a.Emails.Any(e =&gt; e.ToUpper().Contains(email))).ToArray();
</code></pre>
<p>and that should be translated exact to the same SQL query - but is does not:</p>
<blockquote>
<p>The LINQ expression 'e =&gt; e.ToUpper().Contains(__email_0)' could not
be translated. Either rewrite the query in a form that can be
translated, or switch to client evaluation explicitly by inserting a
call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or
'ToListAsync'. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for
more information.</p>
</blockquote>
<p>The only thing that works in my case is</p>
<pre><code>var email = &quot;admin&quot;.ToUpper();
var accounts = dataContext.Accounts.Where(a =&gt; String.Join(',', a.Emails).ToUpper().Contains(email)).ToArray();
</code></pre>
<p>which translates into</p>
<pre><code>-- @__email_0='ADMIN'
SELECT a.user_name, a.emails
FROM account AS a
WHERE (@__email_0 = '') OR (strpos(upper(array_to_string(a.emails, ',', '')), @__email_0) &gt; 0)
</code></pre>
<p>That gives me similar, but not exact <strong>the same</strong> result I tried to get.</p>
<p>I can make the field in database to be jsonb type, but I think the problem still exists: there is no way to create C# LINQ query I need.</p>
<p>So the question is what is the right way to create C# LINQ query that gives me table records where array field (column of PostgreSQL array type) has at least one element that corresponds <strong>ilike</strong> condition?</p>

