# Database lookup/dictionary tables - design issue - hardcoding GUIDs
[Link to question](https://stackoverflow.com/questions/5556769/database-lookup-dictionary-tables-design-issue-hardcoding-guids)
**Creation Date:** 1302028676
**Score:** 1
**Tags:** database, database-design
## Question Body
<p>Below question arose in my head when refactoring complex stored procedure that was a bottleneck in my database... Let me introduce to the topic. Suppose we have lookup/dictionary table like (it contains GUID as Foreign Key to other tables and name which is human readable):</p>

<pre><code>CREATE TABLE [dbo].[PlayerStatus](
    [PlayerStatusId] [uniqueidentifier] NOT NULL,
    [PlayerStatusName] [nvarchar](50) NOT NULL,
 CONSTRAINT [PK_PlayerStatus] PRIMARY KEY CLUSTERED 
(
    [PlayerStatusId] ASC
))
</code></pre>

<p>and there's a <strong>Player</strong> table :</p>

<pre><code>    CREATE TABLE [dbo].[Player](
[PlayerId] [uniqueidentifier] NOT NULL,
[PlayerStatusId] [uniqueidentifier] NOT NULL,
[PlayerName] [nchar](10) NOT NULL, 
[PlayerSurname] [nchar](10) NOT NULL, 
CONSTRAINT [PK_Player] PRIMARY KEY CLUSTERED  ( [PlayerId] ASC )) ON [PRIMARY]
</code></pre>

<p>Pretty sraightforward.</p>

<p>Let's say that somewhere in the code there's huge query that accesses a great deal of tables:</p>

<pre><code>SELECT ...
FROM Player JOIN PlayerStatus ON Player.PlayerStatusId = PlayerStatus.PlayerStatusId
.....
WHERE PlayerStatus.PlayerStatusName = 'Active' ....
</code></pre>

<p>Now, in my stored procedure, according to execution plan <strong>Players</strong> table was included in resultset at the beginning. Assuing that this is very large table with milions of rows, hash join between <strong>Player</strong> and <strong>PlayerStatus</strong> could be time consuming. By optimizing this query I could rewrite it to someting like this</p>

<pre><code>SELECT ...
FROM Player .....
WHERE PlayerStatus.PlayerStatusId = '46bb6a12-4cd9-4b6c-84c2-7444f5f45eb6' ....
</code></pre>

<p>And that's exactly what I did in my bottleneck procedure. That way, I removed 4 similar lookup/dictionary tables that contained different type of statuses. To my suprise, I managed to improve performance by 50%, even though I thought that such tables won't impact performance at all. But that's side plot. My question is: <strong>what do you thing of hardcoding guids?</strong></p>

<p><strong>EDIT</strong></p>

<ul>
<li>I do have PK indexes on PlayerStatus.PlayerStatusId and Player.PlayerId</li>
<li>I do have FK constraint on Player.PlayerStatusId:</li>
</ul>

<blockquote>
  <p>ALTER TABLE [dbo].[Player]  WITH CHECK
  ADD  CONSTRAINT
  [FK_Player_PlayerStatus] FOREIGN
  KEY([PlayerStatusId]) REFERENCES
  [dbo].[PlayerStatus]
  ([PlayerStatusId])</p>
</blockquote>

<ul>
<li>Player table constains about 2mln records, PlayerStatus table contains about 25 records</li>
</ul>

## Answers
### Answer ID: 5556889
<p>Answer - Don't hardcode the GUID. That leads to where is the criteria? In the status table. How to specify it? If string is immutable, fine, use that if you want, I prefer a logical IsActive flag. If performance is unacceptable, revisit - using info we discussed</p>

<p>Do you have a foreign key constraint?</p>

<p>If you are doing an inner join and DO NOT have a foreign key constraint, each row has to be matched (to satisfy the logic of the inner join) regardless of whether the column is consumed.</p>

<p>If you have a foreign key constraint to a unique column (a PK, obviously), the optimizer knows that there can be one and only one and it can eliminate the need to match because it knows it will be satisified.</p>

<p><a href="http://www.simple-talk.com/sql/t-sql-programming/constraint-yourself!/" rel="nofollow">Constraints are your friend.</a></p>

<p>As the other answer indicates, you also need an index on your status foreign key, and I would also review the execution plan to see what exactly is going on.</p>

<p>As far as hardcoding the GUID, it's unusual, since GUIDs are generally quite anonymous.</p>

<p>Also, I typically would have a logical column, like IsActive in the status, since you might have several "statuses" which are equivalent logically in certain circumstances, like Status IN ('Closed', 'Locked', 'Suspended', '') => IsInactive = 1, while only ('Locked') => IsLocked = 1.  FWIW, I tend not to use a single status string, but to use physical flags for individual states on accounts and then logical combinations of these as logical flags for query criteria.</p>

<p>I re-read what you posted and as far as your execution plan, this is going to change depending on the statistics in the table.  I double very much that the plan would be the same for 100 Players as it would be for 1 Million players - definitely check that before you try to do any premature optimization.  Also, in testing, be sure statistics are updated - sometimes a plan which is good for a million rows will freak out for one row.</p>

### Answer ID: 5557320
<p>Hard coding GUIDs or other numeric IDs may not look very elegant, but from my experience sometimes it proved to be quite beneficial as far as <b>performance</b> is concerned.</p>

<p>Your example is quite simple, but if you had a more complex query with many joins, removing one join could speed up the query. An example in your code would be removing join with PlayerStatus and filter using PlayerStatusID from Player table instead of using PlayerStatusName from PlayerStatus.</p>

<p><br />
There are two more thing to consider when it comes to hard coding GUIDs/IDs:</p>

<ol>
 <li> GUID/ID is usually a PK in a table and referenced by FK, so it's harder to change GUID/ID than it is to change i.e. status name. Changing PlayerStatusName in your example from 'Active' to 'In action' would make your query using PlayerStatusName useless. So using GUIDs/IDs guarantees that queries are based on solid columns (PKs, FKs)
 <li> Using GUIDs/IDs in queries requires little discipline if you have multiple environments for example. You need to make sure relevant IDs in tables holding dictionaries (i.e. PlayerStatus) are the same across all database instances.
</ol>

### Answer ID: 5557221
<p>Please keep in mind, clustered indexes are not suggested on GUID columns. Convert your clustered indexes to regular PK indexes and run your queries again. You might notice the difference.</p>

