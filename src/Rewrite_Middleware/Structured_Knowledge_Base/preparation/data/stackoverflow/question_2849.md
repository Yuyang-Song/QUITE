# Why is SQLite still not able to write quickly from multiple threads in serialised mode?
[Link to question](https://stackoverflow.com/questions/55655530/why-is-sqlite-still-not-able-to-write-quickly-from-multiple-threads-in-serialise)
**Creation Date:** 1555084804
**Score:** 1
**Tags:** c#, multithreading, sqlite, locking, entity-framework-core
## Question Body
<p>I am trying to write records to SQLite using EF Core 2.2 very quickly (1000 rows with a delay of about 20ms) using multiple threads. I get this error:</p>

<blockquote>
  <p>System.InvalidOperationException: 'A second operation started on this
  context before a previous operation completed. This is usually caused
  by different threads using the same instance of DbContext, however
  instance members are not guaranteed to be thread safe. This could also
  be caused by a nested query being evaluated on the client, if this is
  the case rewrite the query avoiding nested invocations.'</p>
</blockquote>

<p>I can use <code>WAL (Write Ahead Logging)</code> which works better but still causes the issue, if I use a manual lock with with WAL then it works, but I do not like the inconvenience of having a separate files, which do not get save to the main db if there is a crash. Using a simple lock without WAL also works, but there are freezes for up to a few seconds at a time.</p>

<p>Why does this error happen when the SQLite assembly has been compiled with this config:</p>

<pre><code>COMPILER=msvc-1700
DEFAULT_FOREIGN_KEYS
ENABLE_COLUMN_METADATA
ENABLE_FTS3_PARENTHESIS
ENABLE_FTS4
ENABLE_FTS5
ENABLE_JSON1
ENABLE_RTREE
THREADSAFE=1
</code></pre>

<p><code>THREADSAFE=1</code> means serialised according to <a href="https://www.sqlite.org/threadsafe.html" rel="nofollow noreferrer">https://www.sqlite.org/threadsafe.html</a> which should prevent issues when multiple threads are trying to use the same DbContext to write to the db.</p>

<blockquote>
  <p>SQLITE_THREADSAFE=1) the SQLite library will itself serialize access
  to database connections and prepared statements so that the
  application is free to use the same database connection or the same
  prepared statement in different threads at the same time.</p>
</blockquote>

<p>I would like to understand why this is happening.</p>

