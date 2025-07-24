# MySqlCommand.ExecuteNonQuery() not filling MySqlParameter(s)
[Link to question](https://stackoverflow.com/questions/16059222/mysqlcommand-executenonquery-not-filling-mysqlparameters)
**Creation Date:** 1366199395
**Score:** 0
**Tags:** c#, mysql
## Question Body
<p>Background: I am rewriting my ASP.NET application - currently it uses MS SQL database but I need to support also MySQL (both in the same time!).</p>

<p>Most of work is done - I used <strong>MySQL Connector/Net</strong> for work with MySQL database from C# (Visual Studio 2010) - but I have troubles with certain SQL queries. This is SQL query I need to execute:</p>

<pre><code>"SELECT @username=username FROM t_Users WHERE id=@id"
</code></pre>

<p>Here is my code:
</p>

<pre><code>public static int ExecuteSqlNonQuery(string i_szQuery)
{
    bool bConnectionWasOpen = false;
    AbstractConnection dbConnection = CMSSQLInstanceCreator.CreateConnection();            

    if(dbConnection.IsMySQL())
    {
        MySqlConnection aSqlConnection = dbConnection.GetMysConnection();
        try
        {
            if (aSqlConnection.State == System.Data.ConnectionState.Closed)
                aSqlConnection.Open();
            else
                if (aSqlConnection.State == System.Data.ConnectionState.Open)
                    bConnectionWasOpen = true;
                else
                    throw new ApplicationException("Connection not available!");

            List&lt;MySqlParameter&gt; aParameters1 = new List&lt;MySqlParameter&gt;();
            aParameters1.Add(new MySqlParameter("@username", MySqlDbType.VarString, 128));
            aParameters1.Add(new MySqlParameter("@id", MySqlDbType.Int32));
            aParameters1[0].Direction = System.Data.ParameterDirection.Output;                
            aParameters1[1].Direction = System.Data.ParameterDirection.Input;
            aParameters1[1].Value = (int)1;

            MySqlCommand aSqlCommand = new MySqlCommand(i_szQuery, aSqlConnection);
            aSqlCommand.CommandType = System.Data.CommandType.Text;
            aSqlCommand.CommandTimeout = 0;
            aSqlCommand.Parameters.Clear();
            aSqlCommand.Parameters.AddRange(aParameters1.ToArray());

            int iResult = aSqlCommand.ExecuteNonQuery();
            if(iResult &lt;= 0)
                Debug.WriteLine("aResult &lt;= 0: " + i_szQuery);
            return iResult;
        }
        catch (Exception ex)
        {
            throw new ApplicationException("Cannot execute query!\nReason: '" + ex.Message + "'", ex);
        }
        finally
        {
            if (!bConnectionWasOpen &amp;&amp; aSqlConnection.State == System.Data.ConnectionState.Open)
                aSqlConnection.Close();
        }
    }
    else
    {
      //... almost the same for MS SQL
    }
}
</code></pre>

<p>The problem is that the Output parameter <strong>@username</strong> (System.Data.ParameterDirection.Output;) is not filled with the value from query.</p>

<p>If I use other query - e.g. </p>

<pre><code>UPDATE t_Users SET password=@new_password WHERE (password=@old_password AND id=@user)
</code></pre>

<p>Everything is fine.</p>

<p>I cannot return scalar as there are many other queries like </p>

<pre><code>SELECT @username=username, @is_blocked=is_blocked, @full_name=full_name, @must_change_pwd=must_change_pwd ...
</code></pre>

<p>returning many values and I do not want to rewrite most of code.</p>

<p>It looks like there is problem only in MySQL because the same code works with MS SQL fine.</p>

<p>What should I use to force MySqlParameter to load the value from query?</p>

## Answers
### Answer ID: 33065261
<p>It apparently is a shortcoming in the MySql .Net connector, see <a href="http://bugs.mysql.com/bug.php?id=75267" rel="nofollow noreferrer">#75267</a>. Tested it with connector v6.9.7 and MySql server 5.5.45. It is still broken and the bug report - of december 2014 - is still open. Output parameters work for stored procedures, with a command type StoredProcedure, and do not work for a SELECT statement that assigns output parameters as part of the select; command type Text.</p>
<p>2023-02-16 Update. A couple of weeks ago it is fixed in version 8.0.32. I tested it by updating Connector/NET to 8.0.32, and by using NuGet package MySql.Data 8.0.32.</p>
<p>A command of type text, an output parameter and an ExecuteNonQuery now works for the following case:</p>
<pre><code>SET @valNum:=(SELECT ValueNumber FROM `sky.application` WHERE Name='Agents')
</code></pre>
<p>Value @valNum can then be retrieved through the output parameter.</p>
<p>Note that retrieving two values does not work as follows, despite it does the job in the Workbench:</p>
<pre><code>SELECT @valNum:=ValueNumber, @instNum:=InstanceNumber FROM `sky.application` WHERE Name='Agents'
</code></pre>
<p>Error: Parameter 'valNum:=ValueNumber' not found in the collection.
Same error if retrieving one value.</p>
<p>Fortunately the following syntax works:</p>
<pre><code>SELECT ValueNumber, InstanceNumber INTO @valNum, @instNum FROM `sky.application` WHERE Name='Agents'
</code></pre>

### Answer ID: 16059875
<p>You should be able to read the value of the output like this </p>

<pre><code>aSqlCommand.Parameters["@username"].Value
</code></pre>

