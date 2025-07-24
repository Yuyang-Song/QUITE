# php: sql-injection &gt; how to prevent when no prepared statement can be used?
[Link to question](https://stackoverflow.com/questions/58461641/php-sql-injection-how-to-prevent-when-no-prepared-statement-can-be-used)
**Creation Date:** 1571471679
**Score:** -3
**Tags:** php, prepared-statement, sql-injection
## Question Body
<p>A simple question: I have a framework which does not use prepared statements (mySQLi).
How can sql injections be avoided when I have some user input (made through a public form but no HTML-code is allowed).
That comment has to be stored in a mysqli database.</p>

<p>What is the best practice to detect and remove possible injection code?
Please no suggestions to use prepared statements, they are not availabe without rewriting the whole framework!</p>

<p><strong>EDIT</strong></p>

<p>I was NOT asking how to do a MySQLi query!
I asked how to prevent sql-injections on the php-level.
To repeat: some website visitor leave a comment in a plain text field.
Inside this comment this visitor (the script kiddie) thinks, he can post a sql-injection.</p>

<p>Now again: how the delete this pseudocode from the comment BEFORE adding it to the database.
Answers like "hey, use a prepared statement", "use pdo", "use this kind of query with these parameters" are NOT answering my question.
Also answers like "change" your framework" or NOT adequate!</p>

<p>I know that this could such code could be removed by preg_replace(..) and so on.
And yes, I know the opinion of some here not to use this technique .. so better do not answer in that direction!</p>

## Answers
### Answer ID: 58468163
<p>You might think that using an "escaping" function like <a href="https://www.php.net/manual/en/mysqli.real-escape-string.php" rel="nofollow noreferrer">mysqli::real_escape_string()</a> on every input is just as safe as using prepared statements.</p>

<p>Except:</p>

<ul>
<li><p>Escaping doesn't work for numeric inputs, only quoted strings and quoted dates.</p></li>
<li><p>Escaping has some unexpected cases where it doesn't work. These are edge cases, but they exist. See some examples in answers for <a href="https://stackoverflow.com/q/5741187/20860">SQL injection that gets around mysql_real_escape_string()</a></p></li>
<li><p>Escaping is harder when writing code. Doing it correctly is time-consuming and meticulous, and easy to get wrong. Developers are often tempted to skip it.</p></li>
</ul>

<p>Developers who care about preventing SQL injection recommend using query parameters instead for several reasons, including but not limited to the following:</p>

<ul>
<li><p>Query parameters also work for numeric values.</p></li>
<li><p>Code that uses query parameters is easier to write and read, and less prone to mistakes. We expect that once they have the habit of using query parameters, developers use this method more reliably, and therefore vulnerabilities are less likely.</p></li>
</ul>

<p>For example, you could write code like the following:</p>

<pre><code>$sql = "INSERT INTO mytable (col1, col2, col3, col4, col5, col6) 
  VALUES ('" . mysqli_real_escape_string($_POST['col1']) . "', " 
  . $mysqli-&gt;real_escape_string($_POST['col2']) . "', '" 
  . $mysqli-&gt;real_escape_string($_POST['col3']) . "', '" 
  . $mysqli-&gt;real_escape_string($_POST['col4']) . ", '" 
  . $mysqli-&gt;real_escape_string($_POST['col5']) . "', '" 
  . $mysqli-&gt;real_escape_string($_POST['col6']) . "')";
</code></pre>

<p>Can you spot the mistakes? With enough time, I’m sure you can. But it will slow down your coding and may give you eyestrain as you look for missing quote characters and other mistakes.</p>

<p>But it’s so much easier to write this, and easier to read it afterwards:</p>

<pre><code>$sql = "INSERT INTO mytable (col1, col2, col3, col4, col5, col6) 
  VALUES (?, ?, ?, ?, ?, ?)";
</code></pre>

<p>Query parameters are safe for more data types, and they help you write code more quickly, with fewer mistakes. That's a big win.</p>

<p>Like the other comments above, I disagree with your claim that MySQLi doesn't support query parameters. It's clearly shown in the documentation: <a href="https://www.php.net/manual/en/mysqli.prepare.php" rel="nofollow noreferrer">https://www.php.net/manual/en/mysqli.prepare.php</a></p>

<p>If you have some wrapper code that uses MySQLi but doesn't support <code>mysqli::prepare()</code>, then I recommend you stop using that wrapper code. Either write features for your framework so that it uses query parameters, or else get another framework.</p>

<hr>

<blockquote>
  <p>Also answers like "change" your framework" or NOT adequate!</p>
</blockquote>

<p>Look, here's the truth: if you can't write code that handles user input safely, then you shouldn't accept user input. </p>

<p>You suppose there are ways of using <code>preg_replace()</code> but there aren't. There are so many ways of injecting code (either SQL or Javascript), that you would end up filtering out many <em>legitimate</em> user comments as well. How would your users react if your web app stripped quotes and apostrophes from their comments? What other characters do you need to strip out?</p>

<p>Query parameters are the most effective solution for this problem. Your resistance to them is absurd. </p>

<p>It's like an electrician who asks, "How can I prevent getting shocked? But I can't use insulated gloves or tools, so don't suggest that."</p>

