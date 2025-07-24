# How to rewrite to a specific server according to the subdomain name
[Link to question](https://stackoverflow.com/questions/41305367/how-to-rewrite-to-a-specific-server-according-to-the-subdomain-name)
**Creation Date:** 1482513093
**Score:** 0
**Tags:** c#, asp.net-mvc, subdomain, iis-8
## Question Body
<p>A domain name is pointing to the web server named "Rewrite" (asp.net mvc application). I would like to query the database and rewrite all the pages from another web server according to subdomain name. Each customer has a specific subdomain. Basically, every page will be generated from another web server.
I just want the "Rewrite" web server to show the pages from another server which will be selected dynamically according to the subdomain name.</p>

<p>For example:</p>

<ul>
<li><p>If <strong>user1.mydomain.com</strong> is requested to the mydomain server that will use the web server <strong>www1</strong>, but the url on the client side won't change: <strong>user1.mydomain.com</strong></p></li>
<li><p>If <strong>user1.mydomain.com/Report</strong> is requested to the mydomain server that will use the web server <strong>www1</strong> (so <strong>www1/Report</strong>), but the url on the client side won't change: <strong>user1.mydomain.com/Report</strong></p></li>
<li><p>If <strong>user2.mydomain.com</strong> is requested to the mydomain server that will use the web server <strong>www2</strong>, but the url on the client side won't change: <strong>user2.mydomain.com</strong></p></li>
</ul>

<p>I've read we can add a rewrite rule in the web.config file, but it seems to be a static solution. Unless I can have an automated process to modify the web.config file automatically when we need to create/modify/remove a new client (subdomain) and create a long configuration list. Also, we can have a few thousand clients.</p>

<p>It is a new architecture solution, so the web servers can be hosted on Azure App Service or it can use IIS on a VM.</p>

<p>Also, will that work with a SSL wildcard?</p>

<p>Any idea would be welcome.</p>

## Answers
### Answer ID: 41307609
<p>What you are describing is a reverse proxy server. You can do this with IIS but as you mentioned the rules are somewhat static, so for every "user#" to "www#" pair you may have to setup a new rule, unless maybe the number on the www side always matches the number on the user side (I'm guessing that's not the case"</p>

<p><a href="https://blogs.msdn.microsoft.com/carlosag/2010/04/01/setting-up-a-reverse-proxy-using-iis-url-rewrite-and-arr/" rel="nofollow noreferrer">https://blogs.msdn.microsoft.com/carlosag/2010/04/01/setting-up-a-reverse-proxy-using-iis-url-rewrite-and-arr/</a></p>

<p>There may be a more efficient way to do this with NGINX (take a look at the LUA and MAP modules as options).</p>

