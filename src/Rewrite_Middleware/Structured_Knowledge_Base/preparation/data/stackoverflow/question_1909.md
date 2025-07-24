# NHibernate: SQL query results mapping
[Link to question](https://stackoverflow.com/questions/11860437/nhibernate-sql-query-results-mapping)
**Creation Date:** 1344413994
**Score:** 6
**Tags:** .net, nhibernate
## Question Body
<p>I have a problem with a SQL query results in NHibernate 3.1.0.4000 (I'm using MS SQL Server 2005 database). I have two tables: <code>Adverts</code> and <code>Investments</code>, which are mapped to entities: <code>Advert</code> and <code>Investment</code>. <code>Adverts</code> are connected with <code>Investments</code> via <code>InvestmentId</code> column (and a foreign key).</p>

<p>To save results of my query I created a following inner class:</p>

<pre><code>    class InvestmentWithAdvertsCount
    {
        public Investment inv { get; set; }

        public int cnt { get; set; }
    }
</code></pre>

<p>and the query is as follows:</p>

<pre><code>var investementsWithAdvertCounts = _session.CreateSQLQuery(
                            "select {inv.*}, (select count(1) from Adverts where InvestmentId = inv.Id) cnt from Investments inv")
                            .AddScalar("cnt", NHibernateUtil.Int32)
                            .AddEntity("inv", typeof(Investment))
                            .SetResultTransformer(NHibernate.Transform.Transformers.AliasToBean(typeof(InvestmentWithAdvertsCount)))
                            .List&lt;InvestmentWithAdvertsCount&gt;();
</code></pre>

<p>When I run this query I receive a collection of <code>InvestmentWithAdvertsCount</code> instances that have a correctly filled <code>cnt</code> property, but the <code>inv</code> property is set to <code>null</code>. I spent some time digging into the NHibernate source and it seems that the <em>inv</em> alias is somehow lost from the query and NHibernate does not even try to fill the <code>inv</code> property. If I remove the <code>.SetResultTransformer</code> part I receive a list of arrays (of type <code>object[2]</code>) with first element set to <code>Investment</code> entity and second element set to its corresponding adverts count. Could you please tell me how to change this query to make the <code>InvestmentWithAdvertsCount</code> filled correctly? Or maybe there is a way to rewrite this query to QueryOver, Criteria or HQL (keeping the generated SQL code efficient)?</p>

<p>I would be really greatful for any help on this issue. Thanks</p>

## Answers
### Answer ID: 11884536
<p>Here's a clean way to do it, processing the results with very simple LINQ to objects:</p>

<pre><code>session.CreateSQLQuery(
    "select {inv.*}, (select count(1) ... inv")
    .AddScalar("cnt", NHibernateUtil.Int32)
    .AddEntity("inv", typeof(Investment))
    .List&lt;object[]&gt;()
    .Select(x =&gt; new InvestmentWithAdvertsCount {inv = x[0], cnt = x[1]})
    .ToList();
</code></pre>

