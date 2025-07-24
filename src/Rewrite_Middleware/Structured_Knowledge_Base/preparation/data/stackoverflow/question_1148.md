# c# datatable row count returns 1 for empty table
[Link to question](https://stackoverflow.com/questions/61018703/c-datatable-row-count-returns-1-for-empty-table)
**Creation Date:** 1585940187
**Score:** 0
**Tags:** c#, sql-server, executereader, record-count
## Question Body
<p>I'm querying a SQL Server database and filling a datatable. But even when my sql returns no values, the datatable row count seems to be one. Here's my code:</p>

<pre><code>strSQL = "My sql string"
cmd.CommandText = strSQL;
cmd.Parameters.AddWithValue("@wsNo", wsNo);
cmd.Parameters.AddWithValue("@reachNo", reachNo);
using (DataTable dt = new DataTable())
    {
        dt.Load(cmd.ExecuteReader());
        MyTextbox.Text = dt.Rows.Count.ToString();
        myGridview.DataSource = dt;
        myGridview.DataBind();
    }
</code></pre>

<p>The gridview displays the data correctly, and doesn't display at all if the sql returns no records. But I want to display the record count in a textbox, and that's always 1 when there are no records. A couple of places I've checked imply that ExecuteReader might be the wrong tool for this job, but if so, it isn't clear to me what I should be usi</p>

<p>EDIT: I rebuilt this code using a data adapter, and it seems to be working now. I don't see why, shouldn't make a difference, but I guess rewriting the code fixed whatever I was doing wrong. No further comments necessary. Thanks to people who replied.</p>

## Answers
### Answer ID: 61019075
<p>Typically you will want to fill your DataSet with DataAdapters.  You don't need a DataTable to bring back one record with a DataReader.  But here's how you can do it:</p>

<pre><code>DataTable dt = new DataTable("TableName");

using (connection)
{
    SqlCommand command = new SqlCommand(sSQL, connection);
    connection.Open();

    using (SqlDataReader reader = command.ExecuteReader())
    {
        dt.Load(reader);
    }
}

YourControl.Text = dt.Rows.Count;
</code></pre>

