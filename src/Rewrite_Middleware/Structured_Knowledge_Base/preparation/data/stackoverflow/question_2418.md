# SQL Server - Single User Mode - Persist Which User
[Link to question](https://stackoverflow.com/questions/33420210/sql-server-single-user-mode-persist-which-user)
**Creation Date:** 1446137508
**Score:** 0
**Tags:** sql-server, t-sql, sql-server-2008-r2, single-user, invoke-sqlcmd
## Question Body
<p><strong>Question</strong></p>

<p>Is there a way, when putting a database into single user mode, to specify that user (in my case it is the current user), and to ensure that even after that user disconnects, the single session kept reserved for that defined user; i.e. so it is genuinely single-user rather than single-concurrent-user?</p>

<p><strong>Background</strong></p>

<p>To give some context...</p>

<p>We have some scripts to refresh data in our test environments.
Recently one failed with an error stating that the user account under which the scripts are run did not have access to the database.
On investigation, the user was a sysadmin on the database; so this is clearly not true.
However, I found that the script puts the database into <code>Single User</code> mode.
When looking at the active sessions on the DB I can see that the single user is different to the expected account (rather it's another service account belonging to a system which polls this database intermittently).
My assumption is the following has happened:</p>

<ul>
<li>Script runs as UserA</li>
<li>Script puts DB to Single User mode</li>
<li>Script performs some query/ies</li>
<li>Script closes current connection whilst doing some other tasks</li>
<li>UserB attempts to connect to DB; success as the UserA session is now closed</li>
<li>UserB's session stays open (as UserB is a service with connection pooling, even after the operation's completed the session remains open).</li>
<li>UserA attempts to reconnect to DB; access denied as the single session is taken by UserB</li>
</ul>

<p>There are various possible solutions.</p>

<ul>
<li>Rewrite the script to keep a persistent connection (potentially lots of effort especially as I'm unfamiliar with the code)</li>
<li>Disable all services which may try to connect intermittently (kind of defeats the point of using a single-user mode / also a lot of additional effort to investigate all the accounts which may connect, and to maintain this)</li>
<li>Add a catch to the script to kill competing SPIDs and thus reclaim the single user session (I don't like killing SPIDs as this affects transactional integrity)</li>
<li>use magic (i.e. see accepted answer to this question; hopefully)</li>
</ul>

<p><strong>Update</strong></p>

<p>The code uses PowerShell's <code>Invoke-SqlCmd</code>, which creates and drops connections for every command run; so as soon as the database is put in single-user mode the connection's dropped.
I looked at this commands parameters to see if there were options for pooling/persisting connections, but the closest I could find was <code>DedicatedAdministratorConnection</code>, which it seems I should steer well clear of (<a href="http://www.brentozar.com/archive/2011/08/dedicated-admin-connection-why-want-when-need-how-tell-whos-using/" rel="nofollow">http://www.brentozar.com/archive/2011/08/dedicated-admin-connection-why-want-when-need-how-tell-whos-using/</a>) despite my initial hopes.</p>

## Answers
### Answer ID: 33423228
<p>Sorry, no magic. There's no native solution for what you need. SQL Server makes sure the session that set single-user-mode is the session that survives. Once that session terminates (user disconnect, network broken, etc...), the "slot" is now available to any other connection including certain background worker threads or the SSMS object browser. DAC is not a good idea for anything other than rescue operations.</p>

<p>You could use sqlcmd to run the scripts or call a script file from PS (invoke-sqlcmd -inputfile "c:\mysqlfile.sql" -serverinstance "servername\serverinstance" -database "mydatabase") so it's executed in a single session rather than individual sessions from PS. </p>

<p>There are many other ways to prevent users from connecting to the DB (triggers, security, etc...) but those are typically risky in that you need to be very careful implementing the blocks and making sure the blocks are safely and correctly removed when done. This is non-trivial as you need to consider loss of connection or loss of instance and how to deal with the state after resume or recovery. Gets real messy, real quick so tread carefully.</p>

