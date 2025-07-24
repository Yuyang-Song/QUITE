# Merge params in rewrite paths
[Link to question](https://stackoverflow.com/questions/33259323/merge-params-in-rewrite-paths)
**Creation Date:** 1445430463
**Score:** 0
**Tags:** url-rewriting, couchdb
## Question Body
<p>Can I merge params as one in rewrite handlers or VHOST ?</p>

<p>In example:</p>

<pre><code>{
       "from": "/:db/:year/:doc",
       "to": "../../../:db%2F:year/:doc",
       "method": "GET"

   }
</code></pre>

<p>I have database named mydb/2015. In URL slash '/' will be URL-encoded to %2F. I would like to have pretty URL and query:</p>

<pre><code>/mydb%2F2015/myDocId
</code></pre>

<p>change to</p>

<pre><code>/mydb/2015/myDocId
</code></pre>

<p>DocId could have chars which should be URL-encoded.</p>

## Answers
### Answer ID: 33314562
<p>I'm afraid this is not permitted:</p>

<blockquote>
  <p>You can have / as part of the document ID but if you refer to a
  document in a URL you must always encode it as %2F. One special case
  is _design/ documents, those accept either / or %2F for the / after
  _design, although / is preferred and %2F is still needed for the rest of the DocID.</p>
</blockquote>

<p><a href="https://wiki.apache.org/couchdb/HTTP_Document_API#Documents" rel="nofollow">Prooflink</a></p>

