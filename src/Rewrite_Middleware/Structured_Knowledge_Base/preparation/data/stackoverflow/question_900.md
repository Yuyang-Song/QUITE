# How to redirect your users subdomain accounts to a subfolder
[Link to question](https://stackoverflow.com/questions/48963790/how-to-redirect-your-users-subdomain-accounts-to-a-subfolder)
**Creation Date:** 1519481737
**Score:** -1
**Tags:** php, .htaccess
## Question Body
<p>Please, I'm working on a project where I need to capture the subdomain of my website as a string and query the user database, and then display the result in another page, without altering the URL.</p>

<p>For instance:
If a user visits <strong><a href="https://kelly.domain.com.xyz" rel="nofollow noreferrer">https://kelly.domain.com.xyz</a></strong>, it converts the subdomain name <strong>"Kelly"</strong> into a string called <strong>id</strong>, searches for the result and returns the query in "userpage.php?id=kelly" internally, without changing the URL <a href="https://kelly.domain.com.xyz" rel="nofollow noreferrer">https://kelly.domain.com.xyz</a>.</p>

<p>What this means is that userpage.php is the hidden page for the user subdomain.</p>

<p>My question is, how do I rewrite the .htaccess to get the subdomain name and sends it to userpage.php</p>

<p>Below is what I have tried so far, but it doesn't seem to work:</p>

<pre><code>RewriteEngine on
RewriteCond %{HTTP_HOST} ^(.*)\.domain\.com\.xyz
RewriteRule ^(.*)$ https://domain.com.xyz/subdomains/$1 [L,NC,QSA]
RewriteRule    ^subdomains/([A-Za-z0-9-]+)?$    subdomains/userpage.php?id=$1    [NC,L]    
</code></pre>

<p>Apologies if my code sucks, but I'm not so good with .htaccess</p>

## Answers
### Answer ID: 48963891
<p>Instead of htaccess use php. For php try below code to get subdomain.</p>

<pre><code>$id = array_shift(explode('.', $_SERVER['HTTP_HOST']));
</code></pre>

<p>instead of url parameter, you will get direct value.</p>

