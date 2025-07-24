# WordPress with phpMyAdmin - 404&#39;s everywhere
[Link to question](https://stackoverflow.com/questions/6169170/wordpress-with-phpmyadmin-404s-everywhere)
**Creation Date:** 1306689440
**Score:** 5
**Tags:** wordpress, plugins, phpmyadmin, http-status-code-404
## Question Body
<p>So I've been trying to make several changes to a custom WordPress theme which introduces an entire overhaul of the Dashboard. I keep finding little issues with the original theme that I need to fix (not properly checking for duplicate posts when you import new ones, post metadata not getting stored correctly, posts not getting sorted into their proper categories, etc.)</p>

<p>As I've been working with this I've needed to look at and modify the database countless times to either see what the theme is doing to the database or fix things it screwed up. Unfortunately I was unable to install phpMyAdmin so I've been making changes by directly typing SQL and inserting it into the theme in appropriate places, then having the script <code>die()</code> so I can see the output of my SQL.</p>

<p>Suddenly it hit me that I could find a plugin which integrates phpMyAdmin functionality into WordPress. So I installed wp-phpMyAdmin.</p>

<p>Everything seems to be going well until I try to actually <strong>DO</strong> anything. I can view the tables, view the rows, and look at everything. But when I try to edit a row or delete a row I get redirected to a 404 error, saying that whichever part of phpMyAdmin I happened to be accessing (for example, <code>tbl_row_action.php</code>) doesn't exist. If I go directly to these pages without submitting the form to edit or delete a row then they work just fine and I receive an error message that my SQL query was blank.</p>

<p>Has anyone else experienced this? I really can't figure out exactly why or where it's sending a 404. It's absolutely ridiculous.</p>

<p>EDIT - A little further information:</p>

<p>I've learned that I <strong>only</strong> get a 404 error when phpMyAdmin calls <code>sql.php</code> with the <code>sql_query</code> parameter set</p>

<p>EDIT (again) - One further update:</p>

<p>I only get the 404 error when sql_query contains a valid query. Looking through <code>sql.php</code> (I haven't spent TOO much time looking, mind you) I do notice that it seems to parse the query and determine if you're <code>SELECT</code>ing, <code>DROP</code>ing, <code>DELETE</code>ing, etc. so they can check your user permissions. It may be related to this parsing code.</p>

<p>The following queries did not give me a 404:</p>

<pre><code>test
SELECT test
SELECT test FROM test
SELECT test FROM post_meta
DELETE
DROP
DROP test
</code></pre>

<p>The following gave me a 404:</p>

<pre><code>SELECT * FROM test
SELECT * FROM post_meta
DELETE FROM
DELETE FROM test
DELETE FROM post_meta
DROP TABLE
DROP TABLE test
</code></pre>

<p>MORE EDITS -</p>

<p>So at the very top of sql.php I placed this line of code:</p>

<pre><code>die("Test");
</code></pre>

<p>It doesn't die when I make the bad queries listed above. It goes straight to the 404 message. Clearly this is something to do with WordPress's redirect script and not with phpMyAdmin</p>

<p>FINAL EDITS - </p>

<p>I've done a lot more research and been grep'ing the heck out of WordPress.</p>

<p>I highly suspect that I am having this issue as the result of some new WordPress security feature. Older versions of WordPress apparently used to allow SQL to be input into URL's, which posed a HUGE security risk. As a result it's understandable that they wouldn't allow SQL to be passed through URL's now. Just before the template the value of <code>is_404()</code> is being set to true. It's being set within <code>WP::parse_request()</code> (which is called by <code>WP::main()</code> which is called by <code>wp()</code> which is called within <code>wp-blog-header.php</code>)</p>

<p>Any time there is a suspected SQL query <strong>ANYWHERE</strong> in the requested URI, I get kicked to a 404 page. I would like to change this behavior while making as few modifications to WordPress core as possible. I need someone who is really good with WordPress to help me here. I presume an answer exists involving the $wp_rewrite variable, which contains a multitude of URL rewrite rules.</p>

<p>PROBLEM FINALLY DISCOVERED - </p>

<p>For anyone interested who finds this post or was following it or simply had similar issues, I finally located the source of the 404 errors. It didn't lie with WordPress at all. The problem fell to mod_security, an Apache module which prevents any requests that look suspicious (including those with SQL in the request URI)</p>

<p>Always remember to set your mod_security settings properly.</p>

## Answers
### Answer ID: 6415748
<p>WordPress shouldn't be interfering with phpMyAdmin, since the plugin loads it in a isolated iframe.</p>

<blockquote>
  <p>As one of his specifications for the project he wants ONLY WordPress installed on his server...</p>
</blockquote>

<p>The plugin is, nonetheless, still <em>phpMyAdmin</em> (albeit 'wrapped' in the WordPress UI). In other words, <em>you've already installed it</em> ;)</p>

<blockquote>
  <p>...to avoid the hassle of updating and maintaining other software...</p>
</blockquote>

<p>'Software' can be a dangerous term when talking web-apps - that's not to say don't use it <em>at all</em>, but for some it can conjure up thoughts of blue screens and runtime errors ;)</p>

<p>In other words, just stress that PMA is simply a collection of files on the server - it has no database of it's own, it's effectively stateless, and removal is as simple as <code>RMD /phpmyadmin</code>.</p>

<blockquote>
  <p>...he wants to be able to make all necessary administrative changes from the WordPress Dashboard</p>
</blockquote>

<p>Despite the points I've already made, if it is <em>absolutely</em> essential that there is database management access within the dashboard, I'm about to write a quick alternative that uses <a href="http://phpminiadmin.sourceforge.net/" rel="nofollow">phpMiniAdmin</a> instead  (that's how I stumbled on this question oddly!), and I'd be happy to share it for you to try out.</p>

### Answer ID: 6409683
<p>As @molnarm pointed out in the comments, why not just removed phpMyAdmin and connect to MySQL over SSH, using something like <a href="http://wb.mysql.com/" rel="nofollow">MySQL Workbench</a> or <a href="http://www.sequelpro.com/" rel="nofollow">Sequel Pro</a>. </p>

<p>You would have a much easier and faster way to interact with MySQL and could delete the nightmare that is phpMyAdmin.</p>

