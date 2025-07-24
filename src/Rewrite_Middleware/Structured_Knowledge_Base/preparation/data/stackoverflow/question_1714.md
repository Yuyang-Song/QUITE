# writing SQL queries - methods to write complicated ones!
[Link to question](https://stackoverflow.com/questions/4809938/writing-sql-queries-methods-to-write-complicated-ones)
**Creation Date:** 1296075451
**Score:** 1
**Tags:** c#, mysql, visual-studio
## Question Body
<p>Hey guys, does anyone have any suggestions that might help with the following?</p>

<p>I am rewriting some software, which I did for a prototype for where I work, I am turning it into a more OOP compliant program :)</p>

<p>I have just written a custom database handler class to deal with my connections, my queries etc. The idea is that this database handler does everything needed to deal with the DB and only returns the result set of the query being run.</p>

<p>Anyways, I have just written a few methods which write my SQL queries for me - the idea being that I pass it some arguments in the form of an Array and the class writes the SQL String needed to query, which removes SQL injection problems. </p>

<p>The problem I have is; with normal selects (with where arguments and order/group by ) and insert and update, These all work fine. But if I want to pass a query which might have a join, or a multi-table join or a where-clause that contains a like or a sub select on the where (this one might be doable with running the select method twice!) </p>

<p>I can't work out how to get the method to produce these queries. Does anyone have any suggestions? - Might have to build custom ones where there is no way around not writing the query myself.</p>

<p>The other idea is over complicating things and to just perform a call that removes slashes contained in the passed string.</p>

<p>Thanks in advance, </p>

<p>vade</p>

<p>btw if it doesnt make much sense, been coding since 7 this morning, brain dying slowly! :)T</p>

## Answers
### Answer ID: 4810155
<p>If you have the option on the table you could look into doing a LINQ to SQL datalayer. That will let you work with your tables and query results as classes. </p>

<p>Its very easy to get started making a .dbml of your database, <a href="http://msdn.microsoft.com/en-us/library/bb386940%28v=vs.90%29.aspx" rel="nofollow">check out a walk through on MSDN</a></p>

<p>It also leaves the dynamic SQL authoring to the MS Language team, so thats nice.</p>

### Answer ID: 4810125
<p>If you need a complex query-building mechanism, consider one of the many ORM frameworks already developed, such as NHibernate or MSEF. These allow you to create some pretty complex queries using Linq (compiler-checked; gotta love it) that then are translated to SQL.</p>

### Answer ID: 4809973
<p>I would encourage you to consider writing <a href="http://dev.mysql.com/doc/refman/5.0/en/stored-routines.html" rel="nofollow">stored procedures</a> for the functionality you need rather than trying to write some kind of generic query building mechanism.</p>

### Answer ID: 4809967
<p>You could just use sqlcommand with parameters instead <a href="http://www.csharp-station.com/Tutorials/AdoDotNet/Lesson06.aspx" rel="nofollow">http://www.csharp-station.com/Tutorials/AdoDotNet/Lesson06.aspx</a></p>

