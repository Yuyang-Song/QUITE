# Setting the http_response_code() in PHP after using header() prevents the page from loading
[Link to question](https://stackoverflow.com/questions/57478054/setting-the-http-response-code-in-php-after-using-header-prevents-the-page-f)
**Creation Date:** 1565700468
**Score:** -3
**Tags:** php, header, http-response-codes
## Question Body
<p>I'm using a php script to send users from mysite.com/id=123 to mysite.com/my-id-title</p>

<p>I could use .htaccess file to rewrite the URL (which is -of course the natural solution- but given that the replacement information for the url is not in the original parameter provided by the url, but requires a database query (as you can see in the example) I cannot do that with just mod_rewrite. 
And to make matters more difficult, I do not have access to Apache, I can just use the .htaccess.</p>

<p>So, I thought, as a workaround, to generate a rule though php, which does work using header('Location:'.$reenvioA);</p>

<p><strong>The problem is that PHP generates a 302 response code, instead of 200. A 200 response is what I need to create a sitemap and for SEO reasons.</strong></p>

<p><a href="https://i.sstatic.net/upNmh.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/upNmh.png" alt="enter image description here"></a></p>

<p>So, in order to prevent that, I thought about telling php that I want a 200 code, so I force it. </p>

<p>I've tried quite a few ways:</p>

<pre><code>header("HTTP/1.1 200 OK");
header('Location:'.$reenvioA);
</code></pre>

<p>Maybe forcing it before and after the Location header?</p>

<pre><code>header("HTTP/1.1 200 OK");
header('Location:'.$reenvioA);
header("HTTP/1.1 200 OK");
</code></pre>

<p>And then I've tried doing it <a href="https://www.php.net/manual/en/function.header.php" rel="nofollow noreferrer">using their optional arguments</a>: </p>

<pre><code>header('Location:'.$reenvioA, false, 200);
</code></pre>

<p>Maybe just letting the second argument remain true?</p>

<pre><code>header('Location:'.$reenvioA, true, 200);
</code></pre>

<p>And then just setting the variable with the response itself: </p>

<pre><code>header('Location:'.$reenvioA);
http_response_code(200);
</code></pre>

<p>So far, none has worked, because as soon as I forced the response, the page won't load. It seems that php won't fetch the page, even when the response code is set after header(Location:url).
<a href="https://i.sstatic.net/99LHW.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/99LHW.png" alt="enter image description here"></a></p>

<p><strong>What can I do?</strong></p>

## Answers
### Answer ID: 57478414
<p>You can't do that, since you are redirecting you can only use 3xx response codes, any response code not in the 3xx range will not work.</p>

<p>(If its a option you can use JS to redirect and get a 200 without changing any headers)</p>

