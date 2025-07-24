# Sphinx/Solr/Lucene/Elastic Relevancy
[Link to question](https://stackoverflow.com/questions/3498046/sphinx-solr-lucene-elastic-relevancy)
**Creation Date:** 1281999130
**Score:** 1
**Tags:** lucene, solr, sphinx
## Question Body
<p>We have an extremely large database of 30+ Million products, and need to query them to create search results and ad displays thousands of times a second. We have been looking into Sphinx, Solr, Lucene, and Elastic as options to perform these constant massive searches.</p>

<p>Here's what we need to do. Take keywords and run them through the database to find products that match the closest. We're going to be using our OWN algorithm to decide which products are most related to target our advertisements, but we know that these engines already have their own relevancy algorithms.</p>

<p>So, our question is how can we use our own algorithms on top of the engine's, efficiently. Is it possible to add them to the engines themselves as a module of some sort? Or would we have to rewrite the engine's relevancy code? I suppose we could implement the algorithm from the application by executing multiple queries, but this would really kill efficiency.</p>

<p>Also, we'd like to know which search solution would work best for us. Right now we're leaning towards Sphinx, but we're really not sure.</p>

<p>Also, would you recommend running these engines over MySQL, or would it be better to run them over some type of key-value store like Cassandra? Keep in mind there are 30 Million records, and likely to double as we move along.</p>

<p>Thanks for your responses!</p>

## Answers
### Answer ID: 3513579
<p>I can't give you an entire answer, as I haven't used all the products, but I can say some things which might help.</p>

<ol>
<li>Lucene/Solr uses a vector space model. I'm not certain what you mean by you're using your "own" algorithm, but if it gets too far away from the notion of tf/idf (say, by using a neural net) you're going to have difficulties fitting it into lucene. If by your own algorithm you just mean you want to weight certain terms more heavily than others, that will fit in fine. Basically, lucene stores information about how important a term is to a document. If you want to redefine the calculation of how important a term is, that's easy to do. If you want to get away from the whole notion of a term's importance to a document, that's going to be a pain.</li>
<li>Lucene (and as a result Solr) stores things in its custom format. You don't need to use a database. 30 million records is not an remarkably large lucene index (depending, of course, on how big each record is). If you do want to use a db, use hadoop. </li>
<li>In general, you will want to use Solr instead of Lucene. </li>
</ol>

<p>I have found it very easy to modify Lucene. But as my first bullet point said, if you want to use an algorithm that's not based on some notion of a term's importance to a document, I don't think Lucene will be the way to go.</p>

### Answer ID: 3498484
<p>I actually did something similar with Solr. I can't comment on the details, but basically the proprietary analysis/relevance step generated a series of search terms with associated boosts and fed them to Solr. I think this can be done with any search engine (they all support some sort of boosting).</p>

<p>Ultimately it comes down to what your particular analysis requires.</p>

