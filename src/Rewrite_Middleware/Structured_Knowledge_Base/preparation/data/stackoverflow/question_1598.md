# How can I store my Rewrite Rules in a database?
[Link to question](https://stackoverflow.com/questions/936539/how-can-i-store-my-rewrite-rules-in-a-database)
**Creation Date:** 1243887229
**Score:** 3
**Tags:** mysql, apache, .htaccess, url-rewriting
## Question Body
<p>Im developing a new site, and I'd like to store my rewrite rules in a database, instead of right in the .htaccess files.</p>

<p>I have another site that uses Opensef (<a href="http://sourceforge.net/projects/opensef/" rel="nofollow noreferrer">http://sourceforge.net/projects/opensef/</a>) with a Joomla! installation that is doing this, but im not even 100% how it works underneath the hood.</p>

<p>How can I store these rules in a database, query for them on request and rediret to the clean URL if found? Is there a better way to do this instead of loading up a .htaccess file (there may be 1000's of entries)?</p>

<p>Thank you,</p>

## Answers
### Answer ID: 988598
<p>What you probably want is a single rewrite rule to handle every unknown request that comes in and then pass that to a small script that will handle the lookups &amp; generate redirects.  You could even skip the rewrite rule completely and use the Apache <a href="http://httpd.apache.org/docs/2.0/mod/core.html#errordocument" rel="nofollow noreferrer">ErrorDocument directive</a> to pass unknown URLS into the script.</p>

<p>You've been pretty slim on the details of what this 'new site' is but, you might want to consider building yourself a <a href="http://en.wikipedia.org/wiki/Front_controller" rel="nofollow noreferrer">Front Controller</a> for the app &amp; having it take care of all the incoming URLs.  Many (most?) web app frameworks take this approach.</p>

### Answer ID: 987878
<p>Assuming all these pages are ultimately in Joomla, I think using .htaccess or mod_rewrite is a mistake.</p>

<p>I think you're much better off learning how Openserf works. I'd imagine it has a little piece of code that runs early on for every request that queries the database and issues a Redirect through PHP if there's a hit. A further advantage of this approach is that it should even be possible to have Joomla rewrite links on its pages to point to the clean version in the first place, saving the user an unneeded redirect </p>

<p>Incidentally, this is how the Pathauto module in Drupal does it, and I use that all the time on some pretty high volume sites with many thousands of pages.</p>

### Answer ID: 975390
<p>I think that the best approach to use rules stored in a database is:</p>

<ul>
<li>Store the rules in your database through your admin panel of your site.</li>
<li>Then after updating database, generate a new .htaccess using the rules in DB using your server-side language solution.</li>
<li>Replace old .htaccess with new one.</li>
</ul>

<p>This avoids the server load. It's similar to Aiden Bell solution.</p>

### Answer ID: 936562
<p>Grab the <a href="http://tuckey.org/urlrewrite/" rel="nofollow noreferrer">UrlRewriteFilter</a>, butcher it to use a DB, and use that in Tomcat instead of Apache.</p>

<p>Tomcat is a fine web server and can do many things Apache can do (like FastCGI for PHP), and writing stuff like this for it is trivial compared to writing such things for Apache.</p>

### Answer ID: 936561
<p>You can get mod_rewrite to generate a <strong>map from external source</strong> such as executing a PHP or Python file which can get the data from the database and create a mod_rewrite map.</p>

<p><a href="http://httpd.apache.org/docs/2.0/misc/rewriteguide.html" rel="noreferrer">http://httpd.apache.org/docs/2.0/misc/rewriteguide.html</a>
(See right at the bottom)</p>

<p>For example</p>

<pre><code>RewriteMap    quux-map       prg:/path/to/map.quux.pl
</code></pre>

<p><strong>Good Luck</strong></p>

