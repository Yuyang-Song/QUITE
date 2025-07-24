# SELECT COUNT(DISTINCT v)) performance
[Link to question](https://stackoverflow.com/questions/22960271/select-countdistinct-v-performance)
**Creation Date:** 1397040618
**Score:** 1
**Tags:** sql, database, performance, distinct
## Question Body
<p>Simple question. How can I rewrite a query like this:</p>

<pre><code>SELECT a.name, MAX(b.value), MIN (b.value), COUNT(DISTINCT(b.value))
FROM tableA a
LEFT JOIN tableB b 
       ON a.type = b.type
WHERE b.value IS NOT NULL
GROUP BY a.name
</code></pre>

<p>So that it doesn't run dog-slow on a big-but-not-massive sized table? (let's say 1 million rows). Or would it be possible to do some other 'magic trick' on the database to make that query run quickly?</p>

<p>Normalising the data further is out of the question in this particular case :)</p>

<p><strong>Bit of additional information as requested</strong> </p>

<p>Ideally, the solution would work for both MySQL and MS SQL Server 2008, although SQL Server is definitely the priority of those.</p>

<p>The two tables should look like this:</p>

<pre><code>Table A:
    type INT NOT NULL PRIMARY KEY
    name VARCHAR(500

Table B:
    idTableC INT NOT NULL
    type INT NOT NULL
    value VARCHAR (50)

Table C:
    idTableC INT NOT NULL PRIMARY KEY
    ...
</code></pre>

<p>So generally, we want to go say: for each item in table C, get all items in table B with their type, specified in table A.</p>

<p><em>However</em>, it is also necessary to be able to say: for every 'type' in table A, get a summary of information associated with it in table B. It's this second case that this question's concerned with :)</p>

## Answers
### Answer ID: 22960484
<p>You can use non-clustered indexes on foreign keys, I mean 2 index on <code>[A.Type]</code> and <code>[B.Type]</code> also you can have two other indexes on the columns in select <code>[A.Name]</code>, <code>[B.value]</code></p>

<p>So that everything that your query needs is in an index.</p>

### Answer ID: 22960395
<p>Unsure which database you are using but you could ensure there is an index on the foreign key tableA.type and additionally an index on tableB.type which contains tableB.value. That way SQL won't need to go back to the data page to get the value and can simply retrieve it from the index. You should be careful with this as if it's a large value it could slow your index down.</p>

