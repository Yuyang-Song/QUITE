# Does ElasticSearch query optimizer understand that `{ from: null, to:null }` timerange filter is a no-op?
[Link to question](https://stackoverflow.com/questions/58133579/does-elasticsearch-query-optimizer-understand-that-from-null-tonull-tim)
**Creation Date:** 1569583415
**Score:** 1
**Tags:** elasticsearch, query-optimization
## Question Body
<p>I'm using ElasticSearch 1.5.2.</p>

<p>In Java, I compose a query like this:</p>

<pre class="lang-java prettyprint-override"><code>public QueryBuilder composeQuery(
    String brand,
    String product,
    /** inclusive, nullable */
    Instant start,
    /** inclusive, nullable */
    Instant end
    ) {
    final QueryBuilder nominalQuery = QueryBuilders.boolQuery()
        .must(QueryBuilders.matchQuery("brand", brand))
        .must(QueryBuilders.matchQuery("product", product));

    final QueryBuilder withRangeApplied;
    if (start == null &amp;&amp; end == null) {
        withRangeApplied = nominalQuery;
    } else {
        final RangeFilterBuilder rangeFilter
            = FilterBuilders.rangeFilter("timestamp");
        rangeFilter.gte(start);
        rangeFilter.lte(end);
        withRangeApplied = QueryBuilders.filteredQuery(
            nominalQuery,
            rangeFilter);
    }
    return withRangeApplied;
}
</code></pre>

<p>But I dislike that I have to do this null check. We'll have a lot of these in our codebase as our product grows. I'd rather have all code go down the same path, like this:</p>

<pre class="lang-java prettyprint-override"><code>public QueryBuilder composeQuery(
    String brand,
    String product,
    /** inclusive, nullable */
    Instant start,
    /** inclusive, nullable */
    Instant end
    ) {
    final QueryBuilder nominalQuery = QueryBuilders.boolQuery()
        .must(QueryBuilders.matchQuery("brand", brand))
        .must(QueryBuilders.matchQuery("product", product));

    final RangeFilterBuilder rangeFilter
            = FilterBuilders.rangeFilter("timestamp");
        rangeFilter.gte(start);
        rangeFilter.lte(end);
    return QueryBuilders.filteredQuery(
        nominalQuery,
        rangeFilter);
}
</code></pre>

<p>This would mean that we unnecessarily impose on our query a <code>{ start: null, end: null }</code> range-filter. Does this create any extra work for ElasticSearch?</p>

<p>I used the Profile API (upon an empty ES 2.4.1 database with similar indices and mappings -- not a fair test, but the only resource available to me) to ask some questions about the query.</p>

<p><code>{ start: null, end: null }</code> shows up in the query plan as:</p>

<pre><code>{
    query_type: "MultiTermQueryConstantScoreWrapper",
    lucene: "timestamp:[* TO *]",
    time: "0.0003ms",
    breakdown: {
        create_weight: 344
    }
}
</code></pre>

<p>That time is an order of magnitude smaller than either of my "TermQuery" elements. Which suggests to me that it's a relatively cheap filter. However, "non-null filter" had exactly the same, tiny time cost. So I'm not convinced it's a no-op.</p>

<p>The presence of this "null filter" did not increase rewrite time (compared to "no filter").</p>

<p>Whereas a "non-null filter" had ~double the rewrite time of either "null filter" or "null filter".</p>

<p>From these results: I'm led to believe that "null filter" adds a <em>negligible</em> amount of work compared to "no filter" (in fact, adds the same negligible cost as the "non-null filter"). Could anybody confirm more conclusively that this no-op filter is cheap (or is optimized out)?</p>

