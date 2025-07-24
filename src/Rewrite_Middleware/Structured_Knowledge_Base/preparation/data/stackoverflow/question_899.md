# How can I improve this conditional UPDATE query?
[Link to question](https://stackoverflow.com/questions/48823748/how-can-i-improve-this-conditional-update-query)
**Creation Date:** 1518773679
**Score:** 2
**Tags:** sql, postgresql
## Question Body
<p>I have a table <code>t</code> with several columns, let's name them <code>a</code>, <code>b</code> and <code>c</code>. I also have a <code>state</code> column which indicates the current state. There is also an <code>id</code> column.</p>

<p>I want to write the following query: <em>update column <code>a</code> always, but <code>b</code> and <code>c</code> only if the application <code>state</code> is still equal to the database <code>state</code></em>. Here, the <code>state</code> column is used for optimistic locking.</p>

<p>I wrote this query as following:</p>

<pre><code>UPDATE t
SET    a = $a$,
       b = (CASE WHEN state = $state$ THEN $b$ ELSE b END),
       c = (CASE WHEN state = $state$ THEN $c$ ELSE c END)
WHERE  id = $id$ AND
       (
         a != $a$ OR
         b != (CASE WHEN state = $state$ THEN $b$ ELSE b END) OR
         c != (CASE WHEN state = $state$ THEN $c$ ELSE c END)
       )
</code></pre>

<p>Here, <code>$id$</code>, <code>$a$</code>, ... are input variables from the application. The second part of the <code>WHERE</code> clause is to avoid updates which do not effectively update anything.</p>

<p>This query works as expected, but is very clumsy. I am repeating the same condition several times. I am looking for a way to rewrite this query in a more elegant fashion. If this was a simple <code>SELECT</code> query, I could do something with a <code>LATERAL JOIN</code>, but I cannot see how to apply this here.</p>

<p>How can I improve this query?</p>

## Answers
### Answer ID: 48823962
<p>The only filter you need is on ID = $id</p>

<p>The case statement says don't change it in the update if the state doesn't match, so you don't need to filter it.</p>

<p>EDIT</p>

<pre><code>where Id = $id and a !=$a
   Or (state = $state and (b !=b or c!= $c))
</code></pre>

<p>If you do any more than that then"always update a" will not necessary be true.</p>

<p>3rd attempt checks for the possibility of a remaining the same, but b or c updating.</p>

### Answer ID: 48824136
<p><strong>EDIT:</strong> It Took me a while to realize my fault here: The question obviously targets at a single update, while my answer tried to update many rows. However, if you need to execute this Update for a set of rows you could: </p>

<ul>
<li>Insert the needed parameters in a temporary table </li>
<li>Join that table within the "t2" subquery </li>
<li>Select it's columns (e.g. tempTable.b As tempB) </li>
<li>Replace the Parameters (e.g. $b$ -> t2.tempB)</li>
</ul>

<p>.</p>

<pre><code>UPDATE t
SET a=source.a,
    b=source.b,
    c=source.c
FROM 
    (
        SELECT 
            id,
            a, 
            (CASE WHEN UpdateCondition THEN $b$ ELSE b END) AS b,
            (CASE WHEN UpdateCondition THEN $c$ ELSE c END) AS c
        FROM 
            (  
                SELECT state = $state$ As UpdateCondition, * FROM t
            ) As t2
        WHERE 
            id = $id$ AND
            (
                a != $a$ OR
                b != (CASE WHEN UpdateCondition THEN $b$ ELSE b END) OR
                c != (CASE WHEN UpdateCondition THEN $c$ ELSE c END)
            ) AS source
WHERE t.id=source.id;
</code></pre>

<p>The Sub query for t2 gives you your state Condition and executes the calculation for it only once per row.</p>

<p>The subquery for "source" gives you the mapped values and filters those without changes.</p>

### Answer ID: 48824096
<p>This seems a bit cleaner(untested):</p>

<hr>

<pre><code>WITH src AS (
        SELECT    $a$ AS a
       , (CASE WHEN state = $state$ THEN $b$ ELSE b END) AS b
       , (CASE WHEN state = $state$ THEN $c$ ELSE c END) AS c
        FROM t
        WHERE  id = $id$
        )
UPDATE t dst
SET a=src.a, b=src.b, c=src.c
FROM src
WHERE  dst.id = src.id
AND   (src.a, src.b, src.c) IS DISTINCT FROM (dst.a, dst.b, dst.c)
        ;
</code></pre>

### Answer ID: 48823966
<p>Split the query in two:</p>

<pre><code>UPDATE t
SET    a = $a$
WHERE  id = $id$

UPDATE t
SET    b = $b$,
       c = $c$
WHERE  id = $id$ AND
       state = $state$
</code></pre>

<p>If you need atomicity, wrap in a transaction.</p>

