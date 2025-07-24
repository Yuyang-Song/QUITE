# Python abstraction-layer for SQL
[Link to question](https://stackoverflow.com/questions/50154948/python-abstraction-layer-for-sql)
**Creation Date:** 1525349979
**Score:** 0
**Tags:** python, sql, json, database, wrapper
## Question Body
<p>I'm currently using Python to store files in a JSON Database. However the JSON has started to become rather large, and inefficient (reading a 20MB file, changing one value, writing 20MB back to disk again, takes rather long)</p>

<p>So, I was thinking about switching to SQL (SQLite or Mysql), however I don't want to change my entire code. So far, I've been reading the JSON into lists/arrays and access them rather easily </p>

<pre><code>database["key"] = "NewValue"
</code></pre>

<p>But if I switched to SQL, I'd have to deal with long SQL queries (select from.....insert into....), apart from the entire overhead-stuff (connect, execute, etc.). That requires me to rewrite every single data-access in my code.</p>

<p>Is there a way (maybe some sort of wrapper), where I can just keep my existing code-base, and let the wrapper the conversion for me in the background?</p>

