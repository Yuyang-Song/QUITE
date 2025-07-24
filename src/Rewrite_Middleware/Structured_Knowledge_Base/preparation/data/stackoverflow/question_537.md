# How does one check if a table exists in an Android SQLite database?
[Link to question](https://stackoverflow.com/questions/3058909/how-does-one-check-if-a-table-exists-in-an-android-sqlite-database)
**Creation Date:** 1276749606
**Score:** 95
**Tags:** android, database, sqlite
## Question Body
<p>I have an android app that needs to check if there's already a record in the database, and if not, process some things and eventually insert it, and simply read the data from the database if the data does exist. I'm using a subclass of SQLiteOpenHelper to create and get a rewritable instance of SQLiteDatabase, which I thought automatically took care of creating the table if it didn't already exist (since the code to do that is in the onCreate(...) method). </p>

<p>However, when the table does NOT yet exist, and the first method ran upon the SQLiteDatabase object I have is a call to query(...), my logcat shows an error of "I/Database(26434): sqlite returned: error code = 1, msg = no such table: appdata", and sure enough, the appdata table isn't being created.</p>

<p>Any ideas on why? </p>

<p>I'm looking for either a method to test if the table exists (because if it doesn't, the data's certainly not in it, and I don't need to read it until I write to it, which seems to create the table properly), or a way to make sure that it gets created, and is just empty, in time for that first call to query(...)</p>

<p><strong>EDIT</strong>
<br/>
This was posted after the two answers below:
<br/>
I think I may have found the problem. I for some reason decided that a different SQLiteOpenHelper was supposed to be created for each table, even though both access the same database file. I think refactoring that code to only use one OpenHelper, and creating both tables inside it's onCreate may work better...</p>

## Answers
### Answer ID: 65718941
<p>Kotlin solution, based on what others wrote here:</p>
<pre><code>    fun isTableExists(database: SQLiteDatabase, tableName: String): Boolean {
        database.rawQuery(&quot;select DISTINCT tbl_name from sqlite_master where tbl_name = '$tableName'&quot;, null)?.use {
            return it.count &gt; 0
        } ?: return false
    }
</code></pre>

### Answer ID: 58736854
<p>i faced that and deal with it by try catch as simple as that i do what i want in table if it not exist will cause error so catch it by exceptions and create it :) </p>

<pre><code>SQLiteDatabase db=this.getWritableDatabase();
        try{
            db.execSQL("INSERT INTO o_vacations SELECT * FROM vacations");
            db.execSQL("DELETE FROM vacations");
        }catch (SQLiteException e){
            db.execSQL("create table o_vacations (id integer primary key ,name text ,vacation text,date text,MONTH text)");
            db.execSQL("INSERT INTO o_vacations SELECT * FROM vacations");
            db.execSQL("DELETE FROM vacations");
        }

</code></pre>

### Answer ID: 7863401
<p>Try this one:</p>

<pre><code>public boolean isTableExists(String tableName, boolean openDb) {
    if(openDb) {
        if(mDatabase == null || !mDatabase.isOpen()) {
            mDatabase = getReadableDatabase();
        }

        if(!mDatabase.isReadOnly()) {
            mDatabase.close();
            mDatabase = getReadableDatabase();
        }
    }

    String query = "select DISTINCT tbl_name from sqlite_master where tbl_name = '"+tableName+"'";
    try (Cursor cursor = mDatabase.rawQuery(query, null)) {
        if(cursor!=null) {
            if(cursor.getCount()&gt;0) {
                return true;
            }
        }
        return false;
    }
}
</code></pre>

### Answer ID: 57668727
<p><strong><em>Important</em></strong> condition is <strong>IF NOT EXISTS</strong> to check table is already exist or not in database</p>

<p>like...</p>

<pre><code>String query = "CREATE TABLE IF NOT EXISTS " + TABLE_PLAYER_PHOTO + "("
            + KEY_PLAYER_ID + " TEXT,"
            + KEY_PLAYER_IMAGE + " TEXT)";
db.execSQL(query);
</code></pre>

### Answer ID: 11966655
<p>Although there are already a lot of good answers to this question, I came up with another solution that I think is more simple. Surround your query with a try block and the following catch:</p>

<pre><code>catch (SQLiteException e){
    if (e.getMessage().contains("no such table")){
            Log.e(TAG, "Creating table " + TABLE_NAME + "because it doesn't exist!" );
            // create table
            // re-run query, etc.
    }
}
</code></pre>

<p>It worked for me!</p>

### Answer ID: 7332125
<p><code>no such table exists: error</code> is coming because once you create database with one table after that whenever you create table in same database it gives this error.</p>

<p>To solve this error you must have to  create new database and inside the  onCreate() method you can create multiple table in same database.</p>

### Answer ID: 39304365
<pre><code> public boolean isTableExists(String tableName) {
    boolean isExist = false;
    Cursor cursor = db.rawQuery("select DISTINCT tbl_name from sqlite_master where tbl_name = '" + tableName + "'", null);
    if (cursor != null) {
        if (cursor.getCount() &gt; 0) {
            isExist = true;
        }
        cursor.close();
    }
    return isExist;
}
</code></pre>

### Answer ID: 31358047
<pre><code> // @param db, readable database from SQLiteOpenHelper

 public boolean doesTableExist(SQLiteDatabase db, String tableName) {
        Cursor cursor = db.rawQuery("select DISTINCT tbl_name from sqlite_master where tbl_name = '" + tableName + "'", null);

    if (cursor != null) {
        if (cursor.getCount() &gt; 0) {
            cursor.close();
            return true;
        }
        cursor.close();
    }
    return false;
}
</code></pre>

<ul>
<li>sqlite maintains sqlite_master table containing information of all tables and indexes in database.</li>
<li>So here we are simply running SELECT command on it, we'll get cursor having count 1 if table exists.</li>
</ul>

### Answer ID: 15298688
<p>.....
Toast t = Toast.makeText(context, "try... "  , Toast.LENGTH_SHORT);
        t.show();</p>

<pre><code>    Cursor callInitCheck = db.rawQuery("select count(*) from call", null);

    Toast t2a = Toast.makeText(context, "count rows " + callInitCheck.getCount() , Toast.LENGTH_SHORT);
    t2a.show();

    callInitCheck.moveToNext();
    if( Integer.parseInt( callInitCheck.getString(0)) == 0) // if no rows then do
    {
        // if empty then insert into call
</code></pre>

<p>.....</p>

### Answer ID: 7505197
<p>This is what I did:</p>



<pre class="lang-java prettyprint-override"><code>/* open database, if doesn't exist, create it */
SQLiteDatabase mDatabase = openOrCreateDatabase("exampleDb.db", SQLiteDatabase.CREATE_IF_NECESSARY,null);

Cursor c = null;
boolean tableExists = false;
/* get cursor on it */
try
{
    c = mDatabase.query("tbl_example", null,
        null, null, null, null, null);
        tableExists = true;
}
catch (Exception e) {
    /* fail */
    Log.d(TAG, tblNameIn+" doesn't exist :(((");
}

return tableExists;
</code></pre>

### Answer ID: 3064342
<p>Yep, turns out the theory in my edit was right: the problem that was causing the onCreate method not to run, was the fact that <code>SQLiteOpenHelper</code> objects should refer to databases, and not have a separate one for each table. Packing both tables into one <code>SQLiteOpenHelper</code> solved the problem.</p>

### Answer ID: 3059112
<p>You mentioned that you've created an class that extends <code>SQLiteOpenHelper</code> and implemented the <code>onCreate</code> method. Are you making sure that you're performing all your database acquire calls with that class? You should only be getting <code>SQLiteDatabase</code> objects via the <code>SQLiteOpenHelper#getWritableDatabase</code> and <code>getReadableDatabase</code> otherwise the <code>onCreate</code> method will not be called when necessary. If you are doing that already check and see if th <code>SQLiteOpenHelper#onUpgrade</code> method is being called instead. If so, then the database version number was changed at some point in time but the table was never created properly when that happened. </p>

<p>As an aside, you can force the recreation of the database by making sure all connections to it are closed and calling <code>Context#deleteDatabase</code> and then using the <code>SQLiteOpenHelper</code> to give you a new db object.</p>

### Answer ID: 3058934
<p>I know nothing about the Android SQLite API, but if you're able to talk to it in SQL directly, you can do this:</p>

<pre><code>create table if not exists mytable (col1 type, col2 type);
</code></pre>

<p>Which will ensure that the table is always created and not throw any errors if it already existed.</p>

