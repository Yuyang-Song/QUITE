# How optimize application speed + Entity Framework?
[Link to question](https://stackoverflow.com/questions/13495407/how-optimize-application-speed-entity-framework)
**Creation Date:** 1353508115
**Score:** 0
**Tags:** c#, winforms, entity-framework, sql-server-ce
## Question Body
<p>I have a windows application with 11 database with about 1.5 Gb text information.</p>

<p>I use SQL Server CE and Entity Framework.</p>

<p>My application has been finished, but for new version my application, it must run from DVD. Every part of application has a separate database.</p>

<p>Everything is fine, but first query of each database take about 40 sec to run. I searched a lot about this and I found these solutions:</p>

<ol>
<li>pre-generate views to avoid the first time performance</li>
<li>get rid of linq, and rewrite it in ADO.NET</li>
<li>start by profiling the SQL commands actually issued by Entity Framework</li>
</ol>

<p>and ...</p>

<p>I want to ask witch is the best way and fastest to do?</p>

