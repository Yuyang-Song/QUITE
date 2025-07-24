# Empty Char in Where Clause?
[Link to question](https://stackoverflow.com/questions/39849915/empty-char-in-where-clause)
**Creation Date:** 1475576844
**Score:** 1
**Tags:** sql, oracle-database, oracle11g
## Question Body
<p>I have the following table:</p>

<pre><code>  CREATE TABLE SOAUDIT
  (SOU_USER CHAR(8 BYTE), 
   SOU_ORDREF CHAR(8 BYTE),
   SOU_TYPE CHAR(1 BYTE), 
   SOU_DESC CHAR(50 BYTE))
</code></pre>

<p>There is a unique index defined on the first three columns (but no primary key, which is something we have no control over).</p>

<p>And in the table there are some records:</p>

<pre><code>| SOU_USER | SOU_ORDREF | SOU_TYPE | SOU_DESC         |
|----------|------------|----------|------------------|
| proust   |            | S        | recherche        |
| joyce    | 12345678   | S        | pelurious        |
| orwell   | 19841984   | T        | doubleplusungood |
| camus    | 34598798   | P        | peiner           |
</code></pre>

<p>On closer inspection it appears that the value in SOU_ORDREF for user 'proust' is an empty char string of 8 characters.</p>

<p>Now, what I need to be able to do is to query this table based on their unique values (which I will receive from a SQL Server database (just to complicate matters nicely). In the case of SOU_ORDREF the search value will be a blank field:</p>

<pre><code>SELECT * 
FROM SOAUDIT 
WHERE (SOU_USER, TRIM(SOU_ORDREF), SOU_TYPE)
IN (('proust', null, 'S'))
</code></pre>

<p>This doesn't return the record I am looking for. </p>

<p>When I rewrite the query as following:</p>

<pre><code>SELECT * 
FROM SOAUDIT 
WHERE (SOU_USER, SOU_TYPE)
IN (('proust', 'S'))
AND TRIM(sou_ordref) is null
</code></pre>

<p>Then I <em>do</em> get the desired record.</p>

<p>However, I want to be able to pass in more than one record into the <code>WHERE</code> clause so the second version doesn't really help.</p>

## Answers
### Answer ID: 39849999
<p>Try this way:</p>

<pre><code>SELECT * 
FROM test 
WHERE SOU_USER = 'proust'
AND SOU_TYPE = 'S' 
AND TRIM(sou_ordref) = ''
</code></pre>

<p>Since an empty char is different than <code>NULL</code></p>

### Answer ID: 39850281
<p>Oracle -- by default -- treats empty strings and <code>NULL</code> as the same thing.</p>

<p>This can cause awkward behavior, because comparisons to <code>NULL</code> almost never return true.  So a simple expression such as <code>where sou_ordref = ''</code> never returns true, because it is equivalent to <code>where sou_ordref = NULL</code>.</p>

<p>Here is one workaround:</p>

<pre><code>SELECT * 
FROM SOAUDIT 
WHERE (SOU_USER, COALESCE(TRIM(SOU_ORDREF), ' '), SOU_TYPE) IN
          ( ('proust', ' ', 'S') ) 
</code></pre>

<p>Note that this replaces the empty string (<code>NULL</code>) with a space.  It then compares the results to a space.</p>

