# Changing url with .htaccess loses content
[Link to question](https://stackoverflow.com/questions/17210435/changing-url-with-htaccess-loses-content)
**Creation Date:** 1371721494
**Score:** 0
**Tags:** php, .htaccess
## Question Body
<p>I am making a simple CMS, so the page links are <code>domain/index.php?page=1</code> and so on (page2, page3...), and I am pulling the content out of the database with the following line:</p>

<pre><code>$q = "SELECT name, content FROM pages WHERE page_id=$page";
</code></pre>

<p>That all works, but I wanted to change the look of the URLs, so I did with the following in .htaccess</p>

<pre><code>RewriteRule ^([A-Za-z]+)/?$    index.php?page=$1    [NC,L]
</code></pre>

<p>The problem is, now when I click on the page I changed the url (in this case it was ?page=2), I don't pull the content out of the db, I guess because the MySQL query cant find <code>$page</code></p>

<p>How do I remedy this? </p>

<p><strong>EDIT:</strong></p>

<p>I updated the rule to include numeric characters as well but it is still the same.</p>

<pre><code>RewriteRule ^([A-Za-z0-9]+)/?$    index.php?page=$1    [NC,L]
</code></pre>

<p><strong>EDIT2:</strong></p>

<p>Just to hammer the point home, if I for example hardcode <code>page=2</code> in the rewrite rule it works, but obviously I want that to happen dynamically. In this case <code>$1</code> should become <code>2</code>.</p>

## Answers
### Answer ID: 17210486
<p>Are you sure</p>

<pre><code>$q = "SELECT name, content FROM pages WHERE page_id=$page";
</code></pre>

<p>is directly taken from your code? It has a few quite severe problems:</p>

<ul>
<li>You probably (and rightfully so) do not have <code>register_globals</code> enabled. So <code>$page</code> should actually be <code>$_GET['page']</code>.</li>
<li>Your query is prone to attacks, you should always <code>mysql_real_escape_string()</code> parameters going into your queries.</li>
<li>A user could enter non-numeric values. Those would not be catched but would probably end up in syntax errors.</li>
</ul>

<p>My advice? There is no point in writing all this stuff yourself. Instead use an existing modern CMS or framework. 99% of the mistakes and security holes you'd end up creating have been taken into account in them already.</p>

