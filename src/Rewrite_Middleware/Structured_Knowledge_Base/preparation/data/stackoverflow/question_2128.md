# .htaccess RewriteRule performance (large amount of RegEx)
[Link to question](https://stackoverflow.com/questions/19994332/htaccess-rewriterule-performance-large-amount-of-regex)
**Creation Date:** 1384494254
**Score:** 1
**Tags:** php, regex, apache, .htaccess, mod-rewrite
## Question Body
<p>I am using the following .htaccess rules to rewrite multiple urls on my website:</p>

<pre><code>RewriteEngine On
RewriteRule ^privacy(\w|\s|\+|-|&amp;|;|#)+policy/?$ index.php?page=privacy [NC]
RewriteRule ^([A-Za-z]+)(.*)+foo(\w|\s|\+|-|&amp;|;|#)+bar/?$   index.php?page=$1 [NC]
</code></pre>

<p>The first rule works efficiently for the "privacy policy" page.</p>

<p>The second rule, however, results in a noticeably poor server response time. I believe the way this rule is written causes a delay in querying my database for the ([A-Za-z]+) expression. There is a large amount of RegEx that apply to this rule, and some of the urls contain "extra" words after the RegEx. For example:</p>

<pre><code>www.example.com/North+America+Foo+Bar/
</code></pre>

<p>queries the database for "North" to rewrite the url to</p>

<pre><code>www.example.com/index.php?page=North
</code></pre>

<p>This is the reason why I included (.*) in the rule, but I fear this is the culprit of the slow response time. Complicated, I know.</p>

<p>Any ideas or suggestions to improve this rule for faster performance? I would prefer keeping the www.example.com/Expression+Foo+Bar/ format because hundreds of urls are already indexed by search engines. =/</p>

<p>Thank you for your advice.</p>

## Answers
### Answer ID: 19995677
<p>You don't need to match the whole URI in 2nd rule. Try this rule with simplified regex:</p>

<pre><code> RewriteRule ^([a-z]+)(?=.*?foo.*?bar) index.php?page=$1 [NC]
</code></pre>

