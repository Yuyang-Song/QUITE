# Cloudant Search: what are the conditions for using the count facet?
[Link to question](https://stackoverflow.com/questions/43704808/cloudant-search-what-are-the-conditions-for-using-the-count-facet)
**Creation Date:** 1493543770
**Score:** 0
**Tags:** search, cloudant, faceted-search
## Question Body
<p>I am trying to set up a search index using Cloudant, but I find <a href="https://docs.cloudant.com/search.html#faceting" rel="nofollow noreferrer">the documentation</a> pretty confusing. It states:</p>

<blockquote>
  <h2>FACETING</h2>
  
  <p>In order to use facets, all the documents in the index must include all the fields that have faceting enabled. If your documents do not include all the fields, you will receive a bad_request error with the following reason, “dim field_name does not exist.”</p>
  
  <p>If each document does not contain all the fields for facets, it is recommended that you create separate indexes for each field. If you do not create separate indexes for each field, you must include only documents that contain all the fields. Verify that the fields exist in each document using a single if statement.</p>
  
  <h3>Counts</h3>
  
  <p>The count facet syntax takes a list of fields, and returns the number of query results for each unique value of each named field.</p>
  
  <p>The count operation works only if the indexed values are strings. The indexed values cannot be mixed types. For example, if 100 strings are indexed, and one number, then the index cannot be used for count operations. You can check the type using the typeof operator, and convert using parseInt, parseFloat and .toString() functions.</p>
</blockquote>

<p>Specifically, what does it means when "all the documents in the index include all the fields that have faceting enabled".</p>

<p>For example, if my database consists of the following doc:</p>

<pre><code>{
  "_id": "mydoc"
  "subjects": [ "subject A", "subject B" ]
}
</code></pre>

<p>And I write a search index like so:</p>

<pre><code>function (doc) {
  for(var i=0; i &lt; doc.subjects.length; i++)
    index("hasSubject", doc.subjects[i], {facet: true});
}
</code></pre>

<p>Would this be illegal because <code>mydoc</code> doesn't have a field called <code>hasSubject</code>? And when we rewrite the query to look like;</p>

<pre><code>{
  "_id": "mydoc"
  "hasSubject": true,
  "subjects": [ "subject A", "subject B" ]
}
</code></pre>

<p>Would that suddenly make it OK...?</p>

## Answers
### Answer ID: 43724762
<p>So the new documentation is at <a href="https://console.ng.bluemix.net/docs/services/Cloudant/api/search.html#faceting" rel="nofollow noreferrer">https://console.ng.bluemix.net/docs/services/Cloudant/api/search.html#faceting</a> ; however, the entry on faceting is the same. So no big deal there.</p>

<p>To answer your question though, I think what the documentation is saying is that all the JSON docs in your database must contain the <code>subjects</code> field, which is what you're declaring you want to facet on in your example.</p>

<p>So I would also consider defining your search index like so:</p>

<pre><code>function (doc) {
  if (doc.subjects) {
    for(var i=0; i &lt; doc.subjects.length; i++) {
      if (typeof doc.subjects[i] == "string") {
        index("hasSubject", doc.subjects[i], {facet: true});
      }
    }
  }
}
</code></pre>

<p>And if you had a doc like this in your database:</p>

<pre><code>{
  "_id": "mydoc"
  "hasSubject": true,
}
</code></pre>

<p>I think that would suddenly make your facets NOT ok.</p>

