# Edit field during eloquent query Laravel
[Link to question](https://stackoverflow.com/questions/56522166/edit-field-during-eloquent-query-laravel)
**Creation Date:** 1560151404
**Score:** 0
**Tags:** php, laravel, eloquent
## Question Body
<p><strong>Scenario</strong></p>

<p>I've been building an app for my workplace, unfortunately I wasn't the most knowledgable developer at the time of creating this application. I've been storing expense data in the database with a 'date' field but this date field is essentially a string that I cannot compare any <code>Carbon</code> datetimes to.</p>

<p><strong>Example</strong></p>

<p>An example result would look like this <code>['name' =&gt; 'Spend', 'amount' =&gt; 22.25, 'date' =&gt; '2018-01-12']</code>. So if i wanted to pull all spends from yesterday this is the code I currently use now:</p>

<pre><code>public function getBetween($from, $to)
{
    $all = $this-&gt;getAll();

    foreach($all as $key =&gt; $revenue)
    {
        // dateRepositorys convert to carbon method converts the date to carbon
        // but this is converting the date AFTER the expensive query has been ran
        if($this-&gt;dateRepository-&gt;convertToCarbon($revenue-&gt;date) &lt; $from || $this-&gt;dateRepository-&gt;convertToCarbon($revenue-&gt;date) &gt; $to)
        {
            $all-&gt;forget($key);
        }
    }

    return $all;
}
</code></pre>

<p>This works fine but its a very expensive request since its ran a few times to get an overview of profits. Im trying to follow better coding practices and will eventually rewrite the code and add the date field to the list of dates as stated here: <a href="https://laravel.com/docs/5.8/eloquent-mutators#date-mutators" rel="nofollow noreferrer">https://laravel.com/docs/5.8/eloquent-mutators#date-mutators</a>, but for the time being I wanted to know if this was possible.</p>

<p><strong>Question</strong></p>

<p>Can I do some sort of pre-formatting while fetching data from the database using the eloquent query? so for example:</p>

<p><code>Expense::whereBetween(Carbon::parse('date') &lt;-- /* turn the date field into a carbon object BEFORE performing any checks */, [Carbon::yesterday(), Carbon::yesterday()])-&gt;get()</code></p>

<p><strong>Notes</strong></p>

<p>I understand I could do <code>Carbon::yesterday()-&gt;format('Y-m-d')</code> but this means I lose a lot of carbons functionality since I would essentially only be comparing to strings.</p>

<p>I do know date mutators exist but to my knowledge they only work after the data has been retrieved.</p>

<p>Thank you in advance.</p>

## Answers
### Answer ID: 56522367
<p>you can try casting your field. insert this code into your model.</p>

<pre><code>protected $casts = [
    'date'  =&gt; 'date:Y-m-d',
]
</code></pre>

