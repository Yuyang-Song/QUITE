# Dynamically retrieve attribute-value pairs of Request.RequestUri.Query?
[Link to question](https://stackoverflow.com/questions/64116201/dynamically-retrieve-attribute-value-pairs-of-request-requesturi-query)
**Creation Date:** 1601369919
**Score:** 0
**Tags:** c#, http, url, asp.net-web-api
## Question Body
<p>I have the felling I'm rewriting something that must exist. Is there a better way to get and split all parameters of a http query.</p>
<p>I have this query</p>
<pre><code>http://localhost:59289/api/Company/Example/Sequence/01234567890128/NextRange?Quantity=5000&amp;Order=O1234
</code></pre>
<p>To keep things simple let's say I want to save these 2 parameters as metadata in a JSON string. Parameters can be others. The list of parameters is dynamic. I can let the user choose what he want to pass as parameters, the system will save them as metadata in JSON in my database.</p>
<p>In Immediate Window on Visual studio I can test this:</p>
<pre><code>Request.RequestUri.Query
&quot;?Quantity=5000&amp;Order=O1234&quot;
</code></pre>
<p>Request.RequestUri.Query is a string. I can then split it by &quot;&amp;&quot; and create a dictionary of string then serialize it as JSON. But I'm surprised I have to split this by myself. Is there a better way to query all parameters keys them request all values?</p>
<p>I checked this <a href="https://en.wikipedia.org/wiki/URL" rel="nofollow noreferrer">https://en.wikipedia.org/wiki/URL</a></p>
<p>Solution 1 ----------</p>
<p>I already tried this</p>
<pre><code>var query = @&quot;?Quantity=5000&amp;Order=O1234&quot;;
var p = query
    .TrimStart('?')
    .Split('&amp;')
    .Select(y =&gt; y.Split('='))
    .SelectMany(y =&gt; new Dictionary&lt;string, string&gt;()
    {
        { y[0], y[1] }
    });
</code></pre>
<p>That is my solution manually. I just get an exception in case my string is empty.</p>

## Answers
### Answer ID: 64177119
<p>Request.GetQueryNameValuePairs();</p>

### Answer ID: 64116813
<p>Found:</p>
<pre><code>HttpUtility.ParseQueryString(query);
</code></pre>

