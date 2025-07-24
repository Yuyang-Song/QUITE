# Oracle9i: Filter Expression Fails to Exclude Data at Runtime
[Link to question](https://stackoverflow.com/questions/483940/oracle9i-filter-expression-fails-to-exclude-data-at-runtime)
**Creation Date:** 1233071481
**Score:** 0
**Tags:** sql, oracle-database
## Question Body
<p>I have a relatively simple select statement in a VB6 program that I have to maintain. (Suppress your natural tendency to shudder; I inherited the thing, I didn't write it.)</p>

<p>The statement is straightforward (reformatted for clarity):</p>

<pre><code>select distinct 
   b.ip_address 
from 
   code_table a, 
   location b 
where 
   a.code_item = b.which_id and 
   a.location_type_code = '15' and 
   a.code_status = 'R'
</code></pre>

<p>The table in question returns a list of IP addresses from the database. The key column in question is <code>code_status</code>. Some time ago, we realized that one of the IP addresses was no longer valid, so we changed its status to <code>I</code> (invalid) to exclude it from appearing in the query's results.</p>

<p>When you execute the query above in SQL Plus, or in SQL Developer, everything is fine. But when you execute it from VB6, the check against <code>code_status</code> is ignored, and the invalid IP address appears in the result set.</p>

<p>My first guess was that the results were cached somewhere. But, not being an Oracle expert, I have no idea where to look. </p>

<p>This is <em>ancient</em> VB6 code. The SQL is embedded in the application. At the moment, I don't have time to rewrite it as a stored procedure. (I will some day, given the chance.) But, I need to know what would cause this disparity in behavior and how to eliminate it. If it's happening here, it's likely happening somewhere else.</p>

<p>If anyone can suggest a good place to look, I'd be very appreciative.</p>

## Answers
### Answer ID: 485590
<p>I'd suggest you have a look at the V$SQL system view to confirm that the query you believe the VB6 code is running is actually the query it is running.</p>

<p>Something along the lines of</p>

<pre><code>select sql_text, fetches
where sql_text like '%ip_address%'
</code></pre>

<p>Verify that the SQL_TEXT is the one you expect and that the FETCHES count goes up as you execute the code.</p>

### Answer ID: 484636
<p>There are Oracle bugs that result in incorrect answers. This surely isn't one of those times. Usually they involve some bizarre combination of views and functions and dblinks and lunar phases...</p>

<p>It's not cached anywhere. Oracle doesn't cache results until 11 and even then it knows to change the cache when the answer may change.</p>

<p>I would guess this is a data issue. You have a DISTINCT on the IP address in the query, why? If there's no unique constraint, there may be more than one copy of your IP address and you only fixed one of them.</p>

<p>And your Code_status is in a completely different table from your IP addresses. You set the status to "I" in the code table and you get the list of IPs from the Location table.</p>

<p>Stop thinking zebras and start thinking horses. This is almost certainly just data you do not fully understand. </p>

<p>Run this</p>

<pre><code>select 
   a.location_type_code, 
   a.code_status 
from 
   code_table a, 
   location b 
where 
   a.code_item = b.which_id and 
   b.ip_address = &lt;the one you think you fixed&gt;
</code></pre>

<p>I bet you get one row with an 'I' and another row with an 'R'</p>

### Answer ID: 484033
<p>In addition to the suggestions that IronGoofy has made, have you tried swapping round the last two clauses?</p>

<pre><code>where
   a.code_item = b.wich_id and
   a.code_status = 'R' and
   a.location_type_code = '15'
</code></pre>

<p>If you get a different set of results then this might point to some sort of wrangling going on that results in dodgy SQL actually be sent to the database.</p>

### Answer ID: 483994
<p>Some random ideas:</p>

<ul>
<li><p>Are you sure you committed the changes that invalidate the ip-address? Can someone else (using another db connection / user) see the changed code_status?</p></li>
<li><p>Are you sure that the results are not modified after they are returned from the database?</p></li>
<li><p>Are you sure that you are using the "same" database connection in SQLPlus as in the code (database, user etc.)?</p></li>
<li><p>Are you sure that that is indeed the SQL sent to the database? (You may check by tracing on the Oracle server or by debugging the VB code). Reformatting may have changed "something".</p></li>
</ul>

<p>Off the top of my head I can't think of any "caching" that might "re-insert" the unwanted ip. Hope something from the above gives you some ideas on where to look at.</p>

