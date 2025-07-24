# mariaDB query slow, only first client session
[Link to question](https://stackoverflow.com/questions/74375837/mariadb-query-slow-only-first-client-session)
**Creation Date:** 1668001406
**Score:** 0
**Tags:** sql, performance, mariadb
## Question Body
<p>Maybe just forget everything below...
After investigating, adding indexes we do get other results, and other queries becoming slow...
We really helps is this: Another VM (all the same image)
Open HeidiSQL, monitor the processes, explaining a query also might help. (No changes in the database) Then restart the machine, everything is fast. Just restarting without doing anything in HeidiSQL doesn't work.</p>
<p>In this database first some Temp(TMP) tables are filled (This are real tables!, not in memory temp tables). Then large stored-proc is executed to process the data from the temp tables to the other tables. Depending on the data in the TMP tables the query is very slow. (timeouts). Using HeidiSQL I figured out that one query was always busy.</p>
<p>After a client process kill the same scenario is fast, and stays fast. Even after restart of the machine the scenario stays fast..</p>
<p>In case of 4000 TMPproperty records and 1 TMPTransaction the query is fast. In case of 4000 TMPProperties and 100 TMPTransactions the query is very slow. Leading to timeouts in the client application.
I can image it has something to do with the join between TMPPropertyValue and TMPTransaction, but why only the first time?</p>
<p>Someone an idea what is wrong in the query?</p>
<pre><code>UPDATE TMPPropertyValue, PropertyValue AS PV
    INNER JOIN Object AS O ON PV.ObjectRowId = O.RowId
    INNER JOIN TMPObject AS TMPO ON O.ObjectId = TMPO.ObjectId
    INNER JOIN Transaction AS T ON T.RowId = PV.TransactionRowId
    INNER JOIN Datastore AS D ON P.DatastoreRowId = D.RowId, TMPTransaction AS TT
    SET TMPPropertyValue.Active = CASE
        WHEN TT.TransactionDateTime &gt; T.TransactionDateTime THEN 1
        WHEN TT.TransactionDateTime &lt; T.TransactionDateTime THEN 0
        ELSE
        CASE
            WHEN TT.DatastoreID &gt; D.DatastoreId THEN 1
            ELSE 0
        END
    END 
    WHERE TMPO.RowId = TMPPropertyValue.ObjectRowId
        AND TMPPropertyValue.TransactionRowId = TT.RowId
        AND TMPPropertyValue.Active IS NULL
        AND PV.PropertyRowId = TMPPropertyValue.PropertyRowId
        AND (TT.DatastoreId &lt;&gt; D.DatastoreId OR TT.TransactionSeqNr &lt;&gt; T.TransactionSeqNr)
        AND TMPPropertyValue.IsNew = 1;

</code></pre>
<p>I can't see what I must to rewrite this query, or indexed or so are needed? (As c# developer)</p>
<p>Update:
<em>Killing the client, I managed keep the tmptables content and reproduce the slow query by creating a select statement, also replaced the joins and ',' joins and where with all inner joins.</em></p>
<p>mariadb version 10.3.11</p>
<pre><code>SELECT * FROM TMPPropertyValue
    INNER JOIN TMPObject AS TMPO ON TMPPropertyValue.ObjectRowId = TMPO.RowId
    INNER JOIN Object AS O ON TMPO.ObjectId = O.ObjectId
    INNER JOIN PropertyValue AS PV ON PVA.ObjectRowId = O.RowId
    INNER JOIN Transaction AS T ON T.RowId = PVA.PerceptionRowId
    INNER JOIN Datastore AS D ON T.DatastoreRowId = D.RowId
     INNER JOIN TMPTransaction AS TT ON TMPPropertyValue.PerceptionRowId = TP.RowId
   WHERE PV.PropertyRowId = TMPPropertyValue.PropertyRowId
        AND (TP.DatastoreId &lt;&gt; D.DatastoreId OR TT.TransactionSeqNr &lt;&gt; T.TransactionSeqNr);
</code></pre>
<p>What really makes the query fast again is ommitting the JOIN with the Datastore table. This table is just 3 columns and about 10 records.<br />
A index adding on the key and foreign key doesn't influence the result. (Transaction.DatastoreRowId and Datastore.RowId)</p>
<p>the select return 4004 record and 84/87 columns, depending on datastore join</p>
<pre><code>CREATE TABLE `datastore` (
  `RowId` int(11) NOT NULL AUTO_INCREMENT,
  `DatastoreId` binary(16) NOT NULL,
  `IsSynchronizable` tinyint(1) NOT NULL,
  PRIMARY KEY (`RowId`),
  KEY `IDX_Datastore_DatastoreIdRowId` (`DatastoreId`,`RowId`),
  KEY `IDX_Datastore_RowIdDataStoreId` (`RowId`,`DatastoreId`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci

CREATE TABLE `Transaction` (
  `RowId` int(11) NOT NULL AUTO_INCREMENT,
  `DatastoreRowId` int(11) NOT NULL,
  `TransactionSeqNr` int(11) NOT NULL DEFAULT 1,
  `------
  PRIMARY KEY (`RowId`),
  UNIQUE KEY `IX_PerceptionActive_ContextDatastoreTransSeqNr` (`ContextRowId`,`DatastoreRowId`,`TransactionSeqNr`),
  KEY `IDX_Transaction_TransactionDateTime` (`TransactionDateTime`),
  KEY `IX_Transaction_ContextPerceptionSeqNrTransactionDateTime` (`ContextRowId`,`PerceptionSeqNr`,`TransactionDateTime`),
  KEY `Transaction_Host` (`HostRowId`),
  KEY `FK_Transaction_Datastore` (`DatastoreRowId`),
  KEY `FK_Transaction_User` (`UserRowId`),
  KEY `FK_Transaction_ClassificationDomain` (`ClassificationDomainRowId`),
  CONSTRAINT `FK_Transaction_ClassificationDomain` FOREIGN KEY (`ClassificationDomainRowId`) REFERENCES `classificationdomain` (`RowId`),
  CONSTRAINT `FK_Transaction_Context` FOREIGN KEY (`ContextRowId`) REFERENCES `context` (`RowId`),
  CONSTRAINT `FK_Transaction_Datastore` FOREIGN KEY (`DatastoreRowId`) REFERENCES `datastore` (`RowId`),
  CONSTRAINT `FK_Transaction_Host` FOREIGN KEY (`HostRowId`) REFERENCES `host` (`RowId`),
  CONSTRAINT `FK_Transaction_User` FOREIGN KEY (`UserRowId`) REFERENCES `perceptionuser` (`RowId`)
) ENGINE=InnoDB AUTO_INCREMENT=2208 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
</code></pre>
<p>The explain is the same in both situations
<a href="https://i.sstatic.net/mLBEs.png" rel="nofollow noreferrer">mariadb explain</a></p>

## Answers
### Answer ID: 74442798
<p>What finally fixed the issue:</p>
<ul>
<li>Changed several queries in the stored-proc using better join/cross joins, no mixing etc</li>
<li>Adding some indexes for the columns used in the joins.</li>
</ul>
<p><strong>But what finally did the fix: adding a &quot;Force Index&quot; for the specific query.</strong> (on the new index). (since it was sometimes slow and then after some investigating/trying out using heidisql fast)</p>

