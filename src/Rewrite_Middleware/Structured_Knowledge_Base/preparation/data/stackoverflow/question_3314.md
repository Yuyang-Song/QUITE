# Securing a PHP data request for code injection
[Link to question](https://stackoverflow.com/questions/75927983/securing-a-php-data-request-for-code-injection)
**Creation Date:** 1680602073
**Score:** 0
**Tags:** php, sql, security, code-injection
## Question Body
<br>
The small website I am managing for my club is currently seeing an increased amount of attack attempts. Until now those attacks have not been very sophisticated and therefore nothing happened (yet). Now  I just want to make sure that the way we request content is as protected as possible and not a huge hole in our defence. For that I think I need additional changes to the code, but don't really know where to start.
<p>The setup:
We load our content pages by using $_GET arguments to tell which site to get and then get parsed to a database to get more data for the specific site. This is all done using a rewrite rule so we don't have to use <code>index.php?arg1=this&amp;arg2=that</code> as our URL but can use <code>/pages/arg1/1rg2</code></p>
<p>The code:</p>
<p>The rewrite rule looks as follows:</p>
<pre><code>RewriteRule ^pages/([^/]*)/([^/]*)$ /index.php?arg1=$1&amp;arg2=$2 [B,NE,L]
</code></pre>
<p>The code to then request the data from the database:</p>
<pre><code>$statement = $connection-&gt;prepare(&quot;SELECT * FROM `navigation` WHERE `Name` = :arg2&quot;);
$statement-&gt;bindParam(&quot;:name&quot;, $name);
$statement-&gt;execute();
$result = $statement-&gt;fetch();
</code></pre>
<p>Now what I think i need to do is make additional checks for the arg2 string before I hand it to the database request, since I'm not sure if the binding actually prevents injections, but I am not sure what to check for as the string itself could contain special characters like</p>
<blockquote>
<p>à l' ù</p>
</blockquote>
<p>and likewise symbols like</p>
<blockquote>
<p>; . _ ( ) -</p>
</blockquote>
<p>so I can't just check if it is letters. I though about using regex to check if that string matches anying, like so:</p>
<pre><code>if (!preg_match(&quot;/^([0-9a-z_\s; ._à'ù()-])+$/i&quot;,$arg2)) {
        echo &quot;Non valid string&quot;;
        exit;
  }
</code></pre>
<p>But I am not sure if this is enough to prevent code injection to either the php request or the database or at wore even both?
Do you guys have any tips or idea on how to close it down even more, so that only valid entries (i.e. non code text) will actually result in a query to the system? Or did I already do that and there is - for now - nothing more I can do?</p>

