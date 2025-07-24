# How to make OleDB query read a colon :
[Link to question](https://stackoverflow.com/questions/20810599/how-to-make-oledb-query-read-a-colon)
**Creation Date:** 1388200040
**Score:** 1
**Tags:** mysql, .net, vb.net, oledb
## Question Body
<p>I am working on a GPS app and I need to parse the exploded string sent to the app.<br>
 however, SQL query in OleDB doesn't recognize <code>:</code> as a character. - <em>I think that's the error</em>  </p>

<p>I added a field, <code>Time</code> on my .accdb with text as data type...</p>

<p>04T16:18:42Z   </p>

<p>that is the <em>time</em> data the gps is sending..<br>
but I get syntax error if I am using that through (i just made this short, I use vb.net) -<br>
<code>insert into myTable(Time) values ('" &amp; txtTime.Text &amp; "')</code><br>
that is the query I use. I posted the error yesterday, and it seems that, that is the data that causes syntax error.<br>
what should I do to make it work? Or maybe do something like change its time format, split, rewrite? the main goal is for me to save it to the database. thanks</p>

<p><strong>UPDATE:</strong> this is my code for saving, could you re-arrange it with <code>parameters</code> --</p>

<pre><code>query = "INSERT INTO tblGPSRoutes(Time,Latitude,Longitude,Elevation,Accuracy,Bearing,Speed)"
query &amp;= " VALUES ('" &amp; txtTime.Text &amp; "','" &amp; txtLat.Text &amp; "','" &amp; txtLong.Text &amp; "','" &amp; txtElev.Text &amp; "','" &amp; txtAccuracy.Text &amp; "','" &amp; txtBearing.Text &amp; "','" &amp; txtSpeed.Text &amp; "')"


        databaseFunctions.ExecuteQuery(query)
        MessageBox.Show("Data Saved Successfully.")
</code></pre>

<p><strong>UPDATE2:</strong> now I am using parameters :</p>

<pre><code>Dim con As OleDbConnection
    con = New OleDbConnection
    con.ConnectionString = "Provider=Microsoft.ACE.OLEDB.12.0;Data Source = " &amp; Path.Combine(Application.StartupPath, "markers.accdb")
    con.Open()
    Dim query As String = "INSERT INTO tblGPSRoutes(Latitude,Longitude,Elevation,Accuracy,Bearing,Speed) VALUES (@lat,@long,@elev,@acc,@bearing,@speed)"
    Using cmd As New OleDbCommand(query, con)
        With cmd.Parameters
            '.AddWithValue("@time", txtTime.Text)'
            .AddWithValue("@lat", txtLat.Text)
            .AddWithValue("@long", txtLong.Text)
            .AddWithValue("@elev", txtElev.Text)
            .AddWithValue("@acc", txtAccuracy.Text)
            .AddWithValue("@bearing", txtBearing.Text)
            .AddWithValue("@speed", txtSpeed.Text)
        End With
        cmd.ExecuteNonQuery()
    End Using
</code></pre>

<p>first says, syntax error.. then I removed the <code>time</code> data input. then it works.</p>

## Answers
### Answer ID: 20810674
<p><code>Time</code> is reserved word in Access. So you cannot use it as column name.(I changed it to <code>MyTime</code> in example</p>

<p>Use parameters when you add some application's variables to SQL query.<br>
Then you avoid <a href="http://en.wikipedia.org/wiki/SQL_injection#Parameterized_statements" rel="nofollow">SQL injections</a> and some errors when using special characters in the string value</p>

<pre><code>Dim query As String = "insert into myTable(MyTime, Latitude) values (@TextTime, @Latitude)"
//Then create parameters for your databaseFunctions's functions
Dim parameters As New List(Of OleDbParameters)()
With parameters
    .Add(New OleDbParameter("@TextTime", txtTime.Text))
    .Add(New OleDbParameter("@Latitude", txtLat.Text))
End With
databaseFunctions.ExecuteQuery(query, parameters.ToArray())
MessageBox.Show("Data Saved Successfully.")
</code></pre>

<p>But then you need add/change your <code>databaseFunctions.ExecuteQuery(query)</code> - function to take two parameters</p>

<pre><code>Public Sub ExecuteQuery(query As String, params As OleDbParameters())
    //Here add parameters to OleDbCommand object and execute command
End Sub
</code></pre>

