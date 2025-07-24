# pgp_sym_encrypt/pgp_sym_decrypt error handling
[Link to question](https://stackoverflow.com/questions/13598704/pgp-sym-encrypt-pgp-sym-decrypt-error-handling)
**Creation Date:** 1354082089
**Score:** 7
**Tags:** postgresql, encryption
## Question Body
<p>I had been using MySQL as database and had planned to move to postgresql.  I had used aes_encrypt and aes_decrypt functions in MySQL extensively throughout my application.  So whenever the encryption/decrytion fails, MySQL automatically returns 'null'.</p>

<p>I am unsure how to handle the same in postgresql.  Tried using the pgp_sym_encrypt/pgp_sym_decrypt functions.  If the encryption key is wrong, it throws error "Wrong key/corrupt data".  I tried searching for some functions that could capture this error and return 'null' as in MySQL so that I need not modify my code.  I had been searching but could not find one.</p>

<p>Has anybody used any error handling mechanism for individual queries? I had found that error handling can be done for procedures.  But, I had to completely rewrite the entire application for that.</p>

<p>If you could share some details, it would be of great help.  Thanks.</p>

## Answers
### Answer ID: 13599525
<p>If you wish to avoid modifying your code and have the functions return <code>NULL</code> on error, you can do this by wrapping them in a PL/PgSQL function that uses a <code>BEGIN ... EXCEPTION</code> block to trap the error.</p>

<p>To do this, first I get the SQLSTATE for the error:</p>

<pre><code>regress=# \set VERBOSITY verbose
regress=# SELECT pgp_sym_decrypt('fred','key');
ERROR:  39000: Wrong key or corrupt data
LOCATION:  decrypt_internal, pgp-pgsql.c:607
</code></pre>

<p>I could use this directly in the error handler, but I prefer to use a symbolic name, so I look up the error name associated with 39000 in <a href="http://www.postgresql.org/docs/current/static/errcodes-appendix.html" rel="noreferrer">Appendix A - Error codes</a>, finding that it's the generic function call error <code>external_routine_invocation_exception</code>. Not as specific as we would've liked, but it'll do.</p>

<p>Now a wrapper function is required. Something like this must be defined, with one function for each overloaded signature of <code>pgp_sym_decrypt</code> that you wish to support. For the <code>(bytea,text)</code> form that returns <code>text</code>, for example:</p>

<pre><code>CREATE OR REPLACE FUNCTION pgp_sym_decrypt_null_on_err(data bytea, psw text) RETURNS text AS $$
BEGIN
  RETURN pgp_sym_decrypt(data, psw);
EXCEPTION
  WHEN external_routine_invocation_exception THEN
    RAISE DEBUG USING
       MESSAGE = format('Decryption failed: SQLSTATE %s, Msg: %s',
                        SQLSTATE,SQLERRM),
       HINT = 'pgp_sym_encrypt(...) failed; check your key',
       ERRCODE = 'external_routine_invocation_exception';
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;
</code></pre>

<p>I've chosen to preseve the original error in a <code>DEBUG</code> level message. Here's a comparison of the original and wrapper, with full message verbosity and debug level output.</p>

<p>Enable debug output to show the <code>RAISE</code>. Note that it also shows the *original query text of the <code>pgp_decrypt_sym</code> call, including parameters.</p>

<pre><code>regress=# SET client_min_messages = DEBUG;
</code></pre>

<p>New wrapped function still reports the error if detailed logging is enabled, but returns <code>NULL</code>:</p>

<pre><code>regress=# SELECT pgp_sym_decrypt_null_on_err('redsdfsfdsfd','bobsdf');
LOG:  00000: statement: SELECT pgp_sym_decrypt_null_on_err('redsdfsfdsfd','bobsdf');
LOCATION:  exec_simple_query, postgres.c:860
DEBUG:  39000: Decryption failed: SQLSTATE 39000, Msg: Wrong key or corrupt data
HINT:  pgp_sym_encrypt(...) failed; check your key
LOCATION:  exec_stmt_raise, pl_exec.c:2806
 pgp_sym_decrypt_null_on_err
-----------------------------

(1 row)
</code></pre>

<p>compared to the original, which fails:</p>

<pre><code>regress=# SELECT pgp_sym_decrypt('redsdfsfdsfd','bobsdf');
LOG:  00000: statement: SELECT pgp_sym_decrypt('redsdfsfdsfd','bobsdf');
LOCATION:  exec_simple_query, postgres.c:860
ERROR:  39000: Wrong key or corrupt data
LOCATION:  decrypt_internal, pgp-pgsql.c:607
</code></pre>

<p>Note that <strong>both forms show the parameters the function was called with when it failed</strong>. The parameters won't be shown if you've used bind parameters ("prepared statements"), but you should still consider your logs to be security critical if you're using in-database encryption.</p>

<p>Personally, I think it's better to do crypto in the app, so the DB never has access to the keys.</p>

