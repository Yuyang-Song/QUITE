# Creating friendlier URLs in an ASP.NET WebForm application
[Link to question](https://stackoverflow.com/questions/14087917/creating-friendlier-urls-in-an-asp-net-webform-application)
**Creation Date:** 1356836102
**Score:** 0
**Tags:** c#, asp.net, url-rewriting, webforms
## Question Body
<p>I have an ASP.NET WebForms application. What I am trying to do is create dynamic friendly URLs using <code>RewritePath</code>. What I want to be able to do is grab the subdomain of the URL coming in, check a table in my database called <code>Domains</code> and then depending on the subdomain, rewrite the url adding a query string of <code>?id=1</code> or whatever the <code>id</code> is.</p>

<p>In addition, I would like the path to determine the page to load. So for example:</p>

<pre><code>http://www.mysite.com should go to                --&gt; http://www.mysite.com/Default.aspx
http://dog.mysite.com should go to                --&gt; http://www.mysite.com/MainPage.aspx?id=1
http://cat.mysite.com should go to                --&gt; http://www.mysite.com/MainPage.aspx?id=2
http://cat.mysite.com?p=15 should go to           --&gt; http://www.mysite.com/MainPage.aspx?id=2&amp;p=15
http://cat.mysite.com/OtherPage should go to      --&gt; http://www.mysite.com/OtherPage.aspx?id=2
http://cat.mysite.com/OtherPage?p=15 should go to --&gt; http://www.mysite.com/OtherPage.aspx?id=2&amp;p=15
</code></pre>

<p>Hopefully the examples give you the idea that I am looking for. I would prefer to be able to do this from the global.asax file because I do not have access to the IIS web server machine to be able to install some server-side module for URL rewriting. </p>

<p>Thanks in advance for the help</p>

## Answers
### Answer ID: 14088071
<p>Read <a href="http://weblogs.asp.net/scottgu/archive/2007/02/26/tip-trick-url-rewriting-with-asp-net.aspx" rel="nofollow">this blog of ScuttGu </a> it talks about url renaming in details.</p>

