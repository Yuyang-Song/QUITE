# Guidance on URL rewrite and construction
[Link to question](https://stackoverflow.com/questions/7250574/guidance-on-url-rewrite-and-construction)
**Creation Date:** 1314743508
**Score:** 2
**Tags:** php, apache, url, mod-rewrite
## Question Body
<p>I am about to attempt writing of a photo sharing script and a script/rewrite that transforms numbers into descriptive names. I have a vague idea on how to go about doing this, so I was looking for some general comments/guidance.</p>

<p>Issue 1: I need to have a URL source for a photo which is stored above my root directory. I plan on appending the photo name (which is stored in my database) to my url as a query string, such as: www.mywebsite.com/getphoto.php?12_3.jpg and then writing a php script (getphoto.php) which takes the portion after the '?' and gets that photo from above the root.</p>

<p>Does this make sense and would there be any things to consider?</p>

<p>Issue 2: I want to transform a number at the end of my URL to a descriptive name (ie typing in facebook.com/4 displays facebook.com/zuck). I am not really sure the best way to go about doing this and was hoping for some guidance to get going in the right direction.</p>

<p>Thanks! </p>

## Answers
### Answer ID: 7250652
<p>For Issue 1: a simple rewrite can handle that, you need to use the [QSA] flag. Something like this:</p>

<pre><code>RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_URI} ^.*\.(jpeg|jpg|gif|png|bmp)$
RewriteRule ^(.+)$ /getphoto.php?photo=$1 [L,QSA]
</code></pre>

<p>This will rewrite behind the scenes the url <a href="http://mywebsite.com/12_3.jpg" rel="nofollow">http://mywebsite.com/12_3.jpg</a> to <a href="http://mywebsite.com/getphoto.php?photo=12_3.jpg" rel="nofollow">http://mywebsite.com/getphoto.php?photo=12_3.jpg</a> Note that the 3rd rewrite condition wants the URI to end with an image extension, you may not need it.</p>

<p>For Issue 2, it depends on how something like "4" maps to "zuck". If you are going to hardcode them into your apache config, you can use a RewriteCond:</p>

<pre><code>RewriteEngine On
RewriteCond %{REQUEST_URI} ^/4$
RewriteRule ^.*$ /zuck [L]
RewriteCond %{REQUEST_URI} ^/5$
RewriteRule ^.*$ /mark [L]
</code></pre>

<p>etc. (or replace <code>[L]</code> with <code>[R,L]</code> to redirect instead of rewrite, or alternatively just use <code>Redirect</code>)</p>

<pre><code>Redirect /4 /zuck
Redirect /5 /mark
</code></pre>

<p>etc.</p>

<p>If the mapping is stored in a database, your going to need to do this dynamically, perhaps as a php script to do a redirect, utilizing something similar to Issue 1. The rewrite rule would rewrite to something like <code>/redirect.php?id=$1</code> and your redirect.php script would take the <code>id</code> and do a database lookup to see where to redirect the browser.</p>

