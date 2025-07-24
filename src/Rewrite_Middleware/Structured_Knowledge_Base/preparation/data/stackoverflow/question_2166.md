# Postgresql custom function returning table
[Link to question](https://stackoverflow.com/questions/21531227/postgresql-custom-function-returning-table)
**Creation Date:** 1391441355
**Score:** 2
**Tags:** php, sql, postgresql, stored-procedures, plpgsql
## Question Body
<p>I am using PostgreSQL 9.1.11.<br>
I need to return result of SELECT to my php script. The invocation in php is like this:</p>

<pre><code>$res = $pdb-&gt;getAssoc("SELECT * FROM my_profile();");
</code></pre>

<p>The class code to illustrate what is going on in php</p>

<pre><code>public function getAssoc($in_query) {
  $res = pg_query($this-&gt;_Link, $in_query);
  if($res == FALSE) {
    return array("dberror", iconv("utf-8", "windows-1251", pg_last_error($this-&gt;_Link)));
  }
  return pg_fetch_all($res);
}
</code></pre>

<p>Next comes my function in Postgres. I fully re-create database by dropping in a script when I update any function. (The project is in the early stage of development.) I have little to no experience doing stored procedures.</p>

<p>I get this error:</p>

<blockquote>
<pre><code>structure of query does not match function result type
CONTEXT: PL/pgSQL function "my_profile" line 3 at RETURN QUERY )
</code></pre>
</blockquote>

<p>Trying to write:</p>

<pre><code>CREATE FUNCTION my_profile()
RETURNS TABLE (_nick text, _email text) AS $$
BEGIN
  RETURN QUERY SELECT (nick, email) FROM my_users WHERE id = 1;
END;
$$
LANGUAGE 'plpgsql' SECURITY DEFINER;
</code></pre>

<p>Table structure is:</p>

<pre><code>CREATE TABLE my_users(
  id integer NOT NULL,
  nick text,
  email text,
  pwd_salt varchar(32),
  pwd_hash character(128),
  CONSTRAINT users_pk PRIMARY KEY (id)
);
</code></pre>

<p>When I return 1 column in a table the query works. Tried to rewrite procedure in <code>LANGUAGE sql</code> instead of <code>plpgsql</code> with some success, but I want to stick to plpgsql.</p>

<p>The Postgres 9.1.11, php-fpm I am using is latest for fully updated amd64 Debian wheezy.  </p>

<p>What I want to do is to return a recordset containing from 0 to n rows from proc to php in an associative array.</p>

## Answers
### Answer ID: 21539477
<p><a href="https://stackoverflow.com/a/21531327/939860">@Daniel</a> already pointed out your immediate problem (incorrect use of parentheses). But there is more:</p>

<ul>
<li><p>Never quote the language name <code>plpgsql</code> in this context. It's an <em>identifier</em>, not a string literal. It's tolerated for now since it's a wide-spread anti-pattern. But it may be considered a syntax error in future releases.</p></li>
<li><p>The <code>SECURITY DEFINER</code> clause should be accompanied by a local setting for <code>search_path</code>. Be sure to read the <a href="http://www.postgresql.org/docs/current/interactive/sql-createfunction.html#SQL-CREATEFUNCTION-SECURITY" rel="nofollow noreferrer">according chapter in the manual</a>.</p></li>
</ul>

<p>Everything put together, it could look like this:</p>

<pre><code>CREATE FUNCTION my_profile()
  RETURNS TABLE (nick text, email text) AS
$func$
BEGIN
   RETURN QUERY
   SELECT m.nick, m.email FROM my_users m WHERE m.id = 1;
END
$func$
LANGUAGE plpgsql SECURITY DEFINER SET search_path = public, pg_temp;
</code></pre>

<p>Replace <code>public</code> whit the actual schema of your table.</p>

<p>To avoid possible naming conflicts between OUT parameters in <code>RETURNS TABLE ...</code> and table columns in the <code>SELECT</code> statement I table-qualified column names with the given alias <code>m</code>.</p>

### Answer ID: 21531327
<p>This part is incorrect:</p>

<pre><code>RETURN QUERY SELECT (nick, email) FROM my_users WHERE id = 1;
</code></pre>

<p>You should remove the parentheses around <code>nick,email</code> otherwise they form a unique column with a <code>ROW</code> type.</p>

<p>This is why it doesn't match the result type.</p>

