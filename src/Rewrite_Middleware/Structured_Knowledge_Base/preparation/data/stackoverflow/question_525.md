# Dynamics AX 2012 - adding a custom query based report
[Link to question](https://stackoverflow.com/questions/29938844/dynamics-ax-2012-adding-a-custom-query-based-report)
**Creation Date:** 1430297761
**Score:** 0
**Tags:** sql-server, reporting-services, axapta, microsoft-dynamics
## Question Body
<p>I have created a SQL Server query using Transact-SQL and added it directly to the database as a view.</p>

<p>Then I created a SQL Server Reporting Services report using that query. Now I want to access this report from Microsoft Dynamics AX 2012. I have no idea how to do it. 
As far as I know one has to create a query in AX, then create an AX report, deploy it to AOT and once it's there you can use it in the application.</p>

<p>Do you know a way to use a custom SQL query without writing it again in AOT? My query is pretty complex and it could be impossible to rewrite in AOT.</p>

## Answers
### Answer ID: 29940045
<p>Prerequisites:</p>

<ul>
<li>Visual Studio 2010</li>
<li>Microsoft Dynamics AX Visual Studio Tools installed.</li>
<li>Microsoft Dynamics AX client configured.</li>
<li>SQL Server Data Tools (SSDT) (Add-on for Visual Studio).</li>
</ul>

<p>Create a <em>Report Server Project</em>. </p>

<p>Add the <em>.rdl</em> file downloaded from SSRS server: right click on <em>Reports</em> node -> <em>Add</em> -> <em>Existing item ...</em></p>

<p>Adjust other parts of the report, like datasources.</p>

<p>Right click on the report project -> <em>Add [project name] to AOT</em>.</p>

<p><img src="https://i.sstatic.net/WUNUZ.jpg" alt="Add [project name] to AOT."></p>

<p>The report should be now available in AOT:</p>

<p><img src="https://i.sstatic.net/3VIif.jpg" alt="enter image description here"></p>

<p>Go to <em>AOT -> SSRS Reports -> Reports</em> -> Right-click <em>[Your report] -> Deploy element.</em></p>

<p>You can now create Output menu items which point to your report.</p>

