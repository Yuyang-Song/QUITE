# .NET Library to Parse/Modify/Reconstruct SQL Statement
[Link to question](https://stackoverflow.com/questions/66713257/net-library-to-parse-modify-reconstruct-sql-statement)
**Creation Date:** 1616176218
**Score:** 1
**Tags:** postgresql, vb.net, parsing
## Question Body
<p>I'm currently looking for a library to use in my VB.NET WinForms application to do the following:</p>
<ul>
<li>Parse a SQL statement extracted from the command text in a Crystal Reports <code>.rpt</code> file into its individual clauses (<em><code>SELECT</code>, <code>FROM</code>, <code>JOIN</code>, <code>WHERE</code>, <code>ORDER BY</code>, etc.</em>)</li>
<li>Modify one or more of the parsed clauses of that statement</li>
<li>Recompile/reconstruct the statement with the changes before piping it back into the <code>.rpt</code> file for execution and report generation.</li>
</ul>
<p>Specifically, the SQL statement in question is querying against a PostgreSQL database and looks something like this (<em>mixed-case, quoted identifiers and all</em>):</p>
<pre class="lang-sql prettyprint-override"><code>SELECT * FROM &quot;[SCHEMANAME]&quot;.&quot;[VIEWNAME]&quot; WHERE &quot;[COLUMNNAME]&quot; IN ('[VALUE1]','[VALUE2]');
</code></pre>
<p>Does anyone know of a workable/usable library that will actually do this? I've read through a number of questions on this site as well as other sources found in Google search results for potential solutions, but I've yet to find a viable, working method to accomplish all of this in a reasonable way with exposed properties/methods to &quot;simplify&quot; the process. Just a few of the SO questions I've looked at so far include:</p>
<ul>
<li><strong><a href="https://stackoverflow.com/q/15003128/2569697">SQL parser library - get table names from query</a></strong></li>
<li><strong><a href="https://stackoverflow.com/q/1847801/2569697">Library to parse SQL statements</a></strong></li>
<li><strong><a href="https://stackoverflow.com/q/35648582/2569697">Parse and execute Sql statements from file</a></strong></li>
<li><strong><a href="https://stackoverflow.com/q/12580609/2569697">Parse SQL statement</a></strong></li>
</ul>
<p>All I <em>really</em> want to do is dynamically take this (or <em>any</em>) SQL statement, break out the <code>WHERE</code> clause and modify it, add an <code>ORDER BY</code> clause, then recompile it and update the Crystal Reports <code>Command</code> data source. Yes, I am aware that <em><strong>this specific example</strong></em> can be handled manually <em>very</em> easily, but I also have a number of more complex queries/statements that I'd potentially like to be able to perform a similar operation on without having to rewrite the entire statement or manually find the positions of the clauses and use <code>String.Replace()</code>, or other more complex methods to achieve that goal.</p>
<p>Regardless, what I'd like to see from whatever solution I end up using would be to parse the above statement with <em><strong>at the very least</strong></em> something like the following results:</p>
<pre><code>Statement Type:    SELECT
SELECT Clause:     SELECT *
FROM Clause:       FROM &quot;[SCHEMANAME]&quot;.&quot;[VIEWNAME]&quot;
WHERE Clause:      WHERE &quot;[COLUMNNAME]&quot; IN ('[VALUE1]','[VALUE2]')
</code></pre>
<p>Of course, I'd prefer to have it provide additional levels of &quot;drilling down&quot; - a <code>List(Of&lt;T&gt;)</code> (or something) for the columns in the <code>SELECT</code> clause, specific &quot;keys&quot; from the <code>WHERE</code> clause, etc. I've tested with a number of the parsers available, including a trial of the commercial &quot;<a href="http://www.sqlparser.com/" rel="nofollow noreferrer">General SQL Parser</a>&quot; library and the <a href="https://learn.microsoft.com/en-us/dotnet/api/microsoft.sqlserver.management.sqlparser.parser?view=sql-smo-150" rel="nofollow noreferrer"><code>Microsoft.SqlServer.Management.SqlParser</code></a> library. I've also tried some &quot;less popular&quot; options from the NuGet catalog, including one that uses ANTLR and the GOLD Engine.</p>
<p>In my tests, however, I've not been able to find a totally satisfactory solution. Admittedly, there's an element of unfamiliarity with the tools that definitely plays into my findings, but I'm left wondering if there's anything out there that can do for me what I want or if I'm going to have to &quot;roll my own&quot;. I'd like to be able to do things like:</p>
<ul>
<li><code>WHEREClause.Add(&quot;&quot;&quot;Column1&quot;&quot; = 'NewValue'&quot;)</code></li>
<li><code>ORDERBYClause.Add(&quot;&quot;&quot;Column2&quot;&quot;&quot;, SortOrder.Descending)</code></li>
<li><code>ORDERBYClause.Clear()</code></li>
<li><code>SELECTClause.Remove(&quot;&quot;&quot;ColumnA&quot;&quot;&quot;, &quot;&quot;&quot;Alias&quot;&quot;&quot;)</code></li>
</ul>
<p>The <code>Microsoft.SqlServer.Management.SqlParser</code> library seems to do a decent job of parsing a simple query like the above but, obviously, when it comes to some of the PostgreSQL-specific syntax (<em>e.g.</em>, concatenation with <code>||</code>), it throws errors preventing me from accurately reconstructing the SQL statement.</p>
<p>Licensing costs notwithstanding, the <strong>General SQL Parser</strong> library is one of the only options I've found that supports the PostgreSQL syntax (<em>although it took me a bit to figure out how to get to that point</em>) but doesn't <em>seem</em> to expose the information I need in a useful way for my requirements. If it does, I've not yet been able to get to it. Perhaps I'm being dense, but I've been unable to figure out how to get the <a href="http://www.dpriver.com/blog/list-of-demos-illustrate-how-to-use-general-sql-parser/add-remove-and-modify-condition-in-where-clause-net-version/" rel="nofollow noreferrer">online example</a> to work in my own environment. From what I can tell, getting what I want is going to require the creation of a bunch of &quot;extra&quot; bits just to achieve my goal. Besides, its price is a bit steep for my situation as a one-man Development/IT department.</p>
<p>What would be <em>fantastic</em>, IMO, would be if I could simply do the parsing and such with the <a href="https://www.npgsql.org/" rel="nofollow noreferrer"><code>Npgsql</code> library</a> my application is already using for other database operations, but that doesn't seem to be an option either (unless, again, I'm just overlooking something).</p>
<p>I started playing with the <a href="https://www.codeproject.com/Articles/32524/SQL-Parser" rel="nofollow noreferrer">SQL Parser</a> code from Sergey Gorbenko on CodeProject, but this also doesn't &quot;natively&quot; support PostgreSQL syntax, and the amount of work it would take to bring that &quot;up-to-snuff&quot; is beyond what I have the time or gumption to invest at this point.</p>
<p>As I've said, the example above is very simple, but I'd like to be able to use whatever I eventually find for parsing more complex statements with subqueries, joins, unions, and all sorts of other SQL elements without having to jump through a bunch of hoops every time. Are there any other libraries or projects out there that anyone has been able to successfully use to perform these operations (parse, edit, recompile) with a PostgreSQL-specific SQL statement?</p>

## Answers
### Answer ID: 66715593
<p>You could take a look at ANTLR.  It will generate C# targets and there is an existing SQL grammar (<a href="https://github.com/antlr/grammars-v4/tree/master/sql" rel="nofollow noreferrer">here</a>).  This should be able to parse your SQL and produce an in-memory ParseTree data structure that easily exceeds your requirements.</p>
<p>With ANTLR, take a look at the TokenStreamRewriter.  It allows you to make modifications to the input stream that you parsed and insert of remove content (preserving the rest of the input stream).  I would definitely advise against any string manipulation approach.  That's really just a variation on a SQL injection vulnerability.</p>
<p>It your needs somehow outgrow what TokenStreamRewriter provides (probably unlikely), then you have the full parse tree in memory and could modify that structure in place and work out a listener/visitor to serialize it back out to text.</p>
<p>In short, unless you find a purpose-built SQL modifier tool, this gives you the right approach to properly parse everything, correctly identifying all the pieces, then work with that data structure to write out your modified results.</p>

