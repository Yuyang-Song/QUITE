# RewriteLock hangs Apache on re-start when added to an otherwise working Rewrite / Rewritemap
[Link to question](https://stackoverflow.com/questions/10883176/rewritelock-hangs-apache-on-re-start-when-added-to-an-otherwise-working-rewrite)
**Creation Date:** 1338820809
**Score:** 1
**Tags:** apache, mod-rewrite, virtualhost, rewritemap
## Question Body
<p>I am on a Network Solutions VPS, four domain names share the IP. I have a Rewrite / RewriteMap set up that works. The Rewrite is in the file for the example.com web address at var/www/vhosts/example.com/conf/vhost.conf, the Rewrite being the only thing in the vhost.conf file. It would not work in the main httpd.conf file for the server.</p>

<p>The RewriteMap uses a couple things in the URL typed in by the user (http://example.com/bb/cc) to get a third piece of info (aa) from the matching database record, uses that third piece of info as the query string to load a file, and leaves the originally typed in URL in the address bar while showing the file based on the query string aa.</p>

<p>Here is the Rewrite:</p>

<pre><code>Options +FollowSymlinks
RewriteEngine on
RewriteMap newurl "prg://var/www/cgi-bin/examplemap.php"
RewriteRule ^/(Example/.*) ${newurl:$1} [L]
</code></pre>

<p>When I add the following either above or below the RewriteMap line:</p>

<pre><code>RewriteLock /var/lock/mapexamplelock
</code></pre>

<p>and try to re-start Apache, it hangs and Apache will not re-start. I have tried different file paths (thinking it might be a permissions issue and just hoping it worked of course), taking away the initial /, putting it in quotes, different file types (ie. .txt at the end), different file names, just about anything, and every time it hangs Apache on re-start. The Rewrite / RewriteMap works without it, but I have read a lot on the importance of the RewriteLock, and php is issuing warnings in the log ending in DANGEROUS not to use RewriteLock.</p>

<p>Here is the map (located where the Rewrite says):</p>

<pre><code>#!/usr/bin/php
&lt;?php
include '/pathtodatabase';
set_time_limit(0);
$keyboard = fopen("php://stdin","r");
while (1) {
$line = fgets($keyboard);
if (preg_match('/(.*)\/(.*)/', $line, $igot)) {
$getalias = mysql_query("select aa FROM `table`.`dbase` WHERE bb = '$igot[1]' &amp;&amp; cc =     '$igot[2]'");
while($row=mysql_fetch_array($getalias)) {
$arid = $row['aa'];
}
print "/file-to-take-load.php?aa=$arid\n";
}
else {
print "$line\n";
}
}
?&gt;
</code></pre>

<p>I looked in the main httpd.conf file and there is nothing I can find about RewriteLock that might be interfering. It's just the standard one that came in the set-up of the VPS.</p>

<p>If anyone has an idea about why this would work only without RewriteLock and the possible fix, it would be greatly appreciated.</p>

<p>Thanks   Greg</p>

## Answers
### Answer ID: 12733217
<p>Apache hangs if you define more than one RewriteLock directives or if you use it in a VHOST config.<br />
<br />
The RewriteLock should be specified at server config level and ONLY ONCE. This lock file will be used by all prg type maps. So if you want to use multiple prg maps, I suggest using an internal locking mechanism, for example in PHP there is the flock function, and simply ignore the warning apache writes in the error log.<br />
<br />
See here for more info:<br />
<a href="http://books.google.com/books?id=HUpTYMf8-aEC&amp;lpg=PP1&amp;pg=PA298#v=onepage&amp;q&amp;f=false" rel="nofollow">http://books.google.com/books?id=HUpTYMf8-aEC&amp;lpg=PP1&amp;pg=PA298#v=onepage&amp;q&amp;f=false</a></p>

