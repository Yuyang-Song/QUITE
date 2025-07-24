# Casting text type column to json type in Postgresql
[Link to question](https://stackoverflow.com/questions/32501027/casting-text-type-column-to-json-type-in-postgresql)
**Creation Date:** 1441885563
**Score:** 15
**Tags:** json, postgresql, casting
## Question Body
<p>I have column typed text in my database which has json queries in it. I want to cast type of the column to json in postgresql how can I do that?</p>

<pre><code>UPDATE category_query_copy
set json_queries = query_json
</code></pre>

<p>my query is like this and the error message:</p>

<p>[Err] ERROR:  column "json_queries" is of type json but expression is of type text</p>

<p>LINE 2: set json_queries = query_json
                   ^
HINT:  You will need to rewrite or cast the expression.</p>

## Answers
### Answer ID: 64245763
<p>I don't know why but for some reasons, using cast function does not work on my side. This is what has worked</p>
<pre><code>UPDATE category_query_copy
set json_queries = to_json(query_json)
</code></pre>

### Answer ID: 32502224
<p>PostgreSQL is fussy about data types, and won't <em>implicitly</em> convert from <code>text</code> to <code>json</code> even though they seem like they're both textual types.</p>

<p>You must use an explicit cast, e.g.</p>

<pre><code>UPDATE category_query_copy
set json_queries = CAST(query_json AS json)
</code></pre>

