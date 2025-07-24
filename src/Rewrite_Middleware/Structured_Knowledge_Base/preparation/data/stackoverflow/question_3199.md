# How to test/debug parameterised SQL
[Link to question](https://stackoverflow.com/questions/70988275/how-to-test-debug-parameterised-sql)
**Creation Date:** 1643985897
**Score:** 0
**Tags:** sql, sql-server, prepared-statement, informix
## Question Body
<p>My code (java in this case, but it doesn't matter) executes complex SQL statements against a database. These SQLs are parameterised, with up to 50 parameters in some cases.  They are very complex, often longer than a page of printed paper, joining dozens of tables, subselects, conditional case-when and so on.</p>
<p>The code looks something like this:</p>
<pre><code>final String sql = &quot;SELECT ...&quot;;
PreparedStatement stmt = getDBConnection().prepareStatement(sql);

sql.setString(1, ...);
sql.setInt(2, ...);
sql.setDate(3, ...);
...
sql.setString(50, ...);

ResultSet rs = stmt.executeQuery();
</code></pre>
<p>As the sql statements are parameterised, I can't just copy/paste the SQL statement into a database console to test/debug the statement, since all the &quot;?&quot; in it will cause errors.</p>
<p>When I get incorrect results or syntax errors, I need to be able to debug them somehow - but how?  How can I run this monstrosity in a database console to be able to play with parameters and/or get more specific syntax errors than just &quot;syntax error near '('&quot;?</p>
<p>I have code that runs against MS SQL Server (version 2014 - not in a position to upgrade) and Informix (version 7.3 - again, not in a position to upgrade).  Even one of them would be helpful, although SQL Server is the priority for me.</p>
<p>Note, I am <em>not</em> in at liberty to rewrite the code to run multiple smaller queries instead of the large ones. Please do not suggest rewriting them - this is not what the question is about.</p>

