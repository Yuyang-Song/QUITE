# Slow INNER JOIN Query in MS-Access 2016
[Link to question](https://stackoverflow.com/questions/70350788/slow-inner-join-query-in-ms-access-2016)
**Creation Date:** 1639492806
**Score:** 1
**Tags:** sql, vba, ms-access, ms-access-2016
## Question Body
<p>I inherited responsibility for a MS Access database. That database was grown over 20 years, with things added, removed and changed. In short, it's a convoluted mess. The VBA a code is full of codes like</p>
<pre><code>Dim p, strText, A, B, C, d, E, F, G, H, i, j, K, L, M, N, O, Z, R, Q, kd, AfGb, T, LN, DC, EntBez, TP, pack, Press, Fehler, ksoll, Y, zeileninhalt, dateipfad, auslesezeile As String
</code></pre>
<p><strong>The Problem</strong><br />
It is slow when opening some forms (7-10 seconds loading time). I narrowed it down to the recordsource of these forms, which all use the same query or a variation.</p>
<p>The user enters a job number in the Main form and hits enter. The underlying query then pulls data from two tables based on the unique key JobNr. The result is a single row containing all the info for this job. These infos are displayed in an Editor form, using the query as recordsource.</p>
<p>The database is split into frontend and backend, t1 and t2 are backend tables each with about 20k entries. Backend sits somewhere on the company servers, frontend is saved locally on each user computer.</p>
<p>This is the query:</p>
<pre><code>SELECT *
FROM t1 
INNER JOIN t2 ON t1.JobNr = t2.JobNr
WHERE JobNr = [Forms]![Main]![JobNr];
</code></pre>
<p><code>t1</code> has <code>JobNr</code> as primary key, <code>t2</code> has an <code>ID</code> as primary key, <code>JobNr</code> is not indexed. I want to try indexing it in hope of better performance, but currently can't make changes to the backend during busy work days.</p>
<p>This simple query is slow. The problem seems to be the order of execution. Instead of getting the single entries from t1 and t2 and joining these to a single dataset, Access seems to first join both tables and only after that looks up the single dataset the user is interested in.</p>
<p>I was not able to find a solution to dictate the execution order. I tried different ways, like rewriting the SQL code with nested Selects, something like:</p>
<pre><code>SELECT *
FROM 
    (SELECT * FROM t1 
     WHERE t1.JobNr = [Forms]![Main]![JobNr]) AS q1
INNER JOIN
    (SELECT * FROM t2 
     WHERE t2.JobNr = [Forms]![Main]![JobNr]) AS q2 ON q1.JobNr = q2.JobNr;
</code></pre>
<p>Still slow...</p>
<p>I wanted to try <code>WITH</code> to partition the SQL code, but that's apparently not supported by MS Access SQL.</p>
<p>I tried splitting the query into two queries q1 and q2 in Access, that pull the data from t1 resp. t2 with a third query q3 that does the joining of these supposed subsets to no avail. q1 and q2 individually run blazingly fast with the expected data result, but q3 takes the usual 7-10 seconds.</p>
<p>The current approach I'm working on is running q1 and q2 and saving the acquired data to two temp tables tq1 and tq2 and then joining these in a last query. This works, it rapidly loads the data and displays it in the editor (&lt; 0.5 seconds, hurray!).<br />
The problem I'm facing now is updating any changes the user makes in the editor form to the backend tables t1 and t2.   Right now, user changes don't take and are lost when closing and reopening the job/editor.</p>
<p>Is there any way to make this <code>INNER JOIN</code> query fast without the whole temp table workaround?</p>
<p>If not, how would I go about updating the backend tables from the local temp tables? Changes in the Editor are saved in the temp tables until overwritten by reopening the editor.</p>
<p>I already added intermediary queries, that add the resp. primary keys to the temp tables (this cannot be done directly in the Create Table queries).</p>
<p>I also tried using an Update query when closing the Editor, which doesn't seem to work, but I might have to debug that one, I'm not sure it does anything right now.</p>

## Answers
### Answer ID: 70353230
<p>You need to add a unique index to <code>t2.JobNr</code>, even better make it the primary key.</p>
<p>Everything else is just a waste of time at this point.</p>
<p>Set a date and time for the users to quit their frontends, kick them out if necessary: <a href="https://stackoverflow.com/questions/10905680/force-all-users-to-disconnect-from-2010-access-backend-database">Force all users to disconnect from 2010 Access backend database</a></p>
<p>In the long run, moving from an Access backend to a server backend (like the free SQL Server Express) will be a good idea.</p>
<hr />
<p>Edit: have you tried what happens if you don't do JOIN at all?</p>
<pre class="lang-sql prettyprint-override"><code>SELECT *
FROM t1, t2
WHERE t1.JobNr = [Forms]![Main]![JobNr]
  AND t2.JobNr = [Forms]![Main]![JobNr]
</code></pre>
<p>Normally you want to avoid this, but it might help in this case.</p>

### Answer ID: 70351065
<p>The most obvious rework is to move the filter into the join:</p>
<pre class="lang-sql prettyprint-override"><code>SELECT *
FROM t1 
INNER JOIN t2 ON (t1.JobNr = t2.JobNr AND t2.JobNr = [Forms]![Main]![JobNr])
</code></pre>
<p>My guess is that it's irrelevant if you filter on t1 or t2, but then my guess would also be that Access is smart enough to filter while joining and that appears to be untrue, so check that.</p>
<p>For more detailed performance analysis, a query plan tends to help. See <a href="https://stackoverflow.com/questions/12607296/how-to-get-query-plans-showplan-out-from-access-2010">How to get query plans (showplan.out) from Access 2010?</a></p>
<p>Of course, adjust 14 to your version number.</p>

