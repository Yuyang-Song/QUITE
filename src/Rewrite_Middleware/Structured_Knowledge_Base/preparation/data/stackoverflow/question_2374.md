# How can I use mod_rewrite to proxy the userinfo component of a URI?
[Link to question](https://stackoverflow.com/questions/31752562/how-can-i-use-mod-rewrite-to-proxy-the-userinfo-component-of-a-uri)
**Creation Date:** 1438366339
**Score:** 0
**Tags:** apache, .htaccess, mod-rewrite, couchdb, mod-proxy
## Question Body
<p>This has been driving me crazy. I have a web application that's being served via Apache Web Server. The database server that backs the application is Apache CouchDB, which exposes an HTTP API to retrieve documents and stream attachments.</p>

<p>I've secured the CouchDB database by providing a security object, which only allows certain users to access data within the database, and returns 401 for anonymous requests to HTTP endpoints.</p>

<p>I want to be able to map public URLs to document attachments stored within this database. So, I've attempted to create a rewrite rule inside my .htaccess file that proxies requests from certain URLs directly to CouchDB, while hardcoding the user credentials, like so:</p>

<pre><code>## DOWNLOAD STREAM:
RewriteCond %{HTTP_HOST} ^domain.com$
RewriteRule download/(.*) http://user:pass@127.0.0.1:5984/database/$1 [P]
</code></pre>

<p>In an ideal world, the above example would take the following URL:</p>

<pre><code>http://domain.com/download/UUID/attachment.ext
</code></pre>

<p>And proxy it to:</p>

<pre><code>http://user:pass@127.0.0.1:5984/database/UUID/attachment.ext
</code></pre>

<p>This method does indeed proxy the request to CouchDB, but omits the userinfo component of the URI scheme. So, the request is treated as anonymous and I get a 401 error. <em>The attachment is only streamed if I remove security from the database.</em></p>

<p>I've spent a couple of hours reading up on Apache configuration and experimenting to no avail. Web searches are fruitless because of all the related queries with similar keywords.</p>

<p><strong>How can I ensure that mod_rewrite includes the username and password provided in the rewrite rule when it proxies to CouchDB?</strong></p>

## Answers
### Answer ID: 31764850
<p>I figured it out! Rather than including the username:password as part of the URI scheme, the Authorization header needs to be set independently. The following solution works completely within a <code>.htaccess</code> file, which is important since OS X periodically blows away settings inside VirtualHost sites:</p>

<pre><code>SetEnvIf Request_URI ^/download/* ADD_COUCH_BASIC_AUTH
RequestHeader set Authorization "Basic XXXXXXXXXXXX" env=ADD_COUCH_BASIC_AUTH

## DOWNLOAD STREAM
RewriteCond %{HTTP_HOST} ^example.com$
RewriteRule download/(.*) http://127.0.0.1:5984/database/$1 [P]
</code></pre>

<p>The way this works: we use <code>SetEnvIf</code> to check whether the request path matches the path we want to proxy, and if so, set an arbitrary environment variable <code>ADD_COUCH_BASIC_AUTH</code></p>

<p>On the subsequent line, we add a Basic Auth header to the outgoing request, <em>only if</em> the environment variable we set exists. So, the basic auth header will only be added when requesting a resource via <code>/download/</code>, thus sending authentication credentials to CouchDB.</p>

<p>Note: you'll have to Base64-encode your username:password credentials, and replace <code>XXXXXXXXXXX</code> with the encoded value. An easy way to do this, on a Mac:</p>

<pre><code>echo -n 'user:pass' | openssl base64
</code></pre>

<p>Hope this helps somebody besides me!</p>

