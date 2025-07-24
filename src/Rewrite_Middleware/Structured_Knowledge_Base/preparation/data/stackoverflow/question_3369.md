# Error when translating a query to a field of type &quot;inet&quot; in postgreSql via linq and EF Core
[Link to question](https://stackoverflow.com/questions/77617010/error-when-translating-a-query-to-a-field-of-type-inet-in-postgresql-via-linq)
**Creation Date:** 1701908217
**Score:** 0
**Tags:** entity-framework-core, npgsql
## Question Body
<p>I have an Entity class that contains a property Ipaddr of type <code>IPAddress</code>. It is stored in the postgresql database in a field of type <code>inet</code>, as intended. To search by part of a substring I use a method like this:</p>
<pre><code>public async Task&lt;IEnumerable&lt;Switch&gt;&gt; GetSwitches(string? searchIpaddr, string? searchSysname)
{
           var switches = context.Switches.Include(s =&gt; s.Network) as IQueryable&lt;Switch&gt;;

           if (!string.IsNullOrWhiteSpace(searchSysname))
            {
              searchSysname = searchSysname.Trim();
              switches = switches.Where(s =&gt; EF.Functions.ILike(s.Sysname, $&quot;%{searchSysname}%&quot;));
            }


           if (!string.IsNullOrWhiteSpace(searchIpaddr))
            {
              searchIpaddr = searchIpaddr.Trim();
              switches = switches.Where(s =&gt; EF.Functions.ILike(s.Ipaddr.ToString(), $&quot;%{searchIpaddr}%&quot;));
            }
        
            return await switches.ToListAsync(); 
            

}
</code></pre>
<p>For string property <code>Sysname</code> it works, but for <code>Ipaddr</code> an error occurs</p>
<blockquote>
<p>System.InvalidOperationException: The LINQ expression 'DbSet() .Where(s =&gt; s.Ipaddr.ToString() == __ip_0)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.</p>
</blockquote>
<p>Please tell me how to rewrite the code so that Linq can broadcast a query to the database. I don’t want to get the entire collection and then filter it on the client side, since there can be a lot of data.</p>

