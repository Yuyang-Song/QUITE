# Filtering date in kendo grid with inherited model
[Link to question](https://stackoverflow.com/questions/66216030/filtering-date-in-kendo-grid-with-inherited-model)
**Creation Date:** 1613427024
**Score:** 0
**Tags:** c#, asp.net-core, kendo-grid, filtering
## Question Body
<p>I want to filter bithdate in a kendo grid with asp.net core MVC.
I have two model inherited, for example:</p>
<pre><code>public class ParentModel
{
    public DateTime BirthDate { get; set; }
}

public class ChildModel : ParentModel
{
    public string BirthDateAmerican =&gt; BirthDate.ConvertEnglishToAmerican();
}
</code></pre>
<p>I want to filter date in a kendo grid with a date input that writen in american format, but date stored in database is in English format, Then i need to convert it for filtering in model, for this purpose i use linq queryable to get all data and filter it with request received from grid by ToDataSourceResultAsync(request) extension method.</p>
<p>for ex:</p>
<pre><code>public Task&lt;DataSourceResult&gt; GetListByKendoFilter(DataSourceRequest request)
        {
            return Queryable
                .Select(x =&gt; new ChildModel
                {
                    Id = x.Id,
                    ParentModel.BirthDate = x.BirthDate
                }).OrderByDescending(o =&gt; o.BirthDate).ToDataSourceResultAsync(request);
        }
</code></pre>
<p>the filter input in request is in American format that should be compared with english format date field that stored in database.and i get this error.</p>
<p>The LINQ expression {expression...} could not be translated.
Either rewrite the query in a form that can be translated,
or switch to client evaluation explicitly by inserting a call to either
AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync().
See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.&quot;}
System.Exception {System.InvalidOperationException}.</p>
<p>It seems that date change method in childmodel doesnt executed and the format is not comparable with database.</p>
<p>Pls do not change the senario and give your solutions for this senario.
Excuse me for bad english :)</p>

