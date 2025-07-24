# Query designer in winforms app
[Link to question](https://stackoverflow.com/questions/14546544/query-designer-in-winforms-app)
**Creation Date:** 1359283220
**Score:** 10
**Tags:** .net, sql, winforms, user-interface
## Question Body
<p>I'm working on a Winforms C# application for a client which replaces their old MS Access based solution. It's a complete rewrite and now uses SQL Server as its database. This software is now in the final stages of development.</p>

<p>One thing that they've just requested is that ability to do custom queries that the software's UI may not currently let them do at the time they need it.</p>

<p>With their old Access solution, they could use the query designer to create their own custom queries. With the winforms/Sql Server solution they can't do this. They don't want to have to write SQL themselves either.</p>

<p>Can anyone think of a good solution to this problem? Perhaps a Winforms library which allows the user to create a graph of business objects and "and|or" logic. Or some other type of UI which allows them to customise queries, almost like they could do in Access (but perhaps more domain specific).</p>

<h2>Update</h2>

<p>I've flagged Yaqub's answer as the answer, as this is the closest to what I was looking for at the time. I ended up though writing a custom form for them to generate their queries:</p>

<p><img src="https://i.sstatic.net/9dUYf.jpg" alt="enter image description here"></p>

<p>The "Select table ..." combobox in the second group only shows tables that have been added to the top listbox.</p>

<p>Because the database layout is pretty much set in stone now, I've written code to intelligently calculate any joins required. For example, if they add two indirectly related tables in the top group, then when it generates the SQL, it'll add any required joins to relate those. If the database layout does change, I've made it very easy to change FK references in the query editor's code.</p>

<p>For the condition group, the value control (4th control down in that group) changes depending on the field type (textbox, numerical up/down control, datepicker, checkbox).</p>

<p>When they click on "Run query", they get another form with a gridview displaying the results. In that results form, they can export to a tab delimited file.</p>

<p>I've given them the first version of this, and they seem very happy with it so far.</p>

<p>I didn't want to go the Access route because the whole point of this new version of the software is moving them away from Access (well, not the whole point, as there's a lot more functionality in there too). It seemed a huge step back to keep that dependency with Access there. It also means that if they save lots of custom queries in Access, and I ever change the database schema, I'll most likely break their queries. I don't want them having access to the database like that. In my mind, it's asking for trouble. The only thing that should be touching the database is the new software, and any automated database backups we do - nothing else, especially not users!</p>

<p>Another advantage to doing it within the software, is that I can do post processing on the query results. For example, there are quite a few data analysis algorithms that are run in the software which are written in the .NET code. So I can add fields to this interface that allow them to select the results of these algorithms.</p>

## Answers
### Answer ID: 14587209
<p>You may find the <a href="http://www.codeproject.com/Articles/43171/A-Visual-SQL-Query-Designer" rel="nofollow">Visual SQL Query Designer</a> helpful. It will give you an idea that how you can implement this functionality.</p>

<p>This tool can be used to design SQL queries. Its UI is very basic as compared to SQL Server Management Studio. Its limitation is that it uses <code>OLEDB</code> connection string. You can download the source code from <a href="http://www.codeproject.com/KB/database/QueryDesigner/QueryDesignerSource.zip" rel="nofollow">here</a>. </p>

<p><strong>EDIT:</strong></p>

<p><a href="http://devtools.korzh.com/query-builder-winforms/" rel="nofollow">EasyQuery.NET WinForms</a> can be an option but its not free.</p>

<p><a href="http://www.c-sharpcorner.com/UploadFile/neelamiyer/QueryBuilder12012005042244AM/QueryBuilder.aspx" rel="nofollow">This article</a> may also help you a bit.</p>

### Answer ID: 14704671
<p>I worked on similar tool, basically this tool provides business users to creates report in data grid by drag and drop on business views. We created views on top of tables and maintain metadata information like fields relations etc. metadata tables. If tables are having referential integrity then tool is getting information from sql server master database.</p>

<p>We got help from this utility provided on codeproject. You can go through this basic application which create sql query by drag and drop and you can change as per your need.</p>

<p><a href="http://www.codeproject.com/Articles/43171/A-Visual-SQL-Query-Designer" rel="nofollow">http://www.codeproject.com/Articles/43171/A-Visual-SQL-Query-Designer</a></p>

### Answer ID: 14651390
<p>Have you considered using the SSRS portion of SQL, and giving them access to the ReportBuilder tool?  It has a decent interface for power users.  If you have your primary keys and foreign keys set up in the database, it will recognize those relationships and assist the user in building multi-table queries.  The tool can be downloaded directly from the SSRS web portal, you can integrate the reports directly into your .Net app using the ReportViewer control, or you can use simple HTTP requests to pull them back as Excel, PDF, etc.</p>

### Answer ID: 14589676
<p>One traditional "Microsoft" answer to this is to let them keep using Access... only point it at the SQL server and just let them build their custom queries there.</p>

<p>If you want to get fancy, you can build in a query user role and account, grant only read access to it, and even limit that baked-in role user account to some percentage of the total system load with the Resource Governor stuff if necessary.</p>

<p>There is no shame in prototyping new stuff in Access before rolling it up into real code, either.</p>

