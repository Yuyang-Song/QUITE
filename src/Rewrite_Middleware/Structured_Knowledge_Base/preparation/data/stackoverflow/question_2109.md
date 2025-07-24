# SqlDataReader to read into List&lt;string&gt;
[Link to question](https://stackoverflow.com/questions/19299935/sqldatareader-to-read-into-liststring)
**Creation Date:** 1381418682
**Score:** 13
**Tags:** c#, sql, wcf, ado.net, sql-server-express
## Question Body
<p>I am writing a method in C# to query a SQL Server Express database from a WCF service. I have to use ADO.NET to do this (then rewrite it with LINQ later on).</p>

<p>The method takes two strings (<code>fname, lname</code>) then returns a "Health Insurance NO" attribute from the matching record. I want to read this into a list (there are some other attribs to retrieve as well). </p>

<p>The current code returns an empty list. Where am I going wrong?</p>

<pre><code>public List&lt;string&gt; GetPatientInfo(string fname, string lname)
{
    string connString = "Data Source=.\\SQLEXPRESS;AttachDbFilename=C:\\Users\\xxxx\\Documents\\Visual Studio 2010\\Projects\\ADOWebApp\\ADOWebApp\\App_Data\\ADODatabase.mdf;Integrated Security=True;User Instance=True";

    SqlConnection conn = new SqlConnection(connString);

    string sqlquery = "SELECT Patient.* FROM Patient WHERE ([First Name] = '"+fname+"') AND ([Last Name] = '"+lname+"')";
    SqlCommand command = new SqlCommand(sqlquery, conn);
    DataTable dt = new DataTable();

    List&lt;string&gt; result = new List&lt;string&gt;();

    using (conn)
    {
        conn.Open();

        using (SqlDataReader reader = command.ExecuteReader())
        {
            while (reader != null &amp;&amp; reader.Read())
            {
               dt.Load(reader);
               result.Add(Convert.ToString(reader["Health Insurance NO"]));
            }
        }
     }

     return result;
}
</code></pre>

## Answers
### Answer ID: 19300200
<p>I would do it this way:</p>

<pre><code> conn.Open();
 using (SqlDataReader reader = command.ExecuteReader())
 {
     dt.Load(reader);                  
 }

 foreach (var row in dt.AsEnumerable())
 {
     result.Add(row["Health Insurance NO"].ToString());
 }
</code></pre>

### Answer ID: 19300086
<p>You are trying to load a <code>DataTable</code> via <code>DataTable.Load</code> >in a loop&lt;. You just need that once. You're also using <code>reader.Read()</code> in the loop. <a href="http://msdn.microsoft.com/en-us/library/system.data.sqlclient.sqldatareader.read.aspx"><code>SqlDataReader.Read()</code></a> advances the reader to the next record without to consume it. If you're going to use <code>DataTable.Load</code> you don't need to read the reader first. So you just have to remove the loop completely  to load the table.</p>

<p>But since you want to return a list you don't need the <code>DataTable</code> at all, just loop the reader:</p>

<pre><code>List&lt;string&gt; result = new List&lt;string&gt;();
using (conn)
{
    conn.Open();
    using (SqlDataReader reader = command.ExecuteReader())
    {
        while(reader.Read())
        {
            result.Add(Convert.ToString(reader["Health Insurance NO"]));
        }
    }
}
</code></pre>

<p>Apart from that, you are open for sql-injection without sql-parameters.</p>

