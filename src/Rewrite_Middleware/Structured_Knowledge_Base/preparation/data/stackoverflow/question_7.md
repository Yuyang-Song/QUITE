# Jena TDB: Nested Transactions
[Link to question](https://stackoverflow.com/questions/10165096/jena-tdb-nested-transactions)
**Creation Date:** 1334516508
**Score:** 4
**Tags:** java, transactions, jena, triplestore
## Question Body
<p>I'd like to rewrite my current code for making use of transactions. However, according to the Jena documentation (<a href="http://incubator.apache.org/jena/documentation/tdb/tdb_transactions.html" rel="nofollow noreferrer">http://incubator.apache.org/jena/documentation/tdb/tdb_transactions.html</a>) nested transactions are not supported.</p>

<p>Let's say, I'd like to query some data from the database and add a rdfs:label to each resource found. Would I have to strictly separte reading and writing code like in the following code, or is there a more efficient way to implement this example?</p>

<pre><code>Dataset dataset = ...; 
dataset.begin(ReadWrite.READ);

ArrayList&lt;Resource&gt; res = new ArrayList&lt;Resource&gt;();

try{
    QueryExecution qe = QueryExecutionFactory.create("SELECT ?x WHERE { ?x a &lt;Whatever&gt; . }", dataset); 
    ResultSet rs = qe.execSelect();

    try
    {
        while(rs.hasNext())
        {
            QuerySolution s = rs.nextSolution();
            RDFNode node = s.get("x"); 
            if(node.isResource) res.add(node.asResource()); 
        }

    }finally{ qe.close(); }

}finally{ dataset.end(); }

dataset.begin(ReadWrite.WRITE); 
try{
    Property label = model.getProperty("http://www.w3.org/2000/01/rdf-schema#label"); 
    for(Resource r : res)
    {
        r.addProperty(label, "text"); 
    }
    dataset.commit();

}finally{ dataset.end(); }
</code></pre>

<p>I've posted this question on <a href="http://web.archive.org/web/20150721121104/http://answers.semanticweb.com:80/questions/15852/jena-tdb-nested-transactions" rel="nofollow noreferrer">semanticweb.com</a>, but haven't received any answers, so I hope someone here can help me. </p>

## Answers
### Answer ID: 10186943
<p>It's true that nested transactions are not supported in TDB, however you can do as many reads as you want in a WRITE transaction. So, start a ReadWrite.WRITE transaction and do all you processing there. No need of nested transactions for what you want to do.</p>

<p>For more on TDB's transaction support, please, look at the official documentation here:</p>

<ul>
<li><a href="http://incubator.apache.org/jena/documentation/tdb/tdb_transactions.html" rel="nofollow">http://incubator.apache.org/jena/documentation/tdb/tdb_transactions.html</a></li>
</ul>

