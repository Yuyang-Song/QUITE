# How to aggregate a collection of items in one cell of an ASPxGridView
[Link to question](https://stackoverflow.com/questions/8827101/how-to-aggregate-a-collection-of-items-in-one-cell-of-an-aspxgridview)
**Creation Date:** 1326318242
**Score:** 2
**Tags:** c#, linq, devexpress, aspxgridview, llblgenpro
## Question Body
<p>I'm using ASP.NET 3.5, LLBLGenPro 3.0, and DevExpress 10.1.7.  I have an ASPxGridView with a LinqServerModeDataSource.  Each row of the ASPxGridView corresponds to a TaskEntity from LLBLGenPro.  One of the properties of TaskEntity is OrganizationCollection, which is a collection of related OrganizationEntities.  What I'd like to do is add a column to the ASPxGridView called OrgList, which would display the list of related Organizations by name (ideally in a <code>&lt;br&gt;</code>-delimited list, so each item will be in its own row, but the list will be all in the same cell, which works if the column has its EncodeHtml property set to "False").  </p>

<p>Currently, I have in the lsmdsTasks_Selecting() event (this is a simplified example):</p>

<pre><code>IQueryable&lt;TaskEntity&gt; taskQuery;

taskQuery = TaskQueryStore.GetTasks(...);

var query = from task in taskQuery
            select new 
                   {
                       task.Id,
                       task.TaskName,
                       OrgList = ???
                   }

e.KeyExpression = "Id";
e.QueryableSource = query;
</code></pre>

<p>So far, I have tried a few things for the "???", with the following results:</p>

<p>First, I tried:  </p>

<pre><code>OrgList = task.OrganizationCollection.Aggregate("", (acc, item) =&gt; (acc == "" ? "" : acc + "&lt;br&gt;") + item.OrgName)
</code></pre>

<p>This gave me the following ORMException: "'Aggregate' isn't supported in this Linq provider. Please try to rewrite the query using methods which are supported."  </p>

<p>Then, I tried:</p>

<pre><code>OrgList = String.Join("&lt;br&gt;", task.OrganizationCollection.Select(x =&gt; x.OrgName).ToArray())
</code></pre>

<p>This gave me the following ORMException: "Method call to 'Join' doesn't have a known mapped database function or other known handler."</p>

<p>The only thing that has kind of worked has been:  </p>

<pre><code>OrgList = GetOrgList(task.Id)
</code></pre>

<p>and then defining the <code>GetOrgList()</code> method separately, which takes the task Id and builds the list in the format I want it, and returns it as a string.  This actually did show the data in the grid the way I want it, but the downside was that when you try to sort on this column it doesn't work correctly, and when you try to filter on this column using the AutoFilter it just filters everything out, regardless.  Plus, I suppose it is hitting the database several extra times more than necessary.  </p>

<p>Is there any way to get this to work with sorting and filtering intact?  Or will I need to disable these features for this column?  </p>

## Answers
### Answer ID: 13474261
<p>Try using a template with a repeater for your column. You can pass the OrgList from the column to the repeater using databinding.</p>

<p>Something like this :</p>

<pre><code>&lt;asp:Repeater runat="server" ID="repeater" Datasource='&lt;%# OrgList %&gt;'&gt;
...
</code></pre>

### Answer ID: 9363414
<p>I ended up fetching the tasks with a prefetchPath to Organization, and then using Aggregate in a Linq2Objects in-memory query, then passing the resulting list to my grid's datasource, and that worked.  </p>

