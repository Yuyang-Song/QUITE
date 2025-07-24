# Laravel 5.4: Converting a raw SQL query in Laravel Eloquent
[Link to question](https://stackoverflow.com/questions/50122426/laravel-5-4-converting-a-raw-sql-query-in-laravel-eloquent)
**Creation Date:** 1525201909
**Score:** 0
**Tags:** php, mysql, sql, laravel, eloquent
## Question Body
<p>I'm trying to rewrite this SQL query but I'm stuck at this point</p>

<p>The query is meant to join the projects table to the project_progress table by using a sub-query to only join on the latest entry</p>

<pre><code>SELECT * FROM projects
JOIN project_progress ON project_progress.id = 
(
    SELECT id FROM project_progress
    WHERE project_progress.project_id = projects.id
    ORDER BY project_progress.created_at DESC
    LIMIT 1
)
WHERE project_progress.next_action_date &lt; NOW()
AND projects.status != 'Complete'
AND projects.member_id = 1
ORDER BY projects.title ASC
</code></pre>

<p>To:</p>

<pre><code>$projects = App\Project::where('member_id', 1)
    -&gt;join('project_progress', function ($join) {
        $join-&gt;on('project_progress.id', '=', function ($query) {
            $query-&gt;select('project_progress.id')
                -&gt;from('project_progress')
                -&gt;where('project_progress.project_id', 'projects.id')
                -&gt;orderBy('project_progress.created_at', 'desc')
                -&gt;limit(1);
        });
    })
    -&gt;where('project_progress.next_action_date', '&lt;', Carbon\Carbon::now())
    -&gt;notCompleted()
    -&gt;orderBy('projects.project_title', 'asc')
    -&gt;get();
</code></pre>

<p>I think some thing is wrong with this line but I'm not sure how to write it</p>

<pre><code>$join-&gt;on('project_progress.id', '=', function ($query) {
</code></pre>

<p>ErrorException (E_ERROR) strtolower() expects parameter 1 to be string, object given \vendor\laravel\framework\src\Illuminate\Database\Grammar.php</p>

## Answers
### Answer ID: 50123730
<p>Use <code>where()</code>:</p>

<pre><code>$join-&gt;where('project_progress.id', '=', function ($query) {
</code></pre>

