# MySQL: automatic mapping of UTC to Local Timezone
[Link to question](https://stackoverflow.com/questions/6710647/mysql-automatic-mapping-of-utc-to-local-timezone)
**Creation Date:** 1310749489
**Score:** 2
**Tags:** mysql, datetime, timezone, convert-tz
## Question Body
<p>I have a forum where users can post comments. When a comment is created its corresponding datetime value is stored in UTC format. </p>

<p>I intend to present the data in local time, say 'ASIA/SINGAPORE'; </p>

<p>2 options:</p>

<ol>
<li>use <code>convert_tz</code> each time querying the database. I dont like the
approach, cause it makes me rewrite the <code>select_expr</code> each time querying.</li>
<li>use <code>SET time_zone = 'ASIA/SINGAPORE';</code></li>
</ol>

<p>As for the second option, I want to know what is the validity scope of the command (no super privilege here). more specifically, say if i'm using a php application, does the config gets invalid as i close db connection? should i issue the command each time querying the db?</p>

<p>Tnx.</p>

## Answers
### Answer ID: 6710851
<p>MySQL variables are scoped in the connection (lowest level, between libmysql &lt;-> mysqld). It means, that if PHP itself or some application library uses any kind of mysql connection pooling, then you could observe this variable disappearing (because of invisible connection switching), and the variable definitely will disappear after disconnecting.</p>

<p>If you are not happy rewriting your query, you probably could select apropriate tz name on the fly -- say, form a users table, as long as you have the id of the logged user, like this: </p>

<pre><code>SELECT convert_tz( ..., ..., (select user_tz from users where user_id = ...))
</code></pre>

