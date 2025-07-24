# url rewrite rules with php and mysql
[Link to question](https://stackoverflow.com/questions/34175874/url-rewrite-rules-with-php-and-mysql)
**Creation Date:** 1449655352
**Score:** 0
**Tags:** php, mysql, .htaccess, mod-rewrite, url-rewriting
## Question Body
<p>I am new in writing url rewrite rules. Can you help me in writing rewrite rules. My current browser url is </p>

<pre><code>http://localhost/live/match-page.php?mid=770&amp;sid=7
</code></pre>

<p>My anchor tag for that url is given below</p>

<pre><code>&lt;a target='_blank' href="match-page.php?mid=&lt;?php echo $rec-&gt;ID?&gt;&amp;sid=&lt;?php echo $rec-&gt;stream_id?&gt;" style="color:#ffae00;"&gt;  &lt;?php echo $rec-&gt;CatName; ?&gt; - &lt;?php echo $rec-&gt;Title; ?&gt; &lt;/a&gt;
</code></pre>

<p>How I edit <code>.htaccess file</code> then I show my browser url like given bellow here:</p>

<pre><code>http://www.cricmelive.tv/live/177/south-africa-v-india-test-live-streaming
http://www.cricmelive.tv/live/Basketball-live-streaming
</code></pre>

<p>how make anchor tage for url rewrite mode? </p>

<p>It is true that I made new queries for it? And pass to the database. If it is possible how do it.</p>

## Answers
### Answer ID: 34176576
<p>Add this code to htaccess file</p>

<pre><code> Options -MultiViews +FollowSymLinks
 RewriteEngine On
 RewriteRule ^/?live/([A-Za-z0-9-]+)/([A-Za-z0-9-]+)/?$ /match-page.php?mid=$1&amp;sid=$2 [L]
</code></pre>

<p>On match-page.php, you can get <code>mid</code> and <code>sid</code>, assuming you add url like <code>http://www.cricmelive.tv/live/770/7/Basketball-live-streaming</code></p>

<p><strong>EDIT</strong></p>

<p>Add this code to htaccess file</p>

<pre><code> Options -MultiViews +FollowSymLinks
 RewriteEngine On
 RewriteRule ^/?live/([0-9]+)/([0-9]+)/?$ /match-page.php?mid=$1&amp;sid=$2 [L]
</code></pre>

### Answer ID: 34176900
<p>What you are asking is how can you replace your current url patterns with a cleaner scheme (clean urls).</p>

<p>Your match page logic behind the scenes is most likely using 'mid' and 'sid' to do some kind of database lookup for the results.</p>

<p>Minimal change could be to change to a new url format like this:</p>

<pre><code>http://www.example.com/live/MID/SID/text-descriptor
http://www.example.com/live/770/7/south-africa-v-india-test-live-streaming
</code></pre>

<p>.htaccess</p>

<pre><code>RewriteEngine On
RewriteRule ^live/([0-9]+)/([0-9]+)/ match-page.php?mid=$1&amp;sid=$2 [L]
</code></pre>

<p>Then change your links to output the new pattern:</p>

<pre><code>$href = '/live/' . $rec-&gt;ID . '/' . $rec-&gt;stream_id . '/' . $rec-&gt;text; // text from category or title (isn't needed by script.)
</code></pre>

### Answer ID: 34176559
<p>I hope these help. I'm a little confused though, you say you need both <code>mid</code> &amp; <code>sid</code> yet the examples above are different ~ one has both the <code>mid</code> and <code>sid</code> parameters yet the other only has one, presumably <code>sid</code></p>

<pre><code>#htaccess

RewriteEngine On
RewriteBase /

RewriteRule ^live/(.+)$ live/match-page.php?sid=$1 [NC,L]
RewriteRule ^live/([0-9]+)/(.+)$ live/match-page.php?mid=$1&amp;sid=$2 [NC,L]


/* php */
/* Match first style rewrite rule */
echo "&lt;a target='_blank' href='/live/{$rec-&gt;stream_id}' style='color:#ffae00;'&gt;  {$rec-&gt;CatName} - {$rec-&gt;Title} &lt;/a&gt;";

/* match second style rewrite rule */
echo "&lt;a target='_blank' href='/live/{$rec-&gt;ID}/{$rec-&gt;stream_id}' style='color:#ffae00;'&gt;  {$rec-&gt;CatName} - {$rec-&gt;Title} &lt;/a&gt;";
</code></pre>

<p>There are two ways in which you can use <code>urlrewrite</code> - one as shown here where you generate your links as shown to match the pattern set in the rewrite rule and the other method is to use the links as you had them originally and use apache to make the ugly querystring into the new, pretty url. For examples of how to do the latter, have a look at some of the posts by <a href="https://stackoverflow.com/users/548225/anubhava">Anubhava</a> ~ he is a master!</p>

