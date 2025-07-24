# Room database rewrites values with the same id
[Link to question](https://stackoverflow.com/questions/73648947/room-database-rewrites-values-with-the-same-id)
**Creation Date:** 1662639288
**Score:** 0
**Tags:** android, sql, sqlite, android-room
## Question Body
<p>I work with the room database (many-to-many relationship). I try to save the list of cast into a table. But the database sees that I insert cast with the same id (movie id) and just rewrites the value. Any idea how to correct it?</p>
<p>I insert a list with the help of the following query:</p>
<pre><code>   @Insert(onConflict = OnConflictStrategy.REPLACE)
   suspend fun insertCast (cast: List &lt;CastDbModel&gt;)
</code></pre>
<p><a href="https://i.sstatic.net/702uy.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/702uy.png" alt="enter image description here" /></a></p>
<p>But when I try to get the data I get the last data that was inseted.</p>
<pre><code>   @Transaction
   @Query(&quot;select * FROM `cast` WHERE id = :id&quot;)
   fun getAllCastAssociatedWithMovie(id: Int): List&lt;CastDbModel&gt;
</code></pre>
<p><a href="https://i.sstatic.net/e5WdI.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/e5WdI.png" alt="enter image description here" /></a></p>
<pre><code>@Entity(tableName = &quot;movie&quot;)
data class MovieDbModel(
   @PrimaryKey(autoGenerate = false)
   val id: Int,
   val poster_path: String,
   val overview: String,
   val title: String)

@Entity(tableName = &quot;cast&quot;)
@TypeConverters(CastConverter::class)
data class CastDbModel(
   @PrimaryKey(autoGenerate = false)
   val id : Int,
   val cast: Cast
)

data class Cast(
   val name: String,
   val profile_path: String?,
   val character: String
)
data class MovieWithListOfCast(
   @Embedded /* The parent */
   val movie: CastDbModel,
   @Relation(
       entity = CastDbModel::class, /* The class of the related table(entity) (the children)*/
       parentColumn = &quot;id&quot;, /* The column in the @Embedded class (parent) that is referenced/mapped to */
       entityColumn = &quot;id&quot;, /* The column in the @Relation class (child) that is referenced (many-many) or references the parent (one(parent)-many(children)) */
       /* For the mapping table */
       associateBy = Junction(
           value = MovieCastCrossRef::class, /* The class of the mapping table */
           parentColumn = &quot;movieIdMap&quot;, /* the column in the mapping table that maps/references the parent (@Embedded) */
           entityColumn = &quot;castIdMap&quot; /* the column in the mapping table that maps/references the child (@Relation) */
       )
   )
   val castList: List&lt;CastDbModel&gt;
)

@Entity(
   tableName = &quot;movie_cast&quot;,
   primaryKeys = [&quot;movieIdMap&quot;,&quot;castIdMap&quot;],
   foreignKeys = [
       /* A MovieId MUST be a value of an existing id column in the movie table */
       ForeignKey(
           entity = MovieDbModel::class,
           parentColumns = [&quot;id&quot;],
           childColumns = [&quot;movieIdMap&quot;],
           /* Optional (helps maintain referential integrity) */
           /* if parent is deleted then children rows of that parent are deleted */
           onDelete = ForeignKey.CASCADE,
           /* if parent column is changed then the column that references the parent is changed to the same value */
           onUpdate = ForeignKey.CASCADE
       ),
       ForeignKey(
           entity = CastDbModel::class,
           parentColumns = [&quot;id&quot;],
           childColumns = [&quot;castIdMap&quot;],
           onDelete = ForeignKey.CASCADE,
           onUpdate = ForeignKey.CASCADE
       )
   ]
)
data class MovieCastCrossRef(
   val movieIdMap: Int,
   @ColumnInfo(index = true)
   val castIdMap: Int
)
</code></pre>

## Answers
### Answer ID: 73654601
<p>Each Cast MUST have a unique <strong>id</strong>, otherwise a conflict will happen. In your case, if the same id is used, due to the use of <code>OnConflictStrategy.REPLACE</code> the conflict results in the cast being replaced with the data as per the new Cast.</p>
<p>What you should be doing to insert a new Cast, is to insert the new Cast letting the <strong>id</strong> be generated (by specifying an id of null in the case of AutoGenerate=false), retrieving the generated id e.g. using <code>fun insertCast (cast: List &lt;CastDbModel&gt;): LongArray</code></p>
<p>However, with <code>val id: Int,</code> then you cannot specify null. So you should use var id: Int?=null (same for Movie).</p>
<p>Then when you want to add a Cast to a Movie, you insert a MovieCastCrossreference with the movieIdMap as the id from the respective Movie and with castIdMap as the id from the respective Cast.</p>
<p>With some minor changes to your code:-</p>
<pre><code>@Entity(tableName = &quot;movie&quot;)
data class MovieDbModel(
    @PrimaryKey(autoGenerate = false)
    var id: Int?=null, /*&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt; CHANGED to var and default value of null so id can be generated */
    val poster_path: String,
    val overview: String,
    val title: String)

@Entity(tableName = &quot;cast&quot;)
@TypeConverters(CastConverter::class)
data class CastDbModel(
    @PrimaryKey(autoGenerate = false)
    var id : Int?=null, /*&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt; CHANGED to var and default value of null so id can be generated */
    val cast: Cast
)
</code></pre>
<p>And with an @Dao annotated Interface :-</p>
<pre><code>@Dao
interface AllDao {

    @Insert(onConflict = OnConflictStrategy.IGNORE)
    fun insertMovie(movie: List&lt;MovieDbModel&gt;): LongArray
    @Insert(onConflict = OnConflictStrategy.IGNORE)
    fun insertCast (cast: List &lt;CastDbModel&gt;): LongArray
    @Insert(onConflict = OnConflictStrategy.IGNORE)
    fun insertMovieCastXrossRef(movieCastCrossRef: MovieCastCrossRef): Long

    @Transaction
    @Query(&quot;&quot;) /* Allows the function to have the @Transaction Applied */
    fun insertCastListForASingleMovie(movieId: Int, castList: List&lt;Int&gt;) {
        for (castId in castList) {
            insertMovieCastXrossRef(MovieCastCrossRef(movieId,castId))
        }
    }
}
</code></pre>
<ul>
<li>note how the Inserts return a value (LongArray for inserting a List, and just Long for a single insert)</li>
</ul>
<p>using an @Database annotated class (with .allowMainThredQueries for convenience and brevity) name <strong>TheDatabase</strong> and the following code in an activity:-</p>
<pre><code>class MainActivity : AppCompatActivity() {
    lateinit var db: TheDatabase
    lateinit var dao: AllDao
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        db = TheDatabase.getInstance(this)
        dao = db.getAllDao()


        /* Define some Movies */
        val movieList = listOf&lt;MovieDbModel&gt;(
            MovieDbModel(null,&quot;p1&quot;,&quot;blah1&quot;,&quot;M1&quot;), /* when run first odds on id will be 1 */
            MovieDbModel(null,&quot;p2&quot;,&quot;blah2&quot;,&quot;M2&quot;), /* id likely 2 */
            MovieDbModel(7654,&quot;p3&quot;,&quot;blah3&quot;,&quot;M3&quot;), /* id as given i.e 7654 */
            MovieDbModel(null,&quot;p4&quot;,&quot;blah4&quot;,&quot;M4&quot;), /* id likely 7655 */
            /* Will very likely NOT BE INSERTED as Movie with id 1 will likely exist */
            MovieDbModel(1,&quot;pOoops&quot;,&quot;blahOoops&quot;,&quot;MOoops&quot;)
        )
        /* Insert the Movies setting the movieId accordingly from the returned list of inserted id's
            noting that if an insert failed (was ignored i.e. returned id is -1) then a different Log message
         */
        var movieIndex = 0
        for (movieId in dao.insertMovie(movieList)) {
            if (movieId &gt; 0) {
                Log.d(&quot;MOVIEINSERT&quot;,&quot;Movie ${movieList[movieIndex].title} was inserted with an ID of $movieId&quot;)

            } else {
                Log.d(&quot;MOVIEINSERT&quot;,&quot;Movie ${movieList[movieIndex].title} insert FAILED due to CONFLICT&quot;)
            }
            movieList[movieIndex++].id = movieId.toInt()
        }

        /* Define some CastDBModels */
        val castList = listOf&lt;CastDbModel&gt;(
            CastDbModel(null,Cast(&quot;Fred&quot;,&quot;fredprofile&quot;,&quot;fred is fred&quot;)),
            CastDbModel(null,Cast(&quot;Mary&quot;,&quot;maryprofile&quot;,&quot;mary is mary&quot;)),
            CastDbModel(null, Cast(&quot;Anne&quot;,&quot;anneprofile&quot;,&quot;anne is anne&quot;)),
            CastDbModel(50124,Cast(&quot;Tom&quot;,&quot;tomprofile&quot;,&quot;tom is tom&quot;)),
            CastDbModel(null,Cast(&quot;Bert&quot;,&quot;bertprofile&quot;,&quot;bert is bert&quot;)),
            CastDbModel(null,Cast(&quot;Jane&quot;,&quot;janeprofile&quot;,&quot;jane is jane&quot;)),
            /* Will very likely NOT BE INSERTED as Movie with id 1 will likely exist */
            CastDbModel(1,Cast(&quot;Oooops&quot;,&quot;NOPROFILE&quot;,&quot;NOCHARACTER&quot;))
        )
        /* Similar to movies */
        val castIdList = dao.insertCast(castList)
        var castIndex = 0
        val castListToUse: ArrayList&lt;Int&gt; = ArrayList()
        for (castId in castIdList) {
            if (castId &gt; 0) {
                Log.d(&quot;CASTINSERT&quot;,&quot;Cast ${castList[castIndex].cast.name} was inserted with an ID of $castId&quot;)
                castList[castIndex].id = castId.toInt()
                castListToUse.add(castId.toInt())
            } else {
                Log.d(&quot;CASTINSERT&quot;,&quot;Cast ${castList[castIndex].cast.name} insert Failed&quot;)
            }
            castIndex++
        }
        /* Add all the inserted Casts to the 3rd Movie */
        dao.insertCastListForASingleMovie(movieList[3].id!!,castListToUse)
    }
}
</code></pre>
<p>The the Log Includes :-</p>
<pre><code>2022-09-09 11:21:52.778 D/MOVIEINSERT: Movie M1 was inserted with an ID of 1
2022-09-09 11:21:52.778 D/MOVIEINSERT: Movie M2 was inserted with an ID of 2
2022-09-09 11:21:52.778 D/MOVIEINSERT: Movie M3 was inserted with an ID of 7654
2022-09-09 11:21:52.778 D/MOVIEINSERT: Movie M4 was inserted with an ID of 7655
2022-09-09 11:21:52.778 D/MOVIEINSERT: Movie MOoops insert FAILED due to CONFLICT

2022-09-09 11:21:52.832 D/CASTINSERT: Cast Fred was inserted with an ID of 1
2022-09-09 11:21:52.833 D/CASTINSERT: Cast Mary was inserted with an ID of 2
2022-09-09 11:21:52.833 D/CASTINSERT: Cast Anne was inserted with an ID of 3
2022-09-09 11:21:52.833 D/CASTINSERT: Cast Tom was inserted with an ID of 50124
2022-09-09 11:21:52.833 D/CASTINSERT: Cast Bert was inserted with an ID of 50125
2022-09-09 11:21:52.833 D/CASTINSERT: Cast Jane was inserted with an ID of 50126
2022-09-09 11:21:52.833 D/CASTINSERT: Cast Oooops insert Failed
</code></pre>
<ul>
<li>This demonstrates that you can insert with a specific id *<em>IF THE SPECIFIC IS IS UNIQUE</em> or with a generated id (AutoGenerate does not in fact force/stop auto generation, it just alters how to get generated id's).</li>
</ul>
<p>To demonstrate the bonus insert an entire CastList to be related to a single Movie. The <strong>movie_cast</strong> table ends up being :-</p>
<p><a href="https://i.sstatic.net/64u7s.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/64u7s.png" alt="enter image description here" /></a></p>
<ul>
<li>i.e. the 4TH (index 3) movie's id is 7655 so movieIdMap is the same for all rows</li>
<li>and each castIdMap reflects the castId.</li>
</ul>

