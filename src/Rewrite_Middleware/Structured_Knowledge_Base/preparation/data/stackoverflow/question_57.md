# Combining URI_REQUEST and HTTP_HOST in an .htaccess file
[Link to question](https://stackoverflow.com/questions/11460341/combining-uri-request-and-http-host-in-an-htaccess-file)
**Creation Date:** 1342125837
**Score:** 1
**Tags:** php, .htaccess, codeigniter, mod-rewrite, url-shortener
## Question Body
<p>I'd like to do link shortening using PHP and Apache/.htaccess.</p>

<p>Here's how a link on my site looks:</p>

<p><a href="https://mysite.com/item/this-is-a-book-on-toasters" rel="nofollow">https://mysite.com/item/this-is-a-book-on-toasters</a></p>

<p>Here's how I'd like the shortened link to look for the above link.</p>

<p><a href="https://ms.co/Im8y2x" rel="nofollow">https://ms.co/Im8y2x</a></p>

<p>Currently, this is what I have in my .htaccess file:</p>

<pre><code>RewriteCond %{HTTP_HOST} ^ms\.co$ [NC]
RewriteCond %{HTTPS} =on
RewriteRule ^(.*)$ https://mysite.com/item/$1 [L,R=301]
</code></pre>

<p>So going to ms.co does redirect to mysite.com. My problem is that my PHP code at mysite.com/item has no knowledge of the 6 digit string (in this case, <code>Im8y2x</code>) so I can't query my database for the 6 digit string's matching URI (in this case, <code>/this-is-a-book-on-toasters</code>).</p>

<p>I know I need something added to my .htaccess Rewrite rules I'm just not sure what it is. Might someone be able to help?</p>

## Answers
### Answer ID: 11480238
<p>I figured out my own question. If you just leave out <code>R=301</code> then you'll preserve the URI (in this case, <code>Im8y2x</code>) and then you can access it with your scripting language (in my case, PHP) to redirect it to the full length URI.</p>

<p>So <strong>instead</strong> of this: </p>

<pre><code>RewriteRule ^(.*)$ https://mysite.com/item/$1 [L,R=301]
</code></pre>

<p>do this:</p>

<pre><code>RewriteRule ^(.*)$ https://mysite.com/item/$1 [L] 
// the only difference is the lack of ",R=301"
</code></pre>

### Answer ID: 11460450
<p>How about this?</p>

<pre><code>RewriteCond %{HTTP_HOST} ^ms\.co/$1 [NC]
RewriteCond %{HTTPS} =on
RewriteRule ^(.*)$ https://mysite.com/item/$1 [L,R=301]
</code></pre>

