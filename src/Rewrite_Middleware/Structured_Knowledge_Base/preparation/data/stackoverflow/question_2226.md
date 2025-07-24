# Use URL segments as jQuery $.post variables
[Link to question](https://stackoverflow.com/questions/24970477/use-url-segments-as-jquery-post-variables)
**Creation Date:** 1406373590
**Score:** 1
**Tags:** php, jquery, post, url-rewriting
## Question Body
<p>I would like to be able to use jQuery $.post with url segments as follows:</p>

<pre><code>www.mysite.com/stats/user1
</code></pre>

<p><code>www.mysite.com/stats</code> is the landing page, with this code on it:</p>

<pre><code>var user = //get user1 from the url;

$.post('stats.php', {username : user}, function(results){...});
</code></pre>

<p>The username should be posted to a PHP backend which then does some database querying.</p>

<p>Is this possible? I might be able to use .htaccess to redirect users from <code>stats/user1</code> to <code>stats/</code>, but I don't have much experience in this area.</p>

<p>Many thanks in advance for your help.</p>

<hr>

<p><strong>EDIT</strong></p>

<p>In response to Loopo's answer:</p>

<p>I can use <code>.htaccess</code> to rewrite incoming URLs as follows:</p>

<p><code>RewriteRule ^/stats/(.*)$ stats.php?username=$1 [L]</code>.</p>

<p>This would allow me to enter a URL such as <code>mysite.com/stats/user123</code>, which the server would interpret as <code>mysite.com/stats?username=user123</code></p>

<p>In <code>stats.php</code> can I then use <code>$user = $_GET['username']</code>?</p>

## Answers
### Answer ID: 24970983
<p>It seems you are mixing some concepts up. </p>

<p>If you want to pass data to a webserver, you can do it in two ways; POST or GET. (There is also PUT and DELETE but we'll ignore that here.)</p>

<p>If you are using a GET request, the data is in the URL, normally in a format like</p>

<pre><code>mysite.com/mypage.php?param1=value1&amp;param2=value2....
</code></pre>

<p>the slashes normally act as a path separator to tell the webserver where to look for the resource that answers the request. </p>

<pre><code>mysite.com/myapp/myfolder/resources/logo.png
</code></pre>

<p>would tell the server where to find and then send the file <code>logo.png</code> to the client.</p>

<p>If you want to have parameters in the path, you can also use redirection (.htaccess) to have virtual resources.</p>

<p>as in your example.</p>

<pre><code>www.mysite.com/stats/user1
</code></pre>

<p>there is no stats folder with a script for every user. </p>

<p>You'll have to tell your webserver when someone asks for some path that looks like<br>
<code>/stats/&lt;something&gt;</code><br>
the request should be served by some script (probably 'stats.php') and the parameters that are passed to the script will be <code>&lt;something&gt;</code></p>

<p>in your .htaccess this might look like:</p>

<pre><code> RewriteRule ^/stats/(.*)$ stats.php/$1 [L]
</code></pre>

<p>In a POST request the parameters are not visible in the url. </p>

<p>So your stats.php would have to be called without the username in the URL, but instead in the POST variables, i.e. in your case POSTing to stats.php/user1 and then including the username again in the POST variables is redundant.</p>

<p>So your stats.php could deal with a POST request by reading in the parameters and creating/updating a new user with the values provided in the POST parameters, while dealing with GET requests by returning the user's stats as they are now.</p>

<p>What I am describing is <a href="https://stackoverflow.com/q/671118/32763">REST</a>, see <a href="http://www.lornajane.net/posts/2012/building-a-restful-php-server-understanding-the-request" rel="nofollow noreferrer">also</a></p>

