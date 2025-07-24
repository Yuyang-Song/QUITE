# DataSet to XML file in legacy ASP.NET Web Forms application
[Link to question](https://stackoverflow.com/questions/68039706/dataset-to-xml-file-in-legacy-asp-net-web-forms-application)
**Creation Date:** 1624039616
**Score:** -1
**Tags:** c#, asp.net
## Question Body
<p>I'm trying to identify a legacy ASP.NET Web Forms web application project as &quot;code first&quot; or &quot;database first&quot; (or &quot;model first&quot;). My observations are:</p>
<ul>
<li>Entity Framework is not being used</li>
<li>a SQL database is accessed for a DataSet, which is then written out to an XML file (which is used as the data source)</li>
<li>there are .cs classes identifying the structure of the target data display (table rows etc)</li>
<li>XmlDataSource is not being used</li>
</ul>
<p>EDIT:
The project appears to be an XML-file-as-database project, but based on a SQL database; with the ability to rewrite the XML database by re-querying a the SQL database.</p>
<p>I find this two-step a little odd, and so I am wondering if this is common for ASP.NET web applications, and what the possible advantages of handling data this way are.</p>

## Answers
### Answer ID: 68039904
<p>Microsoft defines a <a href="https://learn.microsoft.com/en-us/dotnet/api/system.data.dataset?view=xamarinios-10.8" rel="nofollow noreferrer">DataSet</a> (in part) like this:</p>
<blockquote>
<p>The DataSet, which is an in-memory cache of data retrieved from a data source, is a major component of the ADO.NET architecture. The DataSet consists of a collection of DataTable objects that you can relate to each other with DataRelation objects.</p>
</blockquote>
<p>From my experience, and as near as I can tell from the docs, a DataSet cannot be used in a code-first approach, as it does not have the same capabilities as Entity Framework. As to the XML:</p>
<blockquote>
<p>A DataSet can read and write data and schema as XML documents. The data and schema can then be transported across HTTP and used by any application, on any platform that is XML-enabled.</p>
</blockquote>
<p>XML (along with the associated C# classes) is the typical format of a DataSet in a Visual Studio project. Following the advent of Entity Framework, DataSets are no longer the recommended method for accessing data in an ASP.NET project (or any other .NET project for that matter).</p>

