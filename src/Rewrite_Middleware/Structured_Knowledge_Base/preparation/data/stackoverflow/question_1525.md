# How to manage the same database from different classes? (android/sqlite)
[Link to question](https://stackoverflow.com/questions/8524866/how-to-manage-the-same-database-from-different-classes-android-sqlite)
**Creation Date:** 1323973818
**Score:** 0
**Tags:** java, android, database, sqlite
## Question Body
<p><strong>In my android app I had one class doing the following functions:</strong><br>
<em>storing data from an XML source into a database;</em><br>
<em>loading the data from the database;</em><br>
<em>rewriting to the database from the xml source if the data was more than 24 hours old;</em><br>
that all worked fine.</p>

<p><strong>I am now trying to write a new table to that same database from another class.</strong><br>
So I followed the same procedures/set-up as in the first class and now the program crashes (force close error) and the android log cat gives the following errors:<br>
<em>SQL error: msg= table "table-name" does not exist</em><br>
<em>error inserting (query) into table "table-name"</em> (this error is repeated for each insert attempted)</p>

<p>The problem is, the "table-name" it gives me (saying it doesn't exist) is the table from the first class which worked fine before.</p>

<p>Here is some relevant code:  </p>

<pre><code>public class CurrencyConverter {
public static String XML_SOURCE = "http://rss.timegenie.com/forex.gz";
public static long LAST_UPDATE=0;
private static SQLiteHelper.DatabaseAdapter dbAdapter;
private final static String TBL_NAME = "tbl_currency";
private final static String KEY_CODE = "code";
private final static String KEY_DESC = "description";
private final static String KEY_RATE = "rate";

private final static void createOrOpenDB(Context context) {
    SQLiteHelper dbHelper = new SQLiteHelper();
    TableObjectMaker tableObjs = dbHelper.new TableObjectMaker();
    tableObjs.addTable(TBL_NAME, new String[] {
             "_id integer primary key autoincrement",
             KEY_CODE + " text not null",
             KEY_DESC + " text not null",
             KEY_RATE + " real not null"
             });
    dbAdapter = dbHelper.new DatabaseAdapter(context);
    dbAdapter.open(tableObjs, "local_data", 1);
}
private final static void writeToDB(NodeList nodes) {
    if (nodes==null) return;
    List&lt;ContentValues&gt; content = SQLiteHelper.getContentValues(nodes,
            new String[] {KEY_CODE,KEY_DESC,KEY_RATE});
    for (ContentValues c:content) {
        dbAdapter.insertRowInTable(TBL_NAME, c);
    }
}
private final static void closeDB() {
    dbAdapter.close();
}
public static void updateDB(Context context) {
    Document xmlDocument = GZip.getResourceAsXML(XML_SOURCE,true);
    NodeList nodes = xmlDocument.getElementsByTagName("data");
    createOrOpenDB(context);
    writeToDB(nodes);
    closeDB();
    LAST_UPDATE = Calendar.getInstance().getTimeInMillis();
}
...
}  
</code></pre>

<p>The other class has identical database access/write methods as above, except with its own table name and field names, and it uses the same "local_data" name for the database name.
How can I get both classes to read and write to their own table in the same database?</p>

## Answers
### Answer ID: 8524946
<p>Move all access to the data base into a <a href="http://developer.android.com/guide/topics/providers/content-providers.html" rel="nofollow">ContentProvider</a>. Each class can then interact with the ContentProvider, which then interacts with the database.</p>

