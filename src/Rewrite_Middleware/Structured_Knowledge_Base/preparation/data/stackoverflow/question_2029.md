# AJAX URL requests in Drupal 7 on localhost Apache2 don&#39;t include base URL or base path
[Link to question](https://stackoverflow.com/questions/16508879/ajax-url-requests-in-drupal-7-on-localhost-apache2-dont-include-base-url-or-bas)
**Creation Date:** 1368372268
**Score:** 0
**Tags:** javascript, ajax, drupal, mod-rewrite, drupal-7
## Question Body
<p>I am currently stuck with a problem in my local Drupal 7 environment. As Drupal 7 site configurations can get very complex, I will try to explain my problem in as much details as possible.</p>

<p>The site sits in a sub folder in my local environment, I have more projects running on my localhost, so preferably I would like to keep the projects separated. In addition, for this site I have two separate folders, one for development and one for production that share the same database, so a solution by adding fake domains would not work here I think (correct me if I'm wrong).</p>

<p>So the main problem seems to be that AJAX requests don't include the base URL or base path and I can't login on <code>http://localhost/mysite/devel/docroot/user</code> because the AJAX request would go to <code>http://localhost/system/ajax</code> or <code>http://localhost/ajax_register/login/ajax</code> and therefore would not return the correct JSON response.</p>

<p>How can this be solved? Are configurations in Apache's <code>httpd.conf</code> or <code>.htaccess</code> enough to make this work?</p>

<p>Here's what I did so far, first in <code>settings.php</code>:</p>

<pre><code>$base_url = 'http://localhost/mysite/devel/docroot';
$base_path = '/mysite/devel/docroot/';
</code></pre>

<p>Next, I've tried the following with rewrite rules in <code>httpd.conf</code>:</p>

<pre><code>&lt;IfModule mod_rewrite.c&gt;
    RewriteEngine on
    RewriteCond %{HTTP_REFERER} .*devel.*$ [OR]
    RewriteRule ^/sites/(.*)$ /mysite/devel/docroot/sites/$1
    RewriteRule ^/system/(.*)$ /mysite/devel/docroot/system/$1
    RewriteRule ^/ajax_register/(.*)$ /mysite/devel/docroot/ajax_register/$1
&lt;/IfModule&gt;
</code></pre>

<p>Here I got the following pop up with HTML (that seems to be from <code>index.php</code>) in the response text instead of the expected JSON response:</p>

<pre><code>An AJAX HTTP error occurred.
HTTP Result Code: 404
Debugging information follows.
Path: http://localhost/ajax_register/login/ajax
StatusText: error
ResponseText: lots of HTML...
</code></pre>

<p>Then without rewrite rules but using proxies instead in <code>httpd.conf</code>:</p>

<pre><code>&lt;IfModule mod_proxy.c&gt;

    ProxyRequests Off
    ProxyPreserveHost On

    &lt;Proxy *&gt;
        Order deny,allow
        Allow from all
    &lt;/Proxy&gt;

    RewriteEngine on

    ProxyPass /system/ http://localhost/mysite/devel/docroot/system/
    ProxyPassReverse /system/ http://localhost/mysite/devel/docroot/system/
    &lt;Location /system/&gt;
        Order allow,deny
        Allow from all
    &lt;/Location&gt;

    ProxyPass /ajax_register/ http://localhost/mysite/devel/docroot/ajax_register/
    ProxyPassReverse /ajax_register/ http://localhost/mysite/devel/docroot/ajax_register/
    &lt;Location /ajax_register/&gt;
        Order allow,deny
        Allow from all
    &lt;/Location&gt;

&lt;/IfModule&gt;
</code></pre>

<p>For the proxy directives, a similar 404 not found error was given for the POST AJAX request, except that now the response text is in JSON format.</p>

<pre><code>An AJAX HTTP error occurred.
HTTP Result Code: 404
Debugging information follows.
Path: http://localhost/ajax_register/login/ajax
StatusText: error
ResponseText: some JSON code...
</code></pre>

<p>Without both the rewrite rules and the proxy directives I get the following error in the JavaScript pop up:</p>

<pre><code>An AJAX HTTP error occurred.
HTTP Result Code: 404
Debugging information follows.
Path: http://localhost/ajax_register/login/ajax
StatusText: error
ResponseText: 
404 Not Found
Not Found
The requested URL /ajax_register/login/ajax was not found on this server.
</code></pre>

<p>Finally in <code>.htaccess</code> I've tried to rewrite the base to the following:</p>

<pre><code>RewriteBase /mysite/devel/docroot/
</code></pre>

<p>and here I get the same 404 error as was the case when both the rewrite rules and proxy directives are commented out in <code>httpd.conf</code>. I would also like to add that in the database, in the table <code>languages</code> I've set the domain for the English language to <code>localhost</code>.</p>

<p>I don't understand, why is the base not included in front of the AJAX URL requests? And how can I add it? When I query <code>Drupal.settings.basePath</code> in Firebug I do get the value that I've set in <code>settings.php</code> :S - Does someone have any ideas?</p>

## Answers
### Answer ID: 16509933
<p>There are many solutions for your problem, but I'm gonna try to focus on the most mature one. I assume you are using windows as your environment.</p>

<p>You said you were running your projects on localhost, which is where your first mistake is.</p>

<p>Localhost is nothing but a form of weird domain name you specify. When you request a domain like "www.google.com" or "localhost" the following steps occur:</p>

<ol>
<li>The browser checks a specific file for the requested domain. This file is called <a href="https://en.wikipedia.org/wiki/Hosts_%28file%29" rel="nofollow">hosts file</a></li>
<li>If the domain name is found in the hosts file, the browser sends a request to the IP address specified in the hosts file</li>
<li>If the domain name is not found in the hosts file, the browser queries domain name servers which return the corresponding IP adress.</li>
</ol>

<p>Now localhost is nothing but a domain name specified in your hosts file, which points to the loopback address.(127.0.0.1).</p>

<p>So the magic trick here is to bind your custom hosts like "project1", "project2" etc.. to that loopback adress(127.0.0.1).</p>

<p>Than when you send a request to "project1" in your browser, the server running on port 80 will respond as if you typed "localhost".</p>

<p>The second part you need to take care of is called <a href="http://httpd.apache.org/docs/2.2/vhosts/" rel="nofollow">virtual hosts</a>. When you send a request with a specific domain name, a special header is included in your http request called "Host". </p>

<p>Lets assume, that you redirect all this custom domains to the same IP (127.0.0.1). In order for apache to serve a different project, you should instruct apache to look at the "Host" header and resolve it for the corresponding project.</p>

<p>Again you do that by setting <a href="http://httpd.apache.org/docs/2.2/vhosts/examples.html" rel="nofollow">virtual hosts</a>.</p>

<p>A lot of frameworks and content managing systems in PHP have some ugly ways to insert some magic "$BASE_PATH" variable, which is a bad practice as that could be achieved with relative paths in pure html and a properly configured server.</p>

