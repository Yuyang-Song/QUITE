# marklogic delete &gt; insert &gt; cpf action on new document
[Link to question](https://stackoverflow.com/questions/21232469/marklogic-delete-insert-cpf-action-on-new-document)
**Creation Date:** 1390216310
**Score:** 1
**Tags:** transactions, xquery, marklogic
## Question Body
<p>see UPDATE below!</p>

<p>I have the following issue: We are collecting (millions) of documents (tweets) into ML and on insert we have a cpf job that creates metadata for each document. More precise it adds a geotag based on location(if location or coordinates are present).</p>

<p>Now we have a database that has been collecting tweets without the geotagger active. We would like to process the stored tweets with this cpf job by deleting and re-inserting each document that does not yet have a proper metadata geotag element.
Then cpf does it's job and geotaggs the "new" document.</p>

<p>We have written the following code to delete and insert the documents but we get a XDMP-CONFLICTUPDATES error. I have been reading about transactions and tried several things, the ";" trick. wrapping in xdmp:eval or splitting up the delete and insert in two separate function calls from xdmp:spawn.</p>

<p>Still no luck.</p>

<p>spawn-rename.xqy</p>

<pre><code>xquery version "1.0-ml";

declare namespace j = "http://marklogic.com/xdmp/json/basic";
declare variable $to_process external;

declare function local:document-rename(
   $old-uri as xs:string, $new-uri as xs:string)
  as empty-sequence()
{
    (:xdmp:set-transaction-mode("update"),:)
    xdmp:eval(xdmp:document-delete($old-uri)),
    (:xdmp:commit():)

    let $permissions := xdmp:document-get-permissions($old-uri)
    let $collections := xdmp:document-get-collections($old-uri)
    return xdmp:document-insert(
      $new-uri, doc($old-uri),
      if ($permissions) then $permissions
      else xdmp:default-permissions(),
      if ($collections) then $collections
      else xdmp:default-collections(),
      xdmp:document-get-quality($old-uri)
    )
};

for $d in map:keys($to_process)
let $rename := local:document-rename($d, map:get($to_process,$d))
return true()
</code></pre>

<p>and to run the job for a specific set of documents we use:</p>

<pre><code>xquery version "1.0-ml";
declare namespace j = "http://marklogic.com/xdmp/json/basic";
declare namespace dikw = 'http://www.example.com/dikw_functions.xqy';
import module namespace json = "http://marklogic.com/xdmp/json" at "/MarkLogic/json/json.xqy";

let $foo := cts:uris((),(), cts:not-query(cts:element-query(xs:QName("j:dikwmetadata"), cts:element-query(xs:QName("j:data"), cts:and-query(())))))
let $items := cts:uri-match("/twitter/403580066367815680.json") (:any valid uri or set of uris:)

let $map := map:map()

    let $f := doc($items[1])
    let $id := $f/j:json/j:id/text()
    let $oldUri := xdmp:node-uri($f)
    let $newUri := fn:concat("/twitter/", $f/j:json/j:id/text(), ".json")
    let $put := map:put($map,$oldUri,$newUri)

    let $spawn := xdmp:spawn("/Modules/DIKW/spawn-rename-split.xqy", (xs:QName("to_process"), $map))

return ($oldUri, " - ", $newUri) 
</code></pre>

<p>Question:</p>

<p>How can I set up the code so that it deleted the documents in the map first in a separate transaction and inserts them back later so cpf can do it's geotagging?</p>

<hr>

<p>UPDATE</p>

<p>Ok so per grtjn his comments (thx so far!)
I try to rewrite my code like :</p>

<pre><code>xquery version "1.0-ml";
declare namespace j = "http://marklogic.com/xdmp/json/basic";

let $entries := cts:uri-match("//twitter/*")
let $entry-count := fn:count($entries)

let $transaction-size := 100 (: batch size $max :)
let $total-transactions := ceiling($entry-count div $transaction-size)

(: set total documents and total transactions so UI displays collecting :)
(: skip 84 85
let $set-total := infodev:ticket-set-total-documents($ticket-id, $entry-count)
let $set-trans := infodev:ticket-set-total-transactions($ticket-id,$total-transactions)
:)
    (: create transactions by breaking document set into maps
each maps's documents are saved to the db in their own transaction :)
let $transactions :=
    for $i at $index in 1 to $total-transactions
    let $map := map:map()
    let $start := (($i -1) *$transaction-size) + 1
    let $finish := min((($start - 1 + $transaction-size),$entry-count))
    let $put :=
        for $entry in ($entries)[$start to $finish]
        (: 96
        let $id := fn:concat(fn:string($entry/atom:id),".xml")
        :)
        let $id := fn:doc($entry)/j:json/j:id/text()
        return map:put($map,$id,$entry)
    return $map

(: the callback function for ingest 
skip 101 let $function := xdmp:function(xs:QName("feed:process-file"))
:)
let $ingestion :=
    for $transaction at $index in $transactions
    return true()
    return $ingestion (: this second return statement seems odd? :)
    (: do spawn here? :)
    (: xdmp:spawn("/modules/spawn-move.xqy", (xs:QName("to_process"), $map)) :)
</code></pre>

<p>Now I am puzzled, to get this 'working' I needed to add the last return which seems not right. Also I am trying to figure out what exactly happens, If I run the query as is it returns with a timeout error.
I would like to first understand what the transaction actually does. 
Sorry for my ignorance but seems that performing a (relatively simple) task as renaming some docs looks not that simple?</p>

<p>for completeness my spawn-move.qry here:</p>

<pre><code>xquery version "1.0-ml";

declare namespace j = "http://marklogic.com/xdmp/json/basic";
declare variable $to_process external;


declare function local:document-move(
   $id as xs:string, $doc as xs:string)
  as empty-sequence()
{
    let $newUri := fn:concat("/twitter/", $id, ".json")
    let $ins := xdmp:document-insert($newUri,fn:doc($doc))
    let $del := xdmp:document-delete($doc) 
    return true()
};

for $d in map:keys($to_process)
let $move := local:document-move($d, map:get($to_process,$d))
return true()
</code></pre>

## Answers
### Answer ID: 21238750
<p>Actually, if you have your CPF pipelines configured to handle updates like creates (this is the default configuration) then just reinserting the document is enough:</p>

<p>xdmp:document-insert($d, doc($d))</p>

### Answer ID: 21238222
<p>I suspect you are not actually renaming the documents, but just re-inserting them. The <code>rename</code> function you quote does not anticipate that situation and does a superfluous <code>document-delete</code> if <code>$old-uri</code> is identical to <code>$new-uri</code>. Add an <code>if</code> around the delete to skip it in that case. Keep everything else to preserve permissions, collections, quality, and properties. The <code>document-insert</code> function already removes pre-existing document before the actual insert. See also:</p>

<p><a href="http://docs.marklogic.com/xdmp:document-insert" rel="nofollow">http://docs.marklogic.com/xdmp:document-insert</a></p>

<p>You might also consider adding a bit of logic to do multiple spawns. You would want to re-insert docs in batches of 100 to 500 docs ideally, depending on hardware and forest config. There is a nice example of how to calculate 'transactions' in this infostudio collector on github (starting from line 80):</p>

<p><a href="https://github.com/marklogic/infostudio-plugins/blob/master/collectors/collector-feed.xqy" rel="nofollow">https://github.com/marklogic/infostudio-plugins/blob/master/collectors/collector-feed.xqy</a></p>

<p>You can also consider doing the geo-work inside those transactions, instead of delegating that to CPF. But if your geo-lookup involves external calls, which could for instance be slow, then stick with CPF..</p>

<p>HTH!</p>

### Answer ID: 21236647
<p>It looks like in your sample that you are trying to delete and write the document to the same URI in the same step.  you may get around this with xdmp:commit().  However, another solution would be to first rename the document in one batch (move them ALL out of the way) and then after that is done, move them back in batches.</p>

