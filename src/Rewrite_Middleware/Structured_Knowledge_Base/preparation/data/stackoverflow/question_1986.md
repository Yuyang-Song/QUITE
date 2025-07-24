# Rewrite Rule finds directory and rewrites path as &#39;directory/?directory&#39;
[Link to question](https://stackoverflow.com/questions/14610604/rewrite-rule-finds-directory-and-rewrites-path-as-directory-directory)
**Creation Date:** 1359568727
**Score:** 0
**Tags:** regex, url, mod-rewrite, url-rewriting, directory
## Question Body
<p>I've been using this Apache Rewrite Rule for some time now, and it usually gives me great results:  </p>

<pre><code>RewriteRule ^([^\.]+)/?$ index.php?$1 [L]
</code></pre>

<p>When a user visits <code>www.mysite.com/about-us</code>, the server displays the content from <code>www.mysite.com/index.php?about-us</code>. The content is stored in a database, and I search for each page's content with the query string ('about-us'). This was working just fine until recently.  </p>

<p>A new site that I'm building has a directory (we'll call it 'folder') that's the same name I want for the query string--that is, instead of looking for an index file inside the <code>newsite.com/folder</code> directory, <code>www.newsite.com/folder</code> should route through <code>index.php</code> and use 'folder' as a search parameter. Instead, I get this:  </p>

<pre><code>www.newsite.com/folder/?folder
</code></pre>

<p>in which my code interprets the query string as 'folder/'. So the first problem is that the URL looks strange; the second problem is that my pages are stored without any trailing slashes.  </p>

<p>Of course I could adjust my code to take off any slashes after receiving the query string, but that could make it more challenging to create URLs that emulate a folder structure, like <code>www.newsite.com/user/images/month</code>. And it still wouldn't get rid of the funky URL I already have.</p>

<p>I suspect there is a simple solution that makes my URLs pretty and keeps the server from looking for files in my directories (unless the user explicitly asks for an html or php file). Thanks for your input.</p>

## Answers
### Answer ID: 15828233
<p>Add "DirectorySlash Off" to the start of the ".htaccess" file</p>

<p>I had the same problem and found a similar post which simply referenced to the DirectorySlash documentation (<a href="http://httpd.apache.org/docs/2.2/mod/mod_dir.html" rel="nofollow">http://httpd.apache.org/docs/2.2/mod/mod_dir.html</a>)</p>

