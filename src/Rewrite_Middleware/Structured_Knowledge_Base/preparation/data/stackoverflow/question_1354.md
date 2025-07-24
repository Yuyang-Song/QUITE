# C# SQL query with user input
[Link to question](https://stackoverflow.com/questions/72144753/c-sql-query-with-user-input)
**Creation Date:** 1651854814
**Score:** -1
**Tags:** c#, sql
## Question Body
<p>I tried to make software that could be use as a database for libraries so I started to learn SQL I alredy did way to save a book into the database but I am stuck at searching in database I really dont know how to write query with user input I tried to google but cant find the answer I am stuck at this problem for a while now, please help me someone (I write my code normally in my native language but I rewrited it in english but if I forgot something to rewrite I am sorry I am in a bit of hurry when writing this).</p>
<pre><code>try
        {
            using (connection = new SqlConnection(connectionString))
            {
                if(connection.State == ConnectionState.Closed)
                    connection.Open();
                using(DataTable dt = new DataTable(&quot;Search&quot;))
                {
                    using(SqlCommand cmd = new SqlCommand(&quot;SELECT * FROM books WHERE name = @name OR name LIKE @name&quot;, connection))
                    {
                        cmd.Parameters.AddWithValue(&quot;@name&quot;, txtboxSearchName.Text);
                        cmd.Parameters.AddWithValue(&quot;author&quot;, string.Format(&quot;%{0}%&quot;, txtboxSearchAuthor.Text));
                        SqlDataAdapter adapter = new SqlDataAdapter();
                        adapter.Fill(dt);
                        dataGridView1.DataSource = dt;
                    }
                }
            }
        }
        catch (Exception)
        {
            MessageBox.Show(&quot;Something went wrong&quot;, &quot;error&quot;, MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
</code></pre>

## Answers
### Answer ID: 72145025
<p>From What i understood you're trying to search for something in your database</p>
<p>your query looks is :</p>
<pre><code> SELECT * FROM books WHERE name = @name OR name LIKE @name
</code></pre>
<ul>
<li><p>the <strong>=&quot;&quot;</strong> sign means that the name must equal the parameter @name</p>
</li>
<li><p>the &quot;<strong>LIKE</strong>&quot; operator  is used in a WHERE clause to search for a specified pattern in a column</p>
</li>
</ul>
<p>so if you're looking for books with a specific name you can use :</p>
<pre><code> SELECT * FROM books WHERE name = @name 
</code></pre>
<p>if you're looking for books with names that are similar to @name you can use :</p>
<pre><code>SELECT * FROM books WHERE name like @name
</code></pre>
<p>when using the like operator you should use the % to specify the similarities
<a href="https://www.w3schools.com/sql/sql_ref_like.asp" rel="nofollow noreferrer">refer to this article so u can understand</a></p>
<p>i guess in your case the like is for author</p>
<p>here is your final fix :</p>
<pre><code>    using(SqlCommand cmd = new SqlCommand(&quot;SELECT * FROM books WHERE name = @name OR name LIKE @author&quot;, connection))
                        {
                            cmd.Parameters.AddWithValue(&quot;@name&quot;, txtboxSearchName.Text);
// you were missin an @ in author parameter
                            cmd.Parameters.AddWithValue(&quot;@author&quot;, string.Format(&quot;%{0}%&quot;, txtboxSearchAuthor.Text));
                            SqlDataAdapter adapter = new SqlDataAdapter();
                            adapter.Fill(dt);
                            dataGridView1.DataSource = dt;
                        }
</code></pre>

### Answer ID: 72144993
<p>You have almost completed the task; however, some issues should be corrected:</p>
<pre><code>try {
  // Remove old DataSource if any
  if (dataGridView1.DataSource is IDisposable old)
    old.Dispose();

  using (connection = new SqlConnection(connectionString)) {
    // Let sql be readable
    // name = @name seems to be redundant: LIKE is broader in the context
    string sql = 
       @&quot;SELECT * 
           FROM books 
          WHERE name LIKE @name&quot;;

    using(SqlCommand cmd = new SqlCommand(sql, connection)) {
      // Your command uses just one parameter - @name; no @author is used  
      cmd.Parameters.AddWithValue(&quot;@name&quot;, txtboxSearchName.Text);

      // SqlDataAdapter must know which command to use
      SqlDataAdapter adapter = new SqlDataAdapter(cmd);

      DataTable dt = new DataTable(&quot;Search&quot;);

      adapter.Fill(dt);
      dataGridView1.DataSource = dt;
    }
  }
}
catch (DbException e) { // Don't catch (= swallow) all the exception 
  // Message: let user know what went wrong - e.Message
  MessageBox.Show($&quot;Something went wrong: {e.Message}&quot;, 
                   &quot;Error&quot;, 
                    MessageBoxButtons.OK, 
                    MessageBoxIcon.Error);
}  
</code></pre>

