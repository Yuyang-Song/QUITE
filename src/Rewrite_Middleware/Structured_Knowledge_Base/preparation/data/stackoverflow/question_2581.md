# DateTime column not working in MS Access tables linked to MySQL backend
[Link to question](https://stackoverflow.com/questions/41454177/datetime-column-not-working-in-ms-access-tables-linked-to-mysql-backend)
**Creation Date:** 1483487646
**Score:** 1
**Tags:** mysql, odbc, ms-access-2016, mysql-odbc-connector
## Question Body
<p>I have a MySQL database with a Microsoft Access (2016) front-end. I have a number of linked tables in the Access DB which contain DateTime columns.</p>

<p>I have been running this DB successfully on both my home PC and notebook for quite a while, but recently had to replace my notebook, so have just installed on (well copied onto) a new notebook. On this new instance, none of my date filters are working. On investigation, I have noticed very strange behaviour: if I open one of the linked tables, click on any value in one of the date columns and select the option to filter on just that value, nothing is displayed. If I write a query to filter for example</p>

<pre><code>WHERE [Date]=#01/01/2017# 
</code></pre>

<p>nothing is returned. If I rewrite this to</p>

<pre><code>WHERE CDate([Date])=#01/01/2017# 
</code></pre>

<p>it returns the correct record(s) (incidentally I chose this date to demonstrate that it is not a UK/US date format problem).</p>

<p>The column is correctly showing as a DateTime column in the linked table in the front-end, and if I write a query to display the year, month and day values of said column, it returns the correct values.</p>

<p>I am running Windows 10 Home, fully updated, with Access 2016 MSO 16.0.7571.7063 and MySQL Connector/ODBC 5.3.6 on both machines. I can find no other settings in Access that differ between the two machines, and my locale and language settings also seem to be the same on both, as far as I can tell.</p>

<p>I tried converting the MySQL column to Date instead of DateTime, but it made no difference. I have also refreshed, then deleted and relinked the tables on the version on the new notebook, and even repaired the Office installation and still no joy.</p>

<p>Incidentally, if I copy the linked table to a local table, it works fine.</p>

<p>I have no idea what could be causing this. Since everything else seems to be the same, is it possible there is some registry setting that is different on my new notebook from my other PC(s)?  </p>

<p>EDIT: I have just tried the following clause on the notebook</p>

<pre><code>WHERE [Date]&gt;=#01/01/2017# And [Date]&lt;=#31/12/2016#
</code></pre>

<p>and it returns all records!</p>

<p>FURTHER EDIT: I have also tried running the following query  </p>

<pre><code>Select count([date]) from daysworked where [date]&gt;=#dd/mm/yyyy#
</code></pre>

<p>in some VBA, for a range of dates. Whenever dd is between 1 and 20 (inclusive) it returns 1753 (all rows). Whenever dd is 21 or greater, it returns zero, whatever the values of mm and yyyy. That looks to me like it might be interpreting the dd as a century value. Since MySQL dates are in format yyyy-mm-dd, I suppose that could make some sort of sense, but I would expect the ODBC connector to be dealing with the conversion from Access to MySQL format. And it clearly does that fine on all other machines I have run this on.</p>

## Answers
### Answer ID: 41472200
<p>I have now built a new DB, with all the back-end tables added as new linked tables, and it has solved the problem. </p>

<p>I have checked as many settings as I can, and can't find any differences between the two DBs, so I can only conclude that the old front-end DB had become corrupted. Thought I'd better post this as an answer in the very unlikely event that anyone else ever has the same problem!</p>

### Answer ID: 41463642
<p>I have created new DB on the notebook and added the linked table there using the same ODBC DSN, and it works ok. So it must be something to do with the specific accdb file I am using. I can't find any DB settings that would do it, so I am starting to suspect corruption. </p>

<p>At least this gives me a fix, albeit a painful one, of building a new Access accdb and moving all my objects into it. But I would love to know why this is happening only on my notebook and not on any other PC running the same accdb file and same ODBC connector.</p>

### Answer ID: 41459699
<p>Do you have a time part included? What will this return:</p>

<pre><code>WHERE [Date] Between #01/01/2017# And #01/02/2017# 
</code></pre>

<p>Or try to display the numeric value on both machines and compare:</p>

<pre><code>NumDate: CDbl([Date])
</code></pre>

<p>Or do you actually have text:</p>

<pre><code>WHERE [Date] = '01/01/2017' 
</code></pre>

