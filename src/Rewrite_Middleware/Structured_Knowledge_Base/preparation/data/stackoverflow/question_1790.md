# sqlite3 python query with multiple variables error
[Link to question](https://stackoverflow.com/questions/8032299/sqlite3-python-query-with-multiple-variables-error)
**Creation Date:** 1320634538
**Score:** 1
**Tags:** python, sqlite
## Question Body
<p>I looked all over for the answer to my question and could not find any good answer.... I am using python with the sqlite3 module to query a database. The problem is that I cannot get a sql query to hold multiple variables. For example...</p>

<p>I can get this query to work perfectly. ("wordsofar" is the variable name)</p>

<pre><code>c.execute("SELECT word FROM wordlist WHERE word LIKE ?", wordsofar)
</code></pre>

<p>However I cannot get this code to work. ("wordsofar" and "noletter" are the variable names)</p>

<pre><code>c.execute("SELECT word FROM wordlist WHERE word LIKE ? AND word NOT LIKE ?", (wordsofar, noletter))
</code></pre>

<p>It gives me the error: "Error binding parameter 0" </p>

<p>I have tried to rewrite the query so instead of "?" it is using the named convention such as shown by <a href="http://docs.python.org/py3k/library/sqlite3.html" rel="nofollow">http://docs.python.org/py3k/library/sqlite3.html</a> (about half way down the page) but that did not solve the problem.</p>

<p>Any help would be much appreciated. Thank-you!</p>

## Answers
### Answer ID: 8032769
<p>This line (that you say works) shows that <code>wordsofar</code> is a sequence of one element:</p>

<pre><code>c.execute("SELECT word FROM wordlist WHERE word LIKE ?", wordsofar)
</code></pre>

<p>In this case the second line should be:</p>

<pre><code>c.execute("SELECT word FROM wordlist WHERE word LIKE ? AND word NOT LIKE ?", 
          wordsofar + (noletter,))
</code></pre>

<p>If <code>noletter</code> is a string and <code>wordsofar</code> is a tuple (as you say in your comment).</p>

<p><a href="http://docs.python.org/library/sqlite3.html#sqlite3.Cursor.execute" rel="nofollow"><code>execute()</code> docs</a> say that the second argument is always <code>parameters</code>. If you use '?' then number of parameters (<code>len(parameters)</code>) is equal to number of '?' in the sql statement.</p>

### Answer ID: 8032456
<p>You code looks fine.</p>

<p>The problem is in the data.  Either <em>wordsofar</em> or <em>noletter</em> is an object that sqlite3 doesn't know how to store.</p>

<p>One solution is to pickle the object.  Another solution is to supply converter and adapter functions.</p>

<p>Use <a href="http://docs.python.org/library/sqlite3.html#sqlite3.register_adapter" rel="nofollow noreferrer">register_adapter</a> to register a callable to convert the custom Python type type into one of SQLite’s supported types. </p>

<p>The docs also describe how to supply converters to handle the reverse conversion:</p>

<blockquote>
  <p>SQLite natively supports only the types TEXT, INTEGER, FLOAT, BLOB and
  NULL. If you want to use other types you must add support for them
  yourself. The detect_types parameter and the using custom converters
  registered with the module-level <a href="http://docs.python.org/library/sqlite3.html#sqlite3.register_converter" rel="nofollow noreferrer">register_converter()</a> function allow
  you to easily do that.</p>
</blockquote>

<p>Here's a related <a href="https://stackoverflow.com/questions/5142975/keeps-getting-error-binding-parameter-0-probably-unsupported-type">SO question with answers</a>.</p>

