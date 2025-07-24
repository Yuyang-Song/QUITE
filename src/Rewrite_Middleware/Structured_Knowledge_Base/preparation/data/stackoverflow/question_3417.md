# Changing the collation of a SQL Server / Azure database
[Link to question](https://stackoverflow.com/questions/79084462/changing-the-collation-of-a-sql-server-azure-database)
**Creation Date:** 1728866955
**Score:** 0
**Tags:** sql-server
## Question Body
<p>I have some test/prod databases in collation <code>Latin1_General_CI_AS</code>.</p>
<p>I have written a script to change one of the test databases for every char/nvarchar column in every table to <code>Latin1_General_100_CI_AS_SC_UTF8</code></p>
<p>This is to handle chinese data and also to allow mixed case to be found in SQL queries</p>
<p>I know I could change database collation but this would require doing a bacpac and changing the collation in the bacpac and then doing an import on the bacpac - on a 500GB prod db this isnt really an option. Also I would need to make the database collation <code>Latin1_General_100_CS_AS_SC_UTF8</code> - the difference being CS as every object would become case sensitive and our application would need a complete rewrite for every SQL query / object etc.</p>
<p>So back to my problem above, can I keep the db in <code>Latin1_General_CI_AS</code> and just keep all existing and create new string columns as <code>Latin1_General_100_CI_AS_SC_UTF8</code>.</p>

