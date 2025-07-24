# Rewrite dynamic URLs in lots of HTML files
[Link to question](https://stackoverflow.com/questions/22056103/rewrite-dynamic-urls-in-lots-of-html-files)
**Creation Date:** 1393458601
**Score:** 0
**Tags:** c#, replace
## Question Body
<p>I am working on a migration project form a legacy Intranet to a new product.</p>

<p>All the html files are stored on a file system but will be chucked into a database and I am cleansing a lot of HTML already, what I need to do now is to rewrite URLs so that they will continue to work</p>

<p>At the moment we have thousands of files with query string links like so:</p>

<pre><code>&lt;a href="site.get?section&amp;PAGE277"&gt;Hanoi&lt;/a&gt;
&lt;a href="site.get?section&amp;PAGE278"&gt;Ho Chi Minh City&lt;/a&gt;
&lt;a href="site.get?section&amp;PAGE245"&gt;Hong Kong&lt;/a&gt;
</code></pre>

<p>I need something to alter all the links to instead look like:</p>

<pre><code>&lt;a href="/sites/pages/PAGE277.aspx"&gt;Hanoi&lt;/a&gt;
&lt;a href="/sites/pages/PAGE278.aspx"&gt;Ho Chi Minh City&lt;/a&gt;
&lt;a href="/sites/pages/PAGE245.aspx"&gt;Hong Kong&lt;/a&gt;
</code></pre>

<p>The number will always be a three digit number</p>

<p>I'm already doing a lot of other transformation in the HTML but got stuck on this one</p>

<p>Any ideas?</p>

<p>Thanks in advance</p>

<p>Edit: the pages will be migrated to SharePoint and hence be stored in a SharePoint content database for internal use.</p>

<p>Edit2:</p>

<p>This solved the problem but can it be done neater?</p>

<pre><code>public static string ReplacePageUrl(string content)
{
    string updatedContent = content;

    for (int i = 1; i &lt; 1000; i++)
    {
        updatedContent = updatedContent.Replace("site.get?section&amp;PAGE" + i.ToString("D3"),
            "href=\"/sites/pages/page" + i.ToString("D3") + ".aspx");
    }

    return updatedContent;
}
</code></pre>

## Answers
### Answer ID: 22056383
<p>modifying the database and keep a single instance of it is quite dangerous and it could be error prone, in the case you are doing URL modifications try the following scenario:</p>

<p><strong>Do a 301 redirect:</strong></p>

<blockquote>
  <p>The HTTP response status code 301 Moved Permanently is used for
  permanent redirection, meaning current links or records using the URL
  that the 301 Moved Permanently response is received for should be
  updated to the new URL provided in the Location field of the response. - Wikipedia</p>
</blockquote>

<p>by doing this you aren't going to lose whatever the ranking you have on your current pages and it won't affect SEO at all.</p>

<p><strong>Create or copy the new content to another Database</strong></p>

<p>Once you have the list of urls you are going to redirect the you can perform the url changes on this database (the new url structure) and then you can analyze and study the redirections and do all the necesary modifications to this database without having broken links.</p>

<p><strong>Test the redirections</strong></p>

<ul>
<li><p>I would suggest to test your redirections prior to launch your product to production (this sounds quite obvious isn't it) but make sure that you are modifying your local ETC file system to point the domain of your application to the 127.0.0.1 ip</p></li>
<li><p>Run several tests on google, write whatever the url pattern you are testing to a google query like "page1.aspx?param=1" site:yourdomain.com and try every single pattern / redirection just to make sure eveything is working.</p></li>
</ul>

<p>I think that a safer way to work and it could give you the flexibility to at least miss a couple of links without having broken links.</p>

<p>EDIT:</p>

<p>Well if you need to replace or modify HTML and that's your only concern I'd recommend you to use <a href="http://htmlagilitypack.codeplex.com/" rel="nofollow">HTML Agility Pack</a> you can do linq queries to the HTMl elements doing filters, elements modifications, that will make your scenario a lot easier! </p>

<p>something like this:</p>

<pre><code>var links = html.DocumentNode
           .Descendants("tr")
           .Where(tr =&gt; tr.GetAttributeValue("class", "").Contains("alt"))
           .SelectMany(tr =&gt; tr.Descendants("a"))
           .ToArray();
</code></pre>

### Answer ID: 22056385
<p>I'd recommend Notepad++ (<a href="http://notepad-plus-plus.org" rel="nofollow">http://notepad-plus-plus.org</a>) to replace the text in your files.</p>

<p>Then you can use the "Replace in files" function with a regular expression...</p>

<p>With regular expressions enabled in the find/replace box, replace this:</p>

<pre><code>&lt;a href="site\.get\?section&amp;(.*)"&gt;(.*)&lt;/a&gt;
</code></pre>

<p>With this:</p>

<pre><code>&lt;a href="/sites/pages/\1\.aspx"&gt;\2&lt;/a&gt;
</code></pre>

