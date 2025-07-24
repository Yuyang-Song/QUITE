# Matching rows by date on a Laravel 9 application using php-carbon objects
[Link to question](https://stackoverflow.com/questions/75364284/matching-rows-by-date-on-a-laravel-9-application-using-php-carbon-objects)
**Creation Date:** 1675702399
**Score:** 1
**Tags:** php, laravel-9, php-carbon
## Question Body
<h3>The background</h3>
<p>I am building a Laravel application and I have an upsert method on a Booking Controller for updating/inserting bookings.
On upsert.blade.php I want to display a <code>&lt;select&gt;</code> element with a list of days into which a booking can be moved (or inserted).</p>
<p>There is a 'holidays' table with only one column: 'day' (of type datetime, precision 6). Each entry on this table means the system will be on holidays for that day, so bookings cannot be made or transfered into days that appear on this table.</p>
<p>Now, I want the <code>&lt;option&gt;</code>s in the above mentioned <code>&lt;select&gt;</code> to be disabled when they correspond to a holiday.</p>
<h3>What I tried:</h3>
<p>The view (upsert.blade.php)</p>
<pre class="lang-php prettyprint-override"><code>  &lt;select&gt;
    &lt;option value=&quot;&quot; disabled selected&gt;Select&lt;/option&gt;

    @foreach($days as $day)

    &lt;option value=&quot;{{ $day['value'] }}&quot; @disabled($day['disabled'])&gt;
      {{ $day['display'] }}
    &lt;/option&gt;

    @endforeach
  &lt;/select&gt;
</code></pre>
<p>The controller action:</p>
<pre class="lang-php prettyprint-override"><code>public function upsert()
    {
        $now = Carbon::now();
        $last = Carbon::now()-&gt;addDays(30);
        $holidays = DB::table('holidays');

        $days = [];

        // Populate $days with dates from $now until $last
        while($now-&gt;lte($last))
        {
            array_push($days, [
                'value' =&gt; $now-&gt;toDateString(),
                'display' =&gt; $now-&gt;format('l j F Y'),
                /* 
                 * Mark day as disabled if holidays matching current
                 * day is greater than 1 
                 * DOESN'T WORK
                 */
                'disabled' =&gt; $holidays-&gt;whereDate('day', $now)-&gt;count()
            ]);
            $now-&gt;addDay();
        }

        return view('upsert', [
            'days' =&gt; $days,
        ]);
    }
</code></pre>
<h3>The problem</h3>
<p>The line labelled 'DOESN'T WORK' doesn't work as expected (I expect the query to return 1 if there is a holiday for the current day in the loop, thus marking the day as disabled). It only matches the first day of the loop if it's a holliday, but it <strong>won't match any other days</strong>.</p>
<p>Note: I have cast the 'day' property of the Holiday model to 'datetime' so Laravel casts the value to a Carbon object when accessing it.</p>
<h4>Attempts to solve it</h4>
<p>I tried replacing</p>
<pre class="lang-php prettyprint-override"><code>$holidays = DB::table('holidays');
</code></pre>
<p>with</p>
<pre class="lang-php prettyprint-override"><code>$holidays = Holiday::all();
</code></pre>
<p>but that throws the following exception</p>
<pre><code>Method Illuminate\Database\Eloquent\Collection::whereDate does not exist.
</code></pre>
<p>So I tried rewriting the query to (note <code>whereDate</code> was replaced by <code>where</code>):</p>
<pre class="lang-php prettyprint-override"><code>'disabled' =&gt; $holidays-&gt;where('day', $now-&gt;toDateString().' 00:00:00.000000')-&gt;count()
</code></pre>
<p>But this would never match</p>
<h3>The solution</h3>
<p>After around 6 hours of fiddling about with this line, reading Laravel documentation and talking to ChatGPT, I couldn't come up with an answert to why this is happening so I replaced the problematic line with</p>
<pre class="lang-php prettyprint-override"><code>'disabled' =&gt; Holiday::whereDate('day', $now)-&gt;count()
</code></pre>
<p>Which does the job but I think is terrible for performance due to so many (in my opinion unecessary) round trips to the database.</p>
<h3>The question</h3>
<p>Could anyone shed some light on this?
Although I've found a solution, I don't think it would scale and I also didn't learn a thing from the experience, I still have no idea why the first query is only matching the first day and no other days. Or why the second one using <code>where()</code> doesn't match <strong>any</strong> days at all when it is comparing strings and I am using the exact format the strings are stored in on the database.</p>
<p>Or maybe the problem is not on the query, but on the Carbon object?</p>
<p>If you want to reproduce it, follow steps on this gist:
<a href="https://gist.github.com/alvarezrrj/50cd3669914f52ce8a6188771fdeafcd" rel="nofollow noreferrer">https://gist.github.com/alvarezrrj/50cd3669914f52ce8a6188771fdeafcd</a></p>

## Answers
### Answer ID: 75366738
<p><code>DB::table('holidays')</code> instantiates an <code>Illuminate\Database\Query\Builder</code> object. The <code>where</code> method modifies that object in place.</p>
<p>So if you're looping from January 1st-3rd and are adding a new <code>where</code> condition on each loop, that's going to fail because now you are basically querying this. Obviously the <code>day</code> column cannot match 3 different dates.</p>
<pre class="lang-sql prettyprint-override"><code>SELECT * FROM holidays
WHERE DATE(day) = '2022-01-01'
  AND DATE(day) = '2022-01-02'
  AND DATE(day) = '2022-01-03'
</code></pre>
<p>That's also why it only worked on the first loop for you, because at that point there is only 1 where condition.</p>
<p>You would need to move the instantiation inside the <code>while</code> loop so that it gets reset on each loop. Which is basically what you did in your solution.</p>
<p>Re: performance, what you were trying to do would not have saved you any DB cycles anyway. Each time you call <code>count()</code> you are hitting the database, regardless of whether it's a new <code>$holidays</code> object or not.</p>
<p>If you're concerned about performance, one thing you could do is fetch all of the holidays between the start &amp; end date in a single query.</p>
<pre class="lang-php prettyprint-override"><code>// May need to call toDateString() on $now and $last
$holidays = Holiday::whereBetween('day', [$now, $last])
    -&gt;get()
    -&gt;pluck('id', 'day'); // Assuming day is a DATE column not DATETIME or TIMESTAMP

// This will give you a collection with an underlying array like this:
// ['2022-07-04' =&gt; 1, '2022-12-25' =&gt; 2]

while($now-&gt;lte($last))
{
    array_push($days, [
        // Now you can instantly look it up in the array by the date
        'disabled' =&gt; isset($holidays[$now-&gt;toDateString()]),
    ]);
    $now-&gt;addDay();
}
</code></pre>

