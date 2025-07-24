# Use prepopulated SQLite database in android while using exisntent android API
[Link to question](https://stackoverflow.com/questions/19704383/use-prepopulated-sqlite-database-in-android-while-using-exisntent-android-api)
**Creation Date:** 1383216368
**Score:** -2
**Tags:** android, database, sqlite
## Question Body
<p>I wan't to use database file, that I've created on my computer.</p>

<p>While <a href="http://www.reigndesign.com/blog/using-your-own-sqlite-database-in-android-applications/" rel="nofollow">this</a> is working, I'm considering that as a bad workaround, as it's not using existent API, while creating its own api.</p>

<p>I want to be able to use getWritableDataBase(), onCreate(SQLiteDatabase db) and onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) methods.</p>

<p>So, that's what I did and it's not working for some reason. I thought that if I would rewrite existent database it would work, but when querying I'm getting table not exists exception.</p>

<pre><code>public void onCreate(SQLiteDatabase db) {
    File f = new File(db.getPath());
    try {
        InputStream is = context.getResources().getAssets().open("words1.db");
        int size = is.available();
        byte[] buffer = new byte[size];
        is.read(buffer);
        is.close();
        FileOutputStream fos = new FileOutputStream(f);
        fos.write(buffer);
        fos.close();
    } catch (IOException e) {
        // TODO Auto-generated catch block
        e.printStackTrace();
    }   
}
</code></pre>

<p>So how could I use prepopulated database, while using existent api?</p>

## Answers
### Answer ID: 19705965
<p>The easiest way to pre-package a database with your application is to use <a href="https://github.com/jgilfelt/android-sqlite-asset-helper" rel="nofollow">Jeff Gilfelt's <code>SQLiteAssetHelper</code></a>. While it does require you to add a small JAR to your project, his code is tested and debugged, and it requires very little additional code on your part.</p>

<p><a href="https://github.com/commonsguy/cw-omnibus/tree/master/Database/ConstantsAssets" rel="nofollow">Here is a sample project</a> demonstrating the use of <code>SQLiteAssetHelper</code>.</p>

