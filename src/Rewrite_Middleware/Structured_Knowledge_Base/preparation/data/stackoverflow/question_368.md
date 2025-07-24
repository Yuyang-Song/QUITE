# Row-level security in a client-database scenario
[Link to question](https://stackoverflow.com/questions/22904101/row-level-security-in-a-client-database-scenario)
**Creation Date:** 1396847685
**Score:** 7
**Tags:** database, security, postgresql, architecture, row-level-security
## Question Body
<p>I am looking for a good pattern to implement row-level security controls (via e.g. a proxy, man-in-the-middle web service, or stored procedures) suitable for use in a client->database environment.  I control both the client and the database.  Some requirements:</p>

<ul>
<li>Forbidding users from seeing rows in query results that they don't have permission to see</li>
<li>Allowing users to INSERT and UPDATE their own rows into the table, which gives them permission to see them</li>
<li>(soft requirement) allowing users to grant others access to read or write their rows</li>
<li>An open-source or low-cost solution that runs on Linux.  As I understand it, no free database implements row-level security as such.  Oracle supports this but it's way too $$$$.  Postgres <a href="http://wiki.postgresql.org/wiki/Row-security">might be implementing this in 9.4</a>, but it was originally targeted for 9.3 and slipped and there is discussion on the ML that it may slip again.  I'm tentatively thinking about using postgres just because they seem the furthest along on this feature.</li>
</ul>

<p>Some (not terribly good) ideas I've had:</p>

<ul>
<li>Use postgresql's security barrier views and deny the user access to the underlying table.  Unfortunately there is <a href="http://wiki.postgresql.org/wiki/Automatically_updatable_security_barrier_views">no good way to insert a row into a security barrier view</a>, so some privileged proxy/webservice would have to handle insert statements.  This seems hard to get right.</li>
<li>Use regular views, and deny the user access to the underlying table.  This allows <code>insert</code>, but I would need to lock down the permissions pretty tightly (e.g. no creating functions), and <a href="http://rhaas.blogspot.com/2012/03/security-barrier-views.html">there seem to be a lot of gotchas (like divide by zero) that leak information</a>.</li>
<li>Define some subset of SQL, and create a proxy that is your only point of communication with the database.  The proxy parses your SQL query and rewrites it to enforce security requirements.  This seems hard to do in general, but perhaps I could get away with a very small SQL subset until postgres implements row-level security for real.</li>
<li>Just have different tables for different users (or even different DBs).  However I'm not sure how well this scales to lots of users.  Also, this doesn't seem to meet the soft requirement.</li>
<li>Find some commercial but reasonable-cost DB that actually supports this</li>
<li>Use <a href="http://postgresql.1045698.n5.nabble.com/Re-v9-4-row-level-security-td5774153.html">Veil</a> but it doesn't seem to be maintained, and it has most of the limitations of other solutions</li>
</ul>

<p>I have done a lot of googling on this topic but I have yet to see a postmortem of how someone solved this problem in a real-world scenario.  There is <a href="http://msdn.microsoft.com/en-us/library/bb669076%28v=vs.110%29.aspx">some documentation for MS SQL</a> but seems to be <a href="https://www.mail-archive.com/mysql@lists.mysql.com/msg105224.html">discouraged in MySQL</a> and writeups are basically nonexistent for postgres.</p>

<p>This seems like a very common problem, but I guess many people are writing web applications and are content to handcuff their users to certain pre-vetted queries, but I really need to give my users as much flexibility as I can to query the data with my client.</p>

## Answers
### Answer ID: 36574525
<p>I am working on such proxy here <a href="https://github.com/jbaliuka/sql-analytic" rel="nofollow">https://github.com/jbaliuka/sql-analytic</a>
It was developed for reporting/analytical purposes  initially but I plan to implement gateway application so that I can navigate DB and execute SQL with DML via JavaScript from browser.It  might be useful as the Olingo plugin to publish database as OData Service too. </p>

### Answer ID: 25635744
<p>I've done this in Oracle and SQL Server at the database level, as well as via a web server with preset authorization controls (non-free-form query), as well as via SQL parser that enables free-form query. My take:</p>

<pre>
1. Approach 1: Use database-level mechanisms, where user A is the database user
   that creates / owns / fully controls all tables, views, and other
   objects, and user B, C, D... are the end user accounts that utilize
   the objects that A grants access to.
  a. Pros
    i. Might be easier to maintain; you may need fewer test cases to confirm that it 
       works properly
    ii. Allows you to distribute an application that uses direct ODBC connections 
        (such as a Microsoft Access file) to multiple users, who can each have separate
        row-level security
    iii. Allows real-time updates to access control (either to individual permissions, 
         or to entire sets of permissions), via back-end database changes
    iv. You don't have to worry about application security, because you are relying on
        the database for all security (including the security of your admin account)
  b. Cons:
    i. Requires a separate database user account for each end user. This is generally
       not desirable for, for example, tens of thousands of users
    ii. By using ODBC, users are directly connecting to the database server, which could
        be a security weakness under some circumstances (which depends on more factors than
        are in scope for this question)
    iii. Performance takes a significant hit. Another barrier to scalability
    iv. For these and other reasons, this approach is generally not considered best
        practice for production use
  c. Implementation:
    i. For Oracle, as you noted, there is built-in support
    ii. For SQL Server, this can be implemented using views and instead-of triggers,
        where the view or stored proc does SELECTs and triggers perform writes
        in a controlled manner. This can get the job done,
        but it is cumbersome, and requires a fair amount of code, much of which needs to
        be changed whenever your authorization approach changes (such as changing what
        fields in what ACL tables will authorize what actions based on what values in the
        tables you want to secure). Furthermore, each set of code needs to be added to each
        table you want to secure. Oracle, on the other hand, does something akin to
        parsing the SQL statement and interjecting a where clause whenever the table you
        are securing is involved. This is a far more flexible approach, but would be very
        difficult to implement in SQL server unless you can write a SQL parser in T-SQL
    iii. For postgreql and mysql, I believe you can implement the same approach as described
         above for SQL Server, if this is the way you want to go. I suppose, in postgresql
         you could write a SQL parser in C which performs the transformation to add the
         necessary where clauses, make it available as a database function, pass your free-
         form SQL to this function in your trigger or stored proc, and use the resulting
         modified SQL as the query that gets run (or just have the C function run the query
         and pass that back to the view). But that might be a lot of work for some added
         flexibility for queries that you could not anticipate.

2. Approach 2: Use an application in the middle. So either your application uses User A to log
   in and do its stuff (not recommended, but technically, works fine), or you can set up a
   more restricted User B just for your application, which can do everything that any end user
   can do (e.g. view / change data), but nothing more (e.g. drop table). You rely on the
   application to control access.
  a. Pros: this is how most web and similar client-server applications work, and you'll find
     lots of resources available for doing this
  b. Cons:
   i. you can't use this approach if you want to provide end users with an ODBC connection
      (or an application that uses ODBC)
   ii. As you point out, usually this is implemented in a manner that does not allow for
       free-form SQL. There are two ways to address this latter concern:
    A. Create your own SQL parser (this is your "proxy" solution), which your application
       will use to parse any free-form SQL request (this will end up being similar to
       Oracle's implementation, except that your SQL monkeying occurs in your application,
       whereas Oracles occurs in the database). For all elements of the request that your
       parser identifies as a table, you will perform a lookup in your ACL table to determine
       what the "WHERE" predicate is (if any) related to that table, that will be added to
       the SQL request before it is sent to the server. If you are familiar with creating
       your own programming language parsers, this approach shouldn't be too hard, but if not,
       you might not want to try-- you may find that trying to solve even simple use cases
       ends up being just as complicated as solving any use case, so you either build a proper
       parser that is completely flexible, or you get mired in bug fixing forever. In
       addition, this approach will hit your performance hard just as Approach 1 does.
    B. Create a user-interface that provides the type of query functionality you want without
       truly being free-form. You would have to ensure the interface can support every
       conceivable query you want to accept. While this is not ideal based on what you asked,
       you may find it to be a more cost-effective approach given the amount of work to get
       your SQL parser correct, if you haven't done it before, 

</pre>

<p>Overall, my recommendation is to go with Approach 1 if you have a very small-scale project and it will save you time to use ODBC (for example, I did this for a pilot/test project where we built the application in Microsoft Access in 2 weeks), and otherwise, unless flexibility is truly the number 1 priority and performance is not important, to go with Approach 2 using a structured interface that allows the application to control access, and also to provide you with greater control over performance.</p>

### Answer ID: 23023474
<p>The whole row level security topic is quite controversial. My personal take on this is that you are barking at the wrong tree trying to implement this at the database ACL layer. I know that Oracle supports this but imo it was a really bad idea since the beginning and has caused a lot more frustration than good. I know you feel tempted to reuse the existing access control functionality just to save on lines of code but i myself would not dare to go down this road just because you might end up in a dead end due to the expectations vs reality of how the ACL is implemented vs how you would like it to work.</p>

