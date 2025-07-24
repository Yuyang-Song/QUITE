# Reusing the connection and prepare statement to mysql database
[Link to question](https://stackoverflow.com/questions/42771658/reusing-the-connection-and-prepare-statement-to-mysql-database)
**Creation Date:** 1489432409
**Score:** -1
**Tags:** c#, mysql
## Question Body
<p>I am having a function which calls different functions that connect to the mysql database and queries the database. Here I am not sure how can I reuse my <code>conn and cmd</code> to make more efficiency in the code. To have the connection creaeted in <code>Validation()</code> once and reuse them in the other function wherever I am trying to connect to database. Below is what I am doing</p>

<pre><code>    private static void Validation(List&lt;Employee&gt; EmpList, string Group)
    {
        ValidateName(EmpList, Group);
        ValidateDept(EmpList, Group);
     }
    public static void ValidateName(List&lt;Employee&gt; EmpList, string Grp)
    {
        var connStr = ConfigurationManager.ConnectionStrings["MyConnectionString"].ConnectionString;

        string selectQuery;

        for (int i = 0; i &lt; EmpList.Count; i++)
        {
           selectQuery = "Select Name from Employee where Group = @Group  AND @Name in (FirstName, LastName);";
            using (MySqlConnection conn = new MySqlConnection(connStr))
            using (MySqlCommand cmd = new MySqlCommand(selectQuery, conn))
            {
                cmd.Parameters.Add("@Group", MySqlDbType.VarChar).Value = Grp;
                cmd.Parameters.Add("@Name", MySqlDbType.VarChar).Value = EmpList[i].Name;
                conn.Open();
                var reader = cmd.ExecuteReader();
                List&lt;string&gt; lineList = new List&lt;string&gt;();
                while (reader.Read())
                {
                    lineList.Add(reader.GetString(0));
                }
                if (lineList.Count &lt;=0)
                {
                   WriteValidationFailure(EmpList[i], "Failed");
                }
                conn.Close();
        }       
      }
    }

   public static void ValidateBreedingDept(List&lt;Employee&gt; EmpList, string Grp)
    {
        var connStr = ConfigurationManager.ConnectionStrings["MyConnectionString"].ConnectionString;

        string selectQuery;

        for (int i = 0; i &lt; EmpList.Count; i++)
        {
            selectQuery = "Select DepartmentName from Department where Group = @Group AND DepartmentName = @Dept;";
            using (MySqlConnection conn = new MySqlConnection(connStr))
            using (MySqlCommand cmd = new MySqlCommand(selectQuery, conn))
            {
                cmd.Parameters.Add("@Group", MySqlDbType.VarChar).Value = Grp;
                cmd.Parameters.Add("@Dept", MySqlDbType.VarChar).Value = EmpList[i].Dept;
                conn.Open();
                var reader = cmd.ExecuteReader();
                List&lt;string&gt; lineList = new List&lt;string&gt;();
                while (reader.Read())
                {
                    lineList.Add(reader.GetString(0));
                }
                if (lineList.Count &lt;= 0)
                {
                    WriteValidationFailure(listOfMouse[i], "Failed");
                }
                conn.Close();
            }
        }
    }
</code></pre>

<p>I am new to connecting to database and querying from c#. And also how to rewrite the queries to use Prepare statements. I understand I can use <code>cmd.Prepare()</code> but can I reuse the parameters from one function in to another.</p>

## Answers
### Answer ID: 42771779
<p>"reuse my conn and cmd to make more efficiency in the code"</p>

<p>You don't need to worry about that. C# takes care of it by using something called connection pool. </p>

<p>All "closed" connections do not really close the underlying connection but rather returned to the connection pool for later use which is exactly what you are trying to do</p>

<p><a href="https://msdn.microsoft.com/en-us/library/8xx3tyca%28v=vs.110%29.aspx?f=255&amp;MSPPError=-2147217396" rel="nofollow noreferrer">Read more on MSDN</a></p>

