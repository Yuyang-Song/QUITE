# Best practices for converting an existing website into a website with SEF URL
[Link to question](https://stackoverflow.com/questions/1733476/best-practices-for-converting-an-existing-website-into-a-website-with-sef-url)
**Creation Date:** 1258179715
**Score:** 3
**Tags:** asp-classic, url-rewriting, seo
## Question Body
<p>I've got a website that was created about an year ago and its been constantly revised since then. The website is coded in classic ASP, contains about ~50 pages -- some are multi-purpose, and contains old-school style links such as:</p>

<pre><code>/news.asp?PageIndex=4
/news.asp?SearchString=Obama
/news.asp?SearchString=Obama&amp;PageIndex=4
/news.asp?NewsID=1
</code></pre>

<p>I have IIRF v2 installed which allows access to URL rewriting functionality so this I do not have to worry about. What I am worried about is how to replace about 300 links to .ASP pages with SEF urls. As far as my understanding is concerned, I have to add a database query (to extract title of the record being linked) for each link. </p>

<p>I need advice on how to begin converting the website into a SEF URL powered website with as little code change as possible. Wrapper classes and tried-and-tested techniques and pointers to best practices will be appreciated. </p>

## Answers
### Answer ID: 1804125
<p>If you want to do URL Rewriting without changing frameworks or anything, may I suggest that you take a look at <a href="http://learn.iis.net/page.aspx/460/using-url-rewrite-module/" rel="nofollow noreferrer">IIS7 Url Rewriting Module</a>?</p>

<p>However, if you are rewriting part of your application in .NET ... you might want to consider <a href="http://www.asp.net/MVC/" rel="nofollow noreferrer">ASP.NET MVC</a>. It already build simple built-in URL Rewriting module and definitely allows you to keep on using your old "WebForms" (if ASP.NET) or your classic ASP pages.</p>

### Answer ID: 1780356
<p>At news.asp (and whatever other old pages you have) put something (a class? I don't know, I have never used ASP) that parses the old-style URL and redirects (with a HTTP redirect code) to the new URL.</p>

### Answer ID: 1733750
<p>Don't forget to permanently redirect each and every old link to a new one (use 301 HTTP code).</p>

