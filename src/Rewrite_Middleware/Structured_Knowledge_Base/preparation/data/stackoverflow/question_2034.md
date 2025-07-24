# How to emulate Oracle (+) outer join notation in in-memory database used to run Java unit tests?
[Link to question](https://stackoverflow.com/questions/16675382/how-to-emulate-oracle-outer-join-notation-in-in-memory-database-used-to-run)
**Creation Date:** 1369155074
**Score:** 3
**Tags:** java, oracle-database, hsqldb, outer-join
## Question Body
<p>We are using HSQLDB with Oracle database syntax(jdbc:hsqldb:mem:TestDB;sql.syntax_ora=true) for our datalayer unit tests.</p>

<p>(We realize this is not ideal and it would be better if we could test against an actual Oracle db. However this is not an option, since we want to make sure we can run our automated tests anywhere. In a later step, all queries are also tested in integration tests on an actual Oracle database, which is setup similar to the production database.)</p>

<p>Is there any way to support the Oracle outer join (+) notation for queries with HSQLDB?</p>

<p>In my own opinion we should not use the (+) notation but the standard outer join notation instead. However, the guys that are in charge of tuning the queries use this notation, so communication with them would get more difficult/errorprone.
Although it might be an option if no solution is found, this is not the question here.</p>

<p>I found the following thread:
<a href="http://comments.gmane.org/gmane.comp.java.hsqldb.user/5756" rel="nofollow">http://comments.gmane.org/gmane.comp.java.hsqldb.user/5756</a>
With the QueryRewrite patch mentioned there, I would have the necessary hook to handle the (+) myself, but that interface never made it to the official HSQL release.</p>

<p>Is there another workaround to this for HSQL?</p>

<p>We could add the query rewriting somewhere in our unit tests themselves(instead of at the test db level), but it would be better if we can avoid that.</p>

<p>If there is no workaround for HSQL, is there any other in-memory database/database starteable from a jar, that supports this (+) outer join notation?</p>

## Answers
### Answer ID: 16689531
<p>Simply do not use it. There were times when Oracle optimizer dealt these two syntax-es differently. As of 11g it's over and there is no reason to insist on this syntax.</p>

<p>But anyway Oracle has another SQL syntax enhancements - like analytic queries for example. Maybe you should use OracleXE for your automated tests.</p>

### Answer ID: 16689363
<p>I think you have already quoted all the "easy" possibilities in your question.</p>

<p>So the only remaining approach would be to rewrite the query in your code before sending it over to HSQLDB. </p>

<p>It should be simpler to write the queries to not using the (+) notation, and then to rewrite them (using a script) for your database tuners. That rewrite should be easier than the other direction, because the standard notation carries more information in its structure.</p>

