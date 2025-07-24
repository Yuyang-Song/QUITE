# Update on Insert HSQLDB
[Link to question](https://stackoverflow.com/questions/29700066/update-on-insert-hsqldb)
**Creation Date:** 1429275932
**Score:** 1
**Tags:** java, sql, hsqldb
## Question Body
<p>I am trying to rewrite code, that was using MySQL database, to use HSQLDB. I have an <code>INSERT INTO ... ON DUPLICATE KEY UPDATE</code> query. Is there an alternative of this method for HSQLDB.</p>

<p>Code:</p>

<pre><code>PreparedStatement ps = conn.prepareStatement("INSERT INTO user_stats "
    + "(user, balance, kills, level)"
    + " VALUES(?, ?, ?, ?) ON DUPLICATE KEY "
    + "UPDATE balance=VALUES(balance), kills=VALUES(kills), level=VALUES(level)");

ps.setString(1, playername);
ps.setDouble(2, PluginInterract.getESSBalance(playername));
ps.setInt(3, PluginInterract.getKills(playername));
ps.setDouble(4, PluginInterract.getPluginLevel(playername));
</code></pre>

## Answers
### Answer ID: 31356472
<p>From version 2.3.3 (June 2015) HSQLDB supports <code>INSERT INTO  ... ON DUPLICATE KEY UPDATE ...</code> in MYS compatibility mode.</p>

<p>Refer: <a href="http://hsqldb.org/doc/guide/guide.html#coc_compatibility_mysql" rel="nofollow noreferrer">http://hsqldb.org/doc/guide/guide.html#coc_compatibility_mysql</a></p>

<p>But version 2.3.3 doesn't support <code>Values(COLUMN_NAME)</code> method of MySQL.</p>

### Answer ID: 29700142
<p>Not according to <a href="http://hsqldb.org/doc/2.0/guide/dataaccess-chapt.html#dac_insert_statement" rel="nofollow">the documentation</a>.  The <a href="http://hsqldb.org/doc/2.0/guide/dataaccess-chapt.html#dac_merge_statement" rel="nofollow"><code>MERGE</code></a> statement might do what you want, however.  Here is an untested example based on the documentation for <code>MERGE</code>:</p>

<pre><code>MERGE INTO user_stats USING (VALUES(?, ?, ?, ?))
    AS vals(user, balance, kills, level) ON user_stats.user = vals.user
    WHEN MATCHED THEN UPDATE SET user_stats.balance = vals.balance, user_stats.kills = vals.kills, user_stats.level = vals.level
    WHEN NOT MATCHED THEN INSERT VALUES vals.user, vals.balance, vals.kills, vals.level
</code></pre>

