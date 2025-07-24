# C# Issue: What is the simplest way for me to load a .MDB file, make changes to it, and save the changes back to the original file?
[Link to question](https://stackoverflow.com/questions/518239/c-issue-what-is-the-simplest-way-for-me-to-load-a-mdb-file-make-changes-to-i)
**Creation Date:** 1233872374
**Score:** 5
**Tags:** c#, datatable, dataadapter, ms-jet-ace, oledbconnection
## Question Body
<p>My project that I am working on is almost finished. I am loading a .MDB file, displaying the contents on a DataGrid and attempting to get those changes on the DataGrid and save them back into the .MDB file. I am also going to create a function that allows me to take the tables from one .MDB file and save it to another .MDB file. Of course, I cannot do any of this if I cannot figure out how to save the changes back to the .MDB file.</p>

<p>I have researched Google extensively and there are no answers to my question. I consider myself a beginner at this specific topic so please don't make the answers too complicated -- I need the simplest way to edit a .MDB file! Please provide programming examples.</p>

<ol>
<li>Assume that I've already made a connection to a DataGrid. How do I get the changes made by the Datagrid? Im sure this one is simple enough to answer.</li>
<li>I then need to know how to take this Datatable, insert it into Dataset it came from then take that Dataset and rewrite the .MDB file. (If there is a way of only inserting the tables that were changed I would prefer that.)</li>
</ol>

<p>Thank you in advance, let me know if you need more information. This is the last thing I am probably going to have to ask about this topic...thank god.</p>

<p><strong>EDIT:</strong></p>

<p>The .mdb I am working with is a <strong>Microsoft Access Database.</strong> ( I didnt even know there were multiple .mdb files)</p>

<p>I know I cannot write directly to the .MDB file via a streamwriter or anything but is there a way I can possibly generated a .MDB File with the DataSet information already in it? OR is there just a way that I can add tables to a .MDB file that i've already loaded into the DataGrid. There HAS to be a way!</p>

<p>Again, I need a way to do this <strong><em>PROGRAMMATICALLY</em></strong> in C#.</p>

<p><strong>EDIT:</strong></p>

<p>Okay, my project is fairly large but I use a seperate class file to handle all Database connections. I know my design and source is really sloppy, but it gets the job done. I am only as good as the examples I find on the internet.</p>

<p>Remember, I am simply connecting to a DataGrid in another form. Let me know if you want my code from the Datagrid form (I dont know why you would need it though). DatabaseHandling.cs handles 2 .MDB files. So you will see two datasets in there. I will use this eventually to take tables from one Dataset and put them into another Dataset. I just need to figure out how to save these values BACK into a .MDB file.</p>

<p>Is there anyway to do this? There has to be a way...</p>

<p><strong>EDIT:</strong></p>

<p>From what i've researched and read...I think the answer is right under my nose. Using the "Update()" command. Now while this is re-assuring that there is infact a simple way of doing this, I am still left with the problem that I have no-friggin-clue how to use this update command. </p>

<p>Perhaps I can set it up like this:</p>

<pre><code>Oledb.OledbConnection cn = new Oledb.OledbConnection(); 
cn.ConnectionString = "Provider=Microsoft.ACE.OLEDB.12.0;Data Source=C:\Staff.mdb"; 
Oledb.OledbCommand cmd = new Oledb.OledbCommand(cn); 
cmd.CommandText = "INSERT INTO Customers (FirstName, LastName) VALUES (@FirstName, @LastName)"; 
</code></pre>

<p>I think that may do it, but I dont want to manually insert anything. I want to do both of these instead:</p>

<ul>
<li>Take information that is changed on the Datagrid and update the Access Database File (.mdb) that I got it from</li>
<li>Create a function that allows me to take tables from another Access Database File (.mdb) and replace them in a secondary Access Database file (.mdb). Both files will use the exact same structure but will have different information in them.</li>
</ul>

<p>I hope someone comes up with a answer for this...my project is done all that awaits is one simple answer.</p>

<p>Thank you again in advance.</p>

<p><strong>EDIT:</strong></p>

<p>Okay...good news. I have figured out how to query the .mdb file itself (I think). Here is the code, which doesn't work because I get a runtime error due to the sql command i'm attempting to use. Which will bring me to my next question.</p>

<p><strong>New function code added to DatabaseHandling.cs:</strong></p>

<pre><code>static public void performSynchronization(string table, string tableTwoLocation)
{
    OleDbCommand cmdCopyTables = new OleDbCommand("INSERT INTO" + table + "SELECT * FROM [MS Access;" + tableTwoLocation + ";].[" + table + "]"); // This query generates runtime error
    cmdCopyTables.Connection = dataconnectionA;
    dataconnectionA.Open();
    cmdCopyTables.ExecuteNonQuery();
    dataconnectionA.Close();
}
</code></pre>

<p>As you can see, I've actually managed to execute a query on the connection itself, which I believe to be the actual Access .MDB file. As I said though, the SQL query I've executed on the file doesn't work and generated a run-time error when used.</p>

<p>The command I am attempting to execute is supposed to take a table from a .MDB file and overwrite a table of the same type of a different .MDB file. The SQL command I attempted above tried to directly take a table from a .mdb file, and directly put it in another -- this isn't what I want to do. I want to take all the information from the .MDB file -- put the tables into a Datatable and then add all the Datatables to a Dataset (which i've done.) I want to do this for two .MDB files. Once I have two Datasets I want to take specific tables out of each Dataset and add them to each file like this:</p>

<ul>
<li>DataSetA >>>>----- [Add Tables
(Overwrite Them)] ----->>>>  DataSetB</li>
<li>DataSetB >>>>----- [Add Tables
(Overwrite Them)] ----->>>> DataSetA</li>
</ul>

<p>I want to take those each those Datasets and then put them BACK into each Access .MDB file they came from. Essentially keeping both databases synchronized.</p>

<p>So my questions, revised, is:</p>

<ol>
<li>How do I create a SQL query that will add a table to the .MDB file by overwriting the existing one of the same name. The query should be able to be created dynamically during runtime with an array that replaces a variable with the table name I want to add.</li>
<li>How do I get the changes that were made by the Datagrid to the DataTable and put them back into a DataTable (or DataSet) so I can send them to the .MDB file?</li>
</ol>

<p>I've tried to elaborate as much as possible...because I believe I am not explaing my issue very well. Now this question has grown wayyy too long. I just wish I could explain this better. :[</p>

<p><strong>EDIT:</strong></p>

<p>Thanks to a user below I think I've almost found a fix -- the keyword <em>almost</em>.
Here is my updated DatabaseHandling.cs code below. I get a runtime error "Datatype Mismatch." I dont know how that could be possible considering I am trying to copy these tables into another database with the exact same setup.</p>

<pre><code>using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Data.OleDb;
using System.Data;
using System.IO;

    namespace LCR_ShepherdStaffupdater_1._0
    {
        public class DatabaseHandling
        {
            static DataTable datatableB = new DataTable();
            static DataTable datatableA = new DataTable();
            public static DataSet datasetA = new DataSet();
            public static DataSet datasetB = new DataSet();
            static OleDbDataAdapter adapterA = new OleDbDataAdapter();
            static OleDbDataAdapter adapterB = new OleDbDataAdapter();
            static string connectionstringA = "Provider=Microsoft.Jet.OLEDB.4.0;" + "Data Source=" + Settings.getfilelocationA();
            static string connectionstringB = "Provider=Microsoft.Jet.OLEDB.4.0;" + "Data Source=" + Settings.getfilelocationB();
            static OleDbConnection dataconnectionB = new OleDbConnection(connectionstringB);
            static OleDbConnection dataconnectionA = new OleDbConnection(connectionstringA);
            static DataTable tableListA;
            static DataTable tableListB;

            static public void addTableA(string table, bool addtoDataSet)
            {
                dataconnectionA.Open();
                datatableA = new DataTable(table);
                try
                {
                    OleDbCommand commandselectA = new OleDbCommand("SELECT * FROM [" + table + "]", dataconnectionA);
                    adapterA.SelectCommand = commandselectA;
                    adapterA.Fill(datatableA);
                }
                catch
                {
                    Logging.updateLog("Error: Tried to get " + table + " from DataSetA. Table doesn't exist!");
                }

                if (addtoDataSet == true)
                {
                    datasetA.Tables.Add(datatableA);
                    Logging.updateLog("Added DataTableA: " + datatableA.TableName.ToString() + " Successfully!");
                }

                dataconnectionA.Close();
            }

            static public void addTableB(string table, bool addtoDataSet)
            {
                dataconnectionB.Open();
                datatableB = new DataTable(table);

                try
                {
                    OleDbCommand commandselectB = new OleDbCommand("SELECT * FROM [" + table + "]", dataconnectionB);
                    adapterB.SelectCommand = commandselectB;
                    adapterB.Fill(datatableB);
                }
                catch
                {
                    Logging.updateLog("Error: Tried to get " + table + " from DataSetB. Table doesn't exist!");
                }



                if (addtoDataSet == true)
                {
                    datasetB.Tables.Add(datatableB);
                    Logging.updateLog("Added DataTableB: " + datatableB.TableName.ToString() + " Successfully!");
                }

                dataconnectionB.Close();
            }

            static public string[] getTablesA(string connectionString)
            {
                dataconnectionA.Open();
                tableListA = dataconnectionA.GetOleDbSchemaTable(OleDbSchemaGuid.Tables, new Object[] { null, null, null, "TABLE" });
                string[] stringTableListA = new string[tableListA.Rows.Count];

                for (int i = 0; i &lt; tableListA.Rows.Count; i++)
                {
                    stringTableListA[i] = tableListA.Rows[i].ItemArray[2].ToString();
                }
                dataconnectionA.Close();
                return stringTableListA;
            }

            static public string[] getTablesB(string connectionString)
            {
                dataconnectionB.Open();
                tableListB = dataconnectionB.GetOleDbSchemaTable(OleDbSchemaGuid.Tables, new Object[] { null, null, null, "TABLE" });
                string[] stringTableListB = new string[tableListB.Rows.Count];

                for (int i = 0; i &lt; tableListB.Rows.Count; i++)
                {
                    stringTableListB[i] = tableListB.Rows[i].ItemArray[2].ToString();
                }
                dataconnectionB.Close();
                return stringTableListB;
            }

            static public void createDataSet()
            {

                string[] tempA = getTablesA(connectionstringA);
                string[] tempB = getTablesB(connectionstringB);
                int percentage = 0;
                int maximum = (tempA.Length + tempB.Length);

                Logging.updateNotice("Loading Tables...");
                for (int i = 0; i &lt; tempA.Length ; i++)
                {
                    if (!datasetA.Tables.Contains(tempA[i]))
                    {
                        addTableA(tempA[i], true);
                        percentage++;
                        Logging.loadStatus(percentage, maximum);
                    }
                    else
                    {
                        datasetA.Tables.Remove(tempA[i]);
                        addTableA(tempA[i], true);
                        percentage++;
                        Logging.loadStatus(percentage, maximum);
                    }
                }

                for (int i = 0; i &lt; tempB.Length ; i++)
                {
                    if (!datasetB.Tables.Contains(tempB[i]))
                    {
                        addTableB(tempB[i], true);
                        percentage++;
                        Logging.loadStatus(percentage, maximum);
                    }
                    else
                    {
                        datasetB.Tables.Remove(tempB[i]);
                        addTableB(tempB[i], true);
                        percentage++;
                        Logging.loadStatus(percentage, maximum);
                    }
                }


            }

            static public DataTable getDataTableA()
            {
                datatableA = datasetA.Tables[Settings.textA];

                return datatableA;
            }
            static public DataTable getDataTableB()
            {
                datatableB = datasetB.Tables[Settings.textB];
                return datatableB;
            }

            static public DataSet getDataSetA()
            {
                return datasetA;
            }

            static public DataSet getDataSetB()
            {
                return datasetB;
            }

            static public void InitiateCopyProcessA()
            {
                DataSet tablesA;
                tablesA = DatabaseHandling.getDataSetA();

                foreach (DataTable table in tablesA.Tables)
                {
                    CopyTable(table, connectionstringB);
                }
            }

            public static void CopyTable(DataTable table, string connectionStringB)
            {
                var connectionB = new OleDbConnection(connectionStringB);
                foreach (DataRow row in table.Rows)
                {
                    InsertRow(row, table.Columns, table.TableName, connectionB);
                }
            }

            public static void InsertRow(DataRow row, DataColumnCollection columns, string table, OleDbConnection connection)
            {
                var columnNames = new List&lt;string&gt;();
                var values = new List&lt;string&gt;();

                for (int i = 0; i &lt; columns.Count; i++)
                {
                    columnNames.Add("[" + columns[i].ColumnName + "]");
                    values.Add("'" + row[i].ToString().Replace("'", "''") + "'");
                }

                string sql = string.Format("INSERT INTO {0} ({1}) VALUES ({2})",
                        table,
                        string.Join(", ", columnNames.ToArray()),
                        string.Join(", ", values.ToArray())
                    );

                ExecuteNonQuery(sql, connection);
            }

            public static void ExecuteNonQuery(string sql, OleDbConnection conn)
            {
                if (conn == null)
                    throw new ArgumentNullException("conn");

                ConnectionState prevState = ConnectionState.Closed;
                var command = new OleDbCommand(sql, conn);
                try
                {
                    prevState = conn.State;
                    if (prevState != ConnectionState.Open)
                        conn.Open();

                    command.ExecuteNonQuery(); // !!! Runtime-Error: Data type mismatch in criteria expression. !!!
                }
                finally
                {
                    if (conn.State != ConnectionState.Closed
                        &amp;&amp; prevState != ConnectionState.Open)
                        conn.Close();
                }
            }

            }          
        }
</code></pre>

<p>Why am I getting this error? Both tables are exactly the same. What am I doing wrong? 
Worst case, how do I delete the table in the other Access .MDB file before inserting the exact same structure table with different values in it?</p>

<p>Man I wish I could just figure this out...</p>

<p><strong>EDIT:</strong></p>

<p>Okay, I've come some distance. My question has morphed into a new one, and thus deserves being asked seperately. I have had my question answered as now I know how to execute queries directly to the connection that I have opened. Thank you all!</p>

## Answers
### Answer ID: 519042
<p>To update the original MDB file with changes made to <em>the DataSet</em> (not the DataGrid, since that's just UI over the DataSet) just use the <a href="http://msdn.microsoft.com/en-us/library/system.data.common.dataadapter.update.aspx" rel="nofollow noreferrer">DataAdapter.Update</a> command.</p>

<p>To move tables from 1 to the other is a bit trickier. If the table doesn't already exist in the destination, you'll need to create it using a <a href="http://msdn.microsoft.com/en-us/library/bb177893.aspx" rel="nofollow noreferrer">SQL CREATE statement</a>. Then, <a href="http://msdn.microsoft.com/en-us/library/377a8x4t.aspx" rel="nofollow noreferrer">DataAdapter.Fill</a> a DataSet from the <em>source</em>. Loop through each row and set it's state to RowAdded by calling <a href="http://msdn.microsoft.com/en-us/library/system.data.datarow.setadded.aspx" rel="nofollow noreferrer">DataRow.SetAdded</a>. Then, pass it back to a DataAdapter.Update from the <em>destination</em> database. </p>

<p>EDIT: <a href="https://stackoverflow.com/questions/520506/how-do-i-structure-an-oledbcommand-query-so-that-i-can-take-tables-from-one-acces/520665#520665">Code is on the next question....</a></p>

### Answer ID: 518326
<p>I'm not sure how far you've gotten, but if you looking for a quick drag and drop operation you might want to look at creating a strongly-typed dataset that connects, and using the drag-drop features of the DataSources Tool Window in Visual Studio.</p>

<p>There are definately samples out there, but you will want to.</p>

<ol>
<li>Create a new DataSet </li>
<li>Drag-n-Drop from your DataConnection Tree in Server Explorer</li>
<li>Create a new form </li>
<li>Drag the table from the DataSources Tool</li>
<li>Window on to the form.</li>
<li>voila</li>
</ol>

<p><strong>Update:</strong></p>

<p>First off, I'm not 100% that I understand your issue.  If you can create some LinkTables between the access files that would be best,  then you can copy the data between files using a sql statement like 'INSERT INTO Customers SELECT FirstName, LastName FROM File2.Customers'.  If thats not and option I think your going to have to loop the DataTables and insert the records manually using INSERT statements similar to your last edit.  As for the datagrid, you will probably have to keep track of whats changed by monitoring the RowChanged Event (not sure if thats the exact event) of even do the insert/update statements when the row changes.</p>

<p><strong>Update:</strong></p>

<p>to loop the datatable you would do something like this.  not tested.  I just updated this again to include the MakeValueDbReady function.  This is not tested either and I'm not sure if I've handle all the cases or even all the cases correctly.  You'll really have to debug the sql statement and make sure its generating the right value.  Each database handles is values differently. Atleast this way the value parse is extracted away.  I also realized that instead of hard coding the TableName you should be able to get it from a property on the DataTable</p>

<pre><code>void CopyTable(DataTable table, string connectionStringB)
{
    var connectionB = new OleDbConnection(connectionStringB);
    foreach(DataRow row in table.Rows)
    {
        InsertRow(row, table.Columns, table.TableName, connectionB);
    }
}

public static void InsertRow(DataRow row, DataColumnCollection columns, string table, OleDbConnection connection)
{
    var columnNames = new List&lt;string&gt;();
    var values = new List&lt;string&gt;();

    // generate the column and value names from the datacolumns    
    for(int i =0;i&lt;columns.Count; i++)
    {
        columnNames.Add("[" + columns[i].ColumnName + "]");
        // datatype mismatch should be fixed by this function
        values.Add(MakeValueDbReady(row[i], columns[i].DataType));
    }

    // create the sql
    string sql = string.Format("INSERT INTO {0} ({1}) VALUES ({2})",
            table,
            string.Join(", ", columnNames.ToArray()),
            string.Join(", ", values.ToArray())
        );

    // debug the accuracy of the sql here and even copy into 
    // a new Query in Access to test
    ExecuteNonQuery(sql, connection);
}

// as the name says we are going to check the datatype and format the value
// in the sql string based on the type that the database is expecting
public string MakeValueDbReady(object value, Type dataType)
{
    if (value == null)
        return null;

    if (dataType == typeof(string))
    {
        return "'" + value.ToString().Replace("'", "''") + "'"
    }
    else if (dataType == typeof(DateTime))
    {
        return "#" + ((DateTime)value).ToString + "#"
    }
    else if (dataType == typeof(bool))
    {
        return ((bool)value) ? "1" : "0";
    }

    return value.ToString();
}

public static void ExecuteNonQuery(string sql, OleDbConnection conn)
{
    if (conn == null)
        throw new ArgumentNullException("conn");

    ConnectionState prevState = ConnectionState.Closed;
    var command = new OleDbCommand(sql, conn);
    try
    {
        // the reason we are checking the prev state is for performance reasons
        // later you might want to open the connection once for the a batch
        // of say 500 rows  or even wrap your connection in a transaction.
        // we don't want to open and close 500 connections
        prevState = conn.State;
        if (prevState != ConnectionState.Open)
            conn.Open();

        command.ExecuteNonQuery();
    }
    finally
    {
        if (conn.State != ConnectionState.Closed
            &amp;&amp; prevState != ConnectionState.Open)
            conn.Close();
    }
}
</code></pre>

### Answer ID: 518398
<p>How are you connecting to the database (the .mdb file)?  Could you post some sample code?  If you're connecting to it correctly than any SQL operations you run against it should be saved in the database automatically.</p>

<p>So after you connect to the database you can execute SQL that will create tables, insert/update/retrieve data, etc.  Trying to build an .mdb file by hand is not advisable.</p>

<p>Here's an example:</p>

<p><a href="http://www.java2s.com/Code/CSharp/Database-ADO.net/Access.htm" rel="nofollow noreferrer">http://www.java2s.com/Code/CSharp/Database-ADO.net/Access.htm</a></p>

### Answer ID: 518264
<p>There are actually more than one format of file with the .mdb extension. So, if I guess the wrong one, this will be the wrong answer. But, it sounds like a Microsoft Access issue.</p>

<p>You don't write directly to an MDB file. They are encrypted and compressed. The easiest way to modify an MDB file is to load it through Access and copy the tables through the methods provided.</p>

