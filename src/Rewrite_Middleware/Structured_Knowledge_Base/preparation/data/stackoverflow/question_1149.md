# Writing less code in ADO.NET (wrapper classes)
[Link to question](https://stackoverflow.com/questions/61068563/writing-less-code-in-ado-net-wrapper-classes)
**Creation Date:** 1586205457
**Score:** 1
**Tags:** c#, sql, ado.net, wrapper, sqlclient
## Question Body
<p>So I'm pretty new to C# in general, but I have a basic knowledge of the language at the moment.</p>

<p>When accessing an SQL database, I've decided that using ADO.NET (SqlClient seems to be the best way to do it, and I have managed to get it working, including using queries.
My issue is that as soon as I start to query the database more often, I seem to just be rewriting very similar code over and over again (which is obviously bad practice).
It's clear that I need to make some sort of class that handles my use of ADO.NET (SqlClient) so that I cant just type something like the following:</p>

<pre><code>DatabaseConnection.Query("SELECT * FROM tblProducts");
</code></pre>

<p>… instead of...</p>

<pre><code>using (SqlConnection cnn = new SqlConnection(cnnString)) // cnnString was defined earlier in the code
{
    SqlCommand cmd = new SqlCommand("SELECT ProductType FROM tblProductTypes", cnn);
    DataTable dt = new DataTable();
    cnn.Open();
    dt.Load(cmd.ExecuteReader());
    cboFilterTypes.DataSource = dt;
    cboFilterTypes.DisplayMember = "ProductType";
    cboFilterTypes.ValueMember = "ProductType";
    cnn.Close();
}
</code></pre>

<p>So I think I need to make a class wrapper (at least that's what I believe it is called), but I'm not too sure on how to go about doing it. Does anyone have any suggestions or tricks that I can use?</p>

<p><em>To be clear, I am not wanting to use the entity framework or anything like that which is built on ADO.NET - I've tried to entity framework and have decided there are too many drawbacks.</em> </p>

## Answers
### Answer ID: 61068690
<p>Sticking with your request for a 'wrapper' you could simply make a static helper method to handle the call to the database such as</p>

<pre><code>    public static DataTable GetDataTable(string query)
    {
        DataTable result = new DataTable();
    using (SqlConnection cnn = new SqlConnection(cnnString)) // cnnString was defined earlier in the code
    {
            SqlCommand cmd = new SqlCommand(query, cnn);
            result = new DataTable();
            cnn.Open();
            result.Load(cmd.ExecuteReader());
            cnn.Close();
     }
return result;
    }
</code></pre>

<p>You could then call this like</p>

<pre><code>    cboFilterTypes.DataSource = GetDataTable("SELECT ProductType FROM tblProductTypes")
    cboFilterTypes.DisplayMember = "ProductType";
    cboFilterTypes.ValueMember = "ProductType";
</code></pre>

<p>I wouldn't recommend this way of data access for anythig other than a tiny project.  If you really don't like EF then Dapper or something similar offers a much more scalable solution.  Stackoverflow itself uses Dapper :)</p>

