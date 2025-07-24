# How to salvage SQL server 2008 query from KILLED/ROLLBACK state?
[Link to question](https://stackoverflow.com/questions/2820576/how-to-salvage-sql-server-2008-query-from-killed-rollback-state)
**Creation Date:** 1273680137
**Score:** 5
**Tags:** sql-server, sql-server-2008, stored-procedures, locking
## Question Body
<p>I have a stored procedure that inserts batches of millions of rows, emerging from a certain query, into an SQL database. It has one parameter selecting the batch; when this parameter is omitted, it will gather a list of batches and recursively call itself, in order to iterate over batches. In (pseudo-)code, it looks something like this:</p>

<pre><code>CREATE PROCEDURE spProcedure AS BEGIN
    IF @code = 0  BEGIN
        ...
        WHILE @@Fetch_Status=0 BEGIN
            EXEC spProcedure @code
            FETCH NEXT ... INTO @code
        END
    END
    ELSE BEGIN

        -- Disable indexes
        ...

        INSERT INTO table
        SELECT (...)

        -- Enable indexes
        ...
</code></pre>

<p>Now it can happen that this procedure is slow, for whatever reason: it can't get a lock, one of the indexes it uses is misdefined or disabled. In that case, I want to be able kill the procedure, truncate and recreate the resulting table, and try again. However, when I try and kill the procedure, the process frequently oozes into a KILLED/ROLLBACK state from which there seems to be no return. From Google I have learned to do an <code>sp_lock</code>, find the spid, and then kill it with <code>KILL &lt;spid&gt;</code>. But when I try to kill it, it tells me</p>

<blockquote>
  <p>SPID 75: transaction rollback in
  progress. Estimated rollback
  completion: 0%. Estimated time
  remaining: 554 seconds.</p>
</blockquote>

<p>I did find a <a href="http://www.sqlteam.com/forums/topic.asp?TOPIC_ID=103218" rel="noreferrer">forum message</a> hinting that another spid should be killed before the other one can start a rollback. But that didn't work for me either, plus I do not understand, why that would be the case... could it be because I am recursively calling my own stored procedure? (But it should be having the same spid, right?)</p>

<p>In any case, my process is just sitting there, being dead, not responding to kills, and locking the table. This is very frustrating, as I want to go on developing my queries, not waiting hours on my server sitting dead while pretending to be finishing a supposed rollback.</p>

<p>Is there some way in which I can tell the server not to store any rollback information for my query? Or not to allow any other queries to interfere with the rollback, so that it will not take so long? Or how to rewrite my query in a better way, or how kill the process successfully without restarting the server?</p>

## Answers
### Answer ID: 27144849
<p>Similarly, a transaction was executing, and user cancelled, freezing the SPID into KILLED\ROLLBACK... not changing IO / CPU.</p>

<p>Two other SPIDs where blocked by this SPID; which I killed.
Thus contention on locks was removed, allowing rollback to conclude.</p>

<p>Reverse logic - SPIDs blocked by SPID, block SPID rollback. </p>

<p>SQL for you :)</p>

### Answer ID: 2820648
<p>When you kill a SQL Server process, it doesn't die immediately, all the work done by that pocesses' active transaction must first be rolled back.  The rollback may take a substantial amount of time - maybe as much time as, or even more than, the query had used in execution prior to the kill.</p>

<p>I have also seen a bug occur where a killed/rolling back process remains indefinitely.  Fortunately in the case I saw this, no significant locks were being held by that process!</p>

<p>There are steps you could take to avoid this but I don't want to recommend anything like that without btter understanding your requirements and situation since it could adversely affect other proceses/queries.</p>

### Answer ID: 2821231
<p>A few comments.</p>

<p>First, gbn is correct with regard to not being able to cancel rollbacks in progress. This is how SQL keeps transactional integrity, and you wouldn't <em>want</em> that behavior changed. If you absolutely don't care and just want to get your DB back to where you were when the last backup was taken, then follow his steps.</p>

<p>One caveat, however. There are times I've seen where a spid <em>isn't really rolling back</em>, its just stuck (usually at 0% or 100% progress). The most reliable indicator in this case is if the CPU/IO counters for the spid in activity monitor are not changing (and the SPID isn't being blocked by another SPID). In this case, you might have to restart the SQL service (don't need to do an entire reboot) to clear the spid.</p>

<p>With regard to re-organizing your query so that these rollbacks don't cripple you, yes, its possible. Just use explicit transactions:</p>

<pre><code>    WHILE @@Fetch_Status=0 BEGIN
        BEGIN TRANS
            EXEC spProcedure @code
        COMMIT TRANS
        FETCH NEXT ... INTO @code
    END
</code></pre>

<p>The data is committed after each batch. If you experience an issue and have to kill the spid, it should only roll back the current batch it is working on.</p>

<p>If even a single batch is too much, you could probably refactor your "spProcedure" to insert in smaller batches of 10k-100k records, committing after each one.</p>

### Answer ID: 2820745
<p>Been here.  Last time for us was processing somewhere around 3.2 Billion records.  The initial statement went to 99% complete within ten minutes; then spent 20 hours on IO.  </p>

<p>The first time through it ran for about 8 hours, then an automated backup job killed the process and bounced the server.  It took nearly 2 days to get it back online so that we could start the process over.. This time making sure the backup process was turned off.</p>

### Answer ID: 2820628
<p>It's rolling back the transaction.</p>

<p>It will keep doing this even if you restart the instance.</p>

<p>If you were 99 million rows into a 100 million row insert or delete, all 99 million need rolled back. You cannot change this behavior. Any single DML statement is atomic.</p>

<p>If you want to fix it:</p>

<ul>
<li>Stop SQL Server</li>
<li>Delete the DB files</li>
<li>Start SQL Server</li>
<li>DROP the DB in its broken state</li>
<li>Restore</li>
</ul>

<p>YMMV of course :-)</p>

### Answer ID: 2820619
<p>As I understand it, not without potentially killing the consistency of the data file by doing something nasty like a hard reset, and then SQL will go into recovery state and still perform aspects of roll back to make sure the rolled back transactions is sucessfully rolled back.</p>

<p>Unless something like a nolock can get you past your existing lock (you've not mentioned if its exclusive lock) - you could probably still script the schema of the table, makes it MyTable2 - and then keep writing queries and go back and alter them when it's finished.</p>

