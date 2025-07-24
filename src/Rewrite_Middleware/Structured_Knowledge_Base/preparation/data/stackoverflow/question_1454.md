# Postgres json_to_recordset with a table
[Link to question](https://stackoverflow.com/questions/76938367/postgres-json-to-recordset-with-a-table)
**Creation Date:** 1692516398
**Score:** 1
**Tags:** json, postgresql
## Question Body
<p>I've written a query that operates on a single JSON document (named 'json_source'), and which returns each element of an array (named 'codes') within the JSON as a separate row, as follows:</p>
<pre><code>SELECT
        json_array_elements(x.codes)-&gt;&gt;'code'
    FROM
        json_to_recordset(json_source-&gt;'findings') AS x(
            codes json
        );
</code></pre>
<p>I have a database table with a JSON column that contains a document with the same structure as json_source. How can I rewrite the query above so that it operates on the table (i.e. with multiple rows of JSON data) rather than just on a single JSON document?</p>

## Answers
### Answer ID: 76964498
<p>You'd use <code>json_to_recordset</code> as a lateral <a href="https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-TABLEFUNCTIONS" rel="nofollow noreferrer">table function</a> call after selecting the rows from your table:</p>
<pre><code>SELECT
    json_array_elements(x.codes)-&gt;&gt;'code'
FROM
    my_table mt,
    json_to_recordset(mt.json_column-&gt;'findings') AS x(codes json);
</code></pre>

### Answer ID: 76938924
<p>This might help:</p>
<pre><code>SELECT
    json_array_elements(t.json_column-&gt;'findings')-&gt;&gt;'code'
FROM
    your_table t;
</code></pre>

