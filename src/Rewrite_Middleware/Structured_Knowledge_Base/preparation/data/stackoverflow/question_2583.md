# MySQL select query finds a result that shouldn&#39;t be found in PDO
[Link to question](https://stackoverflow.com/questions/41578702/mysql-select-query-finds-a-result-that-shouldnt-be-found-in-pdo)
**Creation Date:** 1484083537
**Score:** 1
**Tags:** php, mysql, pdo
## Question Body
<p>So, for a school assignment I have to make a website. This website must contain a functionality that gets articles out of a database.</p>

<p>I can, for example, show article 1 with <em>domain.com/content/article/1/</em>.</p>

<p>However, when I use a URL like this <em>domain.com/content/article/2aadd/</em> it still shows article 2.
Even <em>../10aadd/</em> shows article 10.
If I try to request an article that doesn't exist with like <em>../11aadd</em> (article 11 doesn't exist) it will show an error that it can't find the article, like it should.</p>

<hr>

<p>I use URL rewriting so a URL like this <em>domain.com/content/article/1/</em> is rewritten as <em>domain.com/index.php?c=content&amp;a=article&amp;arg=1</em></p>

<p>I use a database class, every select query is sent to a select-query method. It accepts the following parameters:</p>

<ul>
<li>$q - the query</li>
<li>$params - an array with parameters for the query</li>
<li>$fetch - the fetching mode</li>
</ul>

<p>The following parameters are sent in order to show an article:</p>

<ul>
<li><em>select title,content from PHP2b_OOP_EIND_Articles where id=:id and enabled=1</em></li>
<li>array("id"=>$_GET["arg"])</li>
<li><em>assoc</em></li>
</ul>

<p>In every call of this method a new statement is being prepared and executed with the <em>$params</em> array as parameter.</p>

<hr>

<p>I've dumped out the <em>$params</em> array and it does show the entire string (e.g. 10aadd).</p>

<p>I've tried it without the clean URL.</p>

<p>I've tried to look it up but I couldn't find anything.</p>

<hr>

<p>What could be the cause of this?</p>

## Answers
### Answer ID: 41578815
<p>I suspect your MySQL table's <code>id</code> column is defined as an integer data type.</p>

<p>You're experiencing a peculiarity of MySQL when it coerces a string data type to an integer. </p>

<pre><code>select CAST('10aaadd' AS INT)
</code></pre>

<p>gives back the value <code>10</code>, strangely enough.</p>

<p>Your query, after variable substitution, says <code>WHERE id = '10aaadd'</code>.</p>

<p>Because MySQL implicitly casts that string to an int, it finds the row with the <code>id</code> value of <code>10</code>.  </p>

<p>Weird, huh?</p>

<p>If you expect only integers in a $_GET or $_POST parameter, it's a good idea to check for that and throw an error if the values you receive don't match expectations.  <a href="http://php.net/manual/en/function.is-numeric.php" rel="nofollow noreferrer">PHP's <code>is_numeric()</code> function</a> can do that for you.</p>

