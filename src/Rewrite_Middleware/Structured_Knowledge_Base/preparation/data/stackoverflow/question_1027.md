# Using the same linq when switching EF database
[Link to question](https://stackoverflow.com/questions/55651497/using-the-same-linq-when-switching-ef-database)
**Creation Date:** 1555071581
**Score:** 0
**Tags:** c#, .net, entity-framework, linq
## Question Body
<p>I have a SQLServer database that I access with Entity Framework and run LINQ Queries against. Done in C#. Works fine.</p>

<p>Next step, i would like to change the Connectionstring, so it points to a second database with exactly the same structure and run the LINQ queries. </p>

<p>C# -> LINQ  being strongly typed, does not resolve and compile. </p>

<p>I have tried creating a dbContext object, provided a connectionstring, but the LINQ objects (Tablenames) does not resolve.</p>

<p>I have tried a switch statement to switch between contexts.</p>

<p>I have tried "DaContext.Database.ExecuteSqlCommand", but this it not an option, as I have to rewrite all LINQ to use basic SQL.</p>

<p>What would be the best way to achieve this?</p>

<pre><code>DbContext DaContext;

// Here I changed the connectionstring dynamically
DaContext = new DbContext("HEADCOUNT_NEW_Entities");

// Here I tried a switch statement
switch (APPLICATION_ID)
{

case "HEADCOUNT_NEW":
    DaContext = new WebApplication7.Models.Db_Entities.HEADCOUNT_NEW_Entities();
    break;

case "POSTS_NEW":
    DaContext = new WebApplication7.Models.Db_Entities.POSTS_NEWEntities();
    break; 

// way more Databases to add here, same structure

}

DaContext.Database.ExecuteSqlCommand ("exactly not what i want to do..........");

// This does not resolve the TABS table in LINQ
var jsonData = DaContext.TABS
.Select(c =&gt; new { c.TAB_CONTENT, c.TABLE_NAME, c.SORT_SEQUENCE, c.LEVELS })
.Distinct()
.OrderBy(c =&gt; c.SORT_SEQUENCE)
.ToList();

// More LINQ to follow...
</code></pre>

<p>Expecting a user to log in, use different EF database, with the same LINQ.</p>

<p>Any pointers appreciated.</p>

## Answers
### Answer ID: 55651951
<p>You've created two different DB Contexts:</p>

<ul>
<li><code>WebApplication7.Models.Db_Entities.HEADCOUNT_NEW_Entities</code></li>
<li><code>WebApplication7.Models.Db_Entities.POSTS_NEWEntities</code></li>
</ul>

<p>Code which operates on one won't work on the other, because they're different, with their own different sets of entities.  Additionally, you're not even using those contexts but are trying to use the base <code>DbContext</code> type from the framework, which has <em>no</em> sets of entities:</p>

<pre><code>DbContext DaContext;
</code></pre>

<p>Get rid of one of the DB Contexts and all of its entities.  You don't need to duplicate the code at all.  Just use the context that matches your DB schema.  For example:</p>

<pre><code>var daContext = new WebApplication7.Models.Db_Entities.HEADCOUNT_NEW_Entities();
// now you can query the entity sets on daContext
</code></pre>

<p>Once you have that, circle back to the original task:</p>

<blockquote>
  <p>i would like to change the Connectionstring, so it points to a second database with exactly the same structure</p>
</blockquote>

<p>The connection string is in the configuration, not the code.  Don't change <em>any code</em>.  Just update the connection string in the application's configuration.  For example, in a <code>.config</code> file:</p>

<pre><code>&lt;configuration&gt;
  &lt;connectionStrings&gt;
    &lt;add name="HEADCOUNT_NEW_Entities" connectionString="CONNECTION STRING GOES HERE" providerName="System.Data.SqlClient" /&gt;
  &lt;/connectionStrings&gt;
&lt;/configuration&gt;
</code></pre>

<p>Or in a <code>.json</code> file:</p>

<pre><code>{
  "ConnectionStrings": {
    "HEADCOUNT_NEW_Entities": "CONNECTION STRING GOES HERE"
  }
}
</code></pre>

<p>Pointing to a different database instance with the same schema is a configuration change, not a code change.</p>

