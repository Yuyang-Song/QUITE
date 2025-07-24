# Can I see the SQL that a `SQLPersistM` block would run, without running the query?
[Link to question](https://stackoverflow.com/questions/38303674/can-i-see-the-sql-that-a-sqlpersistm-block-would-run-without-running-the-quer)
**Creation Date:** 1468229888
**Score:** 1
**Tags:** sql, haskell, yesod, persistent
## Question Body
<p>I've got a query like this in <code>persistent</code>:</p>

<pre><code>findUserLocation userId =
  rawSql [str|SELECT name, ST_Transform(coordinates, 4326)
               FROM user 
                 JOIN user_location USING (user_id)
               WHERE user.user_id = ?|]
         [toPersistValue userId]
</code></pre>

<p>I'd like to rewrite this so it doesn't use raw strings, probably into an Esqueleto query, but I want to be sure the end result is equivalent.</p>

<p>Is there a way I can check the SQL my new query will produce <em>without a database connection</em>?<br>
Is there something like <code>SqlPersistM a -&gt; [Text]</code>? (I've searched, to no avail...)</p>

<p>Or do I have to connect to the DB to verify the query?</p>

