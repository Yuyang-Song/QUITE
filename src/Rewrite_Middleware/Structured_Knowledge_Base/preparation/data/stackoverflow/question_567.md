# What is a good lightweight ORM for our needs?
[Link to question](https://stackoverflow.com/questions/3188299/what-is-a-good-lightweight-orm-for-our-needs)
**Creation Date:** 1278434459
**Score:** 3
**Tags:** .net, asp.net, sql-server, orm
## Question Body
<p>Ok I know "what X should I use" is very broad so let me narrow down our usage scenario. Basically, we should have been using an ORM a long time ago. Now though there is no way we can go through and rewrite every line of generated SQL Queries in our C# code. But we want to at least take a few steps in the right direction. So when we write new code(and in free time with refactoring) we want to convert over to some sort of ORM. </p>

<p>What would be a good ORM for this purpose? We are using .Net 3.5 and ASP.Net(webforms). There is nothing insanely complex about our database except for a few tables have a "dynamic" schema. We have a numerous amount of views(not used by the web application much though) and we have/use very few stored procedures. Our database is SQL Server 2005. Our price range is as cheap as possible and open source is preferred. This is a proprietary project however so we can't use a GPL library and such. </p>

<p>About the dynamic schema: Basically in some instances a column(of varying types) can be added or removed to certain tables. </p>

<p>And our view usage is almost non-existent and we could always take out the stored procedure code.. I believe there is only 2 or 3 in the database. </p>

## Answers
### Answer ID: 3188323
<p>I would say that for .NET 3.5 you could use LINQ to SQL which is free, supports Views and Stored Procedures, and has a small learning curve. The only thing I think you'd run in to trouble trying to use would be your &quot;dynamic schema&quot; tables (which you might want to elaborate on).</p>
<p>Another Open Source alternative would be <a href="https://nhibernate.info" rel="nofollow noreferrer">nHibernate</a> which is a great ORM, but has a much steeper learning curve in my opinion.</p>

### Answer ID: 3188373
<p>I would second Justin on suggesting Linq-to-SQL - it's really not dead! </p>

<p>If that's not your choice, or if you need to go against something like SQLite, you should definitely also check out <a href="http://subsonic.github.io/" rel="nofollow noreferrer">Subsonic 3.0</a> - lightweight, easy to use, free, with source - you name it.</p>

### Answer ID: 12443284
<p>I enjoy using <a href="http://www.subsonicproject.com/" rel="nofollow">SubSonic</a> for easy data access it generates classes using T4 so it really easy to change what is being generated. Its more of an active record style data access then a true ORM like nHibernate but linq to sql isn't a true ORM either. </p>

### Answer ID: 5348375
<p>Massive - <a href="https://github.com/robconery/massive" rel="noreferrer">https://github.com/robconery/massive</a></p>

<p>or </p>

<p>PetaPoco - <a href="https://github.com/toptensoftware/petapoco" rel="noreferrer">https://github.com/toptensoftware/petapoco</a> </p>

<p>Both are single .cs files with no dependencies except what's in the GAC.</p>

<p>(full disclosure, PetaPoco is something I wrote)</p>

