# Sanitizing multiple JSON strings sent to MariaDB using RMariaDB and pool in R
[Link to question](https://stackoverflow.com/questions/59321618/sanitizing-multiple-json-strings-sent-to-mariadb-using-rmariadb-and-pool-in-r)
**Creation Date:** 1576236269
**Score:** 1
**Tags:** r, shiny, mariadb
## Question Body
<p>I am currently building a (large) survey and need to send the responses people provide to a database. I have set up my database connection using the <code>pool</code> and <code>RMariaDB</code> packages, and I have written the following function to construct the SQL queries and submit my data (the data is secured with SSL certificates and all this information is passed through the list <code>db_config</code>). </p>

<pre><code>save_db &lt;- function (db_pool, x, db_name, db_config, replace_val) {
  # Construct the DB query to be sent to the database
  if (!replace_val) {
    query &lt;- sprintf(
      "INSERT INTO %s (%s) VALUES ('%s')",
      db_name,
      paste(names(x), collapse = ", "),
      paste(x, collapse = "', '")
    )
  } else {
    query &lt;- sprintf(
      "UPDATE %s SET %s WHERE %s;",
      db_name,
      paste(paste0(names(x)[-1], " = \'", x[-1], "\'"), collapse = ", "),
      paste0(names(x)[1], " = \'", x[1], "\'")
    )
  }

  # Submit the insert query to the database via the opened connection
  RMariaDB::dbExecute(db_pool, query)
}
</code></pre>

<p><code>db_pool</code>is the pool object handling my database connections; <code>x</code> is a named vector with the data that I am sending to the database, where the names corresponds to the column names of my MariaDB and the values are stored as data blobs; <code>db_name</code> is the name of my database; <code>replace_val</code> a boolean.</p>

<p>The data blobs are essentially different output objects from the survey, e.g. vectors or matrices of responses, turned into character strings using the <code>toJSON()</code> from the <code>jsonlite</code> package. </p>

<p>So far, so good. I am able to send data to the database, download it and reconstruct the responses using the <code>fromJSON()</code> command. All is good. However, I do have one security concern. In my survey, I do have a few open-ended questions where people can write what they want. While unlikely, I am concerned that someone might use a SQL injection attack. Worst case scenario, I lose all my data.   </p>

<p>I know of the <code>sqlInterpolate()</code> function from the <code>DBI</code> package. From my understanding, the function escapes any quotation marks, meaning that any value submitted will be turned into a safe string. </p>

<p>What I have not been able to do is modify my function above to work with <code>sqlInterpolate</code>. In my case <code>x</code> is a named vector of length seven where each vector element is a JSON string. Essentially, I need to use <code>sqlInterpolate()</code> on each of the JSON strings. I was wondering if there is an "easy" way of doing this, or if my best course of action would be to completely rewrite my function to send seven individual deposits to the DB, i.e. one for each vector element. </p>

<p>A rather simplified example would be something like this: </p>

<pre><code>library(jsonlite)

# Create some data to test the string on
y &lt;- 1:3
z &lt;- matrix(runif(4), 2, 2)
q &lt;- c("one", "don't")
x &lt;- c(toJSON(y), toJSON(z), toJSON(q))
names(x) &lt;- c("var_1", "var_2", "var_3")
db_name &lt;- "my_db"

# Current sprintf() statement
sprintf(
  "INSERT INTO %s (%s) VALUES ('%s')",
  db_name,
  paste(names(x), collapse = ", "),
  paste(x, collapse = "', '")
)
</code></pre>

<p>And what I would need to interpolate is the values captured by <code>('%s')</code> in the <code>sprintf()</code> statement (and similarly for the update query). Because I am fairly certain that just turning everything into a JSON string would sanitize my DB input?</p>

<p>Any help would be much appreciated.</p>

## Answers
### Answer ID: 59326719
<p>Having spent several hours trying and failing at this today, I believe I managed to find a work around. I have done some testing and it appears to be working. I am posting an answer to my own question in case someone has a similar problem at a different time.</p>

<p>My updated function now looks like this:</p>

<pre><code>save_db &lt;- function (db_pool, x, db_name, db_config, replace_val) {
  # Interpolate the elements of x
  x &lt;- do.call(c, lapply(x, function(y) {
    sql &lt;- "?value"
    sqlInterpolate(db_pool, sql, value = y)
  }))

  # Construct the DB query to be sent to the database
  if (!replace_val) {
    query &lt;- sprintf(
      "INSERT INTO %s (%s) VALUES (%s)",
      db_name,
      paste(names(x), collapse = ", "),
      paste(x, collapse = ", ")
    )

  } else {
    query &lt;- sprintf(
      "UPDATE %s SET %s WHERE %s;",
      db_name,
      paste(paste0(names(x)[-1], " = ", x[-1]), collapse = ", "),
      paste0(names(x)[1], " = ", x[1])
    )
  }

  # Submit the insert query to the database via the opened connection
  RMariaDB::dbExecute(db_pool, query)
}
</code></pre>

<p>It appears that the key was to only use the interpolation on the actual JSON string itself, like so:</p>

<pre><code>  x &lt;- do.call(c, lapply(x, function(y) {
    sql &lt;- "?value"
    sqlInterpolate(db_pool, sql, value = y)
  }))
</code></pre>

<p>And the rest of the function can be used as is. To see this, let's use the example I provided in my original question: </p>

<pre><code>y &lt;- 1:3
z &lt;- matrix(runif(4), 2, 2)
q &lt;- c("one", "don't")
x &lt;- c(toJSON(y), toJSON(z), toJSON(q))
names(x) &lt;- c("var_1", "var_2", "var_3")
db_name &lt;- "my_db"

# Current sprintf() statement
sprintf(
  "INSERT INTO %s (%s) VALUES ('%s')",
  db_name,
  paste(names(x), collapse = ", "),
  paste(x, collapse = "', '")
)
</code></pre>

<p>Which yields the output:</p>

<pre><code>"INSERT INTO my_db (var_1, var_2, var_3) VALUES ('[1,2,3]', '[[0.6573,0.1726],[0.3291,0.9903]]', '[\"one\",\"don't\"]')" 
</code></pre>

<p>If I now transform my x as above and use the updated <code>sprintf()</code> call (Note that the extra single quotation marks are removed):</p>

<pre><code>x &lt;- do.call(c, lapply(x, function(y) {
  sql &lt;- "?value"
  sqlInterpolate(ANSI(), sql, value = y)
}))

sprintf(
  "INSERT INTO %s (%s) VALUES (%s)",
  db_name,
  paste(names(x), collapse = ", "),
  paste(x, collapse = ", ")
)
</code></pre>

<p>I will get:</p>

<pre><code>"INSERT INTO my_db (var_1, var_2, var_3) VALUES ('[1,2,3]', '[[0.6573,0.1726],[0.3291,0.9903]]', '[\"one\",\"don''t\"]')"
</code></pre>

<p>And we see that the single quotation mark in don't is correctly quoted out. If I have missed something crucial in my own solution, please feel free to comment on it. </p>

