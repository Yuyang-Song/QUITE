# In-memory database supporting proprietary INSERT ALL oracle syntax
[Link to question](https://stackoverflow.com/questions/38398386/in-memory-database-supporting-proprietary-insert-all-oracle-syntax)
**Creation Date:** 1468592191
**Score:** 0
**Tags:** sql, oracle-database, oracle11g, integration-testing, mybatis
## Question Body
<p>I need to write a simple query using oracle, java and mybatis:</p>

<pre><code>select * from FOO foo where foo.id IN (ids)
</code></pre>

<p>Now, <code>ids</code> is a large collection of strings, about 7000. Unfortunately, oracle has 1000 elements limit for IN clause. </p>

<p>To overcome this, I can either:</p>

<ol>
<li>concatenate the query dynamically so it becomes:
<code>select * from FOO foo where foo.id IN (chunk1) or foo.id IN (chunk2) ...</code>
I'm not sure if it even works and I really doubt it performs well </li>
<li>use temporary table and rewrite the query to: <code>select * from FOO foo join SOME_TEMPORARY_ID tempids on foo.id = tempids.id</code>. </li>
</ol>

<p>I've decided to go for 2 option. Before performing the query I need to somehow do an efficient batch insert to Oracle. Unfortunately, Oracle has proprietary syntax to do batch inserts:</p>

<pre><code>INSERT ALL
INTO some_table VALUES ('foo')
INTO some_table VALUES ('foo1')
INTO some_table VALUES ('foo2')
....
INTO some_table VALUES ('foo12345')
SELECT * FROM DUAL
</code></pre>

<p>Now, I didn't mention but I want to write an integration test for this, ideally using H2 or any other inmemory database.
Of course H2 doesn't support that syntax. Neither does HSQLDB. </p>

<p>Do you know any in-memory database that fully supports proprietary oracle syntax? Or at least this specific one INSERT ALL clause?</p>

## Answers
### Answer ID: 38415092
<p>Ok, so I've decided that if I really want/have to use oracle proprietary features/syntax, then let's test it against live oracle. </p>

<p>So if you don't care about execution time and happen to have access do Docker on your CI server, then I recommend you these excellent libraries:
<a href="https://mvnrepository.com/artifact/org.testcontainers" rel="nofollow">https://mvnrepository.com/artifact/org.testcontainers</a> (<a href="https://github.com/testcontainers/testcontainers-java" rel="nofollow">https://github.com/testcontainers/testcontainers-java</a>), including oracle-xe module. </p>

<p>I was able to spin up oracle-xe container during my integration tests and test against live oracle instance.</p>

### Answer ID: 38399193
<p>The limit of the length of a single <code>INSERT</code> statement (i.e. the # of records you can specify values for) is a hint that this operation is really best performed with <em>multiple</em> <code>insert</code> statements.</p>

<p>Can you iterate over a list of <code>id</code> values in a program, inserting one (or a few) at a time to your temp table, which you can then proceed to join on for your final query?</p>

<p>Of course, this eventually resembles your original option #1, but really it is a combination of #1 and #2 I guess.  Anyway, it will work! :)</p>

### Answer ID: 38399060
<p>Thanks that you describe your primary problem. 
Check, may be this can help you </p>

<pre><code>where (foo.id, 0) in (('1', 0), ('2', 0),...)
</code></pre>

<p>This simple workaround hasn't limitation. If this answer wouldn't be appropriate then let me know. I delete this answer and think again at your child problem.</p>

