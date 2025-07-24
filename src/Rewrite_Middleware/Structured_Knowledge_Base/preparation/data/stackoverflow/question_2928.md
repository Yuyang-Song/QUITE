# aiopg + sqlalchemy: how to &quot;drop table if exists&quot; without raw sql?
[Link to question](https://stackoverflow.com/questions/58951334/aiopg-sqlalchemy-how-to-drop-table-if-exists-without-raw-sql)
**Creation Date:** 1574243473
**Score:** 15
**Tags:** python, postgresql, sqlalchemy, drop-table, aiopg
## Question Body
<p>I am looking at <a href="https://aiopg.readthedocs.io/en/stable/examples.html#default-value-field-sqlalchemy-usage" rel="noreferrer">examples of aiopg usage with sqlalchemy</a> and these lines scare me:</p>

<pre><code>async def create_table(conn):
    await conn.execute('DROP TABLE IF EXISTS tbl')
    await conn.execute(CreateTable(tbl))
</code></pre>

<p>I do not want to execute raw sql queries when using sqlalchemy. However I can't find any other way to implement the same logic. My attempts were:</p>

<p>1)</p>

<pre><code>await conn.execute(tbl.drop(checkfirst=True))
</code></pre>

<p>This raises:</p>

<blockquote>
  <p>sqlalchemy.exc.UnboundExecutionError: Table object 'tbl' is not
  bound to an Engine or Connection.  Execution can not proceed without a
  database to execute against.</p>
</blockquote>

<p>Also I can't find a way to bind the table to engine because <a href="https://github.com/aio-libs/aiopg/issues/123#issuecomment-232604788" rel="noreferrer">aiopg doesn't support metadata.create_all</a></p>

<p>2)</p>

<pre><code>await conn.execute(DropTable(tbl))
</code></pre>

<p>This raises:</p>

<blockquote>
  <p>psycopg2.errors.UndefinedTable: table "tbl" does not exist</p>
</blockquote>

<p>Seems like <code>DropTable</code> construct doesn't support <code>IF EXISTS</code> part in any way.</p>

<p>So, the question is, is there any way to rewrite <code>await conn.execute('DROP TABLE IF EXISTS tbl')</code> statement into something without raw sql when using aiopg + sqlalchemy?</p>

## Answers
### Answer ID: 69596301
<p><em>This question was posted when the latest version was SQLAlchemy 1.3.11.</em></p>
<p>As of SQLAlchemy 1.4.0, <code>DropTable</code> supports <code>if_exists=True</code>.</p>
<pre class="lang-py prettyprint-override"><code>await conn.execute(DropTable(tbl, if_exists=True))
</code></pre>
<p>Reference: <a href="https://docs.sqlalchemy.org/en/14/core/ddl.html#sqlalchemy.schema.DropTable" rel="noreferrer">https://docs.sqlalchemy.org/en/14/core/ddl.html#sqlalchemy.schema.DropTable</a></p>

