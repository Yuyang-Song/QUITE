# Using keywords async/await in database queries
[Link to question](https://stackoverflow.com/questions/21358098/using-keywords-async-await-in-database-queries)
**Creation Date:** 1390696075
**Score:** 0
**Tags:** c#, windows-phone-7, windows-phone-8, thread-safety, async-await
## Question Body
<p>I have a local database in <code>Windows Phone 8</code> app. The app includes a lot of queries to the database and I don't want bad effect on the responsiveness of UI.</p>

<p>For example I have a table of users and method to get a user from database by id. </p>

<p><strong>Current variant</strong></p>

<pre><code>public class CacheDataContext : DataContext
{
    public static string DBConnectionString = "Data Source=isostore:/Cache.sdf";

    public CacheDataContext(string connectionString)
            : base(connectionString) { }

    public static AutoResetEvent OperationOnDatabaseUser = new AutoResetEvent(true);

    public Table&lt;User&gt; UserItems;
}

public class CacheDataContextUser : CacheDataContext
{
    public CacheDataContextUser(string connectionString)
        : base(connectionString) { }

    public User GetUser(string id)
    {
        try
        {
            OperationOnDatabaseUser.WaitOne();
            using (CacheDataContext context = new CacheDataContext(DBConnectionString))
            {
                //find user in the data base and return 
            }
        }
        finally
        {
            OperationOnDatabaseUser.Set();
        }
    }
}
</code></pre>

<p>I need ensure safety of the data if at the same time on database allow different requests to add, update, delete data. For this I use <code>AutoResetEvent</code>. Not sure what I'm doing it right, but so far no problems.</p>

<p>I can get user from the database:</p>

<pre><code>using (DataBaseUser = new CacheDataContextFriends(ConnectionString))
{
   var user = DataBaseUser.GetUser(id);
}
</code></pre>

<p><strong>Async/await</strong></p>

<p>But I want work with the database using keywords async/await.</p>

<pre><code>public class CacheDataContextUser : CacheDataContext
{
    public CacheDataContextUser(string connectionString)
        : base(connectionString) { }

    private object threadLock = new object();

    public Task&lt;User&gt; GetUser(string id)
    {       
        using (CacheDataContext context = new CacheDataContext(DBConnectionString))
        {
            var result = await Task&lt;User&gt;.Factory.StartNew(() =&gt;
                {
                    lock (threadLock)
                    {
                       //find user in the data base and return  
                    }                  
                });
            return result;          
        }       
    }
}
</code></pre>

<p>I'm afraid to rewrite the method as described above, because I'm not sure it's right. Please tell me what the problem may be. My main goal is to improve the responsiveness of the app.</p>

## Answers
### Answer ID: 21359558
<p>First, <code>AutoResetEvent</code> is the wrong thing to use for exclusive access. In Windows, an "event" like this is a message from one thread to another; in this case, you just want a simple lock:</p>

<pre><code>public class CacheDataContext : DataContext
{
  public static string DBConnectionString = "Data Source=isostore:/Cache.sdf";

  public CacheDataContext(string connectionString)
        : base(connectionString) { }

  protected static readonly object OperationOnDatabaseUser = new object();

  public Table&lt;User&gt; UserItems;
}

public class CacheDataContextUser : CacheDataContext
{
  public CacheDataContextUser(string connectionString)
    : base(connectionString) { }

  public User GetUser(string id)
  {
    lock (OperationOnDatabaseUser)
    {
        using (CacheDataContext context = new CacheDataContext(DBConnectionString))
        {
            //find user in the data base and return 
        }
    }
  }
}
</code></pre>

<p>If you want to improve your responsiveness, then call your data context methods using <code>Task.Run</code>, i.e.:</p>

<pre><code>var user = await Task.Run(() =&gt; GetUser(id));
</code></pre>

<p>Do not expose asynchronous methods on your data context unless the actual database access is asynchronous (i.e., using EF6, <em>not</em> <code>Task.Run</code>).</p>

