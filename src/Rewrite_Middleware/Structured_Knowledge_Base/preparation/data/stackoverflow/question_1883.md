# Boolean wildcard in postgresql
[Link to question](https://stackoverflow.com/questions/11018613/boolean-wildcard-in-postgresql)
**Creation Date:** 1339602403
**Score:** 1
**Tags:** sql, postgresql, boolean, parameterized-query
## Question Body
<p>I have a parameterized postgresql query that users interact with through a PHP front-end.  One of the parameters involves a boolean value, and I want to give the user the option of "True", "False", "Unknown" (Null) or "Doesn't matter" (return any result).</p>

<p>Rewriting the actual query isn't an option (the parameterized queries are stored in a database table, not in the PHP code), so I need to have a boolean "any" value.</p>

<p>Put another way, what value can I assign ":parameter1" in this query to get any row, regardless of the value of "boolean_column"?</p>

<pre><code>SELECT some_column, some_other_column
FROM some_table
WHERE boolean_column = :parameter1
</code></pre>

<p>EDIT: I need to clarify -- <em>I</em> can rewrite the query, but <em>the program</em> cannot rewrite the query (i.e., I can't drop or rewrite the where clause in response to user input at runtime).</p>

<p>EDIT2: Here's my final solution (thanks couling!)</p>

<pre><code>SELECT some_column, some_other_column
FROM some_table
WHERE (:parameter1::text = 'any' OR boolean_column = :parameter1::boolean)
</code></pre>

<p>Of course, the program has to restrict possible values to 'any' or a string value that can be cast to boolean (e.g., 'true', 't', 'false', 'f').</p>

<p>EDIT3:  The previous solution works in PHP with PDO, but does not work with python's psycopg2 or directly in postgresql for some reason.  I've tried a variation with a case statement, like so:</p>

<pre><code>SELECT some_column, some_other_column
FROM some_table
WHERE (CASE WHEN :parameter1::text in ('true', 'false') THEN boolean_column = :parameter1::boolean ELSE TRUE END)
</code></pre>

<p>But that doesn't work either.  It seems no matter what, I can't stop postgresql from trying to evaluate ":parameter1::boolean", even if it's behind a false WHEN condition.  This is a real pickle...</p>

## Answers
### Answer ID: 11018942
<p>Well your query must change. Booleans have two values <code>true</code> and <code>false</code> with nulls never being equal to anything (even null doesn't equal null).</p>

<p>You could of course use:</p>

<pre><code>SELECT some_column, some_other_column
FROM some_table
WHERE (boolean_column = :parameter1 OR :parameter1 is null)
</code></pre>

