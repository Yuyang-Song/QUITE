# Encountering ObjectDisposedException when trying to read from SQLiteDataReader
[Link to question](https://stackoverflow.com/questions/32321466/encountering-objectdisposedexception-when-trying-to-read-from-sqlitedatareader)
**Creation Date:** 1441064230
**Score:** 0
**Tags:** c#, sqlite
## Question Body
<p>I am trying to read through a stored <code>SQLiteDataReader</code> object. In theory, it "should" work because the object is stored in a variable before it is referenced (and doesn't hit an error until the reference line is reached), but maybe I have the wrong idea.</p>

<p>I'm trying to keep my application in a neatly layered architecture. So, each database table having its own C# class with its own methods for select, insert, update, and delete; only the data layer knows how to communicate with the database, etc.</p>

<p>I was running into connection issues earlier when I tried to make one static <code>SQLiteConnection</code> object that all the data layer classes could reference (so as to keep it open and minimize overhead, if any). So I'm trying to go with the <code>using</code> block to make sure the connection is properly disposed each time I need to access the database, and hoping that this won't cause performance issues.</p>

<p>So basically, here is the method in my <code>DatabaseConnection</code> class that handles basic query execution:</p>

<pre><code>public SQLiteDataReader ExecuteQuery(string sql)
{
    SQLiteDataReader rdr = null;
    using(SQLiteConnection conn = new SQLiteConnection(ConnectionString))
    {
        conn.Open();
        SQLiteCommand cmd = conn.CreateCommand();
        cmd.CommandText = sql;
        rdr = cmd.ExecuteReader();
    }
    return rdr;
}
</code></pre>

<p>And here is the code that calls that method. I'll use an object/record of the <code>Associate</code> table as an example.</p>

<pre><code>public class Associate
{
    public int RowId { get; private set; }
    public int Id { get; set; }
    public string Name { get; set; }

    private string password;
    public string Password
    {
        get
        {
            return password;
        }
        set
        {
            password = Hash(value); // external password hashing method
        }
    }

    public Associate() { } // default constructor with default values

    public Associate(int id)
    {
        this.Id = id;
        Select();
    }

    // select, insert, update, delete methods
    private void Select() { ... }

    // these are non-queries and return true/false based on success
    public bool Insert() { ... }
    public bool Update() { ... }
    public bool Delete() { ... }

    /* Method that causes the error */
    public static Associate[] GetAll()
    {
        DatabaseConnection con = new DatabaseConnection();
        SQLiteDataReader rdr = con.ExecuteQuery("SELECT id FROM Associate");

        List&lt;Associate&gt; list = new List&lt;Associate&gt;();

        if (rdr != null)
        {
            while (rdr.Read()) /* this line throws the exception */
            {
                int next = rdr.GetInt32(0);
                list.Add(new Associate(next));
            }
        }

        return list.ToArray();
    }
}
</code></pre>

<p>The idea here is that using the <code>rdr</code> object, I can access the column names directly so that if the database ever changes, I won't have to rewrite a bunch of code to adjust for the column indices (<code>rdr["id"]</code>, <code>rdr["name"]</code>, etc.)</p>

<p>So what I don't understand is why <code>rdr</code> in the calling method is having "object disposed" issues because it's stored in a variable before I reference it. I know the connection is disposed at the end of the called method, but since the returned result is stored, shouldn't it technically be able to "survive" outside the <code>using</code> block?</p>

## Answers
### Answer ID: 32321547
<p>It is the connection that got disposed. The data reader can only read data while the connection still exists.</p>

<pre><code>public SQLiteDataReader ExecuteQuery(string sql)
{
    SQLiteDataReader rdr = null;
    using(SQLiteConnection conn = new SQLiteConnection(ConnectionString))
    {
        conn.Open();
        SQLiteCommand cmd = conn.CreateCommand();
        cmd.CommandText = sql;
        rdr = cmd.ExecuteReader();
    }
    // *** Connection gone at this stage ***
    return rdr;
}
</code></pre>

<p>Your options are to either return a DataTable, e.g.</p>

<pre><code>public DataTable ExecuteQuery(string sql)
{
    SQLiteDataReader rdr = null;
    using(SQLiteConnection conn = new SQLiteConnection(ConnectionString))
    {
        conn.Open();
        SQLiteCommand cmd = conn.CreateCommand();
        cmd.CommandText = sql;
        rdr = cmd.ExecuteReader();

        var dataTable = new DataTable();
        dataTable.Load(rdr);
        return dataTable;
    }
}
</code></pre>

<p>otherwise, you could keep the connection alive inside the DatabaseConnection class:</p>

<pre><code>class DatabaseConnection : IDisposable
{
    private readonly IDbConnection _conn;

    public DatabaseConnection() 
    {
       _conn = new SQLiteConnection(ConnectionString);
    }

    public void Dispose()
    {
       _conn.Dispose();
    }

    public SQLDataReader ExecuteQuery(string sql) 
    {
        ...
    }
}

// sample usage
using (var conn = new DatabaseConnection())
{
   using (var reader = conn.ExecuteQuery("SELECT ...")
   {
       // do your work in here
   }
}
</code></pre>

