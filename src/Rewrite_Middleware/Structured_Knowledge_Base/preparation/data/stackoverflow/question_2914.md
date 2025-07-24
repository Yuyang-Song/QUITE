# Room migration that only adds a @NonNull annotation to primary key on several tables
[Link to question](https://stackoverflow.com/questions/58344847/room-migration-that-only-adds-a-nonnull-annotation-to-primary-key-on-several-ta)
**Creation Date:** 1570809604
**Score:** 0
**Tags:** java, android, sqlite, database-migration, android-room
## Question Body
<p>I am upgrading an app from targeting <strong>sdk 25</strong> to targeting <strong>sdk 29</strong>, all the tables in my room database have a @PrimaryKey annotation but were not annotated with @NonNull. Now that I am targeting sdk 29, room is requiring the @NonNull annotation, unfortunately that causes my app to crash on startup unless I do a fresh install. </p>

<p><strong>Error it causes without fresh install</strong>: </p>

<pre><code>java.lang.RuntimeException: An error occurred while executing doInBackground()
    at android.os.AsyncTask$3.done(AsyncTask.java:318)
    at java.util.concurrent.FutureTask.finishCompletion(FutureTask.java:354)
    at java.util.concurrent.FutureTask.setException(FutureTask.java:223)
    at java.util.concurrent.FutureTask.run(FutureTask.java:242)
    at android.os.AsyncTask$SerialExecutor$1.run(AsyncTask.java:243)
    at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1133)
    at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:607)
    at java.lang.Thread.run(Thread.java:761)
 Caused by: java.lang.IllegalStateException: attempt to re-open an already-closed object: SQLiteDatabase:
</code></pre>

<p>I figured that was because my database had to be migrated because it works on a fresh install.</p>

<p>So far I have found some helpful stack overflow answers such as this <a href="https://stackoverflow.com/questions/805363/how-do-i-rename-a-column-in-a-sqlite-database-table#805508">one</a>.</p>

<p>But that would require me to rewrite every table in my database and making sure I bring all the indices over as well. I do not want to have to do this as I am sure I will miss something and it will create multiple bugs.</p>

<p>Is there a simpler way to do a room migration where I just add the @NonNull annotation to all my primary keys?</p>

<p>Alternatively I have seen mention of grabbing the schema from the SQLite tables that would encapsulate all the indices into a query, but I do not know how to get that schema in my migration.</p>

<p><strong>Example class after I have added NonNull tag:</strong></p>

<pre><code>@Entity(tableName = "FavoriteTrip"
    , indices = { @Index("tripPlanId") }
    , foreignKeys = @ForeignKey(entity = TripPlan.class, parentColumns = "id", childColumns = "tripPlanId"))
public class FavoriteTrip {

    @PrimaryKey @NonNull
    private String id = UUID.randomUUID().toString();
</code></pre>

## Answers
### Answer ID: 58351181
<blockquote>
  <p>Is there a simpler way to do a room migration where I just add the @NonNull annotation to all my primary keys?</p>
</blockquote>

<p>I believe that there is but haven't actually played with it that much <em>(just a quick foray and found that you are still left with creating the Entities to correctly match the tables)</em>. That is to let ROOM convert the database (you might have to delete the <strong>room_master_table</strong>) and that is to use one of the recently added <strong>createFrom</strong> methods.</p>

<ul>
<li><a href="https://developer.android.com/reference/androidx/room/RoomDatabase.Builder#createFromAsset(java.lang.String)" rel="nofollow noreferrer">createFromAsset</a>
-<a href="https://developer.android.com/reference/androidx/room/RoomDatabase.Builder#createFromFile(java.io.File)" rel="nofollow noreferrer">createFromFile</a></li>
</ul>

<p>These will convert the database to one that is acceptable to room BUT as far as I am aware it does not create the Entities, which I've seen has presented quite a few headaches due to the expected .......... found ....... being quite difficult to read.</p>

<p>Another option is something that I've been playing with which converts databases and additionally generates basic Entitity/Dao and Database code (Java). This tool can be found at <a href="https://www.codeproject.com/Articles/5245967/RoomExistingSQLiteDBConverter" rel="nofollow noreferrer">RoomExistingSQLiteDBConverter</a> which has links the source on github.</p>

<ul>
<li>As a very quick overview, </li>
</ul>

<p>:-</p>

<ol>
<li><p>you run the App (probably in an AS emulator, although could be on a real device). </p></li>
<li><p>Copy the database into any (bar 1 reserved folder) folder in public external storage (before or when the App is running, if the latter then click refresh button).</p></li>
<li>Have a look at the various listed components for potential highlighted issues.</li>
<li>When happy click the Convert button.</li>
<li>Copy the database ready for it to be imported (typically as an asset in to the assets folder) to the App being developed/changed.</li>
<li>Copy the code into the appropriate folders in the App.</li>
<li>Edit the code to bring in the appropriate imports.</li>
<li>Write code to copy the database from the assets folder.</li>
<li>Test.</li>
</ol>

