# Writing Legacy asp application in asp.net
[Link to question](https://stackoverflow.com/questions/3126377/writing-legacy-asp-application-in-asp-net)
**Creation Date:** 1277612512
**Score:** 0
**Tags:** asp.net, asp-classic, reporting, infragistics
## Question Body
<p>I need help in choosing the right path while trying to rewrite a legacy application. Just a little bit of oversight, the current application is a web reporting tool in which the columns and the query texts are read from database. Users will filter and hit on a button “Create”, then the report will be displayed on an html page. For performance reasons, the maximum limit is 1000 rows, for a result more than that, the application will export to Excel.</p>

<p>The new requirement is to rewrite the same application in asp.net/Silverlight with a new look and feel and pretty much the same functionality (More number of reports). What is important is the client wants the reports to be displayed in a kind of DataGrid (with Sorting and Grouping capability) and he wants to increase the 1000 row limitation. In addition, he doesn’t want the Paging (he wants to scroll down the rows and analyze the data instead of punching too many pages).</p>

<p>What do you suggest that I should choose? Silverlight or Asp.net? Is there any reporting framework that you guys know? What about crystal reports? Any suggestion to produce an attractive dynamic reporting web application?</p>

<hr>

<p>It seems unrealistic not to have paging but I can understand the user perspective. It is like you have some 2-3k rows in Excel and you want to scroll down and see what your data looks like and if you want further analyze it you go head and sort, group etc...
The user know that ultimately there is a limit on how many data should be displayed on a web application. He just wanted to increase the current 1000 limit with a sorting and grouping capability. 
One thing that comes in to my mind and tested it with is the Infragistics "UltraWebGrid". The DotNet version is so poor in performance that I have to use paging but with the silverlight XamGrid one, I have good success in displaying as many as 15K records in less than 3min(with all grouping and sorting capability). The problem I have using silverlight is the fact that all reports are dynamic that I will be forced to make my datasource to be a datatable. I can't pass entity collection to the silverlight grid since I don't know the columns to be displayed before hand.</p>

## Answers
### Answer ID: 3126429
<p>I've use SSRS (SQL Server Reporting Services) quite successfully for several projects.  It's great for taking a query or stored sproc and just getting some reports with exportability and paging already built in.</p>

<p>The requirement to do away with paging kind of makes me raise my eyebrow.  The guy must have some kind of photographic super brain if he can scroll down a list of 1K+ items and "analyze" the data.  If he can't be talked out of it, then regardless of the technology you use, you'll need to make the query that runs that report work as quickly as possible, because downloading that much data (yes, even in html it gets "downloaded") is going to take a lot of time.</p>

