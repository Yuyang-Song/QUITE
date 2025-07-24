# grouping multiple queries into a single one, with Postgres
[Link to question](https://stackoverflow.com/questions/71489793/grouping-multiple-queries-into-a-single-one-with-postgres)
**Creation Date:** 1647383740
**Score:** 0
**Tags:** postgresql
## Question Body
<p>I have a very simple query:</p>
<pre><code>SELECT * FROM someTable
WHERE instrument = '{instrument}' AND ts &gt;= '{fromTime}' AND ts &lt; '{toTime}'
ORDER BY ts
</code></pre>
<p>That query is applied to 3 tables across 2 databases.</p>
<p>I receive a list of rows that have timestamps (ts). I take the last timestamp and it serves as the basis for the 'fromTime' of the next iteration. toTime is usually equal to 'now'.</p>
<p>This allows me to only get new rows at every iteration.</p>
<p>I have about 30 instrument types and I need an update every 1s.</p>
<p>So that's 30 instruments * 3 queries = 90 queries per second.</p>
<p>How can I rewrite the query so that I could use a function like this:</p>
<pre><code>getData table [(instrument, fromTime) list] toTime
</code></pre>
<p>and get back some dictionary, in the form:</p>
<pre><code>Dictionary&lt;instrument, MyDataType list&gt;
</code></pre>
<p>To use a list of instruments, I could do something like:</p>
<pre><code>WHERE instrument in '{instruments list}'
</code></pre>
<p>but this wouldn't help with the various fromTime as there is one value per instrument.</p>
<p>I could take the min of all fromTime values, get the data for all instruments and then filter the results out, but that's wasteful since I could potentially query a lot of data to throw is right after.</p>
<p>What is the right strategy for this?</p>

## Answers
### Answer ID: 71496029
<p>So there is a single <code>toTime</code> to test against per query, but a different <code>fromTime</code> per instrument.</p>
<p>One solution to group them in a single query would be to pass a list of <code>(instrument, fromTime)</code> couples as a relation.</p>
<p>The query would look like this:</p>
<pre><code>SELECT [columns] FROM someTable
JOIN (VALUES
   ('{name of instrument1}', '{fromTime for instrument1}'),
   ('{name of instrument2}', '{fromTime for instrument2}'),
   ('{name of instrument3}', '{fromTime for instrument3}'),
   ...
) AS params(instrument, fromTime)
ON someTable.instrument = params.instrument AND someTable.ts &gt;= params.fromTime
WHERE ts &lt; 'toTime';
</code></pre>
<p>Depending on your datatypes and what method is used by the client-side driver
to pass parameters, you may have to be explicit about the datatype of
your parameters by casting the first value of the list, as in, for
example:</p>
<pre><code>JOIN (VALUES
   ('name of instrument1', '{fromTime for instrument1}'::timestamptz),
</code></pre>
<p>If you had much more than 30 values, a variant of this query with arrays as parameters (instead of the VALUES clause) could be preferred. The difference if that it would take 3 parameters: 2 arrays + 1 upper bound, instead of <code>N*2+1</code> parameters. But it depends on the ability of the client-side driver to support Postgres arrays as a datatype, and the ability to pass them as a single value.</p>

