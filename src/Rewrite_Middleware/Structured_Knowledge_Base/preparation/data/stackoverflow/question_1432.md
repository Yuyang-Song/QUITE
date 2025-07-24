# Issue on migrating from .NET Core 2.2 to .NET 6
[Link to question](https://stackoverflow.com/questions/76279707/issue-on-migrating-from-net-core-2-2-to-net-6)
**Creation Date:** 1684404285
**Score:** -1
**Tags:** c#, sql-server, entity-framework, .net-6.0, asp.net-core-2.0
## Question Body
<p>I recently migrated my app from .NET Core 2.2  to .NET 6 and upgraded the C# language from C#8 to C#10.</p>
<p>The app uses SQL Server and it's based on database first.</p>
<p>After migration, I noticed 2 changes:</p>
<ol>
<li><p>Entity Framework database first changes column mapping (column's names), Example:</p>
<ul>
<li>The column name in the database: &quot;Topic_Id&quot;,</li>
<li>The column name in the entity will change to: &quot;TopicId&quot; (Removing &quot;_&quot;):</li>
</ul>
<p>Is there a way that I have the exact column name in both the SQL server and Entity Framework?</p>
<p>Please note I am generating the Entity using Scaffold-DbContext:</p>
<blockquote>
<p>PM&gt; Scaffold-DbContext &quot;Server=(servername);Database=(dbname);MultipleActiveResultSets=true;User ID=usr;Password=pass&quot; Microsoft.EntityFrameworkCore.SqlServer -OutputDir Data/DB -force</p>
</blockquote>
</li>
<li><p>After moving to the .NET 6, I need to rewrite my queries - I need to convert them to IEnumerable.</p>
<p>Is there a way that I avoid rewriting all queries?</p>
<ul>
<li><p>In .NET Core 2.2:</p>
<pre><code>db.TblUserCredential UserCredential = this.DbContext.TblUserCredential
   .Where(x =&gt; x.CredentialTypeNavigation.Code.ToLower().Contains(&quot;kingsid&quot;))
   .FirstOrDefault(x=&gt; x.Identifier.Equals(identifier, StringComparison.OrdinalIgnoreCase));
</code></pre>
</li>
<li><p>In .NET 6:</p>
<pre><code>db.TblUserCredential? UserCredential = ((IEnumerable&lt;db.TblUserCredential&gt;)this.DbContext.TblUserCredentials.Include(x =&gt; x.CredentialTypeNavigation))
  .Where(x =&gt; x.CredentialTypeNavigation.Code != null &amp;&amp; x.CredentialTypeNavigation.Code.ToLower().Contains(&quot;kingsid&quot;))
  .FirstOrDefault(x =&gt; x.Identifier != null &amp;&amp; x.Identifier.Equals(identifier, StringComparison.OrdinalIgnoreCase));         
</code></pre>
</li>
</ul>
</li>
</ol>
<p>am I missing anything? Any help would be appreciated</p>

## Answers
### Answer ID: 76280895
<blockquote>
<p>Example: The column name in the database: &quot;Topic_Id&quot;, The column name in the entity will change to: &quot;TopicId&quot; (Removing &quot;_&quot;):</p>
</blockquote>
<p>Try specifying <code>-UseDatabaseNames</code> (or <code>--use-database-names</code> for .NET CLI) in the scaffold command - check out <a href="https://learn.microsoft.com/en-us/ef/core/managing-schemas/scaffolding/?tabs=dotnet-core-cli#preserving-database-names" rel="nofollow noreferrer">Preserving database names</a> section of the <code>scaffold</code> docs.</p>
<blockquote>
<p>Is there a way that I avoid rewriting all queries?</p>
</blockquote>
<p>No. EF Core in 2nd  version had a nasty little feature which was enabled by default - automatic client side evaluation for queries which it could not translate (i.e. it would silently fetch potentially excessive data and perform the rest of operations at the client-side). The following <a href="https://learn.microsoft.com/en-us/ef/core/what-is-new/ef-core-3.x/breaking-changes#linq-queries-are-no-longer-evaluated-on-the-client" rel="nofollow noreferrer">breaking change</a> in EF Core 3 removed this feature and the only option to trigger client side evaluation is to convert query to <code>IEnumerable</code> (for example using <code>AsENumerable</code>). I highly recommend you to investigate the queries and rewrite them in a way so the can be translated completely.</p>

