# EF Core query for one-to-one relations using method syntax
[Link to question](https://stackoverflow.com/questions/76074603/ef-core-query-for-one-to-one-relations-using-method-syntax)
**Creation Date:** 1682090816
**Score:** 0
**Tags:** c#, entity-framework, linq, entity-framework-core, ef-core-3.1
## Question Body
<p>I have 3 tables <code>Applications</code>, <code>Systems</code>, <code>Databases</code>. System can have multiple applications but 0-1 databases. Because of Entity Framework database-first approach, there is no database property in our system class.</p>
<p>I have the following LINQ query (simplified) that works perfectly fine, creates join to databases table and retrieves version property:</p>
<pre><code>var query  = from app in ctx.Apps
             join sys in ctx.Systems on app.SystemId equals sys.SystemId
             join db in ctx.Databases on db.SystemId equals sys.SystemId into dbAt
             from dbAlias  in dbAt.DefaultIfEmpty()
             where ..
             select ApplicationDto {
              ...
               DatabaseVersion = (dbAlias == null ? null : dbAlias.Version)
              ...
              };
</code></pre>
<p>I am in the process of rewriting every query from Linq syntax to method syntax but this one seems impossible to figure out. I can't use <code>.IncludeThen(x =&gt; x.System.Database)</code> cause <code>System</code> doesn't have a <code>Database</code> property.</p>
<p>Is it possible to join on alias (<code>Database</code> type) that can be accessed in select as I did in LINQ? I don't want to add <code>Database</code> class to <code>System</code> because it will probably be removed after next run of</p>
<pre><code>dotnet ef dbcontext scaffold
</code></pre>

