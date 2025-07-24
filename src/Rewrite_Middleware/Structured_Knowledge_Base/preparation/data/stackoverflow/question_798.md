# why we write mysql in $conn = new pdo(); if pdo is platform independent
[Link to question](https://stackoverflow.com/questions/42783774/why-we-write-mysql-in-conn-new-pdo-if-pdo-is-platform-independent)
**Creation Date:** 1489488146
**Score:** 0
**Tags:** php, mysql, mysqli, pdo
## Question Body
<p>In PHP PDO(PHP Data Objects) tutorials I've been reading that the advantage of PDO over MySQLi is that PDO is platform independent. That said means you wrote a script with PHP PDO using MySQL database management system. Later you want to switch your web application to another Database Management System like Oracle, you will not need to rewrite your queries. While in case of MySQLi you had to rewrite your queries.</p>

<p>Now I'm confused by looking at the following line</p>

<blockquote>
  <p>$conn = new PDO("<strong>mysql</strong>:host=$servername;dbname=myDB", $username,
  $password);</p>
</blockquote>

<p>Why do we need to mention the <strong>"mysql"</strong> in the first parameter? And if I've to port my website to another DBMS, would I not need to replace this "mysql" with something like <strong>"oracle"</strong>?</p>

<p>Hopefully somebody clarify this.</p>

<p>Thanks</p>

## Answers
### Answer ID: 54232305
<blockquote>
  <p>PDO provides a data-access abstraction layer, which means that, regardless of which database you're using, you use the same functions to issue queries and fetch data. </p>
</blockquote>

<p>It means you don't have to change your PHP code on DBMS switch, well in most cases, if used correctly. But PDO definitely should know what database you use and how to handle it, driver to use.</p>

<p>Database and type can be safely moved into a config file for later customization.</p>

### Answer ID: 42784388
<p>That's actually a good question, dunno why it was so fiercely downvoted. </p>

<blockquote>
  <p>Later you want to switch your web application to another Database Management System like Oracle, you will not need to rewrite your queries.</p>
</blockquote>

<p>Unfortunately, that's but a nasty rumor. In fact, you'll have to rewrite many queries as well. PDO is just a <a href="https://phpdelusions.net/pdo#why" rel="nofollow noreferrer"><em>Database Access</em> Abstraction layer</a>, means it offers the unified API to access different databases, but it doesn't rewrite SQL queries for you according to different SQL flavors. </p>

<blockquote>
  <p>Why do we need to mention the "mysql" in the first parameter?</p>
</blockquote>

<p>Well, even for your imaginary PDO you'd have to tell somehow, <em>which driver to use</em>. So for the actual PDO as well. It is true that a single wending machine can serve you with either Pepsi or Coke, but it cannot read minds and you have to specify what it would be. </p>

<p>So yes - you have to specify the database you are connecting to <strong>and</strong> rewrite your queries. </p>

<blockquote>
  <p>the advantage of PDO over MySQLi</p>
</blockquote>

<p>That's the most insignificant advantage - there is actually <a href="https://phpdelusions.net/pdo/mysqli_comparison" rel="nofollow noreferrer">much more</a>.</p>

