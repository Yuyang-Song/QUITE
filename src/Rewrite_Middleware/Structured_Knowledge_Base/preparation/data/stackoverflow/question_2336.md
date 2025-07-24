# SQL query in python script, how to get quotes around a parameter?
[Link to question](https://stackoverflow.com/questions/29838808/sql-query-in-python-script-how-to-get-quotes-around-a-parameter)
**Creation Date:** 1429850240
**Score:** 1
**Tags:** python, sql, sqlite
## Question Body
<p>I need to rewrite the php script that handles a POST request and queries a SQLite3 database into python. The Query now looks like this</p>

<pre><code>cursor.execute("SELECT * from "+requestedProgram+" WHERE start LIKE ? ORDER BY start", (requestedDate,))
</code></pre>

<p>the first part until the <em>WHERE</em> condition works (it is not elegant but unfortunately it seems that table names cannot be parametrized). </p>

<p>However, I need to put quotes around the requestedDate string in order to make <em>LIKE</em> work. How do I get quotes around the parameter/variable?</p>

<p>On another note: does the <em>ORDER BY</em> statement even do anything considering the nature of the cursor?</p>

## Answers
### Answer ID: 29838851
<p>Use single quotes, don't use the trailing comma behind requestedDate (it tuple-izes it), and add a trailing wildcard to the string.</p>

<pre><code>cursor.execute("SELECT * from "+requestedProgram+" WHERE start LIKE '?' ORDER BY start", requestedDate + '%')
</code></pre>

<p>Edit: Updated per conversation thread with OP below. Details added for those who stumble across this.</p>

