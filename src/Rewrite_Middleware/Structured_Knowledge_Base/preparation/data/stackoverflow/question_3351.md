# SPARQL to SQL query rewriting engine
[Link to question](https://stackoverflow.com/questions/77010022/sparql-to-sql-query-rewriting-engine)
**Creation Date:** 1693413996
**Score:** 2
**Tags:** sql, sparql, semantic-web
## Question Body
<p>I am looking for ontology based data access (OBDA) system capable of SPARQL to SQL query rewriting to convert the following SPARQL query:</p>
<p><code>SELECT ?interface ?ip  WHERE { ?interface network:hasIpAddress ?ip. ?ip network:containedWithin &quot;192.168.1.0/24&quot;. }</code></p>
<p>or, alternatively:</p>
<p><code>SELECT ?interface ?ip WHERE { ?interface network:hasIpAddress ?ip. FILTER(?ip IN &quot;192.168.1.0/24&quot;). }</code></p>
<p>... to the following SQL query:</p>
<p><code>SELECT interface, ip FROM interfaces WHERE ip_address &lt;&lt; &quot;192.168.1.0/24&quot;</code></p>
<p>*Notes:</p>
<ol>
<li>&quot;&lt;&lt;&quot; operator in SQL WHERE statement is specific to PostgreSQL type &quot;inet&quot;: <a href="https://www.postgresql.org/docs/9.3/functions-net.html" rel="nofollow noreferrer">https://www.postgresql.org/docs/9.3/functions-net.html</a></li>
<li>For a general case, &quot;192.168.1.0/24&quot; may be considered as parameter that must be passed down from SPARQL to SQL filtering engine.*</li>
</ol>
<p>I would be grateful if you could advise solutions for the problem.</p>
<p>I explored Ontop, Sparqlify and a few others alike. They seem to be based on graph materialization approach that assumes &quot;exportability&quot; of SQL database data as triples. To answer query in question query rewriting seems to be needed to employ special index of SQL database to find matching records.</p>

