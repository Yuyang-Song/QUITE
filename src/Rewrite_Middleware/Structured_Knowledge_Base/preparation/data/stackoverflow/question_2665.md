# How to update a db table from pandas dataset with sqlalchemy
[Link to question](https://stackoverflow.com/questions/45630095/how-to-update-a-db-table-from-pandas-dataset-with-sqlalchemy)
**Creation Date:** 1502438960
**Score:** 3
**Tags:** python, pandas, sqlalchemy, pyodbc, pymssql
## Question Body
<p>I need to update a table in a MSSQL database.
The dimension of the table doesn't allow to load the table in memory, modify the dataframe and rewrite it back.</p>

<p>I also need to update only one column at a time so I cannot use the solution proposed in <a href="https://stackoverflow.com/questions/42461959/how-do-i-perform-an-update-of-existing-rows-of-a-db-table-using-a-pandas-datafra">this topic</a> (ie the solution proposes a delete operation of the interested rows, impossible for me cause I can update only one column at time)</p>

<p>So I need to perform something like an update-from query </p>

<pre class="lang-sql prettyprint-override"><code>Update mytable
set mycolumn = dfcolumn
from df
where mytable.key=df.key
</code></pre>

<p>in which <code>mytable</code> is a dbtable and <code>df</code> is a pandas Dataframe.</p>

<p><strong>Is it possible to perform this kind of function with SQLALCHEMY?</strong></p>

## Answers
### Answer ID: 45645003
<p>Create a temp table with the key and the column you want to update in the ms sql database. And then make a update call to the server. The following is the code snippet using sqlalchemy</p>

<p>You can use the following way:</p>

<pre><code>engine = create_engine('mssql+pymssql://scott:tiger@hostname:port/dbname')
df.to_sql('temp_table', engine, if_exists='replace')

sql = "UPDATE final_table AS f" + \
      " SET col1 = t.col1" + \
      " FROM temp_table AS t" + \
      " WHERE f.id = t.id"

with engine.begin() as conn:
   conn.execute(sql)
</code></pre>

