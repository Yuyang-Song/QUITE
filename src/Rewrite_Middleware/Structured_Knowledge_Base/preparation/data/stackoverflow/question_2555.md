# CouchDB Erlang Replication Filter - Slower than Javascript
[Link to question](https://stackoverflow.com/questions/39990772/couchdb-erlang-replication-filter-slower-than-javascript)
**Creation Date:** 1476248136
**Score:** 3
**Tags:** performance, couchdb, replication
## Question Body
<p>We have couchbase lite replicating from Couchdb 1.6.1 using replication filters. The problem is that as the number of documents increases (we have atleast 100k documents in a single database), the replication time becomes slower and slower as the filter has to go through each of the documents(and revisions) to ensure that it matches the replication filter.</p>

<p>We initially had our filter written in Javascript and it was suggested in many places to replace that with Erlang because we can skip the time taken for the JSON serialization/de-serialization that has to be happen in the case of Javascript and also the sandboxing. Writing filters in erlang will bypass all this because its run in the same VM.</p>

<p>With all this and rewriting our filter in Erlang, we find that Erlang replication filters are slower than that of Javascript by an order of 2, which is very strange. Ive been reading Erlang and trying out based on what Ive read, so not very experienced by any means. Our filters are relatively straightforward, so Im struggling to understand why its so slow.</p>

<p>The filters take a query string that contains a list of ids. It then goes through the list of documents that match that id in a few different fields and returns those documents. For e.g. a Customer may have contacts, jobs, estimates etc, when the query contains ids of customers, it brings them all their jobs,estimates,contacts etc.</p>

<p>Im attaching the Javascript and Erlang versions of our filter</p>

<p>Javascript version:<a href="http://pastebin.com/c7AqstWy" rel="nofollow">http://pastebin.com/c7AqstWy</a></p>

<p>Erlang version: <a href="http://pastebin.com/fta9JShM" rel="nofollow">http://pastebin.com/fta9JShM</a> and <a href="http://pastebin.com/mseYiUaR" rel="nofollow">http://pastebin.com/mseYiUaR</a> 
(The second link was another attempt to see if it will make it faster because it doesnt have to go through the case statement at all). </p>

<p>Both the versions using Erlang were 1.8 to 2 times slower than the Javascript ones.</p>

<p>Can someone please take a look and highlight why the Erlang filters could be slower ?</p>

