# Rewrite a UNION view as a dynamic view
[Link to question](https://stackoverflow.com/questions/4997368/rewrite-a-union-view-as-a-dynamic-view)
**Creation Date:** 1297718215
**Score:** 2
**Tags:** sql-server, dynamic, view, union
## Question Body
<p>I've been working on this for days and I can't find a proper solution, I'm hoping someone can help.</p>

<p>We have several database servers (SQL Server) with identical structures, connected by linked servers.  We have a bunch of views that union data across all the servers:</p>

<pre><code>CREATE VIEW Things_view AS
  SELECT id, thing
    FROM server1.database1.dbo.stuff
  UNION ALL
  SELECT id, thing
    FROM server2.database2.dbo.stuff
  UNION ALL
  SELECT id, thing
    FROM server3.database3.dbo.stuff
</code></pre>

<p>There are several problems with this:</p>

<ul>
<li>When we add servers, we have to modify
views.</li>
<li>Our development environments need
the same number of databases and fake linked
servers so we can install these
views.</li>
<li>Some of the servers <em>do not
include</em> data from some of the other servers.  Today we do this with customized views on those servers but that's a deployment nightmare.</li>
</ul>

<p>So I was hoping to rewrite this dynamically.  The goals are:</p>

<ul>
<li>Allow development environments to
contain a different number of databases.  They are likely to
have 2 or more databases on a single server.</li>
<li>Provide a way for each server to
specify which other servers to
include in the results.</li>
<li>Minimize the complexity so the
solution remains somewhat
maintainable.</li>
<li>Create one solution that can be
source controlled and used on all
servers.</li>
</ul>

<p>And most importantly:</p>

<ul>
<li><strong>Expose it as a view with the same
name so we don't have to rewrite our
entire application.</strong></li>
</ul>

<p>Of course, I can't do dynamic SQL in a view or function.  I tried rewriting this as a stored procedure, then using the <a href="http://blogs.technet.com/b/wardpond/archive/2005/08/01/408502.aspx" rel="nofollow">OPENROWSET trick</a> to query the stored proc from a view.  That didn't work because I had to fully qualify the proc with the database name, which would require more dynamic SQL (because the database names are different).  Then I thought about fooling around with synonyms on the master database but that violates the maintenance and source control goals.</p>

<p>I'm perfectly OK with creating a new table with server names and database names and inclusion flags if needed.  In fact, that is ideal because it centralizes the configuration for each environment.</p>

<p>I've been completely baffled by this and now I'm reaching out to you, Internet, in a last-ditch plea for help!</p>

## Answers
### Answer ID: 4997562
<p>This sounds like a job for a data warehouse... <a href="http://en.wikipedia.org/wiki/Data_warehouse" rel="nofollow">http://en.wikipedia.org/wiki/Data_warehouse</a>   You would need this to run at a set schedule so the data would not be realtime.  That is the only downside.</p>

<p>Load data from each <code>server[n].database.tablename</code> using a file similar to the one below. </p>

<pre><code>--Here is how you would administer the script.  One single script that you would only need to modify when you added/removed servers.
So you can easily add this to source control or whatever. You can also do all this, without linked servers, if you look at some ETL tools. like SSIS

insert into dataserver1.datawarehouse.tablename select *,'svr1,'db','tablename' from svr1.db.tablename
insert into dataserver1.datawarehouse.tablename select *,'svr2,'db','tablename' from svr1.db.tablename
insert into dataserver1.datawarehouse.tablename select *,'svr3,'db','tablename' from svr1.db.tablename
insert into dataserver1.datawarehouse.tablename select *,'svr4,'db','tablename' from svr1.db.tablename
insert into dataserver1.datawarehouse.tablename select *,'svr5,'db','tablename' from svr1.db.tablename
insert into dataserver1.datawarehouse.tablename select *,'svr6,'db','tablename' from svr1.db.tablename
insert into dataserver1.datawarehouse.tablename select *,'svr7,'db','tablename' from svr1.db.tablename
insert into dataserver1.datawarehouse.tablename select *,'svr8,'db','tablename' from svr1.db.tablename
</code></pre>

<p>So you are required to create many insert statements.  One for each server/db/table combo you have.</p>

<p><code>insert into dataserver1.datawarehouse.tablename select *,'svr1,'db','tablename' from svr1.db.tablename</code></p>

<p>So as you load the data into this new database table, you will simply append to every row the original servername/databasename/tablename SO.... Your data looks like this</p>

<pre><code>col1 col2 col3 srvnam dbname tbl
foo  bar  some MSSQL1 master mycooltable
foo  bar  some MSSQL2 other  mycooltable
</code></pre>

<p>Now, all you have to do is query off of one table,  it will be really fast, and clean.</p>

### Answer ID: 4997646
<p>Here is what I'd suggest. Create a table to store the configuration for each view on the particular server. 
Then write dynamic sql to create the view script based on those configurations. 
Then run the view script on the server. 
When you want to add a new server, add it to the configurationtable which could have a trigger to automatically recreate the scripts for the views that are being changed. Or have recreating scripts from the table and running them be a standard part of every deployment. </p>

### Answer ID: 4997470
<p>If you have a table keeping track of servers and databases you could build the view dynamically in a trigger on that table.</p>

<p>Look at this answer to another question. It suggests the same thing and has some sample code to alter a view definition in a trigger.</p>

<p><a href="https://stackoverflow.com/questions/4669369/dynamic-table-design-common-lookup-table-need-a-nice-query-to-get-the-values/4767474#4767474">Dynamic table design (common lookup table), need a nice query to get the values</a></p>

<p>It might work for you.</p>

### Answer ID: 4997433
<p>One possible solution is to create a stored procedure that adjusts the view.  For example (not tested):</p>

<pre><code>create procedure dbo.RecreateView
as
declare @sql varchar(max)

select @sql = IsNull(@sql + 'union all ','') +
              'select * from ' + name + '.dbo.YourView '
from   sys.databases
where  name like 'DbNamePrefix%'

set @sql = 'create view dbo.YourView as ' + @sql
exec (@sql)
</code></pre>

<p>You could then call the stored procedure after you add a database, or even from a scheduled task.</p>

### Answer ID: 4997396
<p>Using <strong>Synonym</strong> would be a good option if you are using latest SQL server</p>

