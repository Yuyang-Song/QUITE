# How to efficiently check if a database contains an identical record to a pending insert?
[Link to question](https://stackoverflow.com/questions/9296406/how-to-efficiently-check-if-a-database-contains-an-identical-record-to-a-pending)
**Creation Date:** 1329320596
**Score:** 2
**Tags:** sql, sql-server, performance, indexing
## Question Body
<p>I have some records that I want to "insert or update" into a SQL Server database, via a stored procedure.  These records have a globally unique and stable ID, and a bunch of value attributes (about a dozen).</p>

<p>Checking for insert is straightforward enough - see if the key doesn't exist in the table.</p>

<p>Assuming that the key does exist, I then need to check whether the existing record contains exactly the same values as the current data that I'm passing into the procedure.  At the moment I'm doing this via:</p>

<pre><code>SELECT @identical = CASE WHEN COUNT(*) &gt; 0 THEN 1 ELSE 0 END FROM Table
    WHERE idCol = @newId
      AND valueCol1 = @newValue1
      AND valueCol2 = @newValue2
      AND ...
</code></pre>

<p>This works, but it's not very efficient; I'm able to insert about 70 records per second which is a lot slower than I'd expect.</p>

<p>My first thought was to add an index - but this will be indexing almost every column in the table.  Would that even make sense or would it just be a second copy of the table?  (The ID column is a clustered PK if that's relevant.)</p>

<p>Is there any sensible way to speed up a query that has to check the values of every column?  I'm considering using some sort of hash to detect duplicates, but this adds some space overhead, complexity to the sprocs and small (acceptable) possibility of false positives, so I'd much rather a solution based on indices or rewriting the SQL if one exists.</p>

## Answers
### Answer ID: 9298671
<p>Here is a classic solution</p>

<pre><code>if exists (select * from thetable where idCol = @newID)
begin
    update ....
end
else
begin
   insert ...
end
</code></pre>

### Answer ID: 9297225
<p>Don't test beforehand, just let the where-clauses do the work for you. pseudocode(your syntax may vary)</p>

<pre><code>UPDATE thetable
   SET valueCol1 = @newValue1
     , valueCol2 = @newValue2
     , ...
WHERE idCol = @newId
  AND (valueCol1 &lt;&gt; @newValue1
      OR valueCol2 &lt;&gt; @newValue2
      OR ...
      );

IF (ROWCOUNT &gt; 0) RETURN;

INSERT INTO thetable (idCol, valueCol1, valueCol2, ...)
VALUES (@newId, @newValue1,  @newValue2, ... )
WHERE NOT EXISTS ( SELECT * FROM thetable nx
    WHERE nx.idCol = @newId
    );
</code></pre>

### Answer ID: 9296456
<p>You can use a MERGE statement if you are using SQL Server 2008</p>

