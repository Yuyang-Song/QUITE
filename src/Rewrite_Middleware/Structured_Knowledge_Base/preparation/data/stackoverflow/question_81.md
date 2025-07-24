# Is it bad practice to do &quot;small_table LEFT JOIN large_table&quot;?
[Link to question](https://stackoverflow.com/questions/12210957/is-it-bad-practice-to-do-small-table-left-join-large-table)
**Creation Date:** 1346399081
**Score:** 3
**Tags:** mysql, indexing
## Question Body
<p>I'm connecting to a database which I cannot administer and I wrote a query which did a left join between two tables - one small and one several orders of magnitude larger. At some point, the database returned this error:</p>

<blockquote>
  <p>Incorrect key file for table '/tmp/#sql_some_table.MYI'; try to repair it</p>
</blockquote>

<p>I contacted the administrators and I was told that I'm getting this error because I'm doing the left join incorrectly, that I should NEVER left join a small table to a large table and that I should reverse the join order. The reason they gave was that when done my way, MySQL will try to create a temp table which is too large and query will fail. Their solution fails elsewhere, but that's not important here.</p>

<p>I found their explanation odd, so I ran explain on my query:</p>

<pre><code>           id = '1'
  select_type = 'SIMPLE'
        table = 'small_table'
         type = 'ALL'
possible_keys = NULL
          key = NULL
      key_len = NULL
          ref = NULL
         rows = '23'
        Extra = 'Using temporary; Using filesort'

           id = '1'
  select_type = 'SIMPLE'
        table = 'large_table'
         type = 'ref'
possible_keys = 'ID,More'
          key = 'ID'
      key_len = '4'
          ref = 'their_db.small_table.ID'
         rows = '41983'
        Extra = NULL
</code></pre>

<p>(The 41983 rows in the second table are not very interesting to me, I just needed the latest record, which is why my query has <code>order by large_table.ValueDateTime desc limit 1</code> at the end.)</p>

<p>I was careful enough to do a select by columns which the admins themselves told me, should hold unique values (and thus I assumed indexed), but it seems they haven't indexed those columns.</p>

<p>My question is - is doing the join the way I did ('small_table LEFT JOIN large_table') bad practice in general, or can such queries be made to execute successfully with proper indexing?</p>

<p>Edit:
Here's what the query looks like (this is not the actual query, but similar):</p>

<pre><code>select large_table.ValueDateTime as LastDate,
       small_table.DeviceIMEI as IMEI,
       small_table.Other_Columns as My_Names,
       large_table.Pwr as Voltage,
       large_table.Temp as Temperature
from small_table left join large_table on small_table.ID = large_table.ID
where DeviceIMEI = 500
order by ValueDateTime desc
limit 1;
</code></pre>

<p>Basically what I'm doing is trying to get the most current data for a device, given that Voltage and Temperature change over time. The DeviceIMEI, ID and ValueDateTime should be unique, but aren't indexed (like I said earlier, I don't administer the database, I only have read permissions).</p>

<p>Edit 2:</p>

<p><strong>Please focus on answering my actual question, not on attempting to rewrite my original query.</strong></p>

## Answers
### Answer ID: 12210991
<p>The left join thing is a red herring.</p>

<p>It is however an actual problem of running out of space for temp tables. But the order of your join makes no difference. The only thing that matters is how many rows MySQL must work with.</p>

<p>Which brings me to the LIMIT command:</p>

<p>Here is the problem:</p>

<p>It order to get the single row you asked for, MySQL has to sort the ENTIRE record set, then grab the top one. In order to sort it, it must store it - either in memory or on disk. And that's where you are running out of space. Every single column you requested get stored on disk, for the entire table, then sorted.</p>

<p>This is slow, very slow, and uses a lot of disk space.</p>

<p>Solutions:</p>

<p>You want MySQL to be able to use an index for the sorting. But in your query it can't. It's using an index for the join reference, and MySQL can only use one index per query.</p>

<p>Do you even have an index on the sort column? Try that first.</p>

<p>Another option is to do a separate query, where you select just the ID of the large table, LIMIT 1. Then the temporary table is MUCH smaller since all it has are IDs without all the other columns.</p>

<p>Once you know the ID then retrieve all the columns you need directly from the tables. You can do this in one shot with a subquery. If you post your query I could rewrite it to show you, but it's basically <code>ID = (SELECT ID FROM ..... LIMIT 1)</code></p>

