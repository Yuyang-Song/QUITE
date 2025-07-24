# Laravel Query builder - select top 1 row from another table
[Link to question](https://stackoverflow.com/questions/57987665/laravel-query-builder-select-top-1-row-from-another-table)
**Creation Date:** 1568793123
**Score:** 2
**Tags:** mysql, laravel, laravel-query-builder
## Question Body
<p>I have this SQL query for MySQL which works fine. But I need to rewrite it using query builder and need to avoid <code>DB::raw()</code> completely because development database is different from production. I know far from ideal, but unfortunately it is what it is.</p>

<pre><code>SELECT athletes.*, 
     (
         SELECT performance
         FROM performances
         WHERE athletes.id = performances.athlete_id AND performances.event_id = 1
         ORDER BY performance DESC
         LIMIT 0,1
     ) AS personal_best
FROM athletes
ORDER BY personal_best DESC
Limit 0, 100
</code></pre>

<p>And I'm struggling how to rewrite the <code>personal_best</code> part. I have table of performances for athletes and I need to select only the best performance for each athletes as his personal best.</p>

<p>I was trying to search for answer but all of the answers I found included raw adding raw SQL.</p>

<p>Any ideas or hint would be much appreciated.</p>

<p>Thank you in advance!</p>

<p>So I accepted I might have to use Eloquent for this, but still having trouble to progress. Heres my code:</p>

<pre><code>class Athlete extends Model
{
    /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = 'athletes';

    /**
     * The primary key associated with the table.
     *
     * @var string
     */
    protected $primaryKey = 'id';

    /**
     * Indicates if the model should be timestamped.
     *
     * @var bool
     */
    public $timestamps = false;

    /**
     * Get the performances for the Athelete post.
     *
     * @return HasMany
     */
    public function performances()
    {
        return $this-&gt;hasMany('App\EloquentModels\Performance', 'athlete_id');
    }
}

class Performance extends Model
{
    /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = 'performances';

    /**
     * The primary key associated with the table.
     *
     * @var string
     */
    protected $primaryKey = 'id';

    /**
     * Indicates if the model should be timestamped.
     *
     * @var bool
     */
    public $timestamps = false;
}
</code></pre>

## Answers
### Answer ID: 57987952
<p>Create a new connection at <code>database.php</code> like mysql_dev for development parameters.</p>

<pre><code>DB::connection('mysql_dev')-&gt;table('athletes')
    -&gt;leftJoin('performances','athletes.id','performances.athlete_id')
    -&gt;where('performances.event_id',1)
    -&gt;groupBy('athletes.id')
    -&gt;orderByDesc('personal_best')
    -&gt;select('athletes.*',DB::raw('MAX(performances.performance) AS personal_best')
    -&gt;paginate(100);

</code></pre>

<p>try like this without raw,</p>

<pre><code>DB::connection('mysql_dev')-&gt;table('athletes')
    -&gt;leftJoin('performances','athletes.id','performances.athlete_id')
    -&gt;where('performances.event_id',1)
    -&gt;groupBy('athletes.id')
    -&gt;orderByDesc('performances.performance')
    -&gt;select('athletes.*','performances.performance'
    -&gt;paginate(100);

</code></pre>

### Answer ID: 57987807
<p>If you are using raw SQL just do <code>MAX</code> for performance for each athlete using <code>GROUP BY</code>.</p>

<pre><code>SELECT athletes.*, MAX(performance) AS personal_best
FROM athletes
INNER JOIN performances ON athletes.id = performances.athlete_id AND performances.event_id = 1
GROUP BY athletes.id
ORDER BY personal_best DESC
LIMIT 0, 100
</code></pre>

<p>Laravel Query Builder:</p>

<pre><code>DB::table('athletes')
    -&gt;join('performances', 'athletes.id', '=', 'performances.athlete_id')
    -&gt;where('performances.event_id', '=', 1)
    -&gt;groupBy('athletes.id')
    -&gt;orderBy('personal_best', 'desc')
    -&gt;select('athletes.*',DB::raw('MAX(performance) AS personal_best')
    -&gt;limit(100);
</code></pre>

<p><a href="https://laravel.com/docs/6.x/queries#aggregates" rel="nofollow noreferrer">Doc</a> says that we can do <code>max(personal_best)</code> but not sure how to use it with group by.</p>

<p>I'm afraid you can't avoid <code>DB::raw</code> in Query Builder but you can use <code>eloquent model</code> for the same, as answered by <code>Shaielndra Gupta</code>.</p>

<p>For that you can create model and relationship.</p>

<pre><code>1. Create Model:
php artisan make:model Athelete
php artisan make:model Performance

2. Create relationship between Athelete and Perforamnce.

Update Athelete.php 

    /**
     * Get the performances for the Athelete post.
     */
    public function performances()
    {
        return $this-&gt;hasMany('App\Performance');
    }

3. Get data(didn't verify by myself)
$data = Athelete::with('performances',function ($query) use ($eventId){
    $query-&gt;max('performance')
    $query-&gt;where('event_id',$eventId)
    $query-&gt;orderBy('performance');
})-&gt;get();
</code></pre>

<p>Reference: </p>

<ul>
<li><a href="https://laravel.com/docs/5.1/eloquent#defining-models" rel="nofollow noreferrer">Laravel Model</a></li>
<li><a href="https://laravel.com/docs/5.7/eloquent-relationships" rel="nofollow noreferrer">Laravel Relationship</a></li>
</ul>

### Answer ID: 57988145
<p>you can user Eloquent ORM like this</p>

<pre><code>$data = Athelete::with('performances',function ($query) use ($eventId){
    $query-&gt;max('performance')
    $query-&gt;where('event_id',$eventId)
    $query-&gt;orderBy('performance');
})-&gt;get()
</code></pre>

### Answer ID: 57987809
<p>You can use like below.</p>

<pre><code>$sql1 = "(
         SELECT performance
         FROM performances
         WHERE athletes.id = performances.athlete_id AND performances.event_id = 1
         ORDER BY performance DESC
         LIMIT 0,1
     ) AS personal_best";

$sql2 = "SELECT athletes.*,$sql1          
FROM athletes
ORDER BY personal_best DESC
Limit 0, 100";

$result = DB::select($sql2);
</code></pre>

