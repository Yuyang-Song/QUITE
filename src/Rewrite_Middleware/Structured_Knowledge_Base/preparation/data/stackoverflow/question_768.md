# Help? (edited) Regex matches pattern in IIS URLrewrite test but does not work with a question mark in the real HTTP request
[Link to question](https://stackoverflow.com/questions/4148412/help-edited-regex-matches-pattern-in-iis-urlrewrite-test-but-does-not-work-wi)
**Creation Date:** 1289418345
**Score:** 1
**Tags:** regex, string, url-rewriting
## Question Body
<p>Here is a typical URL I'm trying to rewrite:</p>

<p>Example requested URL:
<a href="http://topleveldomain/search?q=clause1+clause2+clause3&amp;State=FL" rel="nofollow">http://topleveldomain/search?q=clause1+clause2+clause3&amp;State=FL</a></p>

<p>It should rewrite to:
<a href="http://topleveldomain/index.cfm?q=clause1+clause2+clause3&amp;State=FL" rel="nofollow">http://topleveldomain/index.cfm?q=clause1+clause2+clause3&amp;State=FL</a></p>

<p>It sure does look simple enough, but the plus signs (and various query lengths) are giving me fits. I have written a few different Regex expressions that actually test out as having matched according to the URL Rewrite Module in IIS7, but when I apply the rule it doesn't work. I'm certain the problem is in my Regex and not the expression of the replacement text (the rewritten URL with backreferences). The reason I know that is that I've tested a rewrite to a static URL with no backreference to the regex and it still does not work, even though it tests as a match according to the URL Rewrite admin app.</p>

<p>The number of clauses (and plus signs) could be as few as one up to infinity (or breakage, whichever comes first, haha).</p>

<p>Here is the most recent regex I wrote to match that URL. It's the fourth or fifth regex I've written, all of which are showing matches in the URL Rewriter, but not matching in real practice.</p>

<pre><code>search\?q=(\S+)&amp;State=([a-z][a-z])$
</code></pre>

<p>It's my desire to capture two backreferences:</p>

<ol>
<li>The query string, or "q" which is what the user typed in the search box</li>
<li>The state value, which is what the user selected via an HTML SELECT form input</li>
</ol>

<p>The method of data entry also seems not to matter, as I've tried both <code>POST</code>-ing and <code>GET</code>-ting the string data from the application and also by entering the URL into the browser.</p>

<p>Before you say something about the statecode regex, I realize my regex to match the two-letter state code is loose enough to allow invalid USA state codes -- that's not important because the URLs will be published from app/database values.</p>

<p>UPDATE: the failure of the regex pattern to match the input string from the browser is due to the question mark character in the URL being interpreted, whether it comes from the application (written as form submitting a GET) or if it's just typed or pasted into the browser's address bar.</p>

<p>Chalk it up to user error.</p>

<p>The regex after the question mark needs to be entered in the URL Rewrite [additional] Conditions box as a {Query_String} where it also accepts regex patterns.</p>

<p>IMO given the way that IIS/URL Rewrite parse the HTTP request, the test of a URL string which contains a question mark ought to throw an error or match with a disclaimer or warning.</p>

## Answers
### Answer ID: 4148751
<p>What about:</p>

<pre><code>^search\?q=([a-zA-Z0-9_+-]+)&amp;State=([a-zA-Z]{2})$ index.cfm?q=$1&amp;State=$2
</code></pre>

<p>That is, regex pattern:</p>

<pre><code>search\?q=([a-zA-Z0-9_+-]+)&amp;State=([a-zA-Z]{2})
</code></pre>

<p>Replacement:</p>

<pre><code>index.cfm?q=$1&amp;State=$2
</code></pre>

