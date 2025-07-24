# Why is Entity Framework disregarding my orderbys?
[Link to question](https://stackoverflow.com/questions/12695855/why-is-entity-framework-disregarding-my-orderbys)
**Creation Date:** 1349201520
**Score:** 2
**Tags:** linqpad, entity-framework-5
## Question Body
<p>I am rewriting an application which needs to duplicate the alphabetization logic of an old mainframe system.  In the old mainframe system, item change record IDs are alphabetized From A through Z, and then starts over with AA, AB, and so on.  Unfortunately both SQL Server and .NET want to put AA between A and B, so I'm having to jump through some hoops.  I'm trying to sort the change IDs first by descending length and then by alphabetizing in descending order.  </p>

<p>Here is the method I am using to retrieve the data:</p>

<pre><code>protected internal IList&lt;TeamViewModel&gt; GetTeams(string recordId, string changeId)
{
    var viewModels = (from x in repository.Teams
               where x.RecordId == recordId &amp;&amp; x.ChangeId.Length &lt;= changeId.Length &amp;&amp; 
                 (x.ChangeId.CompareTo(changeId) == -1 || x.ChangeId.CompareTo(changeId) == 0)
               orderby x.ChangeId.Length descending, x.ChangeId descending, x.ChangeId descending
               group x by x.TeamId into grp
               select grp.FirstOrDefault())
               .ToList()
               .Select(TeamViewModel.FromEntity)
               .ToList();

            return viewModels;
}
</code></pre>

<p>Each "Record" has a collection of change records, and each change record a ChangeId property and and TeamId that made the change.  I'm trying to get the "newest" (according to the old mainframe sorting logic) change record for each distinct teamId.  In other words, I am attempting to order the records, group them by team, and then grab the first record from each group.</p>

<p>The repository.Teams property returns an IQueryable which wraps the ObjectSet declared in my ObjectContext.</p>

<p>What really blows my mind is that this query works fine when I run it in Linqpad (with default configuration) <strong>and</strong> this very method executes fine from within unit tests when I have injected a mock of my repository into this class, which I have setup to emit the exact same data that is in the SQL database.</p>

<p>But when this method is executed at runtime, it behaves as though the line with the orderbys is completely omitted and in fact gives me the same results that I ge tin Linqpad (with default configuration) when I comment out the line with the orderbys.  SQL Profiler shows that the generated SQL is nigh impossible to decipher by a human, but which does not contain the word "order" in it anywhere.</p>

<p>As a final note, when I configure Linqpad to use my EF-generated typed dataset within my project's assembly, I get the same results that I see at run time, with results appearing as though the orderbys are disregarded.</p>

<p>I wish I could show actual results but the data is proprietary, so just consider that the correct results, as provided by Linqpad and my unit tests, contain change records with IDs like "Y" and "Z" where as the inexplicable (to me) results that I see in my project at runtime are like "A" and "B".</p>

<p>Can anyone see what is occurring here, and just as importantly, what I need to change to make this function as I am expecting?</p>

<p>My project is using entity framework 5.0 and I'm using Linqpad 4.42.01.</p>

<p>Thanks so much!</p>

## Answers
### Answer ID: 12696160
<p>I'll make a wild guess...</p>

<p>Your ChangeId's are all the same length. The database has them mapped as a CHAR(10) column or something instead of a VARCHAR, so A is really "A         " and AB is really "AB        ". Mainframes and COBOL and flat files with offsets come to mind as my rationale. If this is the case you'd have to Trim() the ChangeId first before getting the Length.</p>

### Answer ID: 12695949
<p>Group by does not guarantee to retain the original order.  If you want to order, you must order after the group by.</p>

<p>In fact, it doesn't even make sense to order by before a group by, since the group by is guaranteed to change the order (unless there's only a single group).  </p>

