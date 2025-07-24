# HTACCESS how do i battle with my code to get the right redirect
[Link to question](https://stackoverflow.com/questions/11040548/htaccess-how-do-i-battle-with-my-code-to-get-the-right-redirect)
**Creation Date:** 1339704209
**Score:** 0
**Tags:** php, .htaccess, url, mod-rewrite
## Question Body
<p>My HTACCESS file currently looks like this:</p>

<pre><code>RewriteEngine On        
RewriteBase /

# stop directory listings
#Options -Indexes 

#stops htaccess views
#&lt;Files .htaccess&gt;
#order allow,deny
#deny from all
#&lt;/Files&gt;        

# redirect game folders     
RewriteRule ^games/([^/]+)/([^/]+) games.php?author=$1&amp;slug=$2 [L]   

# redirect edit     
RewriteRule ^protected/edit-game/([^/]+)/([^/]+) protected/edit-game.php?author=$1&amp;slug=$2 [L] 
RewriteRule ^admin/edit-game/([^/]+)/([^/]+) admin/edit-game.php?author=$1&amp;slug=$2 [L]

# redirect view     
RewriteRule ^protected/view-game/([^/]+)/([^/]+) protected/view-game.php?author=$1&amp;slug=$2 [L]   

# redirect user
RewriteRule ^page/([^/]+) user.php?user=$1 [L]  

# remove .php; use THE_REQUEST to prevent infinite loops
RewriteCond %{THE_REQUEST} ^GET\ (.*)\.php\ HTTP
RewriteRule (.*)\.php$ $1 [R=301]     

# remove index
RewriteRule (.*)/index$ $1/ [R=301]

# remove slash if not directory
RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_URI} /$
RewriteRule (.*)/ $1 [R=301]

# add .php to access file, but don't redirect
RewriteCond %{REQUEST_FILENAME}.php -f
RewriteCond %{REQUEST_URI} !/$
RewriteRule (.*) $1\.php [L]   

ErrorDocument 404 /error-404.php
</code></pre>

<p>I have a new requirement to make it so when someone goes www.domain.com/im-a-page-in-database</p>

<p>It goes to my page.php, grabs the hidden 'slug' -> 'im-a-page-in-database' and queries the database returning that specific page object.</p>

<p>Thing is, if I add into my HTACCESS file something like this:</p>

<pre><code># redirect pages/posts 
RewriteRule ^([^/]+) page.php?slug=$1 [L]     
</code></pre>

<p>It just overwrites all the previous rewrites that may be successful and displays my page.php regardless of where it is placed in the htaccess file?? I thought L meant if the rule was recognised... it should stop trying to do stuff. so if i put my new line under all my redirects, it should do the page check last.. but nope :(</p>

<p>Any ideas?</p>

## Answers
### Answer ID: 11040638
<p>Maybe that's because of your 301-Redirect? The browser caches these redirects, so you'll have to try an other browser or clear your cache.</p>

