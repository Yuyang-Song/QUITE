# Select all from database table – but use a function on one of the columns
[Link to question](https://stackoverflow.com/questions/33238922/select-all-from-database-table-but-use-a-function-on-one-of-the-columns)
**Creation Date:** 1445350003
**Score:** 2
**Tags:** php, mysql, mysqli, pdo
## Question Body
<p>Is this even possible, does my title of this question makes sense?</p>

<p>I am struggling and trying to figure out the way to get all from database <code>table</code>, but I need to run a function wether SQL or PHP.</p>

<p>So real short example would be:</p>

<pre><code>SELECT * FROM `table` WHERE `ip` = '$this-&gt;ip'
</code></pre>

<p>However I am using <code>INET_ATON()</code> to store the <code>IP</code> and <code>INET_NTOA()</code> to retrieve it back. I could've also use PHP's function <code>ip2long()</code> and <code>long2ip()</code>, but still I don't know how would I accomplish such a thing using the same <strong>query</strong>?</p>

<pre><code>SELECT `id`, INET_NTOA(`ip`) as `ip`, `points`
FROM `table` WHERE `ip` = INET_ATON('$this-&gt;ip')
</code></pre>

<p>Those are all <code>table columns</code> defined manually to get to the point of what I need to do exactly. But... For this simple project it seems alright to do it this way, but what if I had more columns and only some of them or one of them require some converting? </p>

<p>So how can I accomplish something like... <em>(I know that this is invalid)</em></p>

<pre><code>SELECT * FROM `table` WHERE `ip` = '$this-&gt;ip` BUT INET_NTOA(`ip`) as `ip`
</code></pre>

<hr>

<p>Beside this question, I also wonder is <code>INET_ATON() &amp; INET_NTOA()</code> only <code>MySQL function</code> or <code>SQL</code> function. Because I am planning to rewrite my project to use <code>PDO</code> instead of <code>MySQLi</code> and I am unsure wether those functions will work or I should rely on PHP's built-in same functionality.</p>

## Answers
### Answer ID: 38451754
<p>INET_ATON() &amp; INET_NTOA()
// ALL THESE ARE DEPRECATED!  Use inet_pton()  or inet_ntop() instead!!
The reason for that is they do not work for IPv6 addresses and with more of the internet using IPv6 and not IPv4.</p>

<p>They is both a PHP and an SQL function with the same name convert an IP address into a string and back again.</p>

