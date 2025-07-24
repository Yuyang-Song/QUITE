# simple mod_rewrite is removing my query string
[Link to question](https://stackoverflow.com/questions/16830621/simple-mod-rewrite-is-removing-my-query-string)
**Creation Date:** 1369899946
**Score:** 0
**Tags:** mod-rewrite
## Question Body
<p>I have spent a fair amount of time in the apache documentation, on google and on stackoverflow and I cannot resolve my issue. Here is some background: I am storing images in a database in a blob format. I have a script called imageRender.php that accepts the name of the image as a query string and echos the image within an image tag.</p>

<pre><code>&lt;img src='/script/imageRender.php?name=foo'/&gt;
</code></pre>

<p>In order to simplify the src attribute I am attempting to use apache mod_rewrite to map a simpler src to the one above.</p>

<pre><code>&lt;img src='image=foo'/&gt;
</code></pre>

<p>My relevant rewrite code is:</p>

<pre><code>RewriteCond %{REQUEST_URI} image=(.*)$
RewriteRule . /scripts/imageRender.php?name=%1 [L]
</code></pre>

<p>The relevant sections of the rewrite log are:</p>

<pre><code>(2) init rewrite engine with requested uri /image=foo
(1) pass through /image=foo
(3) [perdir M:/sample/website/] strip per-dir prefix: M:/sample/website/image=foo -&gt; image=foo
(3) [perdir M:/sample/website/] applying pattern '.' to uri 'image=foo'
(4) [perdir M:/sample/website/] RewriteCond: input='/image=foo' pattern='image=(.*)$' =&gt; matched
(2) [perdir M:/sample/website/] rewrite 'image=foo' -&gt; '/scripts/imageRender.php?name=foo'
(3) split uri=/scripts/imageRender.php?name=foo -&gt; uri=/scripts/imageRender.php, args=name=foo
(1) [perdir M:/sample/website/] internal redirect with /scripts/imageRender.php [INTERNAL REDIRECT]
</code></pre>

<p>So it appears that my rewrite is making a call for the right php script; however, the last line of the rewrite log indicates that it is not attaching the query string to the uri. This is proven true by the fact that none of my images are rendering. (I have tested my imageRender.php code, it works perfectly when supplied with an appropriate query string)</p>

<p>In the second to last line of the rewrite log why does it <b>split uri</b>?</p>

<p>Where have I gone wrong?</p>

<p>Any help is greatly appreciated.</p>

