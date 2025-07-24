# Update to a NOTE() column fails through Linked_Server, but works in ZCC
[Link to question](https://stackoverflow.com/questions/78008516/update-to-a-note-column-fails-through-linked-server-but-works-in-zcc)
**Creation Date:** 1708098445
**Score:** 0
**Tags:** sql-server, linked-server, pervasive, pervasive-sql, actian
## Question Body
<p>Question summarized: <br />
How do I get Pervasive SQL 15.2 as a Linked Server into SQL Server 2022 like we did with 9.7 into 2000?</p>
<p>Background and details: <br />
We have an ERP system that's using a Btrieve database and we have extensive extensions written in SQL Server. These queries (including insert and update) work fine on our old production system, but all insert and update queries accessing a NOTE column through the linked server from SQL Server to PSQL fail.</p>
<p>Technical Setup</p>
<div class="s-table-container"><table class="s-table">
<thead>
<tr>
<th></th>
<th>Old</th>
<th>New</th>
</tr>
</thead>
<tbody>
<tr>
<td>OS</td>
<td>Windows Server 2003R2</td>
<td>Windows Server 2019</td>
</tr>
<tr>
<td>Arch</td>
<td>32bit</td>
<td>64bit</td>
</tr>
<tr>
<td>SQL</td>
<td>Microsoft SQL Server 2000</td>
<td>Microsoft SQL Server 2022</td>
</tr>
<tr>
<td>Btrieve</td>
<td>Pervasive 9.5</td>
<td>Zen 15.2</td>
</tr>
<tr>
<td>ODBC</td>
<td>Client Engine Interface</td>
<td>Client Interface</td>
</tr>
</tbody>
</table></div>
<p>How databases were set up and transferred (boring to most)</p>
<blockquote class="spoiler">
<p> The SQL-database was &quot;moved&quot; by generating a CREATE DATABASE script on the old system, changing dboption to ALTER TABLE and running it on the new system. The data itself is transferred through a linked server on the new system to read the latest data from SQL (preparation for the final migration) The Pervasive data was copied from the old system and marked as database by the Zen Control Center.</p>
</blockquote>
<p>Why we need the note-column (not that it matters to the problem)</p>
<blockquote class="spoiler">
<p> The ERP uses NOTE-columns on many tables to encode additional (user defined) pseudo columns. This means we write in a text file what we want to store like &quot;'GDPR signed' as bool&quot; and the ERP shows this as a Checkbox while the NOTE would contain &quot;{GDPR signed:Y}&quot;</p>
</blockquote>
<p>Due to the grown constructs between our ERP and our extensions based on the SQL Server we need to be able to modify the NOTE-column of the tables.</p>
<p>On the old system we would run</p>
<pre><code>UPDATE OPENQUERY(MYLINK, 'SELECT &quot;ID&quot;, &quot;Data&quot;, &quot;MoreData&quot;, Notes FROM MyT') 
SET Notes = 'Hallo Welt' 
WHERE ID = 'XXX'
</code></pre>
<p>and it would just update.</p>
<p>On the new system the same query fails with</p>
<blockquote>
<p>[Zen][ODBC Client Interface][LNA][Zen][SQL Engine]Function sequence error</p>
</blockquote>
<p>What we tried to narrow the problem down</p>
<ul>
<li>We tried to execute the &quot;real&quot; query <code>UPDATE MyT SET Notes='Hello World' WHERE ID='XXX'</code> using ZCC and 'QTODBC 7.0' - both work just fine</li>
<li>We tried to use ODBCtrace to find what is happening, but we couldn't get a trace of the SSMS. It just didn't log anything (RDP on the system itself)</li>
<li>We modified the linked server using different settings, but the only change was broken data in SELECT if changing the wrong parameter (UTF vs ANSI...)</li>
</ul>
<p>What we couldn't try</p>
<ul>
<li>Change the ODBC to Engine Interface - that's 32bit only and &quot;should not be used as it will soon be dropped&quot;</li>
<li>Test with a 32bit SQL - if that would work the project would still be failed - no benefit in trying</li>
</ul>
<p>We are out of ideas on what to check and try.</p>
<p>We are also quite challenged by the changes and renames that happened between SQL Server 2000 and SQL Server 2022 (it took me nearly a day to verify that our old database was setup mostly with the 2022 default settings because I had to translate the dboptions to ALTER TABLE ('read only' = false vs. READ_WRITE ON))</p>
<p>Update 1: Question added at top as it was dropped during formatting/rewriting of the information.</p>

