# CouchDB vhosts and URL rewrites for multiple arguments
[Link to question](https://stackoverflow.com/questions/49967972/couchdb-vhosts-and-url-rewrites-for-multiple-arguments)
**Creation Date:** 1524413072
**Score:** 0
**Tags:** url-rewriting, couchdb, vhosts, couchdb-mango, fauxton
## Question Body
<p>I've tried reading the CouchDB documentation, but I find it a bit vague in this area (FAUXTON, vhost specification).  I've searched and read the responses on stackoverflow for "couchdb vhosts" and "couchdb rewrite url" and tried to apply the advice I can gleen there.  Still stuck on this and would appreciate some specific direction if anyone can provide it.</p>

<p>I have around 1900 documents in a couchDB database. Each document has a "type" key. I've made 30 design documents, one per "type". Each design docuemnt has a view called "all" that returns all rows of the document of that type.</p>

<p>In the information below, dasvm01.com is not the actual server.  It is behind a company firewall and not accessible to the outside world.  I've tried to use it consistently, forgive me if I have errored anywhere.</p>

<p>So, now I can execute a GET like this from a browser:</p>

<pre><code>dasvm01.com:5984/registryservice/_design/airplaneidtypes/_view/all
</code></pre>

<p>My immediate goal is to shorten this to:</p>

<pre><code>dasvm01.com:5984/registryservice/airplaneidtypes
</code></pre>

<p>or</p>

<pre><code>dasvm01.com:5984/registryservice/airplaneidtypes/all
</code></pre>

<p>To this end, I added a rewrites function to the airplaneidtypes design doc:</p>

<pre><code>{
  "_id": "_design/airplaneidtypes",
  "_rev": "11-c28b41a718017cbcd65f82f4acc611cb",
  "views": {
    "all": {
      "map": "function (doc) 
           {  if(doc.ddoc === 'airplaneidtypes') 
               {    emit(doc._rev,doc);  }
           }"
    }
  },
  "language": "javascript",
  "rewrites": [
    {
      "from": "/airplaneidtypes",
      "to": "registryservice/_design/airplaneidtypes/_rewrite",
      "method": "GET"
    }
  ]
}
</code></pre>

<p>Now I think that I need to update the CouchDB daemon:vhosts setting: I took a crack at it, but I really had no level of confidence and it doesn't seem to work. In Fauxton, I have:</p>

<pre><code>daemons     
auth_cache {couch_auth_cache, start_link, []}
... 
vhosts {dasvm01.com:5984, /registryservice/_design/airplaneidtypes/_rewrite, []} 
</code></pre>

<p>Not sure if this is: - close, - way off, - not the correct place, - just needs quotes...</p>

<p>What can you tell me? I don't understand default the notation in Fauxton is trying to convey:</p>

<pre><code>vhosts

    Virtual hosts manager. Provides dynamic add of vhosts without restart, wildcards support and dynamic routing via pattern matching
        [daemons]
            vhosts={couch_httpd_vhost, start_link, []}
</code></pre>

<p>Ultimately, I want/hope to allow the user to pass multiple key:value pairs on the URL and then rewrite them into a MANGO query.  The user would pass something like this:</p>

<pre><code>dasvm01.com:5984/registryservice/airplaneidtypes/model/A320/variant/251N
</code></pre>

<p>that would get rewritten into the MANGO query:</p>

<pre><code>    {
    "selector": {
        "model": "A320",
        "variant": {"$eq": "251N"}
    },
    "fields": [
        "_id",
        "_rev",
        "status",
        "model",
        "variant",
        "variant-type",
        "oem",
        "historicaloem",
        "displaymodel",
        "actsmodel"
    ]
}
</code></pre>

## Answers
### Answer ID: 49974949
<blockquote>
  <p>Ultimately, I want/hope to allow the user to pass multiple key:value
  pairs on the URL and then rewrite them into a MANGO query. The user
  would pass something like this:</p>
  
  <p>dasvm01.com:5984/registryservice/airplaneidtypes/model/A320/variant/251N</p>
</blockquote>

<p>I'm not sure which server-side technology you're using, but in the case of NodeJS/ExpressJS, you can do this:</p>

<hr>

<p>User sends the following GET request from within the browser to ExpressJS server:</p>

<pre><code>GET /registryservice/airplaneidtypes/model/A320/variant/251N
</code></pre>

<p>The ExpressJS which is running on <code>dasvm01.com</code> and listening on (for example) port <code>8080</code> receives the GET request and handles it like this:</p>

<pre><code>app.get('/registryservice/:typeId/model/:modelId/variant/:variantId', (req, res)=&gt;{

  // Now you have acess to req.params object
  // You can use them as you wish:

  mango_query = {
      "selector": {
          "model": `${req.params.modelId}`,
          "variant": {"$eq": `${req.params.variantId}`}
      },
      "fields": [
          "_id",
          "_rev",
          // ...
      ]
  }
  // You can communicate with CouchDB by making HTTP requests
  // to CouchDB server which is running (for example) on 127.0.0.1 and listening
  // on port 5984

  // For sending HTTP requests, you might use `node-fetch` package
})
</code></pre>

<hr>

<p>Basically, the above idea is to use <a href="http://expressjs.com/en/guide/routing.html#route-parameters" rel="nofollow noreferrer" title="Route parameters">route parameters</a> of ExpressJS server, so that you can re-route the user requests.</p>

