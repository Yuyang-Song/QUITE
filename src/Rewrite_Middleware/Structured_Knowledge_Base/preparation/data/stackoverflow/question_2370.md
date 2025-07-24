# Using mod rewrite to use urls without query strings
[Link to question](https://stackoverflow.com/questions/31567339/using-mod-rewrite-to-use-urls-without-query-strings)
**Creation Date:** 1437578345
**Score:** -1
**Tags:** php, apache, .htaccess, mod-rewrite
## Question Body
<p>I am trying to use mod rwerite but I simply cant figure it out...</p>

<p>The way I understand it, the following should be possible:</p>

<p>When a user clicks on a link like this <code>&lt;a href="/contents/folder/somepage_17"&gt;Linktext&lt;/a&gt;</code> then I should be able to make the server believe that I want <code>/contents/folder/somepage.php?id=17</code> and then access the query string via <code>$_GET</code> in the somepage.php file, right?</p>

<p>If so, how would I put that in mod rewrite syntax? Also, I have lots of pages that have dashes in their names, so I'd have quite a high number of URLs like this <code>this-is-a-page_19</code>.</p>

<p>Currently, all my URLs have the query string already in them (like <code>/abc/de/page.php?id=12</code>) but I'd like to have URRLs without query string. However, I need some kind of information, which page is being called because I then access a database to get some information about that page (title, keywords, description,...).</p>

<p>Help highly appreciated!</p>

## Answers
### Answer ID: 31568207
<p>This might work</p>

<pre><code>RewriteEngine On
RewriteBase /
RewriteRule ^contents/folder/somepage_([0-9]+)$ /contents/folder/somepage.php?id=$1 [NC,L]
</code></pre>

<p>And you can then access the GET var using $_GET['id']</p>

