# Using luigi to update Postgres table
[Link to question](https://stackoverflow.com/questions/40707004/using-luigi-to-update-postgres-table)
**Creation Date:** 1479662534
**Score:** 4
**Tags:** postgresql, python-3.5, luigi
## Question Body
<p>I've just started using the <code>luigi</code> library. I am regularly scraping a website and inserting any new records into a Postgres database. As I'm trying to rewrite parts of my scripts to use <code>luigi</code>, it's not clear to me how the <a href="http://luigi.readthedocs.io/en/stable/api/luigi.postgres.html?highlight=marker%20table#luigi.postgres.PostgresTarget" rel="nofollow noreferrer">"marker table"</a> is supposed to be used.</p>

<p><strong>Workflow</strong>:</p>

<ol>
<li>Scrape data</li>
<li>Query DB to check if new data differs from old data.</li>
<li>If so, store the new data in the same table.</li>
</ol>

<p>However, using luigi's <code>postgres.CopyToTable</code>, if the table already exists, no new data will be inserted. I guess I should be using the <code>inserted</code> column in the <code>table_updates</code> table to figure out what new data should be inserted, but it's unclear to me what that process looks like and I can't find any clear examples online.</p>

## Answers
### Answer ID: 40721796
<p>You don't have to worry about marker table much: it's an internal table luigi uses to track which task has already been successfully executed. In order to do so, luigi uses the <code>update_id</code> property of your task. If you didn't declared one, then luigi will use the <code>task_id</code> <a href="https://github.com/spotify/luigi/blob/master/luigi/contrib/rdbms.py#L98" rel="nofollow noreferrer">as shown here</a>. That task_id is a concatenation of the task family name and the first three parameters of your task. </p>

<p>The key here is to overwrite the <code>update_id</code> property of your task and return a custom string that you'll know will be unique for each run of your task. Usually you should use the significant parameters of your task, something like:</p>

<pre><code>@property
def update_id(self):
    return ":".join(self.param1, self.param2, self.param3)
</code></pre>

<p>By <strong>significant</strong> I mean parameters that change the output of your task. I imagine parameters like website url o id, and scraping date. Parameters like the hostname, port, username or password of your database will be the same for any of these tasks so they shouldn't be considered significant.</p>

<p>Notice that without having details about your tables and the data you're trying to save its pretty hard to say how you must build that update_id string, so please be careful.</p>

