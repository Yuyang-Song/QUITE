# Why does my Attach() method trigger a &quot;Entity already exists&quot; InvalidOperationException?
[Link to question](https://stackoverflow.com/questions/70662642/why-does-my-attach-method-trigger-a-entity-already-exists-invalidoperationex)
**Creation Date:** 1641883628
**Score:** 2
**Tags:** c#, winforms, entity-framework
## Question Body
<p>This has stumped me for a few hours. I'm rewriting a Winforms desktop app to support an ASP.NET Core website. The app stores some tables locally in a LiteDB cache, and calls a &quot;using&quot; DBContext to get data.</p>
<p>The desktop app uses a <code>TaxAccount</code> abstract class, which is inherited by <code>Household</code> and <code>Business</code>.</p>
<p>On client search, the app calls GetAccount() to display a single user account. Since the DB can be slow, the cache is updated in the background. Here's the method.</p>
<pre class="lang-cs prettyprint-override"><code>
        /// &lt;summary&gt;
        /// Retrieve a single account from cache. Later, replace the account object with object from server.
        /// &lt;/summary&gt;
        /// &lt;param name=&quot;accountID&quot;&gt;&lt;/param&gt;
        /// &lt;returns&gt;&lt;/returns&gt;
        public TaxAccount GetAccount(int accountID)
        {
            var accounts = Cache.GetCollection&lt;TaxAccount&gt;();
            var account = accounts.FindById(accountID);

            if (GetSingleAccountTask == null || GetSingleAccountTask.IsCompleted)
            {
                GetSingleAccountTask = Task.Run(() =&gt; UpdateAccount(account));
            }

            return account;

            void UpdateAccount(TaxAccount account)
            {
                using (var serverContext = new ApplicationDbContext(ServerOptions))
                {
                    var found = serverContext.Accounts
                        .Include(X =&gt; X.Users)
                        .FirstOrDefault(X =&gt; X.Id == account.Id);

                    account = found;

                    if (found != null)
                    {
                        accounts.Update(found);
                    }
                    else
                    {
                        accounts.Delete(account.Id);
                    }

                }
            }
        }
</code></pre>
<p>I'd like to update single properties of the <code>TaxAccount</code> entity. To do so, I use <code>Attach(taxAccount)</code>, this ideally should update just the property I want.</p>
<pre class="lang-cs prettyprint-override"><code>        public void UpdatePrivateLink(TaxAccount taxAccount, string link)
        {
            // Retrieve collection from cache.
            var accounts = Cache.GetCollection&lt;TaxAccount&gt;();
            using (var serverContext = new ApplicationDbContext(ServerOptions))
            {
                // Attach taxAccount to server context.
                serverContext.Attach(taxAccount);
                taxAccount.PrivateFolderLink = link;
                // Update server.
                serverContext.SaveChanges();
                // Update cache.
                accounts.Update(taxAccount);
            }    
        }
</code></pre>
<p>This doesn't work. It creates a <code>System.InvalidOperationException</code> : <code>The instance of entity type 'Household' cannot be tracked because another instance with the key value '{Id: 1}' is already being tracked</code>. BUT I CAN'T FIND THE ENTITY.</p>
<p>Here's the list of things I've tried:</p>
<ul>
<li>changing the Get() query to .AsNoTracking() does nothing.</li>
<li>serverContext.ChangeTracker.Clear() does nothing.</li>
<li>serverContext.Entry(taxAccount) returns a state of EntityState.Detached</li>
<li>there is no metadata in serverContext.ChangeTracker.ToDebugString()</li>
<li>serverContext.Find(taxAccount.Id) makes a database hit</li>
<li>retrieving directly from the LiteDB cache using accounts.FindbyId(taxAccount.Id) creates the same error.</li>
</ul>
<p>What's worse, if I create a <code>new Household()</code> with the same id, then all of a sudden it does work!</p>
<pre class="lang-cs prettyprint-override"><code>var account = new Household() { Id = taxAccount.Id };
serverContext.Attach(account);
account.PrivateFolderLink = link;
serverContext.SaveChanges();

// Then we have to save in cache.
taxAccount.PrivateFolderLink = link;
accounts.Update(taxAccount);
</code></pre>
<p>This work-around makes no sense to me. Why does EF think <code>taxAccount</code> is tracked on a brand-new DbContext? Why can't I get rid of this tracking without creating a new object?</p>
<p>Would appreciate advice.</p>
<p>EDIT:</p>
<ul>
<li>serverContext.Accounts.Local contains no elements.</li>
</ul>
<p>EDIT:
This test is the simplest implementation that still fails.</p>
<pre class="lang-cs prettyprint-override"><code>
        public void AttachTest(int accountID, string link)
        {
            var accounts = Cache.GetCollection&lt;TaxAccount&gt;();
            var acct = accounts.FindById(accountID);

            using (var serverContext = new ApplicationDbContext(ServerOptions))
            {
                serverContext.Attach(acct);
                acct.PrivateFolderLink = link;
                serverContext.SaveChanges();
            }
        }
</code></pre>
<p>For full debugging: I'm testing on .NET 5.0 console app, the EF version is 5.0.13 hosted on a .NET Standard 2.1 library.</p>
<p>Here's the TaxAccount model I'm using.</p>
<pre class="lang-cs prettyprint-override"><code>    public abstract class TaxAccount
    {
        [Key]
        public int Id { get; set; }

        [MaxLength(200)]
        public string Name { get; set; }

        public bool Archived { get; set; } = false;
        public string PrivateFolderLink { get; set; }

        public List&lt;AppUser&gt; Users { get; set; }
    }

    public class Household : TaxAccount
    {
    }

    public class Business : TaxAccount
    {
        [EmailAddress, MaxLength(500)]
        public string Email { get; set; }
        [MaxLength(500)]
        public string Phone { get; set; }
        [MaxLength(1000)]
        public string Address { get; set; }
    }

</code></pre>
<p>In my ApplicationDbContext, the only <code>fluent</code> logic is to mark the discriminator.</p>
<pre class="lang-cs prettyprint-override"><code>            // Tax Account abstract class.
            builder.Entity&lt;TaxAccount&gt;().HasDiscriminator()
                .HasValue&lt;Household&gt;(nameof(Household))
                .HasValue&lt;Business&gt;(nameof(Business))
                .IsComplete(true);

            builder.Entity&lt;TaxAccount&gt;()
                .Property(&quot;Discriminator&quot;)
                .HasMaxLength(50);
</code></pre>

## Answers
### Answer ID: 70671374
<p>After some experimenting this morning, I figured it out! Luckily, it has nothing to do with the cache or other DbContexts!</p>
<p>The class <code>TaxAccount</code> has an <code>List&lt;AppUser&gt;</code>, which has a property <code>Accounts</code>, which is an <code>List&lt;TaxAccount&gt;</code>. This many-to-many relationship is creating a cycle within the <code>Attach()</code> method that EF Core doesn't deal well with. To prove this, I wrote two tests, both of which worked!</p>
<pre class="lang-cs prettyprint-override"><code>public void AttachTest(int accountID, string link)
        {
            var accounts = Cache.GetCollection&lt;TaxAccount&gt;();
            var acct = accounts.FindById(accountID);
            // We set the Users relation to be null.
            acct.Users = null;

            using (var serverContext = new ApplicationDbContext(ServerOptions))
            {
                serverContext.Attach(acct);
                acct.PrivateFolderLink = link;
                serverContext.SaveChanges();
            }
        }
</code></pre>
<pre class="lang-cs prettyprint-override"><code>public void AttachTestNullUsers(int accountID, string link)
        {
            var accounts = Cache.GetCollection&lt;TaxAccount&gt;();
            var acct = accounts.FindById(accountID);
            // For each user, the Accounts is null, this also breaks the relationship.
            acct.Users.ForEach(X =&gt; X.Accounts = null);

            using (var serverContext ...
        }
</code></pre>
<p>Now, there's two follow-up questions to this:</p>
<ol>
<li>Is this better than creating a new instance of <code>TaxAccount</code> and attaching that?</li>
<li>How does this deal with <code>INSERT</code> and <code>UPDATE</code> operations for the many-to-many relationship?</li>
</ol>
<hr />
<ol>
<li><p>Probably not. Setting <code>acct.Users = null</code> is an unintended outcome, and it'll be easy to forget to restore that relationship once the command is done. OTOH, initializing a <code>new TaxAccount(taxAccount.Id)</code> is a light operation with no effects on the base object.</p>
</li>
<li><p>Poorly, after some testing, <code>Attach()</code> is not a good idea if you want add or remove many-to-many objects. Lookup then update is your best option here.</p>
</li>
</ol>

### Answer ID: 70662907
<h2>From the <a href="https://learn.microsoft.com/en-us/dotnet/api/microsoft.entityframeworkcore.dbcontext.update?view=efcore-5.0" rel="nofollow noreferrer">Microsoft Wiki:</a></h2>
<blockquote>
<p>Begins tracking the given entity and entries reachable from the given entity using &gt;the Modified state by default, but see below for cases when a different state will &gt;be used.</p>
<p>Generally, no database interaction will be performed until SaveChanges() is called.</p>
</blockquote>
<p>My guess is, that the Account is tracked until the changes are saved.</p>

