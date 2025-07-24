# castle activerecord rewrite sql
[Link to question](https://stackoverflow.com/questions/5338090/castle-activerecord-rewrite-sql)
**Creation Date:** 1300359621
**Score:** 0
**Tags:** castle-activerecord
## Question Body
<p>is there anyway to intercept the sql query before it is sent to the database and rewrite it using castle active record ?</p>

## Answers
### Answer ID: 5339299
<p>Set up an interceptor and use <code>OnPrepareStatement</code> to modify the generated SQL. See <a href="http://www.davesquared.net/2008/08/modifying-sql-generated-by-nhibernate.html" rel="nofollow">this example</a>.</p>

