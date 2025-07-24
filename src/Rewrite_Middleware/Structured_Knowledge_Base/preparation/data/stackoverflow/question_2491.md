# Need help on CouchDB rewrites for view with multiple arguments
[Link to question](https://stackoverflow.com/questions/36948391/need-help-on-couchdb-rewrites-for-view-with-multiple-arguments)
**Creation Date:** 1461968783
**Score:** 0
**Tags:** json, url-rewriting, couchdb, vhosts
## Question Body
<p>The original question is below the double bar.
Here is an update and I am hoping for more help.</p>

<p>Hi, </p>

<p>I am finally actively back working on this.
I had this project out-prioritized repeatedly over the past year.
I apologize for not even commenting on your response, it really is giving me hope.</p>

<p>I have a cleaner approach and have made some progress I believe.
I now have around 1900 documents in a database.
Each document has a "type" key.
I've made 30 design documents, one per "type", that each have a view called "all" that returns all rows of the document of that type.</p>

<p>So, now I can execute from a browser a GET like this:</p>

<p>dasvm01.com:5984/registryservice/_design/airplaneidtypes/_view/all</p>

<p>My immediate goal is to shorten this to:</p>

<p>dasvm01.com:5984/registryservice/airplaneidtypes </p>

<p>or </p>

<p>dasvm01.com:5984/registryservice/airplaneidtypes/all</p>

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

<p>Now I think that I need to update the CouchDB daemon:vhosts setting:
I took a crack at it, but I really had no level of confidence and it doesn't seem to work/
In Fauxton, I have:</p>

<pre><code>daemons     
auth_cache {couch_auth_cache, start_link, []}
... 
vhosts {dasvm01.com:5984, /registryservice/_design/airplaneidtypes/_rewrite, []} 
</code></pre>

<p>Not sure if this is: 
 - close, 
 - way off, 
 - not the correct place, 
 - just needs quotes...</p>

<p>What can you tell me?
I don't understand the notation in the default value of Fauxton:</p>

<pre><code>vhosts

    Virtual hosts manager. Provides dynamic add of vhosts without restart, wildcards support and dynamic routing via pattern matching
        [daemons]
            vhosts={couch_httpd_vhost, start_link, []}
</code></pre>

<p>================================================================</p>

<p>I am struggling to get (any) rewrites to work. I've looked at a lot of examples both here and on other sites.  I've tried to emulate the solutions but with no success.  Some level of confusion comes into play because I am passing two arguments to my view. But based on the examples that I see here [10.5.11. /db/_design/design-doc/_rewrite/path<a href="http://docs.couchdb.org/en/latest/api/ddoc/rewrites.html" rel="nofollow noreferrer">1</a> that shouldn't be a problem.</p>

<p>I have this view:</p>

<pre><code> {"dataProvider": {
  "map": "function(doc) {
    if(doc.dataProvider &amp;&amp; doc.status) {
      emit([doc.dataProvider, doc.status], doc); 
      }
    }"
  }
}
</code></pre>

<p>When I hit this URL, the view works fine:</p>

<p>"//ddpspc28:8080/data_providers/_design/basic/_view/dataProvider?key=["TBC-ACT","unstable"]"</p>

<p>I would like to rewrite this so that the URL looks like this:</p>

<p>"//ddpspc28:8080/data_providers/dataProvider?key=["TBC-ACT","unstable"]"</p>

<p>which currently returns:{"error":"not_found","reason":"missing"}</p>

<p>In an effort to do this, I created a field named "rewrites" in my design document "_design/basic" for my database "data_providers".  In the value of rewrites I have this:</p>

<pre><code>"[ 
  {  "from":"/dataProvider",
     "to": "_view/dataProvider"  
  }
 ]”
</code></pre>

<p>I have also tried this:</p>

<pre><code>“[
  {  "from":"/dataProvider",
     "to": "_design/basic/_view/dataProvider"
  }
]”
</code></pre>

<p>I have also tried this:</p>

<pre><code>“[
  {  "from":"dataProvider",
     "to": "/_design/basic/_view/dataProvider"
  }
]”
</code></pre>

<p>I suspect that I may also need a "query" component to the rewrite, but I would be happy at this point to just get the rewrite to take "dataProvider" and anything that follows and replace the dataProvider with the fully qualified path.</p>

## Answers
### Answer ID: 37006799
<p>A rewrite that's defined in the <code>_design/basic</code> document, is accessed at:
<code>//ddpspc28:8080/data_providers/_design/basic/_rewrite</code>.</p>

<p>So, both your first and last try should work, but they'll be accessed at:
<code>//ddpspc28:8080/data_providers/_design/basic/_rewrite/dataProvider</code></p>

<p>Rewrites won't be very useful (to reduce URL sizes) unless you combine them with <a href="https://wiki.apache.org/couchdb/Virtual_Hosts" rel="nofollow">virtual hosts</a>. Combined with virtual hosts can be a nice way to centralize an API.</p>

<p>I typically add a design document with no views (called <code>api</code>) that rewrites to the other design documents' views, etc.</p>

