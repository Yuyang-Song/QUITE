# DB advice and best practices for ASP.NET based web site?
[Link to question](https://stackoverflow.com/questions/7411698/db-advice-and-best-practices-for-asp-net-based-web-site)
**Creation Date:** 1315978465
**Score:** 1
**Tags:** asp.net, mysql, database, linq, entity-framework
## Question Body
<p>I have a web site I developed for displaying the results of some data analysis work I did.  It relied on ASP.NET for the front end and connected to a MySQL back end utilising Entity Framework and LINQ extensively.</p>

<p>I chose MySQL because I personally have used it in the past and like the database, but this resulted in some serious issues when I had to deploy it to a hosting provider (incompatible connectors, access rights, etc.)</p>

<p>I am now getting ready to redevelop and expand the site and I am looking for some advice to avoid the issues I had last time.</p>

<p>The new DB has to serve two roles.  The first is to be a data provider for the charts that are the output of the analysis work.  These tables are straightforward, almost flat files, with 10 tables.  One table has roughly 200k rows of data the rest have aprox 1200 rows of data each.  There are little references or queries between the DB tables, but there are a few.  This data is updated periodically by a back end process and does not need to be added to or edited by the user.</p>

<p>The second role of the DB would be as a basic persistent store for a standard user management system.  It would need to manage data for adding/ removing clients, user names, passwords, access rights. etc.  No financial data or super secure data is involved.</p>

<p>What database approach would you recommend that would give me easy deployment and management at a web host and still allow me to use both Entity Framework and LINQ effectively.</p>

<p>Second, what tools/frameworks should I consider as I rewrite this system.  It is very graphical and data focused.  Presentation of charts and information is the key factor in this site. Are there any new technologies or frameworks that would add specific value to what I am doing? </p>

<p>A few notes.  I am a one man shop and I maintain the entire system myself so I am less worried about enterprise level frameworks than other people.  My focus is on the easy development and deployment of the site.  Maintainability is also a key factor.</p>

<p>I am also an experienced C# developer, but new to ASP.NET and the web side of things.  The first version of this site was a big learning experience.  It was good, but I wasted an enormous amount of time on just understanding new technologies and approaches.  I am very open to learning, but I can't afford the time to get my head around a complete paradigm shift.</p>

<p>I am looking forward to your thoughts, thanks.</p>

<p>Doug</p>

## Answers
### Answer ID: 7411819
<p>The natural choice would be SQL Server. I'd guess by your description that you are way under the maximum space limit of the SQL Server Express edition. I of course supports Entity Framework and the drivers are part of the .NET Framework, so no problem with third party assemblies here.</p>

<p>This will also open up the possibility to host your app in the cloud (Azure) later on, because SQL Azure in fact is a Microsoft SQL Server, so there is no overhead in supporting that.</p>

<p>Regarding user management - ASP.NET has this all build in (Membership, Role and Profile provider) and also a SQL Provider for which default tables are available. So you don't have to design your tables by yourself and it runs very naturally on SQL Server.</p>

