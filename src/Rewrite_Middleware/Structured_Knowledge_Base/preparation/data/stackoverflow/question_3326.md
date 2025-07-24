# How to properly manage connection pooling with the managed driver of Oracle Data Provider for .NET
[Link to question](https://stackoverflow.com/questions/76409376/how-to-properly-manage-connection-pooling-with-the-managed-driver-of-oracle-data)
**Creation Date:** 1685992261
**Score:** 3
**Tags:** c#, .net, oracle-database, odp.net
## Question Body
<p>We have developped a .NET application with an Oracle 12c (12.1.0.4) database. It's a rewrite of an old app, so the database itself isn't new and haven't changed much for the rewrite. The new app is a .NET 6 application, with a frontend (Blazor WASM, not that it matters here) and a web API backend. The backend API expose a number of methods that typically access the database a few times to return and/or write some data. Pretty standard stuff.</p>
<p>We use the managed driver of the Oracle Data Provider for .NET (ODP.NET) to access the database, from the &quot;Oracle.ManagedDataAccess.Core&quot; Nuget package from Oracle, version 3.21.61. An API method will connect to the database only to execute a single query, or in some cases a few queries, so connections are short lived. Those queries aren't handling a lot of data, typically a handful of rows, nothing big.</p>
<p>We just deployed the new app last week, replacing the old one, and in a matter of minutes we ran into severe connection pooling problems, forcing us to shut down the app and investigate. Opening connections were failing, with the error message &quot;<em>Délai d'expiration de la demande de connexion mise en pool</em>&quot; (sorry for the french, it roughly translate to &quot;Timeout while pooling the opening of the connection&quot;, or something like that).</p>
<p>We checked our code, and at first glance noticed that the OracleCommand and OracleDataReader objects weren't disposed, so we fixed that. The OracleConnection were disposed correctly, though. Still, it didn't seemed to solve the issue (although we checked that in a testing environnement, with only us devs accessing the app). We ended up adding calls to ClearPool just before disposing of the connections, which feels wrong to me, as it looks to me like we're basically turning off connection pooling. This helps a lot, though, but we still got connections failure after a day, which led us to increase the size of the pool, from the default number of 100, to 200 and then 250. So far, it seems to hold at 250, but this is worrying.</p>
<p>Basically, according my estimates, we might have, at a given moment, only a dozens users or so, and they're likely not doing things that access the database at the exact same time. So, not a lot. Still, we somehow needed hundreds, and that despite agressively clearing the pool.</p>
<p>Here is a code sample from our app that make a connection to the database (this one is for an update query, so no data reading) :</p>
<pre><code>using (OracleConnection conn = new(_connectionString))
{
    conn.Open();
    OracleCommand cmd = conn.CreateCommand();
    cmd.CommandType = CommandType.Text;
    cmd.CommandText = requete;
    retour.NbEnregistrement = cmd.ExecuteNonQuery();
    cmd.Dispose();
    OracleConnection.ClearPool(conn);
}
</code></pre>
<p>This is essentially like the examples in <a href="https://docs.oracle.com/en/database/oracle/oracle-database/21/odpnt/intro.html" rel="nofollow noreferrer">Oracle's documentation</a>. We open a connection, create a command, use it, then dispose of the command and the connection.</p>
<p>It looks like connection pooling isn't working properly, or at least not the way I think it should. Then again, my understanding of how pooling works might be wrong. I did some tests with our DBA who was monitoring the development database, and we can see that connections do get reused, although not as often as I would expect. On the other hand, since we clear the pools, it shouldn't even be able to reuse connections at all to begin with.</p>
<p>What could be wrong? How come connection pooling is not doing its job, expecially given the low usage, and why was it necessary for us to use ClearPool, which seems to be something that should only be used in unusual cases?</p>

## Answers
### Answer ID: 76721114
<p>I had the same problem and solved it by closing the connection after my database request.</p>
<pre><code>if (conn.State == ConnectionState.Closed)
{
    conn.Open();
}

if (conn.State == ConnectionState.Open)
{
    var query = xxxxxx;
    conn.Close();
}
</code></pre>
<p>i don't really know if it's better to conn.close() or to ClearPool(conn)..</p>

### Answer ID: 76424160
<p>It turned out that there was one case where a OracleConnection wasn't disposed properly. So, the connections used in that context weren't released in the connection pool, and thus sooner or later the pool would reach the limit, no matter how high it was set. Since this was in the most used part of the app, it tended to happen quickly.</p>
<p>I fixed that, and now everything works fine.</p>

