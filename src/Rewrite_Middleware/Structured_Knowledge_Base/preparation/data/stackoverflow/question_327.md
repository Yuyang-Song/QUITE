# Rewriting C# code in ColdFusion while still using .NET objects
[Link to question](https://stackoverflow.com/questions/20907590/rewriting-c-code-in-coldfusion-while-still-using-net-objects)
**Creation Date:** 1388764420
**Score:** 1
**Tags:** .net, coldfusion, coldfusion-10, cfml
## Question Body
<p>I was wondering if anybody could help me rewrite the following C# code in CFML? I have access to DLLs and can successfully access the classes using <code>CFOBJECT</code>. What I can't work out is how to translate the following syntax from C# to CFML. I've been trying all afternoon and am getting nowhere and I can't find any good tutorials on doing anything like this. </p>

<p>The API reference can be seen at <a href="http://api.korzh.com/easyquery/asp-net" rel="nofollow">http://api.korzh.com/easyquery/asp-net</a>.</p>

<p>The code is as follows:</p>

<pre><code>using Korzh.EasyQuery;
using Korzh.EasyQuery.Db;
using Korzh.EasyQuery.WebControls;

protected void Page_Load(Object sender, EventArgs e) 
{ 
  DbQuery query = (DbQuery)Session["QUERY"];
  if (query == null) {  
      //we didn't open this page before

      string modelPath = this.MapPath("~/App_Data/MyModel.xml");

      Korzh.EasyQuery.DataModel model = new Korzh.EasyQuery.Db.DbModel(); 
      model.LoadFromFile(modelPath); 

      query = new Korzh.EasyQuery.Db.DbQuery(); 
      query.Model = model;

      query.Formats.SetDefaultFormats(FormatType.MsSqlServer); 
      Session["QUERY"] = query;
  }
}
</code></pre>

<p>Many thanks!</p>

<p><strong>Clarification:</strong></p>

<p>EasyQuery provide a set of jQuery widgets which use a JSON representation of your database (I do not have any issue with generating the data model as this can be done using a tool provided by EasyQuery) to show the correct columns etc. in the query builder.</p>

<p>When the query is built in the UI it can be sent to the server. The query isn't sent as SQL which would be a security risk but is sent as some kind of obfuscated string. The ASP.NET classes can then be used to convert this string into SQL so a query can be run against a database. What I want to be able to do is to use these ASP.NET classes in ColdFusion to convert the string into SQL.</p>

<p>I believe (but am not sure) that the code at <a href="http://docs.korzh.com/easyquery/aspnet/getting-started-webforms" rel="nofollow">http://docs.korzh.com/easyquery/aspnet/getting-started-webforms</a> demonstrates how to generate the SQL.</p>

## Answers
### Answer ID: 20908109
<p>You would need to use the XmlParse to read the xml file into a  so it can be processed by Coldfusion. I'm not sure that there is a routine to generate the sql to setup the db model in SQL Server.</p>

### Answer ID: 20908052
<p>The Easy Appears to be a complete app that generates SQL queries. It reminds me of a really good looking replacement for Management Studio</p>

<p><img src="https://i.sstatic.net/oddfP.png" alt="enter image description here"></p>

<p><strong>CFQUERY</strong></p>

<p>If you are looking to run SQL, you would just copy the SQL in the lower left corner into <code>&lt;cfquery&gt;</code> tag. (Recommended)</p>

<p><strong>CFOBJECT</strong>
If you are looking to tap into a .Net object via ColdFusion, that can be done via </p>

<pre><code>&lt;cfobject type=".NET" name="mathInstance" class="mathClass"&gt; 
    assembly="C:/Net/Assemblies/math.dll"&gt;
&lt;cfset myVar=mathInstance.multiply(1,2)&gt;
</code></pre>

<p><strong>Source:</strong> <a href="https://learn.adobe.com/wiki/display/coldfusionen/cfobject%3A+.NET+object" rel="nofollow noreferrer">https://learn.adobe.com/wiki/display/coldfusionen/cfobject%3A+.NET+object</a> </p>

<p>If you are looking to rebuild this app in ColdFusion, that is a very large project, and beyond the scope of a SO topic</p>

