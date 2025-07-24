# What are those full-blown abstraction layer for PDO and how to work it with Firebird?
[Link to question](https://stackoverflow.com/questions/16124391/what-are-those-full-blown-abstraction-layer-for-pdo-and-how-to-work-it-with-fire)
**Creation Date:** 1366486698
**Score:** 0
**Tags:** php, pdo, firebird
## Question Body
<p>As MySQL manual says:</p>

<p>"PDO provides a data-access abstraction layer, which means that, regardless of which database you're using, you use the same functions to issue queries and fetch data. PDO does not provide a database abstraction; it doesn't rewrite SQL or emulate missing features. You should use a full-blown abstraction layer if you need that facility."
<a href="http://www.php.net/manual/en/intro.pdo.php" rel="nofollow">http://www.php.net/manual/en/intro.pdo.php</a></p>

<p><strong>What are those full-blown abstraction layers and how do I get them to use with PDO?</strong></p>

<p>I'm interested in use Firebird with PHP to support an old application that I made and port part of it's function to web.</p>

<p>The My SQL manual says that I should use <code>--with-pdo-firebird[=DIR]</code> in <strong>what file? php.ini?</strong></p>

<p>I wonder if in my shared server HostGator account I am able to put the firebird driver and if it will work... Does anyone knows about it? Will I have to make a dedicated server to use data bases other than MySQL in PHP?</p>

<p><em>Sorry for that many doubts!</em></p>

## Answers
### Answer ID: 16124453
<p>I suppose you cannot use your own php installation on a shared server. This <code>--with-pdo-firebird</code> argument is an argument to the <code>configure</code> command of PHP. (when installing PHP)</p>

<p>A full-blown abstraction layer is a class which provides methods like <code>select()</code>, <code>join()</code>, <code>insert</code>, <code>delete</code> etc. (in this specific case). There exist some such libraries (abstraction layers for databases I mean) in the Internet, for example Mediawiki uses such one.</p>

<p>An example how to use such an abstraction layer would be:</p>

<pre><code>$db-&gt;insert("table", ["field1", "field2"])-&gt;select("table2", ["field3", "field4"]);
</code></pre>

