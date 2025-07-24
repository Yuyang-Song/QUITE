# Forcing JPA query to return eagerly all collections / fields
[Link to question](https://stackoverflow.com/questions/15879338/forcing-jpa-query-to-return-eagerly-all-collections-fields)
**Creation Date:** 1365424974
**Score:** 8
**Tags:** java, web-services, jpa, eclipselink
## Question Body
<p>I have few scenarios where the server queries objects from the database by using JPA and then sends the objects to the client over web services.<br>
Since the client expects the full graph in such scenarios I would want to override the lazy loaded collections with eager loading and probably request for batch loading (for performance). 
Is there a way in JPA (or EclipseLink) to override the query in a generic manner (without rewriting the query) and request the full graph?</p>

## Answers
### Answer ID: 15879382
<p>10.1.3. Fetch Joins</p>

<p>JPQL queries may specify one or more join fetch declarations, which allow the query to specify which fields in the returned instances will be pre-fetched.<br></p>

<pre><code>SELECT x FROM Magazine x join fetch x.articles WHERE x.title = 'JDJ'
</code></pre>

<p><br>
The query above returns Magazine instances and guarantees that the articles field will already be fetched in the returned instances.<br><br>
Multiple fields may be specified in separate join fetch declarations:<br></p>

<pre><code>SELECT x FROM Magazine x join fetch x.articles join fetch x.authors WHERE x.title = 'JDJ'
</code></pre>

<p><br></p>

<p>Source  : <a href="http://docs.oracle.com/cd/E13189_01/kodo/docs40/full/html/ejb3_overview_query.html#ejb3_overview_join_fetch" rel="nofollow noreferrer">http://docs.oracle.com/cd/E13189_01/kodo/docs40/full/html/ejb3_overview_query.html#ejb3_overview_join_fetch</a></p>

### Answer ID: 15879853
<p>If you're using eclipselink, you could use the built-in query hints. That way you do not have to rewrite your jpql, but you can define the fetch type in java.</p>

<p><a href="http://wiki.eclipse.org/EclipseLink/UserGuide/JPA/Basic_JPA_Development/Query_Hints#Join_Fetch" rel="nofollow">http://wiki.eclipse.org/EclipseLink/UserGuide/JPA/Basic_JPA_Development/Query_Hints#Join_Fetch</a></p>

