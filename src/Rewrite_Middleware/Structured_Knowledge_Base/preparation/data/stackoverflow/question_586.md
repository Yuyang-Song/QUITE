# How to increase data retrieval?
[Link to question](https://stackoverflow.com/questions/32704957/how-to-increase-data-retrieval)
**Creation Date:** 1442871629
**Score:** 1
**Tags:** c#, .net, parallel-processing, query-performance
## Question Body
<p>I have a query that takes long to execute and eventually times out.</p>

<p>My task is just to get all the data from the table for particular dates.</p>

<p>However, the database table does not have indexes on the date column and query takes long time to execute and times out.</p>

<p>This is piece of code I have:</p>

<pre><code>DateTime dateTo = Convert.ToDateTime(data.DateTo);
DateTime dateFrom = Convert.ToDateTime(data.DateFrom);
command.CommandText = "select * from errorlog where errortime between @dateFrom and @dateTo";
command.Parameters.AddWithValue("@dateTo", dateTo);
command.Parameters.AddWithValue("@dateFrom", dateFrom);
da.SelectCommand = command;
da.Fill(ds);  
</code></pre>

<p>Is there any way to rewrite the logic to improve the performance?</p>

## Answers
### Answer ID: 32705027
<p>Talk to your DBA. Let him create the index. All other things you are going to 'fix' because of this is just a waste of your time and the time of your users.</p>

### Answer ID: 32705002
<p>Since the query timeout happens because of slow database, few solutions are:</p>

<ol>
<li>Increase the timeout value;</li>
<li>Execute the query in the database first as usually they cache the results. This will warm up the data for you, however, I totally understand that, it may not be always possible;</li>
<li>Run query in loop going over the entire date range in chunks and then consolidate your result at your application's end;</li>
<li>Get only the required columns instead of everything.</li>
</ol>

