# Access Couch DB database URL through rewritten URL, with query parameters
[Link to question](https://stackoverflow.com/questions/5059499/access-couch-db-database-url-through-rewritten-url-with-query-parameters)
**Creation Date:** 1298230857
**Score:** 12
**Tags:** couchdb
## Question Body
<p>I have my web site run out of a Couch DB instance, so I have my vhost configured to point to <code>/dbname/_design/app/_rewrite</code>.</p>

<p>I want to be able to access the index page from a web browser, while still accessing the Couch DB API over Ajax, so I set up a pair of rewrite rules in my <code>rewrites</code> field:</p>

<pre><code>[ { "from": "/dbname/*", "to: ../../*" },
  { "from": "/*", "to: *" } ]
</code></pre>

<p>These rules work fine: I can access individual documents through a <code>/dbname/docname</code> URL, and I can point my web browser at the root of the site and access my attachments that way.</p>

<p>I'd now like to access the information on the database itself, in order to pass a <code>since</code> parameter to the <code>_changes</code> API.</p>

<ol>
<li><code>/dbname/</code> works fine</li>
<li><code>/dbname/?name=value</code> doesn't redirect properly. In the Couch DB log, I see lines like <code>'GET' /dbname/_design/..?name=value 404</code>, whereas I'd expect to see <code>'GET' /dbname/?name=value 200</code>.</li>
</ol>

<p>The second case is needed for Ajax from IE, where the <code>jquery.couch.js</code> code adds a fake query string to avoid caching.</p>

<p>How can I phrase my rewrite rules so that Couch DB rewrites <code>/dbname/?name=value</code> correctly?</p>

<p><strong>Edit:</strong> To clarify, query strings work OK as long as there is something after the last / in the URL.</p>

<ul>
<li><code>/dbname/docname?rev=xxx</code> works</li>
<li><code>/dbname/_changes?since=1</code> works</li>
<li><code>/dbname/?_=dummy</code> doesn't work; it rewrites to <code>/dbname/_design/..?_=dummy</code></li>
</ul>

## Answers
### Answer ID: 5062994
<p>I tried to duplicate your problem but it is working. Below is my interaction. (Note, I use the IP address, <code>127.0.0.1:5984</code>, to ensure no vhost/rewrite problems, then I access the "production" site via <code>localhost:5984</code>.</p>

<p><strong>There is a bug</strong> it seems with query parameters being appended to rewrites ending with "..". Instead of rewriting to <code>../?key=val</code> it writes to <code>..?key=val</code> which CouchDB does not parse.</p>

<p>I do not think it is necessary to query a database URL with parameters. So one workaround is to always make sure you never do that. (E.g. if you blindly append no-op parameters to all queries to simplify the code, you'd have to alter that.)</p>

<p>Another workaround is to enable rewrite to the <em>root CouchDB URL</em>. This requires setting <code>/_config/httpd/secure_rewrites</code> to <code>false</code>.</p>

<pre><code>{ "from":"/api/*", "to":"../../../*" }
</code></pre>

<p>Now you can query <code>http://localhost:5984/api/x?key=val</code> or <code>http://localhost:5984/api/x/_changes?since=5</code>. (You cannot query the root URL with parameters&mdash;it's still the bug, but in a less trafficked place.)</p>

<p>Following is the initial terminal session:</p>

<pre><code>$ mkdir t
$ cd t
$ curl -XDELETE 127.0.0.1:5984/x 
{"ok":true}
$ curl -XPUT 127.0.0.1:5984/x 
{"ok":true}
$ curl 127.0.0.1:5984
{"couchdb":"Welcome","version":"1.0.1"}

$ echo -n _design/test &gt; _id
$ mkdir shows
$ echo 'function() { return "hello world!\n" }' &gt; shows/hello.js
$ cat &gt; rewrites.json
[ { "from":"/db/*", "to":"../../*" }
, { "from":"/*"   , "to":"*"}
]

$ echo '{}' &gt; .couchapprc
$ couchapp push http://127.0.0.1:5984/x
$ curl -XPUT http://127.0.0.1:5984/_config/vhosts/localhost:5984 -d '"/x/_design/test/_rewrite"'
"/x/_design/test/_rewrite"

$ curl localhost:5984 # This is the design document.
{"_id":"_design/test","_rev":"1-e523efd669aa5375e711f8e4b764da7a","shows":{"hello":"function() { return \"hello world!\\n\" }"},"couchapp":{"signatures":{},"objects":{},"manifest":["rewrites.json","shows/","shows/hello.js"]},"rewrites":[{"to":"../../*","from":"/db/*"},{"to":"*","from":"/*"}]}
$ curl localhost:5984/_show/hello
hello world!

$ curl localhost:5984/db # This is the DB.
{"db_name":"x","doc_count":1,"doc_del_count":0,"update_seq":1,"purge_seq":0,"compact_running":false,"disk_size":4185,"instance_start_time":"1298269455135987","disk_format_version":5,"committed_update_seq":1}
$ curl localhost:5984/db/_changes
{"results":[
{"seq":1,"id":"_design/test","changes":[{"rev":"1-e523efd669aa5375e711f8e4b764da7a"}]}
],
"last_seq":1}

$ curl localhost:5984/db/_changes?since=1 # Parameters accepted!
{"results":[

],
"last_seq":1}
</code></pre>

