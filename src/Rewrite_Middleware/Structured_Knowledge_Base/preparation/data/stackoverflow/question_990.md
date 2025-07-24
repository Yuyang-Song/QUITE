# Running a .sql file from R
[Link to question](https://stackoverflow.com/questions/53637760/running-a-sql-file-from-r)
**Creation Date:** 1544031093
**Score:** 7
**Tags:** sql, r, rodbc
## Question Body
<p>I have a few .sql files which aggregate a number of tables/views in a SQL Database. I want to be able to direct R to a specific sql file and execute it and return the results in a dataframe.</p>

<p>Googling around it seems that I can only grab actual tables/views which are in the database or I have to rewrite the sql query and run that through the package RODBC. </p>

<p>In python this can be done with pd.read_sql_query </p>

## Answers
### Answer ID: 64683432
<p>You can utilize the readr-package in conjunction with DBI and odbc</p>
<pre><code>install.packages(&quot;readr&quot;)
library(&quot;DBI&quot;)
library(&quot;odbc&quot;) 
library(&quot;readr&quot;) 
df &lt;- dbGetQuery(con, statement = read_file('Query.sql'))
</code></pre>

