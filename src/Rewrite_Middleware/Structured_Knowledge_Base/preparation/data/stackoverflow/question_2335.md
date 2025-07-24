# PDO not pulling data from string but works fine with integer
[Link to question](https://stackoverflow.com/questions/29838496/pdo-not-pulling-data-from-string-but-works-fine-with-integer)
**Creation Date:** 1429847941
**Score:** 0
**Tags:** php, mysql, .htaccess, mod-rewrite, pdo
## Question Body
<p>I'm trying to build a single pages.php file which I can pass slug information too and use mod-rewrite to make database output look like actual pages.</p>

<p>The problem is that the code works but only with integers being passed. If I pass the page_id it will make the call and work, if I pass page_slug it will fail.</p>

<p>Here is my rewrite rule</p>

<pre><code>RewriteRule ^service/(.*)$ pages.php?pid=$1 [QSA,L]
</code></pre>

<p>And here is the select query in pages.php to which I'm using require_once("Database.php"); to call the database file.</p>

<pre><code>$sql = " 
      SELECT 
         page_title,
         page_html_title,
         page_slug,
         page_content
     FROM pages
     WHERE page_slug = $pid
        ";

    $q = $db-&gt;query($sql);
    $q-&gt;setFetchMode(PDO::FETCH_ASSOC);

    $r = $q-&gt;fetch();
</code></pre>

<p>The data is put into html in following matter {$r['page_title']}</p>

<blockquote>
  <p>Paste for pages.php  <a href="http://pastebin.com/qA7zzvnY" rel="nofollow noreferrer">http://pastebin.com/qA7zzvnY</a></p>
  
  <p>Paste for Database.php <a href="http://pastebin.com/8pqXbzby" rel="nofollow noreferrer">http://pastebin.com/8pqXbzby</a></p>
</blockquote>

<p>Here is database tables
<img src="https://i.sstatic.net/Ryhb0.png" alt="enter image description here"></p>

<p>Known problem. </p>

<blockquote>
  <p>SELECT page_slug</p>
</blockquote>

<p>returns empty page, with no error or source code anywhere. </p>

<blockquote>
  <p>SELECT page_id</p>
</blockquote>

<p>returns the page truth pages.php?pid=zzzzzz or rewrite service/zzzzz.html I'm not sure why I can't pull page slug from database when I have done it in past with usernames and other random data. But in the provided $sql code it does not want to work.</p>

## Answers
### Answer ID: 29838596
<p>You need single quotes (or properly escaped double quotes) around <code>$pid</code> in the query. Also, as pointed out in the comments, you are wide open to SQL injection and need to address that immediately.</p>

