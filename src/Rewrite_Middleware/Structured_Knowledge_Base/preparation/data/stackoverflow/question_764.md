# Obtain SQL insert statements from Database Initializer seed method
[Link to question](https://stackoverflow.com/questions/41348190/obtain-sql-insert-statements-from-database-initializer-seed-method)
**Creation Date:** 1482853967
**Score:** 1
**Tags:** c#, sql-server, entity-framework, seeding
## Question Body
<p>I have read this <a href="https://blog.oneunicorn.com/2013/05/28/database-initializer-and-migrations-seed-methods/" rel="nofollow noreferrer">blog</a>: which explains the difference between Database Initializer seeds and Migration seed methods.</p>

<p>I am working on a project, that uses code-first Entity Framework, with migrations enabled. A Database Initializer seed is present and it will execute on my local database, when the database is created. </p>

<p>But in the production environment, I do not have the rights to add databases myself. I need to run update-database -script from package manager console on an empty newly created database and then execute the migrations manually.</p>

<p>As I do not have direct access from my development environment to the production database server, I am thinking out loud: there is no gain in rewriting the Database Initializer to a Migrations Seed.</p>

<p><strong>How can I obtain the script (SQL), that is the insert statements, defined in the Database Initializer seed method?</strong></p>

<p>Of course I can :</p>

<ol>
<li>run update-database on an empty existing database. (no seed method is executed)</li>
<li>run update-database on a non-existing database. (seed method is executed)</li>
</ol>

<p>Do a SQL compare between the 2 databases and get the INSERT queries that way.</p>

<p>But there should be an easier way right?</p>

<p>Why does the <code>update-database -script</code> not show the INSERT statements from the database initializer seed method in the first place?</p>

## Answers
### Answer ID: 41364151
<p>I am not sure if the logging described in <a href="https://msdn.microsoft.com/en-us/library/dn469464(v=vs.113).aspx" rel="nofollow noreferrer">Entity Framework Logging and Intercepting Database Operations</a> will catch the SQL from the DatabaseInitializer. If not you can try to find a 3rd party profiler to catch your SQL. Personally, I use <a href="http://ormprofiler.com/" rel="nofollow noreferrer" title="ORM Profiler">ORM Profiler</a> and it catches everything, however it is not free.</p>

<p>And yes, there should be an easier way.</p>

