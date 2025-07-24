# Android Room - Query Not Calling Expected Constructor
[Link to question](https://stackoverflow.com/questions/72598510/android-room-query-not-calling-expected-constructor)
**Creation Date:** 1655101484
**Score:** 0
**Tags:** android, kotlin, android-sqlite, android-room, dao
## Question Body
<p>I am rewriting my old Sqlite Android app that was in Java to be a Jetpack Compose app in Kotlin that uses a Room database.</p>
<p>I've got about half of the app done but now I am seeing a strange behavior where my DAO query is not returning the data it should be, and the cause seems to be because the correct constructor, defined in my data model class, is not being called.</p>
<p>I am pretty sure this constructor WAS being called back before, before I added a new table to the database. I'm not 100% on this but I think so.</p>
<p>Anyway, here's some relevant code:</p>
<p>Database:</p>
<p><a href="https://i.sstatic.net/9vi8L.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/9vi8L.png" alt="Database tables" /></a></p>
<p>Data Model (I've added an <code>@Ignore</code> property, <code>firearmImageUrl</code>, for this <code>imageFile</code> column from the <code>firearm_image</code> table so it's part of the <code>Firearm</code> object. Maybe not the best way to do this, for joining tables? But this is a small simple app that like 5 people worldwide might use, more likely just me):</p>
<pre><code>@Entity(tableName = &quot;firearm&quot;)
class Firearm {
    @ColumnInfo(name = &quot;_id&quot;)
    @PrimaryKey(autoGenerate = true)
    var id = 0

    var name: String = &quot;&quot;

    var notes: String? = null

    @Ignore
    var shotCount = 0

    @Ignore
    var firearmImageUrl: String = &quot;&quot;

    @Ignore
    constructor() {

    }

    @Ignore
    constructor(
        name: String,
        notes: String?
    ) {
        this.name = name
        this.notes = notes
    }

    @Ignore
    constructor(
        name: String,
        notes: String?,
        shotCount: Int
    ) {
        this.name = name
        this.notes = notes
        this.shotCount = shotCount
    }

    @Ignore
    constructor(
        id: Int,
        name: String,
        notes: String?,
        shotCount: Int
    ) {
        this.id = id
        this.name = name
        this.notes = notes
        this.shotCount = shotCount
    }

    // THIS IS THE CONSTRUCTOR THAT I **WANT** TO BE CALLED AND IS NOT. THIS USED TO HAVE AN 
    // @IGNORE TAG ON IT BUT REMOVING IT DID NOTHING
    constructor(
        id: Int,
        name: String,
        notes: String?,
        shotCount: Int,
        firearmImageUrl: String
    ) {
        this.id = id
        this.name = name
        this.notes = notes
        this.shotCount = shotCount
        this.firearmImageUrl = firearmImageUrl
    }

    // THIS IS THE CONSTRUCTOR THAT IS BEING CALLED BY THE BELOW DAO METHOD, EVEN THOUGH 
    // ITS PARAMETERS DO NOT MATCH WHAT'S BEING RETURNED BY THAT QUERY
    constructor(
        id: Int,
        name: String,
        notes: String?,
    ) {
        this.id = id
        this.name = name
        this.notes = notes
    }
}
</code></pre>
<p>DAO (I removed the <code>suspend</code> keyword just so this thing would hit a debug breakpoint; also this query absolutely works, I copy-pasted it into the Database Inspector and ran it against the db and it returns the proper data with <code>firearmImageUrl</code> populated with a path):</p>
<pre><code>@Query(
        &quot;SELECT f._id, &quot; +
                  &quot;f.name, &quot; +
                  &quot;f.notes, &quot; +
                  &quot;CASE WHEN SUM(s.roundsFired) IS NULL THEN 0 &quot; +
                  &quot;ELSE SUM(s.roundsFired) &quot; +
                  &quot;END shotCount, &quot; +
                  &quot;fi.imageFile firearmImageUrl &quot; +
              &quot;FROM firearm f &quot; +
              &quot;LEFT JOIN shot_track s ON f._id = s.firearmId &quot; +
              &quot;LEFT JOIN firearm_image fi ON f._id = fi.firearmId &quot; +
              &quot;WHERE f._id = :firearmId &quot; +
              &quot;GROUP BY f._id &quot; +
              &quot;ORDER BY f.name&quot;
    )
    fun getFirearm(firearmId: Int): Firearm?
</code></pre>
<p>Repo:</p>
<pre><code>override fun getFirearm(firearmId: Int): Firearm? {
        return dao.getFirearm(firearmId)
    }
</code></pre>
<p>Use Case (I'm dumb and decided to do this Clean Architecture but it's way overkill; this is just an intermediate class and calls the Repo method):</p>
<pre><code>data class FirearmUseCases(
    /**
     * Gets the valid Firearms in the application.
     */
    val getFirearms: GetFirearms,

    /**
     * Gets the specified Firearm.
     */
    val getFirearm: GetFirearm
)

class GetFirearm(private val repository: FirearmRepository) {
    operator fun invoke(firearmId: Int): Firearm? {
        return repository.getFirearm(firearmId)
    }
}
</code></pre>
<p>ViewModel:</p>
<pre><code>init {
        savedStateHandle.get&lt;Int&gt;(&quot;firearmId&quot;)?.let { firearmId -&gt;
            if (firearmId &gt; 0) {
                viewModelScope.launch {
                    firearmUseCases.getFirearm(firearmId)?.also { firearm -&gt;
                        _currentFirearmId.value = firearm.id

                        // and so on... point is, the object is retrieved in this block
                    }
                }
             }
        }
}
</code></pre>
<p>What's happening is the DAO is calling the constructor that I've commented above, and not the constructor that has the parameters that match what the query is returning. Not sure why. That constructor did have an <code>@Ignore</code> tag on it before tonight but I just tried removing it and there was no difference; constructor with only 3 parameters is still being called.</p>
<p>Thanks for any help, this Room stuff is nuts. I should've just stuck with Sqlite lmao. It's such a simple app, the old version was super fast and worked fine. Silly me wanting to learn contemporary design though.</p>

## Answers
### Answer ID: 72608615
<p>I believe that your issue is based upon shotCount being <code>@Ignore</code>d (which you obviously want). Thus, even though you have it in the output, Room ignores the column and thus doesn't use the constructor you wish.</p>
<p>I would suggest that the resolution is quite simple albeit perhaps a little weird and that is to have Firearm <strong>not annotated</strong> with <code>@Entity</code> and just a POJO (with no Room annotation) and then have a separate <code>@Entity</code> annotated class specifically for the table.</p>
<ul>
<li>You could obviously add constructors/functions, as/if required to the Firearm class to handle FirearmTable's</li>
</ul>
<p>e.g.</p>
<pre><code>@Entity(tableName = &quot;firearm&quot;)
data class FireArmTable(
    @ColumnInfo(name = BaseColumns._ID)
    @PrimaryKey
    var id: Long?=null,
    var name: String,
    var notes: String? = null
)
</code></pre>
<ul>
<li>using BaseColumns._ID would change the ID column name should it ever change.</li>
<li>using Long=null? without <code>autogenerate = true</code> will generate an id (if no value is supplied) but is more efficient see <a href="https://sqlite.org/autoinc.html" rel="nofollow noreferrer">https://sqlite.org/autoinc.html</a> (especially the very first sentence)</li>
<li>the above are just suggestions, they are not required</li>
</ul>
<p>and :-</p>
<pre><code>class Firearm() : Parcelable {
    @ColumnInfo(name = &quot;_id&quot;)
    @PrimaryKey(autoGenerate = true)
    var id = 0
    var name: String = &quot;&quot;
    var notes: String? = null
    //@Ignore
    var shotCount = 0
    //@Ignore
    var firearmImageUrl: String = &quot;&quot;

    ....
</code></pre>
<p>Using the above and using (tested with <code>.allowMainThreadQueries</code>) then the following:-</p>
<pre><code>    db = TheDatabase.getInstance(this)
    dao = db.getFirearmDao()

    val f1id = dao.insert(FireArmTable( name = &quot;F1&quot;, notes = &quot;Awesome&quot;))
    val f2id = dao.insert(FireArmTable(name = &quot;F2&quot;, notes = &quot;OK&quot;))
    dao.insert(Firearm_Image(firearmId = f1id, imageFile = &quot;F1IMAGE&quot;))
    dao.insert(Shot_track(firearmId = f1id, roundsFired = 10))
    dao.insert(Shot_track(firearmId = f1id, roundsFired = 20))
    dao.insert(Shot_track(firearmId = f1id, roundsFired = 30))
    dao.insert(Firearm_Image(firearmId = f2id, imageFile = &quot;F2IMAGE&quot;))
    dao.insert(Shot_track(firearmId = f2id, roundsFired = 5))
    dao.insert(Shot_track(firearmId = f2id, roundsFired = 15))

    logFirearm(dao.getFirearm(f1id.toInt()))

    val f1 = dao.getFirearm(f1id.toInt())
    val f2 = dao.getFirearm(f2id.toInt())
    logFirearm(f2)
}

fun logFirearm(firearm: Firearm?) {
    Log.d(&quot;FIREARMINFO&quot;,&quot;Firearm: ${firearm!!.name} Notes are: ${firearm.notes} ImageURL: ${firearm.firearmImageUrl} ShotCount: ${firearm.shotCount}&quot;)
}
</code></pre>
<p>Where getFirearm is your Query copied and pasted, shows the following in the log:-</p>
<pre><code>D/FIREARMINFO: Firearm: F1 Notes are: Awesome ImageURL: F1IMAGE ShotCount: 60
D/FIREARMINFO: Firearm: F2 Notes are: OK ImageURL: F2IMAGE ShotCount: 20
</code></pre>
<p>i.e. <strong>Shotcounts as expected</strong>.</p>

