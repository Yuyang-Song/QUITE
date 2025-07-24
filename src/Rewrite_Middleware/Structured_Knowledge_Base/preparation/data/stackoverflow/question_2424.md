# T-SQL, Find numeric values
[Link to question](https://stackoverflow.com/questions/33594890/t-sql-find-numeric-values)
**Creation Date:** 1446991931
**Score:** 6
**Tags:** sql-server
## Question Body
<p>I did this quiz on <a href="http://www.sql-ex.ru/">http://www.sql-ex.ru/</a>, question 35 to be exact. </p>

<p>The question is as follows:
In Product table, determine the models which consist only of digits or only of latin letters (A-Z, case insensitive).
Result set: model, type of model.</p>

<p>And I gave the correct answer which is:</p>

<pre><code>SELECT model,
       type
FROM   Product
WHERE  Model NOT LIKE '%[^A-Z]%'
        OR Model NOT LIKE '%[^0-9]%' 
</code></pre>

<p>Now my question is why do I need double negations to make it work. 
If I rewrite the code to:</p>

<pre><code>SELECT model,
       type
FROM   Product
WHERE  Model LIKE '%[A-Z]%'
        OR Model LIKE '%[0-9]%' 
</code></pre>

<p>I get the wrong answer:
Your query returned the correct dataset on the first (available) database, but it returned incorrect dataset on the second checking database.
* Wrong number of records (more by 37)</p>

<p>How come that the first example of code gives the correct answer while the second example doesn´t?</p>

<p>I have tried to find answer but no luck. Grateful for an explanation. </p>

## Answers
### Answer ID: 33594906
<pre><code> Where Model LIKE '%[A-Z]%' Or Model LIKE '%[0-9]%'
</code></pre>

<p>Matches rows where <code>Model</code> contains at least one alpha numeric character.</p>

<p>This does not exclude in any way those values that contain mixed alphanumeric and non-alphanumeric characters.</p>

<p>e.g. <code>~A#-</code> would pass because of the presence of the <code>A</code></p>

<p>Moreover your correct query matches either </p>

<ul>
<li><code>'%[^A-Z]%'</code>: those strings which do not contain any non letters (i.e. consist of only letters or are empty) </li>
<li><code>'%[^0-9]%'</code>: those strings which do not contain any non digits (i.e. consist of only digits or are empty).</li>
</ul>

<p>This is not handled at all in your second attempt and a mixed string of letters and digits would be accepted by that.</p>

<p>I would use your first attempt but if you were determined to avoid the double negative you could use</p>

<pre><code>SELECT model
FROM   Product
WHERE  Model LIKE REPLICATE('[A-Z]', LEN(Model))
        OR Model LIKE REPLICATE('[0-9]', LEN(Model)) 
</code></pre>

