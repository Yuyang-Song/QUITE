# Laravel nested whereIn from multiple tables
[Link to question](https://stackoverflow.com/questions/55372635/laravel-nested-wherein-from-multiple-tables)
**Creation Date:** 1553675014
**Score:** 0
**Tags:** laravel, subquery
## Question Body
<p>I'm using Laravel 5.7. How do i rewrite below code as a single nested query?</p>

<p>I'm currently fetching the result using 2 database queries. I go through some of the answers in stackoverflow, but i still have doubts in nesting multiple tables</p>

<pre><code>  $connectedParts = DB::table('part_connections as c')
          -&gt;join('parts_master as p', 'p.id', '=', 'c.part_number_id')
          -&gt;where('c.part_number_id', $partId)
          -&gt;where('p.id', $partId)
          -&gt;pluck('connected_to');

  $connectedComponents = DB::table('part_connections as pc')
                            -&gt;join('parts_master as pm', 'pm.id', '=', 'pc.connected_to')
                            -&gt;where('part_number_id',$partId)
                            -&gt;where('pm.part_type','1')
                            -&gt;whereIn('connected_to', $connectedParts)
                            -&gt;pluck('connected_to');
</code></pre>

<p>Any help would be greatly appreciated.</p>

## Answers
### Answer ID: 55374662
<p>Set your relationship properly in your model first then try this query:</p>

<pre><code>//PartConnection model - add for eager loading
public function master() {
    return $this-&gt;belongsTo('PartMaster::class', 'connected_to', 'id');
}

$query = PartConnection::whereHas(‘master’, function($qry)) use ($partId) {
    $qry-&gt;where(‘parts_master.id’, $partId);
    $qry-&gt;where(‘parts_master.part_type’, 1);
});

$query-&gt;where(‘part_number_id’, $partId);

$connectedComponents = $query-&gt;get();
</code></pre>

<h1>update</h1>

<p>Try this then:</p>

<pre><code>$connectedComponents = DB::table('part_connections as pc')
                        -&gt;join('parts_master as pm', function($join) {
                            $join-&gt;on('pc.connected_to', '=', 'pm.id');
                            $join-&gt;on('pc.part_number_id', '=', 'pm.id');
                        }) //updated this - removed ;
                        -&gt;where('part_number_id',$partId)
                        -&gt;where('pm.part_type','1')
                        -&gt;get();
</code></pre>

