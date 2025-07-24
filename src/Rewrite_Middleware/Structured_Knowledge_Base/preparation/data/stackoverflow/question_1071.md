# Could you rewrite this for me? Left join a table and a subquery
[Link to question](https://stackoverflow.com/questions/5766177/could-you-rewrite-this-for-me-left-join-a-table-and-a-subquery)
**Creation Date:** 1303584442
**Score:** 1
**Tags:** sql, derby
## Question Body
<pre><code>CREATE TABLE TR(STUDENT_ID int, SUBJECT_ID int, grade int);
INSERT INTO tr SELECT * FROM results where results.STUDENT_ID=3;
SELECT * FROM subjects LEFT JOIN tr ON subjects.SUBJECT_ID=tr.SUBJECT_ID;
DROP TABLE TR;
</code></pre>

<p>Is it possible to rewrite the above as one query? I've searched all over the net and still can't do it. I'm using derby database.</p>

<p>The idea is that I want to join table subjects, which has a certain number of rows, with matching results from table results, if there are any for a specific student. If there are no results, I want the ouput rows to contain only data from table subjects. So, the number of output rows will always equal the number of rows in subjects.</p>

<p>The above code works well, but it gives me trouble in my program, because a table has to be created. I would like to avoid that.</p>

## Answers
### Answer ID: 5766203
<pre><code>SELECT *
FROM subjects s
LEFT JOIN (
    SELECT * FROM
    results r
    WHERE r.STUDENT_ID = 3
) x ON s.SUBJECT_ID = x.SUBJECT_ID
</code></pre>

### Answer ID: 5766244
<p>That should be equivalent to</p>

<pre><code>SELECT * FROM subjects
LEFT JOIN results ON results.SUBJECT_ID = subjects.SUBJECT_ID AND results.STUDENT_ID = 3;
</code></pre>

<p>Assuming you have at most one entry in results for a specific student.</p>

### Answer ID: 5766221
<p><code>SELECT * FROM subjects LEFT JOIN results ON subjects.SUBJECT_ID=results.SUBJECT_ID AND results.STUDENT_ID=3;</code></p>

### Answer ID: 5766197
<p>Based on the example query given above, it can be rewritten as</p>

<pre><code>SELECT subjects.* FROM 
subjects LEFT JOIN results 
ON subjects.SUBJECT_ID = results.SUBJECT_ID
WHERE results.STUDENT_ID = 3;
</code></pre>

<p>I haven't worked with derby. But I think, this should work.</p>

