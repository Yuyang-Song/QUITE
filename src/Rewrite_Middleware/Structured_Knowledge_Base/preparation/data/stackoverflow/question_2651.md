# No rows found, C# using OleDB
[Link to question](https://stackoverflow.com/questions/44943037/no-rows-found-c-using-oledb)
**Creation Date:** 1499328037
**Score:** 1
**Tags:** c#, ms-access, oledb
## Question Body
<p>I have been rewriting a C# program to better encapsulate accessing an Access database, using OleDb.  It runs, but doesn't find the row that exists, but running the SQL query in Access does find it.  </p>

<p>The question is: what is wrong with my code?  Why don't I get any rows returned?</p>

<p>I'm using VS 2017 and Access 2013.  The PC is an up-to-date windows 10 x64 machine.</p>

<pre><code>using System;
using System.Collections.Generic;
using System.Data;
using System.Data.OleDb;
using System.Linq;

namespace OleDbTest
{
    class Program
    {
        static void Main( string[] args )
        {
            // Create Profile File object
            ProcessEJFile EJP = new ProcessEJFile(
                "Provider=Microsoft.ACE.OLEDB.12.0;" +
                @"Data Source=E:\Users\sallyw\Documents\Bar.accdb;" +
                "Persist Security Info=False;");

            // Get details of last header - this should return just one row
            string query = 
            //      @"select * from stock_head where sh_ref in ( select max( stock_head.[ sh_ref ] ) FROM stock_head WHERE sh_ref like ""[#]%"")";

                    "select sh_id, sh_ref, sh_lineno, sh_type, sh_supplier, sh_datetime from stock_head where sh_id = 19;";

            //      "select * from stock_head where sh_ref = 19;"

            List&lt;StockHead&gt; shlist = EJP.GetStockHead(query, null );
            if ( shlist == null )
            {
                Console.WriteLine( "shlist is null" );
            }
            else
            {
                Console.WriteLine( "shlist contains {0} entries", shlist.Count );
            }
            Console.ReadLine();
        }
    }

    class ProcessEJFile
    {
        AccessDatabase Accdb = null;

        public ProcessEJFile( string connectionString )
        {
            Accdb = new AccessDatabase( connectionString );
            Console.WriteLine( "ProfessEJFile #1 - connection string = {0}", connectionString );
        }

        public List&lt;StockHead&gt; GetStockHead( string sql, params object[] args )
        {
            DataTable t;
            if ( args == null )
            {
                Console.WriteLine( "GetStockHead #1 - args are NULL " );
            }
            else
            {
                Console.WriteLine( "GetStockHead #2 - {0} arguments passed", args.Count() );
            }

            Accdb.ExecuteQuery( out t, sql, args );

            if ( t != null )
            {
                List&lt;StockHead&gt; shlist = new List&lt;StockHead&gt;();

                foreach ( DataRow r in t.Rows )
                {
                    Console.WriteLine( t.ToString() );
                    //StockHead sh = new StockHead(
                    //    (int)r["sh_id"],
                    //    (string)r["sh_ref"],
                    //    (int)r["sh_lineno"],
                    //    (string)r["sh_type"],
                    //    (string)r["sh_supplier"],
                    //    (DateTime)r["sh_datetime"]);
                    //shlist.Add( sh );
                }
                return shlist;
            }
            else
            {
                Console.WriteLine( "GetStockHead #3 - t is null" );
                return null;
            }
        }
    }
    class AccessDatabase
    {
        public OleDbConnection conn = new OleDbConnection();

        public AccessDatabase( string connection )
        {
            conn.ConnectionString = connection;
        }

        public bool OpenDatabase()
        {
            try
            {
                conn.Open();
            }
            catch ( Exception ex )
            {
                Console.WriteLine( "OpenDatabase()\n" + ex.Message );
                return false;
            }
            return true;
        }

        public void CloseDatabase()
        {
            if ( conn == null )
                return;

            conn.Close();
        }

        public void ExecuteQuery( out DataTable dataTable, string sql, params object[] args )
        {
            dataTable = new DataTable();
            string query;

            // Simplified version not validating or cleaning arguments in any way
            if (args == null )
            {
                query = sql;
            }
            else
            {
                query = string.Format( sql, args );
            }
            Console.WriteLine( "ExecuteQuery #3 - query = '{0}'", query );

            if ( OpenDatabase() )
            {
                OleDbCommand command = new OleDbCommand( query, conn );
                OleDbDataAdapter adapter = new OleDbDataAdapter( command );
                adapter.Fill( dataTable );
            }
            else
            {
                Console.WriteLine( "ExecuteQuery #9 - cannot open database" );
            }
        }
    }

    class StockHead
    {
        public int sh_id;              // autonumber
        public string sh_ref;          // short text
        public int sh_lineno;          // Number
        public string sh_type;         // short text
        public string sh_supplier;     // short text
        public DateTime sh_datetime;   // date/time

        public StockHead( int id, string refno, int lineno, string type, string supplier, DateTime datetime )
        {
            sh_id = id;
            sh_ref = refno;
            sh_lineno = lineno;
            sh_type = type;
            sh_supplier = supplier;
            sh_datetime = datetime;
        }
    }
}
</code></pre>

<p>Data in CSV format, class stock_head shows the Access column types:</p>

<pre><code>1,"#000001",,"IR","INITIAL RESET",20/8/2013 08:33:00
2,"#000002",,"SD","FORMATTING",20/8/2013 08:34:00
3,"#000003",,"SD","FOLDER CREATE",20/8/2013 08:35:00
4,"#000004",,"SD","FOLDER SELECT",20/8/2013 08:35:00
5,"#000005",,"NS","NO SALE",20/8/2013 11:14:00
6,"#000006",,"NS","NO SALE",20/8/2013 11:46:00
7,"#000007",,"NS","NO SALE",20/8/2013 12:16:00
8,"#000008",,"SALE",,20/8/2013 15:11:00
9,"#000009",,"SALE",,20/8/2013 15:30:00
10,"#000010",,"Z1",,20/8/2013 15:32:00
11,"#000011",,"NS","NO SALE",20/8/2013 15:32:00
12,"#000012",,"SALE",,20/8/2013 16:46:00
13,"#000013",,"SALE",,20/8/2013 16:47:00
14,"#000014",,"SALE",,20/8/2013 17:32:00
15,"#000015",,"Z1",,20/8/2013 19:25:00
16,"#000016",,"NS","NO SALE",20/8/2013 19:25:00
17,"#000017",,"Z1",,20/8/2013 21:52:00
18,"#000018",,"NS","NO SALE",20/8/2013 21:52:00
19,"#000019",,"SALE",,23/8/2013 18:27:00
20,"#000020",,"SALE",,23/8/2013 19:06:00
21,"#000021",,"SALE",,23/8/2013 20:24:00
22,"#000022",,"SALE",,23/8/2013 20:36:00
23,"#000023",,"SALE",,23/8/2013 21:21:00
24,"#000024",,"SALE",,23/8/2013 21:57:00
25,"#000025",,"SALE",,23/8/2013 22:38:00
26,"#000026",,"Z1",,23/8/2013 22:40:00
27,"#000027",,"NS","NO SALE",23/8/2013 22:40:00
28,"#000028",,"SALE",,24/8/2013 16:09:00
29,"#000029",,"SALE",,24/8/2013 16:28:00
30,"#000030",,"SALE",,24/8/2013 16:58:00
</code></pre>

## Answers
### Answer ID: 44950468
<p>OK found a fix by amending the StockHead constructor to take the DataRow rather than individual arguments, and checking for any nulls there.</p>

<p>Is it a good way?  Is there a better way?  In a way I like it more as the complications are more tucked away - the line that calls it is now simply</p>

<p><code>StockHead sh = new StockHead( r );</code></p>

<p>Constructor code is now:</p>

<pre><code>    public StockHead( DataRow row )
    {
        this.sh_id = (int)row[ "sh_id" ];
        this.sh_ref = (string)row[ "sh_ref" ];
        if ( !string.IsNullOrEmpty( row[ "sh_lineno" ].ToString() ) )
        {
            this.sh_lineno = (int)row[ "sh_lineno" ];
        }
        this.sh_type = (string)row[ "sh_type" ];
        if ( !string.IsNullOrEmpty( row[ "sh_lineno" ].ToString() ) )
        {
            this.sh_supplier = (string)row[ "sh_supplier" ];
        }
        this.sh_datetime = (DateTime)row[ "sh_datetime" ];
    }
</code></pre>

### Answer ID: 44948210
<p>If I alter the code creating a StockHead object to use literals instead of the correct values it works.  There must be an elegant way of resolving this!</p>

<pre><code>                StockHead sh = new StockHead(
                    (int)r[ "sh_id" ],
                    (string)r[ "sh_ref" ],
                    0,                          //(int)r[ "sh_lineno" ],
                    (string)r[ "sh_type" ],
                    "",                         //(string)r[ "sh_supplier" ],
                    (DateTime)r[ "sh_datetime" ]);
</code></pre>

### Answer ID: 44943149
<p>This is simple to be edit <code>GetStockHead</code> function</p>

<pre><code>public List&lt;StockHead&gt; GetStockHead( string sql, params object[] args )
{
    DataTable t;
    if ( args == null )
    {
        Console.WriteLine( "GetStockHead #1 - args are NULL " );
    }
    else
    {
        Console.WriteLine( "GetStockHead #2 - {0} arguments passed", args.Count() );
    }

    Accdb.ExecuteQuery( out t, sql, args );

    if ( t != null )
    {
        List&lt;StockHead&gt; shlist = new List&lt;StockHead&gt;();

        foreach ( DataRow r in t.Rows )
        {
            Console.WriteLine( t.ToString() );
            StockHead sh = new StockHead(
                (int)r["sh_id"],
                (string)r["sh_ref"],
                (int)r["sh_lineno"],
                (string)r["sh_type"],
                (string)r["sh_supplier"],
                (DateTime)r["sh_datetime"]);
            shlist.Add( sh );
        }
        return shlist;
    }
    else
    {
        Console.WriteLine( "GetStockHead #3 - t is null" );
        return null;
    }
}
</code></pre>

