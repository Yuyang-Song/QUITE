# How should I properly be retrieving database records via SqlConnection?
[Link to question](https://stackoverflow.com/questions/15143685/how-should-i-properly-be-retrieving-database-records-via-sqlconnection)
**Creation Date:** 1362078554
**Score:** 0
**Tags:** c#, .net-4.0, standards, sqlconnection
## Question Body
<p>I'm sure this question has been asked many times, and I dug through a few of the similar ones but couldn't find one that really flushed it out as much as I'd have liked.</p>

<p>I have an application that uses a database helper class to connect and retrieve records from a database. I was considering rewriting it and wanted to know what the best way to do it would be. </p>

<p>Here is roughly how it's set up now (Note: This is already in place, and there are thousands of lines of this stuff).</p>

<p><a href="http://pastie.org/6355776" rel="nofollow"><strong>DatabaseHelper.CS</strong></a></p>

<pre><code>    private SqlConnection conn; 

    public DatabaseHelper()
    {
        // Create database connection
        conn = new System.Data.SqlClient.SqlConnection();
        SqlConnectionStringBuilder connection = new SqlConnectionStringBuilder();
        connection.ConnectTimeout = 150; // Microsft fix for timeout error (known bug)
        connection.MinPoolSize = 20; // Microsft fix for timeout error (known bug)
        connection.DataSource = Properties.Settings.Default.DBString;
        connection.InitialCatalog = Properties.Settings.Default.DBInitCatalog;
        connection.IntegratedSecurity = true;

        if (conn.State != ConnectionState.Connecting)
        {
            conn.ConnectionString = connection.ConnectionString;
        }
     }

    public bool Open()
    {
        if (this.IsOpen()) // IsOpen is just a method that checks connectionstate.
        { return true; }
        else
        {
            try
            {
                conn.Open();
                return true;
            }
            catch (System.Data.SqlClient.SqlException ex)
            {
                // omitted for post
            }
        }
        return false;
    }

    public bool Close()
    {
        if (!this.IsOpen())
        { return true; }
        try
        {
            conn.Close();
            return true;
        }
        catch (System.Data.SqlClient.SqlException ex)
        {
           // omitted for post
        }
        return false;
    }

    public List&lt;string&gt; GetTeamLeaders(string team)
    {
        List&lt;string&gt; leaders = new List&lt;string&gt;();
        string query = "Select Leader FROM Teams WHERE Team = @team_vc";
        try
        {
            using (SqlCommand cmd = new SqlCommand(query, conn))
            {
                cmd.Parameters.Add("@team_vc", SqlDbType.NVarChar).Value = team;
                using (SqlDataReader sdr = cmd.ExecuteReader())
                {
                    int column = sdr.GetOrdinal("Leader");
                    while (sdr.Read())
                    {
                        leaders.Add(sdr[column].ToString());
                    }
                }
            }
        }
        catch (Exception ex)
        {
            // omitted for post
        }
        return leaders;
    }

    private string GetTeamAbbrev(string team)
    {
        string abbrev= "";

        string query = "SELECT Abbrev FROM Teams where Team = @team_vc";
        using (SqlCommand cmd = new SqlCommand(query, conn))
        {
            cmd.Parameters.Add("@team_vc", SqlDbType.NVarChar).Value = team;
            try
            {
                abbrev= Convert.ToString(cmd.ExecuteScalar());
            }
            catch (Exception ex)
            {
                // omitted for post
            }
        }
        return (string.IsNullOrEmpty(location)) ? "None" : abbrev;
    }
</code></pre>

<p><a href="http://pastie.org/6355781" rel="nofollow"><strong>MainApp.CS</strong></a></p>

<pre><code>    private DatabaseHelper dbHelper;

    public MainApp()
    {
        InitializeComponent();
        dbHelper= new DatabaseHelper(); // Instantiate database controller
    }

    private void someButton_Click(object sender, EventArgs e)
    {
        List&lt;string&gt; teamLeaders = new List&lt;string&gt;();

        if (dbHelper.Open())
        {
            teamLeaders = dbConn.GetTeamLeaders(textboxTeam.Text);
            dbHelper.Close();
        }
        else
        {
            return;
        }
        // all the code to use results
    }

    private void someOtherButton_Click(object sender, EventArgs e)
    {
        List abbreviation = string.Empty;

        if (dbHelper.Open())
        {
            abbreviation = dbConn.GetTeamLeaders(textboxTeam.Text);
            dbHelper.Close();
        }
        else
        {
            return;
        }
        // all the code to use results
    }
</code></pre>

<p>Now I'm sure there are some very serious issues with how this is setup, but for me my biggest complaints are always having to open and close the connection.</p>

<p>My first move was to just move the open and close inside the DatabaseHelper methods, so each method (i.e. GetTeamLeaders) would call open and close in itself. But the problem was if it did actually fail to open it was really hard to feed it back up to the main program, which would try to run with whatever value the variable contained when it was made. I was thinking I would almost need an "out" bool that would tag along to see if the query completed, and could check make and check that anytime I used I needed to get something from the database, but I'm sure that has issues to.</p>

<p>Another big problem with this approach is anytime I want to make a call from another form, I have to either make another instance of the helper on that form, or pass a reference to the main one. (Currently my way around this is to retrieve all the information I would need beforehand in the <code>MainApp</code> and then just pass that to the new form). I'm not sure if when I rewrite this there's a good static way to set it up so that I can call it from anywhere.</p>

<p>So is there anything here worth keeping or does it all need to be stripped down and built back from scratch?</p>

