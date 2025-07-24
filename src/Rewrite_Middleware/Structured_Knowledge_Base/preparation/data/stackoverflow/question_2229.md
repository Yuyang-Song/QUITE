# IIS 7.5 URL Rewrite Module - Rewrite Maps with variables
[Link to question](https://stackoverflow.com/questions/25187500/iis-7-5-url-rewrite-module-rewrite-maps-with-variables)
**Creation Date:** 1407428481
**Score:** 1
**Tags:** iis, url-rewriting, iis-7.5, url-rewrite-module, rewritemap
## Question Body
<p>I have several pages on my site that have long and unreadable URLs that I'd like to be able shorten. The problem I'm having is appending query strings with variable values.</p>

<p>For example: 
"www.example.com/dir1/dir2/filename.php" shortens to "www.example.com/file".
"www.example.com/dir1/dir2/filename.php?id=2" would be "www.example.com/file/2".
"www.example.com/dir1/dir2/filename.php?id=2&amp;alt=6" would be "www.example.com/file/2/6".</p>

<p>The values of 'id' and 'alt' are then used by our page to access information in our database, which determines the contents of the page. These values can change, and there is no set amount.</p>

<p>Right now I've got the first example working fine using the following rewrite rules:</p>

<pre><code>&lt;rewrite&gt;
        &lt;outboundRules&gt;
            &lt;remove name="OutboundRewriteUserFriendlyURL1" /&gt;
        &lt;/outboundRules&gt;
        &lt;rewriteMaps&gt;
            &lt;rewriteMap name="StaticRewrites"&gt;
                &lt;add key="/file" value="/dir1/dir2/filename.php" /&gt;                    
            &lt;/rewriteMap&gt;
        &lt;/rewriteMaps&gt;
      &lt;rules&gt;
        &lt;rule name="Rewrite Rule"&gt;
          &lt;match url=".*" /&gt;
          &lt;conditions&gt;
            &lt;add input="{StaticRewrites:{REQUEST_URI}}" pattern="(.+)" /&gt;
          &lt;/conditions&gt;
          &lt;action type="Rewrite" url="{C:1}" /&gt;
        &lt;/rule&gt;
      &lt;/rules&gt;
&lt;/rewrite&gt;
</code></pre>

<p>But I haven't been able to find anything that would allow the URLs to contain variables. Everything I've seen has used static rewrites like my current solution is using, and I can't find anything about allowing arbitrary parameters.</p>

<p>EDIT:</p>

<p>Found a better solution that doesn't use a Rewrite Map. I had attempted a simliar rule previously, but due to the IIS setup on our testing environment it wasn't working as expected. This version should work for most people.</p>

<pre><code>&lt;rule name="Curricula View" stopProcessing="true"&gt;
    &lt;match url="/file(?:/(\d+)(?:/(\d+))?)?" /&gt;
    &lt;action type="Rewrite" url="/dir1/dir2/filename.php?id={R:1}&amp;alt={R:2}" appendQueryString="true" /&gt;
    &lt;conditions&gt;
        &lt;add input="{REQUEST_FILENAME}" matchType="IsFile" negate="true" /&gt;
        &lt;add input="{REQUEST_FILENAME}" matchType="IsDirectory" negate="true" /&gt;
    &lt;/conditions&gt;
&lt;/rule&gt;
</code></pre>

## Answers
### Answer ID: 25244194
<p>Using this rule I was able to avoid using a rewrite map altogether. I had attempted to use something like this originally, but due to the setup of our test environment it wouldn't work without some weird tweaks. This version should work in all normal environments.</p>

<pre><code>&lt;rule name="Curricula View" stopProcessing="true"&gt;
    &lt;match url="/file(?:/(\d+)(?:/(\d+))?)?" /&gt;
    &lt;action type="Rewrite" url="/dir1/dir2/filename.php?id={R:1}&amp;alt={R:2}" appendQueryString="true" /&gt;
    &lt;conditions&gt;
        &lt;add input="{REQUEST_FILENAME}" matchType="IsFile" negate="true" /&gt;
        &lt;add input="{REQUEST_FILENAME}" matchType="IsDirectory" negate="true" /&gt;
    &lt;/conditions&gt;
&lt;/rule&gt;
</code></pre>

<p>EDIT:
I was also able to get the original version with a rewrite map working for anyone interested.</p>

<pre><code>&lt;rule name="Rewrite Map with Variables" enabled="true"&gt;
    &lt;match url="^(.+?)/?/(.*)$" /&gt;
    &lt;conditions logicalGrouping="MatchAny" trackAllCaptures="false"&gt;
        &lt;add input="{ProductMap:{R:1}}" pattern="(.+)" /&gt;
    &lt;/conditions&gt;
    &lt;action type="Rewrite" url="/dir1/dir2/filename.php?id={C:0}&amp;amp;other={R:2}" appendQueryString="true" /&gt;
&lt;/rule&gt;
</code></pre>

