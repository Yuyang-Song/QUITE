# Hibernate FullTextQuery, without search term?
[Link to question](https://stackoverflow.com/questions/19769610/hibernate-fulltextquery-without-search-term)
**Creation Date:** 1383574514
**Score:** 1
**Tags:** java, hibernate, filter, lucene, hibernate-search
## Question Body
<p>I am rewriting a Hibernate/lucene function, <strong>findRangeSorting()</strong>, that retrieves  all records in a table based on a permissions filter.  Right now this is done (very badly) by hand by stitching together HQL (hibernate sql) strings and using that to query the database. </p>

<p>I also have a search function which uses a better programmatic approach by creating filters for the classes using the hibernate annotation and combines Boolean queries into a full text query which then has the filters added to it based on which user is doing the search. 
(Note that is not the entire function)</p>

<p><code>fullTextQuery = fullTextSession.createFullTextQuery(bq, this.type);
            results = tab.getQueryFiltersForSearch(fullTextQuery).setSort(sort).list();</code></p>

<p>I would like to use this functionality for the <strong>findRangeSorting()</strong> function since the filters are already in place, so I would basically just need to have the search return everything. The downside is that searching for "" and * don't accomplish this, and so I need to basically create a <em>FullTextQuery</em> without having to search for an actual term, or possibly <strong>find an alternative method for retrieving a range of rows from a table with filters based on user permissions</strong>. </p>

<p>I do not have the best grasp of hibernate so I might be totally wrong in my assumptions.  Any help is appreciated. </p>

## Answers
### Answer ID: 19772339
<p>To create a query match all documents, you should just be able to use Lucene's <a href="http://lucene.apache.org/core/3_6_0/api/all/org/apache/lucene/search/MatchAllDocsQuery.html" rel="nofollow"><code>MatchAllDocsQuery</code></a>.  I'm not aware of anything in the Hibernate <code>QueryBuilder</code> that creates a <code>MatchAllDocsQuery</code>, but it's simple enough to create one through the Lucene API directly, something like:</p>

<pre><code>org.apache.lucene.search.Query allQuery = new org.apache.lucene.search.MatchAllDocsQuery();
fullTextQuery = fullTextSession.createFullTextQuery(allQuery, this.type); 
results = tab.getQueryFiltersForSearch(fullTextQuery).setSort(sort).list();
</code></pre>

