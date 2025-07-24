# Does having a lot of tables degrade performance?
[Link to question](https://stackoverflow.com/questions/41855634/does-having-a-lot-of-tables-degrade-performance)
**Creation Date:** 1485358713
**Score:** 3
**Tags:** sql-server
## Question Body
<p>We import a huge amount of data weekly from our clients and append it to an internal table in our SQL Server database. We have a manager who believes it's easier and more expedient to create (and hopefully, delete) temporary tables for certain reports we run each week from this data.</p>

<p>(We do something like this--way oversimplified: select records from this main table of customers who owe a dollar or more and are over 21, and we send them bills; then select records for customers who owe less than a dollar and are under 21, and the latter records are then matched to some other table on some join before we send them bills. Current process dumps each of those sets of selected records into separate temporary tables for that week, and after the bills are sent those tables are supposed to be deleted. A bad way to do things, I know...you don't have to tell me that!)</p>

<p>My view is that everything should go into one table, using a column that flags which week's data it is, and just keep the data there and run queries off it using that column's value as a criteria. Or else delete just those records after they are used for the week's reports.</p>

<p><strong><em>NOW....</em></strong></p>

<p>My whole point of asking is this:</p>

<p>Does having a ton of extra (unnecessary) tables slow down database performance?</p>

<p>Or does it just waste disk space and look like a mess when you have to scroll through hundreds of old tables in the SQL Server Management Studio Object Explorer window, but it doesn't really hurt performance?</p>

<p>I'm trying to provide justification to this manager for why we should scrap the routines that make all these temp tables and rewrite it to just select everything from the one main table. It may be a bit of work to redo things, but once it's done it should be more efficient and easier to maintain, etc.</p>

## Answers
### Answer ID: 42001986
<p>I would say you use views for your reports instead of external tables. This way if "source data" needs to be modified or corrected your reports reflect it.</p>

<p>On the disk space, each table is written in it's own file, with its own index file. Table contents that is too big to fit into it(like nvarchar(max)) will be stored in their own file.</p>

<p>Luckely, the database manager(sql server) manages the files for you, so no worries there.</p>

<p>for "big data" assessments it's critical to have as pure as possible input data. So flagging it with a date when created allows you to easely select data that has been made in a certain time period.</p>

<p>Another option is you make a stored procedure that fills a temporary database or a in memory database and returns that, so you can perform a select query on that limited set that is returned.
Sql server will still make files at certain dataset sizes because it's more efficient, but that will clean itself up after you're done.</p>

<p>I would never work with weekly datasets in temp tables.
The only thing I would consider with really really big datasets is making yearly seperate tables, so the indexes can be iterated rather quickly, and a union is relatively cheap if you need multi year statements.</p>

<p>So, to answer your question: 
multiple tables doesn't hamper performance. But, it does developer flexibility and database maintenance, increasing personell cost incrementally. There are better more future proof alternatives.</p>

### Answer ID: 41856269
<p><em>Does having a ton of extra (unnecessary) tables slow down database performance?</em></p>

<p>No. Unless we are talking about zillions of tables I have never seen a performance issue in having too many tables.</p>

<p><em>Or does it just waste disk space and look like a mess when you have to scroll through hundreds of old tables in the SQL Server Management Studio Object Explorer window, but it doesn't really hurt performance?</em></p>

<p>It a preference thing really. It does look like a mess but doesn't really hurt performances.</p>

<p>Now the question is really : Does the effort of cleaning all this worth the time saved in productivity and aggravation of working in this spaghetti ?</p>

