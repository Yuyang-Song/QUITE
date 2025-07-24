# Using IIS7&#39;s Rewrite Module and a database
[Link to question](https://stackoverflow.com/questions/3260071/using-iis7s-rewrite-module-and-a-database)
**Creation Date:** 1279227807
**Score:** 4
**Tags:** iis-7, url-rewriting, mod-rewrite
## Question Body
<p>My company converted from an old website to a new one and we have a bunch of old pages with URLs like this:</p>

<ul>
<li>www.example.com?foo.aspx</li>
<li>www.example.com?foo.aspx?ID=B&amp;utm_source=Foo</li>
<li>www.example.com?foo.aspx?ID=C&amp;utm_source=Foo</li>
</ul>

<p>Those URLs need to go to these pages respectively:</p>

<ul>
<li>www.example.com/ProductA</li>
<li>www.example.com/ProductB?utm_source=Foo</li>
<li>www.example.com/ProductC?utm_source=Foo</li>
</ul>

<p>I can get this to work by using  in my web.config but there are so many I would prefer to do it in the database.  I have been able to partially successfully switch to the database using the article <a href="http://learn.iis.net/page.aspx/803/using-custom-rewrite-providers-with-url-rewrite-module/" rel="nofollow noreferrer">http://learn.iis.net/page.aspx/803/using-custom-rewrite-providers-with-url-rewrite-module/</a>.</p>

<p>My issue is that all of my initially examples redirect to www.example.com/ProductA.  It is as if they are ignoring the Query Strings.  Any idea how to fix this?  My rule in my config file is:</p>

<pre><code>&lt;rule name="DbProviderTest" stopProcessing="true"&gt;
    &lt;match url="(.*)" /&gt;
    &lt;conditions&gt;
    &lt;add input="{DB:{R:1}}" pattern="(.+)" /&gt;
    &lt;/conditions&gt;
    &lt;action type="Redirect" url="{C:1}" appendQueryString="false" /&gt;
&lt;/rule&gt;  
</code></pre>

## Answers
### Answer ID: 3261857
<p>the URL that is matched in the  tag does not include the Query String and that is why you will not see it in your R:1, you should be able to change your condition to be something like:</p>

<pre><code>&lt;add input="{DB:{R:1}?{QUERY_STRING}}" pattern="(.+)" /&gt; 
</code></pre>

