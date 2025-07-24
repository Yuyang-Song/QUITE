# copy database from assets to databases folder of a separate application
[Link to question](https://stackoverflow.com/questions/43670154/copy-database-from-assets-to-databases-folder-of-a-separate-application)
**Creation Date:** 1493340238
**Score:** 0
**Tags:** android, apk
## Question Body
<p>As I have seen other places I have gotten the bottom following two things to work. The application has a button that says copy and onClick it will move the .db file from the assets directory of the running apk to the databases directory of the file.</p>

<p>I would like to know though if its possible to take the DB file and copy it over to the databases directory of an application but not the application currently running? </p>

<p>Or to be more clear my question is can someone give me an example or show me how to edit my code below to place the copied .db in a different app directory than the one that is currently running at the time the db copy and move is being done?</p>

<pre><code>public class DatabaseHelper extends SQLiteOpenHelper{

//The Android's default system path of your application database.
private static String DB_PATH ="/data/data/com.rtt.bltc/databases/";
private static String DB_NAME = "ldeb.db";

private SQLiteDatabase myDataBase;
private final Context myContext;

/**
 * Constructor
 * Takes and keeps a reference of the passed context in order to access to the application assets and resources.
 * @param context
 */
public DatabaseHelper(Context context) {

    super(context, DB_NAME, null, 1);
    this.myContext = context;
    DB_PATH="/data/data/"+context.getPackageName()+"/"+"databases/";
    //DB_PATH="/data/data/com.rtt.bltc"+"/"+"databases/";
}
</code></pre>

<p>/**
     * Creates a empty database on the system and rewrites it with your own database.
     * */
    public void createDataBase() throws IOException{</p>

<pre><code>    boolean dbExist = checkDataBase();

    if(dbExist){
        //do nothing - database already exist
    }else{

        //By calling this method and empty database will be created into the default system path
           //of your application so we are gonna be able to overwrite that database with our database.
        this.getReadableDatabase();

        try {

            copyDataBase();

        } catch (IOException e) {

            throw new Error("Error copying database");

        }
    }

}

/**
 * Check if the database already exist to avoid re-copying the file each time you open the application.
 * @return true if it exists, false if it doesn't
 */
private boolean checkDataBase(){

    SQLiteDatabase checkDB = null;

    try{
        String myPath = DB_PATH + DB_NAME;
        checkDB = SQLiteDatabase.openDatabase(myPath, null, SQLiteDatabase.OPEN_READONLY);

    }catch(SQLiteException e){

        //database does't exist yet.

    }

    if(checkDB != null){

        checkDB.close();

    }

    return checkDB != null ? true : false;
}

/**
 * Copies your database from your local assets-folder to the just created empty database in the
 * system folder, from where it can be accessed and handled.
 * This is done by transfering bytestream.
 * */
private void copyDataBase() throws IOException{

    //Open your local db as the input stream
    InputStream myInput = myContext.getAssets().open(DB_NAME);

    // Path to the just created empty db
    String outFileName = DB_PATH + DB_NAME;

    //Open the empty db as the output stream
    OutputStream myOutput = new FileOutputStream(outFileName);

    //transfer bytes from the inputfile to the outputfile
    byte[] buffer = new byte[1024];
    int length;
    while ((length = myInput.read(buffer))&gt;0){
        myOutput.write(buffer, 0, length);
    }

    //Close the streams
    myOutput.flush();
    myOutput.close();
    myInput.close();

}

public void openDataBase() throws SQLException{

    //Open the database
    String myPath = DB_PATH + DB_NAME;
    myDataBase = SQLiteDatabase.openDatabase(myPath, null, SQLiteDatabase.OPEN_READONLY);

}

@Override
public synchronized void close() {

        if(myDataBase != null)
            myDataBase.close();

        super.close();

}



@Override
public void onCreate(SQLiteDatabase db) {

}

@Override
public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {

}
</code></pre>

<p>//return cursor
    public Cursor query(String table,String[] columns, String selection,String[] selectionArgs,String groupBy,String having,String orderBy){
        return myDataBase.query("profiles", null, null, null, null, null, null);</p>

<pre><code>}
</code></pre>

<p>}</p>

<p>I have included a copy of the CopyDb and the Helper class above and below.</p>

<pre><code>public class CopyDbActivity extends Activity {
/** Called when the activity is first created. */
Cursor c=null;
@Override
public void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.main);

    ((Button)findViewById(R.id.button01)).setOnClickListener(new View.OnClickListener(){
        @Override
        public void onClick(View v) {


             DatabaseHelper myDbHelper = new DatabaseHelper(CopyDbActivity.this);
             try {

                myDbHelper.createDataBase();

        } catch (IOException ioe) {

            throw new Error("Unable to create database");

        }

        try {

            myDbHelper.openDataBase();

        }catch(SQLException sqle){

            throw sqle;

        }
        Toast.makeText(CopyDbActivity.this, "Success", Toast.LENGTH_SHORT).show();



        c=myDbHelper.query("profiles", null, null, null, null,null, null);
        if(c.moveToFirst())
        {
            do {

                Toast.makeText(CopyDbActivity.this,
                        "_id" + c.getString(0) + "\n" +
                        "UUID" + c.getString(1) + "\n" +
                        "NAME" + c.getString(2) + "\n" +
                         Toast.LENGTH_LONG).show();
                         } while (c.moveToNext());
                 }
             }
    });        
    }
   }
</code></pre>

## Answers
### Answer ID: 43670174
<blockquote>
  <p>I would like to know though if its possible to take the DB file and copy it over to the databases directory of an application but not the application currently running? </p>
</blockquote>

<p>No. Your app does not have <em>read</em> access to another app's portion of internal storage, let alone write access.</p>

