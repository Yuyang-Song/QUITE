# Search for multiple values in SQL Server as quickly as possible
[Link to question](https://stackoverflow.com/questions/13801773/search-for-multiple-values-in-sql-server-as-quickly-as-possible)
**Creation Date:** 1355145541
**Score:** 0
**Tags:** sql, sql-server, optimization
## Question Body
<p>I have the following sql statement pulling data from a stored view:</p>

<pre><code>foreach (var id in insert_idlist[0])
{
    mssql_con.Open();
    //top 1 for duplicate removal
    //slowdown?
    var mssql_select = "SELECT * FROM dbo.export_to_web WHERE SKU = '" + id + "'";
}
</code></pre>

<p>I want to rewrite the sql statement to insert all ids into a single query using an IN clause or similar to speed up execution. However I am aware that IN is a relatively slow operation, so I was hoping to get some expert advice on the fastest possible way of retrieving my data.</p>

<p>Speed is my only concern in this question.</p>

<p>Please note that security is not an issue as this application is pulling all it's variables from an internal database with no direct web access.</p>

<p>Updated code:</p>

<pre><code>    try
    {

        //foreach (var id in insert_idlist[0])
        //{
            mssql_con.Open();
            //top 1 for duplicate removal
            //slowdown?
            //var mssql_select = "SELECT * FROM dbo.export_to_web WHERE SKU = '" + id + "'";
            var mssql_select = "SELECT * FROM dbo.export_to_web WHERE SKU IN (" + insert_idlist .Select(x =&gt; "'" + x + "'") .Aggregate((x, y) =&gt; x + "," + y) + ")";
            //var mssql_select = "SELECT * FROM dbo.Book5 WHERE SKU = '"+id+"'";
            SqlCommand cmd = new SqlCommand(mssql_select, mssql_con);
            cmd.CommandTimeout = 0;
            lbl_dev.Text += "teest";

            //Create a data reader and Execute the command
            try
            {
                SqlDataReader dataReader = cmd.ExecuteReader();

                  //Read the data and store them in the list
                 while (dataReader.Read())
                {
                    insert_idlist[1].Add(dataReader["supplier name"] + " " + dataReader["range description"] + " " + dataReader["item description"]);
                    insert_idlist[3].Add(dataReader["Sale Price"] + "");
                    insert_idlist[2].Add(dataReader["WebDesc"] + "");
                    //insert_idlist[3].Add(dataReader["id"] + "");removed
                    insert_idlist[4].Add(dataReader["WebDimensions"] + "");
                    insert_idlist[5].Add(dataReader["RRP"] + "");
                    insert_idlist[6].Add(dataReader["Normal Price"] + "");
                    insert_idlist[7].Add("482"); //add me
                    insert_idlist[8].Add(dataReader["ID"] + "");

                    lbl_dev.Text += dataReader["supplier name"] + " " + dataReader["range description"] + " " + dataReader["item description"];
                    lbl_dev.Text += mssql_select;
                     about_to_insert = about_to_insert + 1;

                }
                lbl_dyn_status.Text = "Record 0 of " + about_to_insert + "updated.";

                dataReader.Close();
                mssql_con.Close();

            }

            catch (Exception e)
            {
                lbl_dev.Text = "" + e.Message;
            }

   // }


            }
            catch (Exception e)
            {
                lbl_dev.Text = "" + e.Message;
            }
</code></pre>

## Answers
### Answer ID: 13801820
<p>If you are on 2008 or higher, the best way to do is pass the values into a Table-Valued Parameter. I always point people to a blog post I wrote <a href="http://www.atlantis-interactive.co.uk/blog/post/2011/05/21/A-generic-list-for-passing-table-valued-parameters-to-SQL-Server.aspx" rel="nofollow">here</a> for that.</p>

<p>However, IN is not necessarily a slow operation, as long as the field that you are searching is indexed appropriately - and it would almost certainly be faster than the 'connection per item' approach.</p>

<p>The SQL would then be something like:</p>

<pre><code>var mssql_select = "SELECT * FROM dbo.export_to_web WHERE SKU IN (" + insert_idlist
                   .Select(x =&gt; "'" + x + "'")
                   .Aggregate((x, y) =&gt; x + "," + y) + ")";
</code></pre>

<p>Disclaimer - that LINQ may not be 100% spot on :)</p>

### Answer ID: 13801804
<blockquote>
  <p>I want to rewrite the sql statement to insert all ids into a single
  query using an IN clause or similiar.</p>
</blockquote>

<p>You can use <code>INSERT INTO ... SELECT ...</code> like so:</p>

<pre><code>INSERT INTO ATable(...)
SELECT * FROM dbo.export_to_web WHERE SKU = someid;
</code></pre>

<p><strong>Note that:</strong> You have to list the columns' names in the <code>INSERT</code> clause to match what is returned by <code>SELECT *</code>.</p>

