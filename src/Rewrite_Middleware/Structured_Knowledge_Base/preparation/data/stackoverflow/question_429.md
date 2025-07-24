# Are table operations in PLSQL more efficient than running them in an external app? (Oracle 10g)
[Link to question](https://stackoverflow.com/questions/25667531/are-table-operations-in-plsql-more-efficient-than-running-them-in-an-external-ap)
**Creation Date:** 1409839421
**Score:** 0
**Tags:** oracle-database, performance, plsql, code-separation
## Question Body
<p>So, I'm reading Ian Abramson's Beginners guide to Oracle Database 10g (coming from using mysql), and it mentions PL/SQL and gives all these great reasons to use it, however I'm doing this in preparation for a rewrite of several applications my company uses.</p>

<p>My head programmer argues that if PL/SQL is no more efficient at database access, all parsing and queries should be done on client side programs to spread the load out from the Oracle server. I argue that we should compartmentalize our code and attempt to avoid code duplication, and PL/SQL may help us do that.</p>

<p>The problem is, we don't actually know (And this book doesn't tell us), how efficient database access is in PL/SQL over an application running on a different machine that makes 3-5 (largish) queries per operation. I would think it's more likely to run faster because (to my knowlege) pl/sql functions store and save their execution plans, and the traditional network overhead would be cut by a factor of 3-5 (depending on the number of queries)</p>

## Answers
### Answer ID: 25667964
<p>This is a  non-trivial question, and and will likely be influenced by your application design.  In general, if you can do it in SQL, do it in SQL.  If you can't do it in SQL, do it in PL/SQL.  If you can't do it in PL/SQL, do it in Java (in the database).  If that doesn't work, do it in external client side code.</p>
<p>Now, that isn't universal.  If you're not doing something database related, then it makes sense to do it on the client side.  If it's highly CPU intensive, and it makes sense to do it in the client, then great.  The reason is, you're paying big money to license Oracle, and you're (probably) paying per CPU.  So, if you're doing a lot of non-database related work on the CPUs licensed for Oracle, that's extremely expensive.</p>
<p>To summarize, if it's actual database related code (insert/update/delete/select), even if it has some non-trivial logic around it, it makes sense to put it in the database.  If it's not actually interacting with the database, it probably doesn't belong in the database.</p>
<p>Finally, your comments about PL/SQL code efficiency are true.  There are efficiencies with PL/SQL around parsing and storing execution plans.  Also, PL/SQL will automatically pre-fetch data.</p>
<p>Lots more information about advantages of PL/SQL can be found here:
<a href="http://docs.oracle.com/database/121/LNPLS/overview.htm#LNPLS00101" rel="nofollow noreferrer">http://docs.oracle.com/database/121/LNPLS/overview.htm#LNPLS00101</a></p>

