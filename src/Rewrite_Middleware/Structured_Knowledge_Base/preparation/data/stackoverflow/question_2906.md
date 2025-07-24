# Rewrite SQLAlchemy query before sending to engine
[Link to question](https://stackoverflow.com/questions/58095907/rewrite-sqlalchemy-query-before-sending-to-engine)
**Creation Date:** 1569405887
**Score:** 0
**Tags:** python, sqlalchemy
## Question Body
<p>Is it possible to rewrite the final, compiled raw query bytes before they are sent to the underlying database engine? I've looked at the Events API, but it doesn't seem to expose such low-level events.</p>

<p>Use case: I want to add a string to the beginning of all queries, containing contextual meta data:</p>

<pre><code>/* {"trace_id":"1234","client_ip":"1.2.3.4", ...} */ SELECT ...
</code></pre>

<p>The data is extracted from the database's query logs, and used to correlate events with other services in the stack.</p>

## Answers
### Answer ID: 58096922
<p>Simply use the <code>before_cursor_execute</code> event with <code>retval=True</code>, as shown in <a href="https://github.com/sqlalchemy/sqlalchemy/wiki/Profiling" rel="nofollow noreferrer">https://github.com/sqlalchemy/sqlalchemy/wiki/Profiling</a></p>

<pre class="lang-py prettyprint-override"><code>@event.listens_for(Engine, "before_cursor_execute", retval=True)
def before_cursor_execute(conn, cursor, statement,
    parameters, context, executemany):
  statement = "/* {} */ {}".format(
    json.dumps({
      "trace_id": "1234",
      "client_ip": "1.2.3.4",
    }),
    statement
  )
  return statement, parameters
</code></pre>

