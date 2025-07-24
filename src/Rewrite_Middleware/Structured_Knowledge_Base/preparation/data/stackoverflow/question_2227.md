# REST client vb.net
[Link to question](https://stackoverflow.com/questions/25118812/rest-client-vb-net)
**Creation Date:** 1407155714
**Score:** 0
**Tags:** .net, json, vb.net, rest, restsharp
## Question Body
<p>I made a project in VB.net that is using MYSQL database. I like to change this with a restfull server I build with Nodejs</p>

<p>All the queries are in MYSQL for example this one.</p>

<pre><code>Function checkuser(ByVal gebruikersnaam As String, ByVal password As String) As Object
        cmd = New MySqlCommand("SELECT * FROM members WHERE username LIKE '" &amp; gebruikersnaam &amp; "' AND password LIKE '" &amp; password &amp; "'", con)
        con.Open()
        reader = cmd.ExecuteReader
        If reader.HasRows Then
            Return reader
        Else
            MsgBox("De inloggevens zijn helaas niet goed")
            con.Close()
            Return Nothing
        End If

    End Function  
</code></pre>

<p>You can see I am using the reader = cmd.ExecuteReader to return my data. Is there a way the rewrite this mysql code to a restfull code with returning the same data as i used with mysql.</p>

<p>At Google I found RestSharp. But does this framework returns the same structure in data like ExecuteReader?</p>

## Answers
### Answer ID: 25119529
<p>In short, no. <code>ExecuteReader</code> will return a class that is specialised to handle rows of data returned by a database; your API is likely returning serialised data in the form of JSON or XML.</p>

<p>The level of abstraction you will need to work at is a level higher than this: it doesn't make sense for a restful API client to return a "database row" object, but at the "next level up" (architecturally) you'll likely find some commonality. Data from a RESTful API can typically be deserialized into a simple object (or list of objects) and, in many systems that talk directly to a database, the output from the <code>DataReader</code> would be used to create a similar object (or list of objects). This is the layer at which your two implementations would typically converge.</p>

<p>The fact that you're returning <code>reader</code> from your function suggests that you might not have this level of abstraction in your existing code (perhaps your front end/business layer are using the <code>reader</code> directly). If that's the case, you will probably need a more thorough refactor in order to consume your REST service's output.</p>

