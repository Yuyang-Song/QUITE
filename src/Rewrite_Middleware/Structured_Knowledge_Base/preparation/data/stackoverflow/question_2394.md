# How to run RESTful zend2 app on remote apache server?Error 404: URL not found on this server
[Link to question](https://stackoverflow.com/questions/32574485/how-to-run-restful-zend2-app-on-remote-apache-servererror-404-url-not-found-on)
**Creation Date:** 1442267273
**Score:** 1
**Tags:** php, apache, .htaccess, rest, zend-framework
## Question Body
<p>I am struggling with deploying my RESTful zend application to a remote apache server for couple of days. I know similar questions has been posted many times. But firstly I am completely new to server configuration world and secondly I've read and tried many of the solutions on those posts without any success. </p>

<p>The app is completely working on the localhost. On the remote server, however, the situation is different. After uploading the whole zend skeleton app to the var/www/html directory of the apache server, The public folder that contains all the front-end code can easily be accessed by this url : domain/myZendApp/public/pathToView. Nevertheless,this is firstly, unprofessional, and secondly I cannot access any of the zend RESTful endpoints that I have developed for my app. In the local host, for instance, the url I use for accessing the users list from the user controllers is like this: myZendApp.localhost/user.</p>

<p>As I said I have tried many solutions from <a href="https://stackoverflow.com/questions/5531655/how-to-deploy-and-run-a-zend-project-on-a-server">this post</a> or many other posts such as creating .htaccess in the root directory or inside the app directory as well as inside the public folder. After many changes, At the moment the .htaccess and index.php files are as below:</p>

<p>var/www/html/myZendApp/public/.htaccess:</p>

<pre><code>RewriteEngine On
# The following rule tells Apache that if the requested filename
# exists, simply serve it.
RewriteCond %{REQUEST_FILENAME} -s [OR]
RewriteCond %{REQUEST_FILENAME} -l [OR]
RewriteCond %{REQUEST_FILENAME} -d
RewriteRule ^.*$ - [NC,L]
# The following rewrites all other queries to index.php. The 
# condition ensures that if you are using Apache aliases to do
# mass virtual hosting, the base path will be prepended to 
# allow proper resolution of the index.php file; it will work
# in non-aliased environments as well, providing a safe, one-size 
# fits all solution.
RewriteCond %{REQUEST_URI}::$1 ^(/.+)(.+)::\2$
RewriteRule ^(.*) - [E=BASE:%1]
RewriteRule ^(.*)$ %{ENV:BASE}index.php [NC,L]
</code></pre>

<p>/var/www/html/whately2.0/.htaccess</p>

<pre><code>SetEnv APPLICATION_ENV development
RewriteEngine On
RewriteRule .* index.php
RewriteCond %{REQUEST_URI} =""
RewriteRule ^.*$ /public/app/index.php [NC,L]
RewriteCond %{REQUEST_URI} !^/public/.*$
RewriteRule ^(.*)$ /public/app/$1
RewriteCond %{REQUEST_FILENAME} -f
RewriteRule ^.*$ - [NC,L]
RewriteRule ^public/.*$ /public/index.php [NC,L]
</code></pre>

<p>/var/www/html/.htaccess</p>

<pre><code>RewriteEngine On  
RewriteBase /whately2.0/public  
RewriteCond %{REQUEST_FILENAME} -s [OR]  
RewriteCond %{REQUEST_FILENAME} -l [OR]  
RewriteCond %{REQUEST_FILENAME} -d  
RewriteRule ^.*$ - [NC,L]  
RewriteRule ^.*$ whately2.0/public/index.php [NC,L]  
</code></pre>

<p>var/www/html/myZendApp/public/index.php:</p>

<pre><code>&lt;?php

chdir(dirname(__DIR__));

// Decline static file requests back to the PHP built-in webserver
if (php_sapi_name() === 'cli-server') {
    $path = realpath(__DIR__ . parse_url($_SERVER['REQUEST_URI'],     PHP_URL_PATH));
if (__FILE__ !== $path &amp;&amp; is_file($path)) {
    return false;
}
unset($path);
}
require 'init_autoloader.php';
Zend\Mvc\Application::init(require 'config/application.config.php')-&gt;run();
</code></pre>

<p>I also created a virtual host pointing to the public folder of the app like below:</p>

<pre><code>&lt;VirtualHost&gt;
   ServerName domain/myZendApp
   DocumentRoot "/var/www/html/myZendApp/public"
   Options Indexes FollowSymLinks
   SetEnv APPLICATION_ENV "development"

    &lt;Directory "/var/www/html/myZendApp/public"&gt;
        DirectoryIndex index.php
        AllowOverride All 
        Order deny,allow
        Allow from all   
    &lt;/Directory&gt;
&lt;/VirtualHost&gt;
</code></pre>

<p>This solution did not work too. and when I want to reach (for example) domain/user I receive 404 error: The requested URL /user was not found on this server. </p>

<p>Now I am really frustrated and cannot find any other solution that I have not done. I will be very thankful if some one tells me how can I access the zend endpoints in the remote host. And please forgive me if I am missing some necessary information here and please let me know if you need more details. </p>

<p>Thanks in advance.</p>

<p>Updates:
After I edited the httpd.conf like below( AllowOverride All instead of  AllowOverride None):</p>

<pre><code>&lt;Directory "/var/www/html/whately2.0/public"&gt;
    AllowOverride All
    allow from all
    Options None
    Require all granted
&lt;/Directory&gt;
</code></pre>

<p>Now when I want to access the domain I get this error(403 forbidden):You don't have permission to access / on this server. 
(I am sure the permission is right)</p>

<p>If I want access domain/permalink again the same 403 error.</p>

<p>Note that before adding the 'AllowOverride All', I could access the domain that showed me the zend skeleton homepage but when I wanted to access domain/permalink(query from database like domain/user) I get the error 404.</p>

<p>Please help me: whatever I do this problem is not going away. I also added this line: LoadModule rewrite_module modules/mod_rewrite.so to the httpd.conf to enable mode-rewrite (Usually it is recommended to uncomment this line in httpd.conf file but I could not find it, so I added it to the code there)</p>

<p>Again: please someone help...</p>

<p>Thanks</p>

