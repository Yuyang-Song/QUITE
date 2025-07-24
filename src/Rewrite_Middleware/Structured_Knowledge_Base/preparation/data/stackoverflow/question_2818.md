# Issue in index upgrading eXist-db version 2 to 4.5
[Link to question](https://stackoverflow.com/questions/53858401/issue-in-index-upgrading-exist-db-version-2-to-4-5)
**Creation Date:** 1545249763
**Score:** 1
**Tags:** lucene, xquery, exist-db
## Question Body
<p>I am in process of upgrading and testing a large installation and have hit one issue I cannot understand. I have a large collection of documents in which my index is created as follows:</p>

<pre><code>&lt;collection xmlns="http://exist-db.org/collection-config/1.0"&gt;
    &lt;index xmlns:mods="http://www.loc.gov/mods/v3" xmlns:xlink="http://www.w3.org/1999/xlink"&gt;
        &lt;fulltext default="none" attributes="false"/&gt;
        &lt;lucene&gt;
            &lt;analyzer class="org.apache.lucene.analysis.standard.StandardAnalyzer"&gt;
                &lt;param name="stopwords" type="org.apache.lucene.analysis.util.CharArraySet"/&gt;
            &lt;/analyzer&gt;
            &lt;analyzer id="ws" class="org.apache.lucene.analysis.WhitespaceAnalyzer"/&gt;
            &lt;text qname="p"/&gt;
            &lt;text qname="li"/&gt;
            &lt;text qname="h1"/&gt;
            &lt;text qname="h2"/&gt;
            &lt;text qname="h3"/&gt;
        &lt;/lucene&gt;
    &lt;/index&gt;
&lt;/collection&gt;
</code></pre>

<p>In my version 2 installation this works perfect. A query returns only element in the list (p, li, h1, h2, h3). It also <em>only</em> returns those elements with the text in the element (as expected). The search function is:</p>

<pre><code>declare function ls:ls($collection as xs:string, $phrase as xs:string) as element()* {
    for $hit in collection(xmldb:encode-uri($collection))//*[ft:query(.,
        &lt;query&gt;
            &lt;phrase&gt;{$phrase}&lt;/phrase&gt;
        &lt;/query&gt;
        )]
        order by $hit/ancestor::div[@class='content']/@doc/string()
        return 
            &lt;tr&gt;
                &lt;td&gt;
                    {$hit/ancestor::div[@class='content']/@doc/string()}
                &lt;/td&gt;
                &lt;td&gt;
                    {$hit/ancestor::div[@class='content']/@title/string()}
                &lt;/td&gt;
                &lt;td&gt;
                    {local-name($hit)}
                &lt;/td&gt;
                &lt;td class="hit_text"&gt;
                    {normalize-space($hit)}
                &lt;/td&gt;
            &lt;/tr&gt;
};
</code></pre>

<p>Just to see the result, here's a snapshot of the web page results:</p>

<p><a href="https://i.sstatic.net/jJjxE.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/jJjxE.png" alt="enter image description here"></a></p>

<p>Of course this is not showing all the results, but trust me ... it is only returning the named elements and only those with "heart" in them.</p>

<p>After export/import of the content to the new version 4 installation most everything else is working perfect. However, even after reindexing the content the exact same xQuery returns unwanted higher level elements (like div) and also returns elements which do not contain the search phrase.</p>

<p>For example, this exact same query shows this result:</p>

<p><a href="https://i.sstatic.net/3jjXy.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/3jjXy.png" alt="enter image description here"></a></p>

<p>Now, oddly enough, if I change the function to remove the wildcard and go only after "h1" (or any other of the named elements), it works:</p>

<pre><code>for $hit in collection(xmldb:encode-uri($collection))//h1[ft:query(.,
</code></pre>

<p>Yields:</p>

<p><a href="https://i.sstatic.net/FIHou.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/FIHou.png" alt="enter image description here"></a></p>

<p>You can see that unlike the previous example, the h1 without "heart" is not returned.</p>

<p>What did I miss in my upgrade? is there some change to Lucene I missed or do not understand?</p>

<h2>Update</h2>

<p>As a hack (IMHO), this works:</p>

<pre><code>let $targets := collection(xmldb:encode-uri($collection))//*[local-name(.) = 'p' or local-name(.) = 'h1' or local-name(.) = 'h2' or local-name(.) = 'h3' or local-name(.) = 'li']
    for $hit in $targets[ft:query(.,
        &lt;query&gt;
            &lt;phrase&gt;{$phrase}&lt;/phrase&gt;
        &lt;/query&gt;
        )]
</code></pre>

<p>But if I remove creating the nodeset $targets and put the collection() in the "for" then it does not work.</p>

<h2>Update II</h2>

<p>There must be something wrong (as in the full text is not enabled or running or ?) because running a similar query in both takes <em>way</em> longer in the new, updated server. </p>

<p>So what did I miss in the upgrade? I have conf.xml calling out Lucene in both. Any hints for what to look for would be great.</p>

<h2>Update III</h2>

<p>Maybe this in the logs is a problem? I doubt it as searching the log of the 2.x version shows the same error.</p>

<pre><code>2018-12-19 19:27:05,570 [qtp14962548-143] ERROR (AnalyzerConfig.java [configureAnalyzer]:173) - Lucene index: analyzer class org.apache.lucene.analysis.WhitespaceAnalyzer not found. (org.apache.lucene.analysis.WhitespaceAnalyzer) 
2018-12-19 19:27:38,852 [qtp14962548-43] INFO  (NativeBroker.java [reindexCollection]:1844) - Start indexing collection /db/EIDO/data/Core 
2018-12-19 19:27:54,837 [qtp14962548-43] INFO  (NativeBroker.java [reindexCollection]:1854) - Finished indexing collection /db/EIDO/data/Core in 15985 ms. 
</code></pre>

<h2>Update IV</h2>

<p>I changed the collection.xconf to as suggested to remove stopwords and removing the WhitespaceAnalyzer:</p>

<pre><code>&lt;collection xmlns="http://exist-db.org/collection-config/1.0"&gt;
    &lt;index xmlns:mods="http://www.loc.gov/mods/v3" xmlns:xlink="http://www.w3.org/1999/xlink"&gt;
        &lt;fulltext default="none" attributes="false"/&gt;
        &lt;lucene&gt;
            &lt;analyzer class="org.apache.lucene.analysis.standard.StandardAnalyzer"/&gt;
            &lt;text qname="p"/&gt;
            &lt;text qname="li"/&gt;
            &lt;text qname="h1"/&gt;
            &lt;text qname="h2"/&gt;
            &lt;text qname="h3"/&gt;
        &lt;/lucene&gt;
    &lt;/index&gt;
&lt;/collection&gt;
</code></pre>

<p>I reindexed the collection. From the log:</p>

<pre><code>2018-12-20 02:14:56,803 [qtp31631875-34] INFO  (NativeBroker.java [reindexCollection]:1844) - Start indexing collection /db/EIDO/data/Core 
2018-12-20 02:15:16,553 [qtp31631875-34] INFO  (NativeBroker.java [reindexCollection]:1854) - Finished indexing collection /db/EIDO/data/Core in 19750 ms. 
</code></pre>

<p>I get the exact same result.</p>

<h2>Update V</h2>

<p>I guess I am punting. Going to run the entire process again this weekend, deleting everything and trying again but this makes no sense and does not work.</p>

<h2>Update VI</h2>

<p>I don't like to punt! Now, in looking at the results, essentially this search in the current installation:</p>

<pre><code> for $hit in collection(xmldb:encode-uri($collection))//*[ft:query(.,
        &lt;query&gt;
            &lt;phrase&gt;{$phrase}&lt;/phrase&gt;
        &lt;/query&gt;
        )]
</code></pre>

<p>Returns every element in the database, whether they have $phrase or not. It returns the div, then the child p, then maybe the child span. All of them. It does not matter whether the word actually exists in the text.</p>

<p>If I change the wildcard "*" to say "h1", it returns only the h1's that actually have that text in them. So something is not right or broken or? I certainly can chnage the element list fed to the ft:query to the exact elements in question (p, h1, h2, h3, li) but that query takes forever in 4.5 and a few seconds in 2.</p>

<h2>Update Likely last</h2>

<p>I gave up and reinstalled everything including Monex. I re-exported the existing DB and imported it. I only change the port to 80 although there are other changes I normally make.</p>

<p>Now, even trying to run the dashboard (after import) yields:</p>

<pre><code>javax.servlet.ServletException: javax.servlet.ServletException: An error occurred while processing request to /exist/apps/dashboard/: err:XPST0081 error found while loading module restxq: Error while loading module modules/restxq.xql: Invalid qname text:groups
    at org.eclipse.jetty.server.handler.HandlerCollection.handle(HandlerCollection.java:146)
    at org.eclipse.jetty.server.handler.gzip.GzipHandler.handle(GzipHandler.java:724)
    at org.eclipse.jetty.server.handler.HandlerWrapper.handle(HandlerWrapper.java:132)
    at org.eclipse.jetty.server.Server.handle(Server.java:531)
    at org.eclipse.jetty.server.HttpChannel.handle(HttpChannel.java:352)
    at org.eclipse.jetty.server.HttpConnection.onFillable(HttpConnection.java:260)
    at org.eclipse.jetty.io.AbstractConnection$ReadCallback.succeeded(AbstractConnection.java:281)
    at org.eclipse.jetty.io.FillInterest.fillable(FillInterest.java:102)
    at org.eclipse.jetty.io.ChannelEndPoint$2.run(ChannelEndPoint.java:118)
    at org.eclipse.jetty.util.thread.QueuedThreadPool.runJob(QueuedThreadPool.java:760)
    at org.eclipse.jetty.util.thread.QueuedThreadPool$2.run(QueuedThreadPool.java:678)
</code></pre>

<p>Which indicates to me that an export of the database and then reimport will not ever work if you have different apps installed. </p>

<p>Unfortunately I have to punt and look at alternate solutions. I could attempt to just rebuild data or something, but the app had 10,000 users. That cannot be recreated.</p>

<p>At this time, I can only say it is not ready for prime time and will just sit on the old database that works perfectly and has done so for years.</p>

<p>And just to note ... after installation of the fresh, clean database and no changes I can access Monex or dashboard. If I import from my backup (as required because it is not binary compatible) it all breaks.</p>

<p>This is an obvious issue to me for the developers.</p>

<h2>Update Again</h2>

<p>I did a completely clean install. After that I can access Monex no issues. I then restore my database. NOTE: There is a question at the moment it is finished which is asking if I wish to upgrade the apps. Not sure the right answer, maybe that is one issue and I answer wrong (I answer no).</p>

<p>After all is reinstalled, I can get to the DB fine and my whole application. But when trying to run Monex, I now get:</p>

<pre><code>&lt;exception&gt;
    &lt;path&gt;/db/apps/monex/modules/view.xql&lt;/path&gt;
    &lt;message&gt;err:XPST0081 error found while loading module indexes: Error while loading module indexes.xqm: Invalid qname text:index-terms&lt;/message&gt; 
&lt;/exception&gt;
</code></pre>

<p>Is the proper answer yes to upgrade the apps? I assume what this means is that the Monex I installed with just a pure installation is overwritten by my version 2 backup and this is causing an error.</p>

<p>I hacked out the part of monex's index causing an issue and got Monex to run. So it is using Lucene:</p>

<p><a href="https://i.sstatic.net/dUHXB.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/dUHXB.png" alt="enter image description here"></a></p>

<p>So, one observation is the issue as to why Monex runs fine but restore my (old) DB kills it. It should not AFAIK.</p>

<p>maybe someone can explain this result to me, I do not understand the second item but I suspect that it is the one returning everything:</p>

<p><a href="https://i.sstatic.net/O0mDw.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/O0mDw.png" alt="enter image description here"></a></p>

<h2>OK, Working</h2>

<p>So. First, i figured out that the restore of my /db will ruin all the /apps (like monex) in a fresh install. Seems strange to me or bad planning on my or others. So to fix this issue, I have a fresh install backup.</p>

<p>After I install the new version of eXist, I restore my old database and then immediately restore the fresh install again. This overwrites all the /apps (like monex) with the latest versions that were installed from my backup but does not ruin mine. Sorry, ridiculous. </p>

<p>Now after that I could test and see the the Lucene index is being used. But that is all it told me, nothing else (as I suspected). </p>

<p>It is obvious that the behavior has changed in the Lucene integration. In my old version, I would send every element and it would only return the hits. In this new version, you cannot do that. If you send something like is done in the code above, it will still return it as a "hit" even if there is none. Therefore, the $collection//* sends the entire structure to the query and it returns everything, whether there is a hit or not. It did not behave this way before.</p>

<p>So the solution is (which is such a hack I hate to even say it), that you can only send the items to the query that you want search to see if there is content that is a hit. WOW. Again, I am sorry but if I am wrong please show me but that is a total hack. If I create an index of all the p's, I only expect the p's back if I do a general search sending it p's, h1's, etc. What happens now is it sends everything back, hit or not, unless you ask for the exact same name of element that you indexed. </p>

<p>It seems like a late/early binding thing. In the old eXist I would send $coll/<em>[ft:query... and it returned what I had as identified elements in my index. Now it does not work that way so you cannot execute the for loop across $coll/</em>[ft:query... as it still returns <em>everything</em>. IMHO that is wrong.</p>

<p>So to solve, I did this, basically execute the search first and then iterate over the results.</p>

<pre><code>declare function ls:ls($collection as xs:string, $phrase as xs:string) as element()* {
    let $coll := collection(xmldb:encode-uri($collection))
    let $hits := ($coll//p | $coll//li | $coll//h1 | $coll//h2 | $coll//h3)[ft:query(.,
        &lt;query&gt;
            &lt;phrase&gt;{$phrase}&lt;/phrase&gt;
        &lt;/query&gt;
        )]
    for $hit in $hits
        order by $hit/ancestor::div[@class='content']/@doc/string()
        return 
            &lt;tr&gt;
                &lt;td&gt;
                    {$hit/ancestor::div[@class='content']/@doc/string()}
                &lt;/td&gt;
                &lt;td&gt;
                    {$hit/ancestor::div[@class='content']/@title/string()}
                &lt;/td&gt;
                &lt;td&gt;
                    {local-name($hit)}
                &lt;/td&gt;
                &lt;td class="hit_text"&gt;
                    {normalize-space($hit)}
                &lt;/td&gt;
            &lt;/tr&gt;
}
</code></pre>

<p>;</p>

<p>And now I updated to test and this works also:</p>

<pre><code>let $hits := (collection(xmldb:encode-uri($collection))//*)[ft:query(.,
    &lt;query&gt;
        &lt;phrase&gt;{$phrase}&lt;/phrase&gt;
    &lt;/query&gt;
    )]
for $hit in $hits ...
</code></pre>

<p>So this is now so close to what I had before, I do NOT need to go after the explicit elements which is correct. The issue is that now they cannot be on the for loop.</p>

<p>The key is here:</p>

<pre><code>(collection(xmldb:encode-uri($collection))//*)
</code></pre>

<p>versus:</p>

<pre><code>collection(xmldb:encode-uri($collection))//*
</code></pre>

<p>And so ... all of that ... and the solution is the the for loop needs to be:</p>

<pre><code>for $hit in (collection(xmldb:encode-uri($collection))//*)[ft:query(.,
    &lt;query&gt;
        &lt;phrase&gt;{$phrase}&lt;/phrase&gt;
    &lt;/query&gt;
    )]
</code></pre>

<p><strong><em>Since this is now solved, maybe someone would like to explain why the old code which did not use () around the individual elements worked but does not in the latest eXist.</em></strong></p>

<p>Just to be exact, I have both systems open for testing.</p>

<p><strong>Version 2x:</strong></p>

<pre><code>for $hit in collection(xmldb:encode-uri($collection))//*[ft:query(.,
</code></pre>

<p>One second, correct answer.</p>

<pre><code>for $hit in (collection(xmldb:encode-uri($collection))//*)[ft:query(.,
</code></pre>

<p>17 seconds, correct answer.</p>

<p><strong>Version 4.5:</strong></p>

<pre><code>for $hit in collection(xmldb:encode-uri($collection))//*[ft:query(.,
</code></pre>

<p>10 seconds, completely wrong answer (div's and non-hits returned)</p>

<pre><code>for $hit in (collection(xmldb:encode-uri($collection))//*)[ft:query(.,
</code></pre>

<p>one second, right answer.</p>

<p>It looks to me that in old eXist, a query returned nothing and in this new eXist is seems to return a result for every element sent, and if no index exists it still returns it.</p>

<h2>One last update</h2>

<p>In looking through the clean install <code>conf.xml</code>, I found a comment in the xquery entry for <code>enable-query-rewriting</code>. This comment suggests that it is experimental and setting to "yes" could lead to incorrect results.</p>

<p>I would note that I do not believe I touched this and a default installation has this value set to "yes". I saved out conf.xml from the clean install as I change many things in it (of course), in looking at the clean installation I see this:</p>

<pre><code>&lt;xquery enable-java-binding="no" disable-deprecated-functions="no" 
        enable-query-rewriting="yes" backwardCompatible="no" 
        enforce-index-use="always"
        raise-error-on-failed-retrieval="no"&gt;
</code></pre>

<p>I changed to "no" and restarted exist-db. Now everything works as it did before, I now have no issues in the search and it returns exactly what I expect with the query written exactly as it was in version 2x.</p>

<h2>So ... what I believe I learned</h2>

<p>I implemented the new range indexes and reindexed the collection based on the comments below and re-enabled the query rewriting. Checking monex I see the indexes but my queries did not use them, it reported index as the legacy "range" and optimization as "No Index".</p>

<p>I found that I cannot do this (which the wildcard would be doing I assume):</p>

<p>($collection//foo | $collection//bar)[contains(.,$phrase)]</p>

<p>or this</p>

<p>($collection//foo , $collection//bar)[contains(.,$phrase)]</p>

<p>or this</p>

<p>$testnodes := $collection//foo | $collection//bar</p>

<p>then </p>

<p>$testnodes[contains(.,$phrase)]</p>

<p>While it works, it does not use the new-range index. These would always report no index used. </p>

<p>But this does use full optimized, new-range indexes:</p>

<p>$collection//foo[contains(.,$phrase)] | $collection//bar[contains(.,$phrase)]</p>

## Answers
### Answer ID: 53861545
<p>We should clear up the errors first...</p>

<ol>
<li>The class for the Whitespace Analyzer should be <code>org.apache.lucene.analysis.core.WhitespaceAnalyzer</code>.</li>
</ol>

<p>Although it doesn't look like you reference the whitespace analyzer by its 'id' so, you could just remove it.</p>

<ol start="2">
<li>The config for your use of the <code>StandardAnalyzer</code> looks wrong to me. You have specified a <code>stopwords</code> parameter, but:

<ol>
<li>its class is wrong, it should be <code>org.apache.lucene.analysis.util. CharArraySet</code>, and </li>
<li>you have not given it any value(s).</li>
</ol></li>
</ol>

<p>If you just want the default stop words, you can omit the parameter entirely.</p>

<p>Once you have made those changes, you should try reindexing and monitor the logs again.</p>

<p>After that you should use the Monex app from the Dashboard in eXist 4.5.0 to examine the available indexes, to check that your data was indexed as you expected.</p>

<h1>Update 1</h1>

<p>From the comment of @kevin-brown:</p>

<blockquote>
  <p>From what I see today, if I do this ($collection//foo | $collection//bar)[fn:contains(.,'string')] no index is used. But if I do this $collection//foo[fn:contains(.,'string')] | $collection//bar[fn:contains(.,'string')],the new-range index is used and optimization is full.</p>
</blockquote>

<p>I can confirm that in certain formulation of the XQuery, eXist-db is not correctly optimising the query to make use of the range index. This is certainly a bug!</p>

<p>The Java Admin Client of eXist-db allows you to show a trace of the query:</p>

<ol>
<li><p><code>($collection//foo | $collection//bar)[fn:contains(., $string)]</code> which Kevin reported did not use the index, produces the trace:</p>

<pre><code>$collection/descendant::{}foo union
    $collection/descendant::{}bar
        [contains(self::node(), $string)]
</code></pre></li>
<li><p><code>$collection//foo[fn:contains(., $string)] | $collection//bar[fn:contains(., $string)]</code> which Kevin reported did correctly use the index, produces the trace:</p>

<pre><code>$collection
(# exist:optimize-field #)
(# exist:optimize #) {
    descendant::{}foo[range:contains(self::node(), $string)]
}
union $collection
(# exist:optimize-field #)
(# exist:optimize #) {
    descendant::{}bar[range:contains(self::node(), $string)]
}
</code></pre></li>
</ol>

<p>In (2) we can clearly see that optimizations are indicated by XQuery pragmas. These mean that a suitable index was detected and will be used during evaluation.</p>

<p>By comparison, in (1) we see that eXist failed to correctly detect the available indexes that could allow for an optimisation.</p>

<p>Sadly, it also seems that eXist-db might have used the wrong axis for these, i.e. descendant rather that descendant-or-self.</p>

<p>I have opened a GitHub issue for eXist-db which reports this problem - <a href="https://github.com/eXist-db/exist/issues/2363" rel="nofollow noreferrer">https://github.com/eXist-db/exist/issues/2363</a></p>

### Answer ID: 53894429
<p>eXist-db 2.2 was released 2014, so long-jump upgrades across two major versions have a tendency to not be straight forward. </p>

<p>It looks like your code is still using the legacy-range index,  which is the likely cause of your unwanted results, as reported by monex.  </p>

<p>This index is marked as deprecated with the new range index to be used instead.</p>

<p>If you can't provide a MWE, you need to figure out which of your queries call the old range index and change them to the new,  or disable the old-range index entirely.</p>

<p>I would not recommend to use e.g. and old monex inside a new exist, and to say <code>yes</code> when asked to upgrade default apps to newer version. You can still run a production site without any default apps. </p>

<p>It's not possible to tell from your examples how <code>for $hit in (collection(xmldb:encode-uri($collection))//*)[ft:query(.,</code> side-steps invocations of the old-range index in your app, it should give you a clue though.      My guess is, if you get rid of those invocations,  you ll see <code>for $hit in collection(xmldb:encode-uri($collection))//*[ft:query(.,</code> to act and work in the same way.</p>

### Answer ID: 53875909
<p>Although I'm still new to eXist, it seems to me there are two ideas being conflated.</p>

<p>Telling Lucene to index something is not the same as putting a predicate on a query Xpath. The <code>qname</code> for a Lucene index doesn't (I believe) mean a given element won't be subject to query. It's just a question of what is indexed by Lucene in order to speed searches? The fact that you found a speed improvement by using a predicate suggests this is true.</p>

<p>When I do my searches, I still restrict the elements subject to query regardless of what I tell Lucene to index. I don't personally see that as a hack - just reducing the 'search pool'. I don't use <code>local-name()</code> as predicate. Rather, I would use the element itself. I'm not sure if there is a cost to using <code>local-name()</code> versus this:</p>

<pre><code>let $coll := collection(xmldb:encode-uri($collection))

let target := $coll//p | $coll//h1 | $coll//h2 | $coll//h3 | $coll//li
</code></pre>

<p>Depending on your XML hierarchy, you might find even more speed by reducing the pool of nodes with <code>collection(xmldb:encode-uri($collection))//some-element</code></p>

<p>The above might use then use Lucene indexes more efficiently? It's worth testing.</p>

<p>Furthermore, although I don't know what the hierarchy of your XML is, you can also explicitly tell Lucene to <em>ignore</em> certain elements (but this is usually for those elements nested inside those which you are indexing):</p>

<pre><code> &lt;ignore qname="div"/&gt;
</code></pre>

<p>NB: I use eXist 4.4</p>

<p>Added: try using <a href="https://exist-db.org/exist/apps/doc/newrangeindex" rel="nofollow noreferrer">range index</a> in addition to Lucene. Also I don't see a name-space in the <code>qnames</code> (plus you have two namespaces operating, and I've added a third for <code>xmlns:xs</code> in the range index).</p>

<p>This example assumes (copied from eXist documentation linked above) a namespace of <code>mods</code> for demonstration. But it must be appended to each <code>qname</code> if there is a specific namespace in the xml collections. </p>

<pre><code>&lt;collection xmlns="http://exist-db.org/collection-config/1.0"&gt;
  &lt;index xmlns:mods="http://www.loc.gov/mods/v3" 
        xmlns:xlink="http://www.w3.org/1999/xlink"  
        xmlns:xs="http://www.w3.org/2001/XMLSchema"&gt;
    &lt;fulltext default="none" attributes="false"/&gt;
    &lt;range&gt;
       &lt;create qname="mods:p" type="xs:string"/&gt;
       &lt;create qname="mods:li" type="xs:string"/&gt;
       &lt;create qname="mods:h1" type="xs:string"/&gt;
       &lt;create qname="mods:h2" type="xs:string"/&gt;
       &lt;create qname="mods:h3" type="xs:string"/&gt;
    &lt;/range&gt;
    &lt;lucene&gt;
        &lt;analyzer class="org.apache.lucene.analysis.standard.StandardAnalyzer"/&gt;
        &lt;text qname="mods:p"/&gt;
        &lt;text qname="mods:li"/&gt;
        &lt;text qname="mods:h1"/&gt;
        &lt;text qname="mods:h2"/&gt;
        &lt;text qname="mods:h3"/&gt;
        &lt;ignore qname="mods:div"/&gt;
    &lt;/lucene&gt;
  &lt;/index&gt;
&lt;/collection&gt;
</code></pre>

<p>Remove namespace declarations that aren't used.</p>

