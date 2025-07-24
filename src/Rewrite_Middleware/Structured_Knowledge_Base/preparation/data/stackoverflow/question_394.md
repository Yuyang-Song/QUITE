# WordPress links all redirect to double URL
[Link to question](https://stackoverflow.com/questions/24297263/wordpress-links-all-redirect-to-double-url)
**Creation Date:** 1403139975
**Score:** 12
**Tags:** mysql, wordpress, .htaccess
## Question Body
<p>A fellow developer built a WordPress website on his local machine. He then migrated the whole installation onto a server. Naturally, all the links in sql were set to <code>localhost:8888</code>. I then ran a SQL update to fix the links so they pointed to the correct domain (which right now is an <code>ipaddress/~username</code> link). I've double checked my work, and it all looks correct.</p>

<pre><code>UPDATE wp_options SET option_value = replace(option_value, 'http://olddomain.com', 'http://newdomain.com');
UPDATE wp_options SET option_value = replace(option_value, 'feed://www.olddomain.com', 'feed://newdomain.com');
UPDATE wp_posts SET guid = replace(guid, 'http://olddomain.com','http://newdomain.com');
UPDATE wp_posts SET post_content = replace(post_content, 'http://olddomain.com', 'http://newdomain.com');
UPDATE wp_postmeta SET meta_value = replace(meta_value, 'http://olddomain.com', 'http://newdomain.com');
</code></pre>

<p>I used that coding, but with the appropriate domain information in there.</p>

<p>So now here’s what’s happening.</p>

<p>Whenever I go to the homepage, it works, but the images don't show up. then i click on a link, or travel to teh wp-admin, and it shows the url twice in the urlbar. so it goes to something like:</p>

<pre><code>http://newdomain.com/~user/http://newdomain.com/~user/post-name-blah-blah-blah
</code></pre>

<p>the <code>.htaccess</code> file is all default, (if WordPress is in a subdirectory should it have a rewrite rule for that instead of just /?)</p>

<p>What could cause every link on the site to go to the same url twice, if none of them are listed like that in SQL?</p>

<p>UPDATE:</p>

<p>Alright, so I erased the whole database and reset that up, and then the site works fine. of course that means I lose all my content. I'm guessing i screwed up the sql query's somewhere down the line. But I can't find anywhere that has two urls, or would even cause this. More updates coming as I figure out my issue.</p>

## Answers
### Answer ID: 45749846
<p>Put <code>http://</code> in front of <code>site_url</code> and <code>Home_url</code> in the <code>wp_option</code> table of your database.</p>

### Answer ID: 24315540
<p>I Solved it! Hopefully if anyone else comes here and has the same mistake, this will help. In the <code>wp_options</code> table the rows for <code>site_url</code> and <code>home</code> need to have <code>http://</code> in front of them. Somehow on my, my sql query busted that portion. Of course I didn't notice because the address looked correct, because that normally works. but in this case it caused a never-ending loop with some links, and in others just doubled the address.</p>

### Answer ID: 24297303
<p>While doing the database adjustments you did might work, I find them to be problematic. Instead whenever one moves a WordPress site, you need to properly adjust configurations in your WordPress install in the <code>wp-config.php</code> file on the following variables:</p>

<pre><code>define('WP_SITEURL', 'http://newdomain.com/wordpress');
define('WP_HOME', 'http://newdomain.com/');
define('WP_CONTENT_DIR', '/path/to/your/wordpress/wp-content');
define('WP_CONTENT_URL', 'http://newdomain.com/wp-content');
</code></pre>

<p>This will force your install to use the <code>newdomain.com</code> URLs.  Also, when you do this the first time set the <code>RELOCATE</code> setting to <code>true</code> like this:</p>

<pre><code>define('RELOCATE', true);
</code></pre>

<p>That basically tells WordPress to rejigger (that’s my technical term for it) it’s stored settings for the new settings. And after you have reloaded your site &amp; it works as expected, set <code>RELOCATE</code> setting back to <code>false</code> like this:</p>

<pre><code>define('RELOCATE', false);
</code></pre>

<p>But you also say this:</p>

<blockquote>
  <p>(if WordPress is in a subdirectory should it have a rewrite rule for
  that instead of just /?)</p>
</blockquote>

<p>That has to change if you are placing WordPress in a subdirectory. So let’s assume that WordPress is in a subdirectory called <code>coolsite/</code>. Then change the default WordPress <code>.htaccess</code> from this:</p>

<pre><code># BEGIN WordPress
&lt;IfModule mod_rewrite.c&gt;
  RewriteEngine On
  RewriteBase /
  RewriteRule ^index\.php$ - [L]
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteRule . /index.php [L]
&lt;/IfModule&gt;
# END WordPress
</code></pre>

<p>To this; note the way I changed the <code>RewriteBase</code> &amp; the last <code>RewriteRule</code>:</p>

<pre><code># BEGIN WordPress
&lt;IfModule mod_rewrite.c&gt;
  RewriteEngine On
  RewriteBase /coolsite/
  RewriteRule ^index\.php$ - [L]
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteRule . /coolsite/index.php [L]
&lt;/IfModule&gt;
# END WordPress
</code></pre>

