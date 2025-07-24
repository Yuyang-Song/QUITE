# Parsing T-SQL to Parameterize a Query
[Link to question](https://stackoverflow.com/questions/170850/parsing-t-sql-to-parameterize-a-query)
**Creation Date:** 1223146817
**Score:** 2
**Tags:** .net, sql-server, parsing
## Question Body
<p>The application I am currently working on generates a lot of SQL inline queries. All generated SQL is then handed off to a database execution class. I want to write a parsing service for the data execution class that will take a query like this:</p>

<pre><code>SELECT field1, field2, field3 FROM tablename WHERE foo=1 AND bar="baz"
</code></pre>

<p>and turn it into something like this:</p>

<pre><code>SELECT field1, field2, field3 FROM tablename WHERE foo=@p1 AND bar=@p2 blah blah blah
</code></pre>

<p>Any thing already written that will accomplish this for me in c# or vb.net? This is intended as a stop gap prior to refactoring the DAL for this project.</p>

<p><strong>UPDATE:</strong> Guys I have a huge application that was ported from Classic ASP to ASP.NET with literally thousands of lines of inline SQL. The only saving grace is all of the generated sql is handed off to a data execution class. I want to capture the sql prior to execution and parameterize them on the fly as a stop gap to rewriting the whole app. </p>

## Answers
### Answer ID: 172954
<p>Refactor now.</p>

<p>You're fooling yourself if you think this one abstraction layer is going to be able to come in quicker and easier.  Deep down, you know it increases risk and uncertainty on the project, but you want to kill the SQL injection problem or whatever problem you are fighting with a magic bullet.</p>

<p>The time you would be taking to write this new parsing subsystem and regression testing the system, you could probably replace all the inline code with calls to relatively fewer code-generated and tested SPs on your DB.  Plus you can do it piece by piece.</p>

<p>Why build a significant piece of throwaway code which will be hard to debug and isn't really inline with what you want the final architecture to look like?</p>

### Answer ID: 171050
<p>Have you considered running a substitution regex on the old code? Something that will extract values from the current queries, replace them with parameters, and append after the query line a Command.Parameters.AddWithValue(paramName, paramValue) call might be possible if the current inline SQL all follow the same value (or if nearly all of them do, and you can fix up the remainder in your favorite editor). </p>

### Answer ID: 171032
<p>I can only think of one benefit that parameterizing queries on the fly would bring:  it would reduce your application's current vulnerability to SQL injection attacks.  In every other way, the best you could possibly hope for is that this hypothetical on-the-fly parser/interpreter wouldn't break anything.</p>

<p>Even if you didn't have to write such a thing yourself (and I bet you do), that's a pretty significant risk to introduce into a production system, especially since it's a stopgap measure that will be discarded when you refactor the app.  Is the risk of a SQL injection attack high enough to justify that?</p>

### Answer ID: 170940
<p>o think your task is too much honerous...
you should create a very robust parser... i think it's better and easier starting to rewrite application, finding points where queries are generated and refactoring code.</p>

<p>Good Loock!</p>

### Answer ID: 170917
<p>I would second the suggestion to use the Command parameters to do what you want.
Any kind of SQL query string parsing is just asking for someone do play an SQL injection game with you. A sample code is below. The Parameters collection is easy to manipulate in the normal way</p>

<pre><code>command.CommandText = "SELECT * FROM table WHERE key_field='?'"
command.Parameters.Append command.CreateParameter(, 8, , , "value") '8 is adBSTR value
set rsTemp = command.Execute
</code></pre>

### Answer ID: 170869
<p>Don't do this. This is way too much work. Plus, there are loads of security risks with this approach.</p>

<p>Look into Command objects and parameterized queries, at the minimum.</p>

<p><a href="http://www.csharp-station.com/Tutorials/AdoDotNet/Lesson06.aspx" rel="nofollow noreferrer">Here is a small tutorial.</a></p>

