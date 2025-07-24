# How to retrieve all document ids matching a search, in elastic search?
[Link to question](https://stackoverflow.com/questions/24252275/how-to-retrieve-all-document-ids-matching-a-search-in-elastic-search)
**Creation Date:** 1402953100
**Score:** 1
**Tags:** elasticsearch
## Question Body
<p>I'm working on a simple side project, and have a tech stack that involves both a SQL database and ElasticSearch. I only have ElasticSearch because I assumed that as my project grows, my full text searching would be most efficiently performed by ES. My ES schema is very simple - documents that I insert into ES have 2 fields, one being the id and the other being the field with the body of text to search. The id being inserted into ES corresponds to that document's primary key id from the SQL database.</p>

<pre><code>insert record into SQL -&gt; insert record into ES using PK from SQL
</code></pre>

<p>Searching would be the reverse of that. Query ES and grab all the matching ids, and then turn around and use those ids to get records from SQL.</p>

<pre><code>search ES can get all PK ids -&gt; use those ids to get documents from SQL
</code></pre>

<p>The problem that I am facing though, is that ES can only return documents in a paginated manner. This is a problem because I also have a <code>WHERE</code> clause on my SQL query, beyond just the ids. My SQL query might look like this ...</p>

<pre><code>SELECT * FROM foo WHERE id IN (1,2,3,4,5) AND bar != 'baz'
</code></pre>

<p>Well, with ES paginating the results, my <code>WHERE</code> clause will always only be querying a subset of the full results from ES. Even if I utilize ES' <code>skip</code> and <code>take</code>, I'm still only querying SQL using a subset of document ids.</p>

<p><strong>Is there a way to get Elastic Search to only return the entire list of matching document ids?</strong> I realize this is here to not allow me to shoot myself in the foot, because doing this across all shards and many many documents is not efficient. Is there no way, though?</p>

<p>After putting in some hours on this project, I've only now realized that I've poorly engineered this, unless I can get all of these ids from ES. Some alternative implementations that I've thought of would be to store the things that I'm filtering on, in SQL, in ES as well. A problem there is that I'd have to update the ES document every time I update the document in SQL. This would require a pretty big rewrite to some of my data access code. I could scrap ElasticSearch all together and just perform searching in Postgres, for now, until I can think of a better way to structure this.</p>

## Answers
### Answer ID: 24969753
<p><a href="http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-request-fields.html" rel="nofollow">http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-request-fields.html</a></p>

<p>please have a look into the elastic search document where you can specify only particular fields that return from the match documents</p>

<p>hope this resolves your problem</p>

<pre><code>{
    "fields" : ["user", "postDate"],
    "query" : {
        "term" : { "user" : "kimchy" }
    }
}
</code></pre>

### Answer ID: 24270699
<p>The elasticsearch not support return each and every doc match to you queries. Because it Ll overload the system.  Instead of this.. Use scroll concept in elasticsearch.. It's lik cursor concept in db's..</p>

<p><a href="http://www.elasticsearch.org/guide/en/elasticsearch/guide/current/scan-scroll.html" rel="nofollow">http://www.elasticsearch.org/guide/en/elasticsearch/guide/current/scan-scroll.html</a></p>

<p>For more examples refer the Github repo. <a href="https://github.com/sidharthancr/elasticsearch-java-client" rel="nofollow">https://github.com/sidharthancr/elasticsearch-java-client</a></p>

<p>Hope it helps.. </p>

