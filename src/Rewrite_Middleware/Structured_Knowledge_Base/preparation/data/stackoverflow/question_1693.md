# Apache: mod_rewrite: Spcaes &amp; Special Characters in URL not working
[Link to question](https://stackoverflow.com/questions/4215673/apache-mod-rewrite-spcaes-special-characters-in-url-not-working)
**Creation Date:** 1290089736
**Score:** 1
**Tags:** apache, mod-rewrite, special-characters, urlencode
## Question Body
<p>i am using APACHE:mod_rewrite to define a set of rules for rewritting URLS</p>

<p>i want this link&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;to be displayed as</p>

<p><code>/myDIR/walls.php?f=All&amp;of=0&amp;s=Newest</code> -> <code>All.html</code></p>

<p>so i am using the following rule </p>

<p><em>text from (.htaccess)</em></p>

<pre><code>RewriteEngine  on
RewriteBase    /myDIR/   
RewriteRule ^All\.html$  papers.php?f=All&amp;of=0&amp;s=Newest
</code></pre>

<p>now these variables that are being passed as 
<code>f=All</code> <code>of=0</code> <code>s=Newest</code> these are being used in query, OBVIOUSLY, and one of these variables, i.e <code>f</code> sometimes has values with spaces and special characters, and i can't avoid that because the database is already in-place and all i am doing rewrite of URLs....</p>

<p>NOW when i try to define a rule like this</p>

<p>i want this link&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;to be displayed as</p>

<p><code>/myDIR/walls.php?f=Characters &amp; Supers&amp;of=0&amp;s=Newest</code> -> <code>Characters &amp; Supers.html</code></p>

<p>which is wrong i know because there shouldn't be any spaces.. so to make it right i define the rule like this</p>

<pre><code>RewriteRule ^Characters%20%26%20Supers\.html$  papers.php?f=Characters%20%26%20Supers&amp;of=0&amp;s=Newest
</code></pre>

<p>it lets me define the rule but when i click my link i get this
<strong>404 Not Found Error "The requested URL /wallz/Characters &amp; Supers.html was not found on this server."</strong></p>

<p><strong>QUESTION:</strong> WHAT To Do ?</p>

<p>my guess is i am not supposed to be doing HTML URL Encoding inside .htaccess</p>

## Answers
### Answer ID: 4234123
<p>Your guess is correct. By the time that a URL has reached mod_rewrite for processing, Apache has already decoded the URL for you. Therefore, if you want to check for any otherwise-encoded characters, you need to use their literal representations.</p>

<p>Since whitespace is used as a delimiter here, you'd also need to escape your spaces:</p>

<pre><code>RewriteRule ^Characters\ &amp;\ Supers\.html$ papers.php?f=%0&amp;of=0&amp;s=Newest
</code></pre>

<p>I believe that using quotation marks will also work, so the following should be equivalent (though it's untested):</p>

<pre><code>RewriteRule "^Characters &amp; Supers\.html$" papers.php?f=%0&amp;of=0&amp;s=Newest
</code></pre>

<p>A final note about Apache's decoding process is that it will automatically remove multiple slashes for you. While not relevant for your example, it's another example of how the URL is transformed prior to reaching your mod_rewrite rules.</p>

