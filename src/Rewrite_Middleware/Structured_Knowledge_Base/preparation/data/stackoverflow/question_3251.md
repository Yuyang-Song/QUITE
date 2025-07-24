# Query n to m SQlite database
[Link to question](https://stackoverflow.com/questions/73585339/query-n-to-m-sqlite-database)
**Creation Date:** 1662134772
**Score:** 0
**Tags:** database, sqlite, kotlin, entity, android-room
## Question Body
<p>I have n to m database (movie and cast). I need to get a list of cast associated with a movie.</p>
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
   val cast: Cast //Arraylist of casts
)
data class Cast(
   @Embedded
   var name: String,
   var profile_path: String?,
   var character: String
)
</code></pre>
<p>Crossreferenced class:</p>
<pre><code>@Entity(
    tableName = &quot;movie_cast&quot;,
    primaryKeys = [&quot;movieIdMap&quot;,&quot;castIdMap&quot;],
    foreignKeys = [
        ForeignKey(
            entity = MovieDbModel::class,
            parentColumns = [&quot;id&quot;],
            childColumns = [&quot;movieIdMap&quot;],
            onDelete = ForeignKey.CASCADE,
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
    var movieIdMap: Int,
    @ColumnInfo(index = true)
    var castIdMap: Int
)
</code></pre>
<p>Relation:</p>
<pre><code>data class MovieWithListOfCast(
    @Embedded /* The parent */
    var movie: MovieDbModel,
    @Relation(
        entity = CastDbModel::class, 
        parentColumn = &quot;id&quot;,
        entityColumn = &quot;id&quot;, 
        associateBy = Junction(
            value = MovieCastCrossRef::class, 
            parentColumn = &quot;castIdMap&quot;, 
            entityColumn = &quot;movieIdMap&quot; 
        )
    )
    var castList: List&lt;CastDbModel&gt;
)
</code></pre>
<p>The Query looks like this:</p>
<pre><code>    @Transaction
    @Query(&quot;select * FROM `cast` WHERE id = :id&quot;)
    fun getAllCastAssociatedWithMovie(id: Int): List&lt;MovieWithListOfCast&gt;
</code></pre>
<p>But I get the following warning:</p>
<p><em>The query returns some columns [cast] which are not used by MovieWithListOfCast. You can use @ColumnInfo annotation on the fields to specify the mapping. You can annotate the method with @RewriteQueriesToDropUnusedColumns to direct Room to rewrite your query to avoid fetching unused columns.
MovieWithListOfCast has some fields [poster_path, overview, title] which are not returned by the query. If they are not supposed to be read from the result, you can mark them with @Ignore annotation. You can suppress this warning by annotating the method with @SuppressWarnings(RoomWarnings.CURSOR_MISMATCH). Columns returned by the query: id, cast.</em></p>
<p>How do I query to get a list of Cast that contains name, profile_path, and character?</p>

## Answers
### Answer ID: 73588341
<p>I believe that you have concepts reversed.</p>
<p><strong>First</strong>,</p>
<p>the <code>@Embedded</code> is the parent thus the <strong>parentColumn</strong> should specify a column in the <code>@Embedded</code>, you have <code>parentColumn = &quot;castIdMap&quot;</code> when it should be <strong><code>parentColumn = &quot;movieIdMap&quot;</code></strong>  along with changing to use <strong><code>entityColumn = &quot;castIdMap&quot;</code></strong>.</p>
<ul>
<li>This would not necessarily be apparent at first but would likely lead to confusion (all depends upon the reversed id's)</li>
</ul>
<p><strong>Second</strong>,</p>
<p>the <strong>MovieWithListOfCast</strong> will get the list of cast for a movie, therefore it needs to get the movie from the <strong>movie table</strong> not the cast table.</p>
<p>So <strong>MovieWithListOfClass</strong> could be:-</p>
<pre><code>data class MovieWithListOfCast(
    @Embedded /* The parent */
    var movie: MovieDbModel,
    @Relation(
        entity = CastDbModel::class,
        parentColumn = &quot;id&quot;,
        entityColumn = &quot;id&quot;,
        associateBy = Junction(
            value = MovieCastCrossRef::class,
            parentColumn = &quot;movieIdMap&quot;,
            entityColumn = &quot;castIdMap&quot;
        )
    )
    var castList: List&lt;CastDbModel&gt;
)
</code></pre>
<p>Along with:-</p>
<pre><code>@Transaction
@Query(&quot;select * FROM `movie` WHERE id = :id&quot;)
fun getAllCastAssociatedWithMovie(id: Int): List&lt;MovieWithListOfCast&gt;
</code></pre>
<p>You could also have (just in case that is what you are thinking):-</p>
<pre><code>data class CastWithListOfMovies(
    @Embedded
    var castList: CastDbModel,
    @Relation(
        entity = MovieDbModel::class,
        parentColumn = &quot;id&quot;,
        entityColumn = &quot;id&quot;,
        associateBy = Junction(
            value = MovieCastCrossRef::class,
            parentColumn = &quot;castIdMap&quot;,
            entityColumn = &quot;movieIdMap&quot;
        )
    )
    var movieList: List&lt;MovieDbModel&gt;
)
</code></pre>
<p>Along with:-</p>
<pre><code>@Transaction
@Query(&quot;select * FROM `cast` WHERE id = :id&quot;)
fun getAllMoviesAssociatedWithCast(id: Int): List&lt;CastWithListOfMovies&gt;
</code></pre>
<p>Putting both into action using your code amended as above and with a suitable @Database annotated class then using:-</p>
<pre><code>class MainActivity : AppCompatActivity() {
    lateinit var db: TheDatabase
    lateinit var dao: AllDao
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        db = TheDatabase.getInstance(this)
        dao = db.getAllDao()

        val m1id = dao.insert(MovieDbModel(100,&quot;posetr001&quot;,&quot;Western&quot;,&quot;The Good, the Bad and the Ugly&quot;))
        val m2id = dao.insert(MovieDbModel(200,&quot;poster002&quot;,&quot;Sci-Fi&quot;,&quot;Star Wars&quot;))
        val m3id = dao.insert(MovieDbModel(300,&quot;poster003&quot;,&quot;Soppy&quot;,&quot;Gone with the Wind&quot;))

        val c1id = dao.insert(CastDbModel(1,Cast(&quot;Actor1&quot;,&quot;acts&quot;,&quot;an actor&quot;)))
        val c2id = dao.insert(CastDbModel(2,Cast(&quot;Actor2&quot;,&quot;acts&quot;,&quot;an actor&quot;)))
        val c3id = dao.insert(CastDbModel(3,Cast(&quot;Actor3&quot;,&quot;acts&quot;,&quot;an actor&quot;)))
        val c4id = dao.insert(CastDbModel(4,Cast(&quot;Actor4&quot;,&quot;acts&quot;,&quot;an actor&quot;)))
        val c5id = dao.insert(CastDbModel(5,Cast(&quot;Actor5&quot;,&quot;acts&quot;,&quot;an actor&quot;)))
        val c6id = dao.insert(CastDbModel(6,Cast(&quot;Actor6&quot;,&quot;acts&quot;,&quot;an actor&quot;)))
        val c7id = dao.insert(CastDbModel(7,Cast(&quot;Actor7&quot;,&quot;acts&quot;,&quot;an actor&quot;)))

        dao.insert(MovieCastCrossRef(m1id.toInt(),c1id.toInt()))
        dao.insert(MovieCastCrossRef(m1id.toInt(),c3id.toInt()))
        dao.insert(MovieCastCrossRef(m1id.toInt(),c5id.toInt()))
        dao.insert(MovieCastCrossRef(m1id.toInt(),c7id.toInt()))

        dao.insert(MovieCastCrossRef(m2id.toInt(),c2id.toInt()))
        dao.insert(MovieCastCrossRef(m2id.toInt(),c4id.toInt()))
        dao.insert(MovieCastCrossRef(m2id.toInt(),c6id.toInt()))

        dao.insert(MovieCastCrossRef(m3id.toInt(),c1id.toInt()))
        dao.insert(MovieCastCrossRef(m3id.toInt(),c2id.toInt()))
        dao.insert(MovieCastCrossRef(m3id.toInt(),c3id.toInt()))
        dao.insert(MovieCastCrossRef(m3id.toInt(),c4id.toInt()))
        dao.insert(MovieCastCrossRef(m3id.toInt(),c5id.toInt()))
        dao.insert(MovieCastCrossRef(m3id.toInt(),c6id.toInt()))
        dao.insert(MovieCastCrossRef(m3id.toInt(),c7id.toInt()))

        logCastWithMovie(c1id.toInt(),&quot;C1&quot;)
        logMovieWithCast(m1id.toInt(),&quot;M1&quot;)
        logCastWithMovie(c2id.toInt(),&quot;C2&quot;)
        logMovieWithCast(m2id.toInt(),&quot;M2&quot;)
        logCastWithMovie(c3id.toInt(),&quot;C3&quot;)
        logMovieWithCast(m3id.toInt(),&quot;M3&quot;)

    }

    fun logMovieWithCast(movieId: Int, tagSuffix: String) {
        var sb = StringBuilder()
        for (cawm in dao.getAllCastAssociatedWithMovie(movieId)) {
            for (c in cawm.castList) {
                sb.append(&quot;\n\t Name is ${c.cast.name} Profile is ${c.cast.profile_path} Character is ${c.cast.character}&quot;)
            }
            Log.d(&quot;DBINFO_CAWM_$tagSuffix&quot;,&quot;Movie is ${cawm.movie.title} cast are:$sb&quot;)
        }
    }
    fun logCastWithMovie(castId: Int, tagSuffix: String) {
        var sb = StringBuilder()
        for (mawc in dao.getAllMoviesAssociatedWithCast(castId)) {
            for (m in mawc.movieList) {
                sb.append(&quot;\n\tTitle is ${m.title} Overview is ${m.overview} Poster is ${m.poster_path}&quot;)
            }
            Log.d(&quot;DBINFO_MAWC_$tagSuffix&quot;,&quot;Cast is ${mawc.castList.cast.name} Movies are $sb&quot;)
        }
    }
}
</code></pre>
<p><strong>Result</strong>s in the log including:-</p>
<pre><code>2022-09-03 08:15:25.084 D/DBINFO_MAWC_C1: Cast is Actor1 Movies are 
        Title is The Good, the Bad and the Ugly Overview is Western Poster is posetr001
        Title is Gone with the Wind Overview is Soppy Poster is poster003
        
2022-09-03 08:15:25.095 D/DBINFO_CAWM_M1: Movie is The Good, the Bad and the Ugly cast are:
         Name is Actor1 Profile is acts Character is an actor
         Name is Actor3 Profile is acts Character is an actor
         Name is Actor5 Profile is acts Character is an actor
         Name is Actor7 Profile is acts Character is an actor
         
2022-09-03 08:15:25.102 D/DBINFO_MAWC_C2: Cast is Actor2 Movies are 
        Title is Star Wars Overview is Sci-Fi Poster is poster002
        Title is Gone with the Wind Overview is Soppy Poster is poster003
        
2022-09-03 08:15:25.109 D/DBINFO_CAWM_M2: Movie is Star Wars cast are:
         Name is Actor2 Profile is acts Character is an actor
         Name is Actor4 Profile is acts Character is an actor
         Name is Actor6 Profile is acts Character is an actor
         
2022-09-03 08:15:25.111 D/DBINFO_MAWC_C3: Cast is Actor3 Movies are 
        Title is The Good, the Bad and the Ugly Overview is Western Poster is posetr001
        Title is Gone with the Wind Overview is Soppy Poster is poster003
        
2022-09-03 08:15:25.117 D/DBINFO_CAWM_M3: Movie is Gone with the Wind cast are:
         Name is Actor1 Profile is acts Character is an actor
         Name is Actor2 Profile is acts Character is an actor
         Name is Actor3 Profile is acts Character is an actor
         Name is Actor4 Profile is acts Character is an actor
         Name is Actor5 Profile is acts Character is an actor
         Name is Actor6 Profile is acts Character is an actor
         Name is Actor7 Profile is acts Character is an actor
</code></pre>

