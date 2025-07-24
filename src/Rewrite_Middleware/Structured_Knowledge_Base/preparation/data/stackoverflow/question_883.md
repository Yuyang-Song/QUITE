# Neo4j: Rewriting UNION returns more then it should
[Link to question](https://stackoverflow.com/questions/48252277/neo4j-rewriting-union-returns-more-then-it-should)
**Creation Date:** 1515951184
**Score:** 0
**Tags:** mysql, neo4j, cypher, union
## Question Body
<p>I'm migrating a MySQL database to a Neo4j one, but I can't rewrite this query correctly.</p>

<p>MySQL Query:</p>

<pre><code>SELECT ID, Nome, Fotografia
    FROM Participante AS pa
    INNER JOIN Filme_temAtor_Participante AS fa ON fa.Participante_ID = pa.ID
    WHERE fa.Filme_ID = 1
UNION
SELECT ID, Nome, Fotografia
    FROM Participante AS pr
    INNER JOIN Filme_temRealizador_Participante AS fr ON fr.Participante_ID = pr.ID
    WHERE fr.Filme_ID = 1
ORDER BY Nome ASC;
</code></pre>

<p>From SQL to Neo4j I stopped using ids and started using the name itself. I made 2 cypher queries, the first one works fine, but the second one doesn't:</p>

<p>First one:</p>

<pre><code>MATCH(f:Filme {Titulo: "Justice League"})
MATCH(a:Participante)&lt;-[:TEM_ATOR]-(f)
MATCH(b:Participante)&lt;-[:TEM_REALIZADOR]-(f)
RETURN a,b;
</code></pre>

<p>Second one:</p>

<pre><code>MATCH(f:Filme {Titulo: "Justice League"})
MATCH(a:Participante)&lt;-[:TEM_ATOR]-(f)
WITH COLLECT({Nome:a.Nome,Fotografia:a.Fotografia}) AS atores
MATCH(b:Participante)&lt;-[:TEM_REALIZADOR]-(f)
WITH atores + COLLECT({Nome:b.Nome,Fotografia:b.Fotografia}) AS ps
UNWIND ps AS p
RETURN  p.Nome, p.Fotografia;
</code></pre>

<p>The output looks like this:
<a href="https://i.sstatic.net/qdddY.png" rel="nofollow noreferrer">output</a></p>

<p>Since the project is in Portuguese I'll provide a dictionary of the relevant words:</p>

<ul>
<li>Participante -> Participant</li>
<li>Filme -> Movie</li>
<li>Fotografia -> Photo</li>
<li>temAtor -> hasActor</li>
<li>temRealizador -> hasDirector</li>
<li>Nome -> Name</li>
</ul>

<p>Any help would be greatly apreciated :)</p>

## Answers
### Answer ID: 48252378
<p>You have to pass along <code>f</code> in the <code>WITH</code> clause:</p>

<pre><code>MATCH(f:Filme {Titulo: "Justice League"})
MATCH(a:Participante)&lt;-[:TEM_ATOR]-(f)
WITH f, COLLECT({Nome:a.Nome,Fotografia:a.Fotografia}) AS atores
MATCH(b:Participante)&lt;-[:TEM_REALIZADOR]-(f)
WITH atores + COLLECT({Nome:b.Nome,Fotografia:b.Fotografia}) AS ps
UNWIND ps AS p
RETURN  p.Nome, p.Fotografia;
</code></pre>

<p>If you do not pass it along, <code>f</code> will be treated as a new variable and it can be bound to any node, not just the <em>Justice League</em> movie.</p>

