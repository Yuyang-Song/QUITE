# Prevent SQL query from hogging database resources. Set max usage?
[Link to question](https://stackoverflow.com/questions/32595154/prevent-sql-query-from-hogging-database-resources-set-max-usage)
**Creation Date:** 1442349330
**Score:** -2
**Tags:** c#, sql-server, stored-procedures
## Question Body
<p>We have a .NET application using ADO.NET and Entity Framework and a lot of legacy stored procedures. Occasionally an operation will bring the database server's CPU to 100% for seconds or even minutes. During this time no other operations can be executed against the database. There is some culprit code which is far too complex and business critical to be feasible refactoring in the short term, but this can also happen from newer code depending on the situation. </p>

<p>I would like to prevent any one SQL operation from taking 100% of the CPU, etc. Is there any way to configure MS SQL to provide no more than, say 20% of the CPU, to any one query? </p>

<p>I know that ideally we would rewrite the code to not be as intensive, but that is not feasible in the short term, so I'm looking for a general setting which ensure this can never happen.</p>

## Answers
### Answer ID: 32595304
<p>Take a look at the <a href="https://msdn.microsoft.com/en-us/library/bb933866.aspx" rel="nofollow">Resource Governor</a> (assuming you're using SQL 2008 or up). A good simple overview on usage <a href="http://blog.sqlauthority.com/2012/06/04/sql-server-simple-example-to-configure-resource-governor-introduction-to-resource-governor/" rel="nofollow">is here</a>.  Though it won't work necessarily on a specific query, using a reasonable classifier function will/should allow you to narrow it down pretty closely if you like.  I don't have 10 rep yet so I can only post 2 links, but if you google "Sql Server classifier function" you'll get some decent guidance.</p>

