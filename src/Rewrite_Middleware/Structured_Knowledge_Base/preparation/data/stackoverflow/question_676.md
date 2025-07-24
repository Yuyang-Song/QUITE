# Saving database data changes in commits (if not sqlite)
[Link to question](https://stackoverflow.com/questions/367273/saving-database-data-changes-in-commits-if-not-sqlite)
**Creation Date:** 1229304809
**Score:** 1
**Tags:** database, version-control
## Question Body
<p>We have a Rails project that uses PostgreSQL-specific queries, so it's uncomfortable to use sqlite even in development mode. The problem is, I'd love to track schema changes in database and omit running migrations on request, and I'd also love to track db-data changes with git, so that I wouldn't need to dump the db and load it on my machine. So basically I only want to do 'git pull' and see the application working with the new schema and data.</p>

<p>What are the possible strategies here?
The only that comes to my mind is to use a simple wrapper that takes an sql-query, checks if it has any db-specific parts and rewrites it for development environment, so that we could still use sqlite. What else?</p>

## Answers
### Answer ID: 8135956
<p>If I understand correctly, you want to be able to track both schema and data changes.</p>

<p>These are, in fact, two very different things - </p>

<ul>
<li><strong>Schema changes</strong> - this is discussed in several other questions (<a href="https://stackoverflow.com/questions/1294758/how-do-you-maintain-revision-control-of-your-database-structure">here</a>, <a href="https://stackoverflow.com/questions/308/is-there-a-version-control-system-for-database-structure-changes">here</a> and <a href="https://stackoverflow.com/questions/1607/mechanisms-for-tracking-db-schema-changes">here</a>).
The main take from the answers to these questions is that you can either dump your schema to SQL files and track them with your regular source control (git, svn, etc.) or you can use a DB specific SW (red-gate, dbmaestro). 
However, this won't allow you to completely re-create an identical copy of a DB on another server. Which brings me to - </li>
<li><strong>Data changes</strong> - This is harder, because (like @jonathan wrote) it's difficult track the changes the DB makes to it's files. I suggest you checkout <a href="http://off-scale.com" rel="nofollow noreferrer">OffScale DataGrove</a>. DataGrove tracks changes to the entire DB (structure+data). You can tag versions in any point in time, and return to older states of the DB with a simple command. It also allows you to create virtual, separate, copies of the same database so each team member can have his own separate DB. All the virtual copies are tracked into the same repository so it's super-easy to revert your DB to someone else's version (what you called "git-pull").</li>
</ul>

<p><em>Disclaimer -  I work at OffScale :-)</em></p>

### Answer ID: 367602
<p>I'm not sure I understand all the nuances of your question - particularly the comments about using SQLite vs PostgreSQL.  If it is to be a multi-DBMS system, then testing with multiple systems is good; if it is to be a single-DBMS system, then working with multiple DBMS is making life pointlessly hard.</p>

<p>Also, you talk about tracking the schema changes in the database...is this storing the information about schema changes separately from DBMS's own system catalog, or do you really mean that you want to track database schema changes (using something outside the database - such as a VCS)?</p>

<p>You also talk about tracking 'DB-data changes' which I take to mean 'the data in the tables in the database'.  Again, I'm not clear if you are thinking of some sort of dump of the data from the database that covers the differences between what was there, say, a day ago and what is there now, or something else.</p>

<p>These issues might be why you didn't get a response for over 4 hours.</p>

<p>When you talk about a 'simple wrapper', you are not talking about something that I'd call simple.  It has to parse arbitrary SQL, work out whether any of it is DBMS-specific, and then apply rewrite rules.  That is a non-trivial undertaking.  Getting the wrapper called in the right places could be non-trivial too - it depends on the set of APIs you are using to access the DBMS, amongst other things.</p>

<p>What else?</p>

<ul>
<li>Use the same DBMS in both production and development?</li>
<li>Tracking just schema changes is non-trivial.  You need to track the essence of the schema (such as table name, column names, etc) and not the accidence (yeah, I was rereading Brooks' "No Silver Bullet" earlier) such as the TabID (which might vary without the schema being materially different).  However, an analysis would tell you whether the schema is different.</li>
<li>Tracking the data changes, independent of schema changes, is also non-trivial.  In general, the volume of such data is large.  You may be able to deal with a full archive or a full unload or export of the database - but ensuring that the data is presented in the same sequence each time may require some care on your part.  If you don't ensure the correct sequencing, the VCS will be recording huge changes due to ordering differences.</li>
</ul>

<p>All the above amounts to the dreaded "<em>it depends</em>" answer.  It depends on:</p>

<ul>
<li>Your DBMS</li>
<li>Your database size</li>
<li>The volatility of your schema</li>
<li>The volatility of your data</li>
</ul>

<p>It only marginally depends on your VCS or platform, fortunately.</p>

