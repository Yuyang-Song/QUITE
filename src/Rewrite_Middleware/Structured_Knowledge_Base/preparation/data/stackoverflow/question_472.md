# Looking for an SQL Rewriting Solution
[Link to question](https://stackoverflow.com/questions/27695706/looking-for-an-sql-rewriting-solution)
**Creation Date:** 1419885758
**Score:** 1
**Tags:** sql-server, vb.net
## Question Body
<p>About 5 years ago, some very long SQL procedures were created by a guy who worked here.</p>

<p>These procedures were used in an ASP.NET database with VB code. Textbox values were hard coded as values for all database entries, regardless of the type the fields needed.</p>

<p>Example:</p>

<pre><code>dim sqlCommand as String = "EXEC dbo.StoredProcedureN N'" &amp; textbox1.Value &amp; "'"
dim oledb as New OleDbCommand(sqlCommand)
</code></pre>

<p>All of this was wrapped in a Try/Catch block. If an exception was raised, the webpage would display "No records found."</p>

<p>Since our database is a Microsoft SQL database, I replaced the <code>OleDbCommand</code> objects with <code>SqlCommand</code> object. I also know the <code>SqlClient</code> namespace and what it will and will not do. Not so with the <code>OleDb</code> package.</p>

<p>Then, I cleaned up the VB code by declaring all of the stored procedure calls and matching those parameters to what is declared in the database.</p>

<p>Example:</p>

<pre><code>Using cmd = new SqlCommand("StoredProcedureN")
  cmd.Parameters.Add("@value1", SqlDbType.NVarChar, 50).Value = textbox1.Value
</code></pre>

<p>So, that's great, except now we are learning that many of these stored procedures have been failing where we had thought there were no records.</p>

<p>Here are 2 errors I am faced with right now:</p>

<blockquote>
  <p>The conversion of a varchar data type to a datetime data type resulted in an out-of-range value.</p>
</blockquote>

<p>and</p>

<blockquote>
  <p>Subquery returned more than 1 value. This is not permitted when the subquery follows =, !=, &lt;, &lt;=, >, >= or when the subquery is used as an expression.</p>
</blockquote>

<p>Now, the problem I have is that I am <strong>NOT</strong> good at understanding what he was trying to do in his Stored Procedures.</p>

<p>Looking at his code, it almost seems like the whole thing could have been written with a single query, and hence turned into a <strong>View</strong>, but my SQL skills are not good enough for me to understand how to write all of this in a few short steps.</p>

<p>I really need these stored procedures fixed up so that we can maintain this code as we migrate the database from an older Windows 2003 server to our new server.</p>

<p>I have created an SQL Fiddle that creates the schema for all tables used in this stored procedure:</p>

<p><a href="http://sqlfiddle.com/#!3/1a6c2/2/1" rel="nofollow">http://sqlfiddle.com/#!3/1a6c2/2/1</a></p>

<p>For those wanting to just see the SQL:</p>

<pre><code>ALTER PROCEDURE [dbo].[PtsInitialView20141229](@afeNum nvarchar(50)) AS BEGIN
  SET NOCOUNT ON;
  DECLARE @ptsSummary TABLE (
  costCodeDesc NVarChar(50),
  costCode NVarChar(50),
  userDesc NVarChar(50),
  approvedAmt Money,
  commitTotal Money,
  stotal Money,
  estCost Money,
  finalCost Money,
  amountDiff Money,
  percentDiff Decimal(18,2),
  noteID Int,
  lastInvoiceTran Char(12),
  lastUserSave Char(12),
  updateIndicator Int
  );
  DECLARE @mproSummary TABLE (
  detCostCode NVarChar(50),
  mproTotal Money
);
DECLARE @ptsUserSummary TABLE ( -- Summarize user table by AFE number and cost code
  userCostCode NVarChar(50),
  userDescribe NVarChar(50),
  userEstimate money,
  userNoteID int,
  userNote NVarChar(MAX)
);
DECLARE @lawsonApproved TABLE ( -- Summarize Lawson Activity table budget by afe and cost code line items
  lawActCostCode NVarChar(50),
  lawActAmount money
);
DECLARE @ptsUserNoteSummary TABLE (
  noteCostCode NVarChar(50),
  userNoteID [int] IDENTITY (1,1) NOT NULL,
  noteText NVarChar(MAX)
);

INSERT INTO @ptsSummary (costCodeDesc, costCode, stotal, lastInvoiceTran) 
  SELECT LEFT(A.description, 20), L.acctCategory, CONVERT(money, SUM(L.tranAmount)), MAX(L.runDate) 
  FROM dbo.lawAPdata L, dbo.mpro_actCodes A 
  WHERE activity = @afeNum and L.acctCategory = A.actCode 
  GROUP BY A.description, L.acctCategory;

INSERT INTO @mproSummary (mproTotal, detCostCode) 
  SELECT SUM((pdqty-pdccqty)*pdprice), pdafecat 
  FROM mpro_detail 
  WHERE pdponum IN (SELECT phponum FROM dbo.mpro_header WHERE (phafeno=@afeNum)) 
  GROUP BY pdafecat;

INSERT INTO @ptsUserSummary (userCostCode, userDescribe, userEstimate) 
  SELECT costCode, userDescription, EstimatedFinal 
  FROM dbo.ptsUserTableMay09 
  WHERE afeNumber=@afeNum;

INSERT INTO @lawsonApproved (lawActCostCode, lawActAmount) 
  SELECT activityCode, acAmount 
  FROM dbo.lawACApproved 
  WHERE afeNumber=@afeNum;

UPDATE @ptsSummary 
  SET commitTotal=(SELECT mproTotal FROM @mproSummary WHERE detCostCode=costCode);

INSERT INTO @ptsSummary (costCodeDesc, costCode, approvedAmt, stotal, estCost, finalCost) 
  SELECT LEFT(A.description,20), L.lawActCostCode, L.lawActAmount, '0', '0', '0' 
  FROM dbo.mpro_actCodes A, @lawsonApproved L 
  WHERE L.lawActCostCode = A.actCode AND L.lawActCostCode NOT IN (SELECT costCode from @ptsSummary);

INSERT INTO @ptsSummary (costCodeDesc, costCode, approvedAmt, commitTotal, stotal, estCost, finalCost) 
  SELECT LEFT(A.description, 20), L.detCostCode, '', L.mproTotal, '', '', '' 
  FROM dbo.mpro_actCodes A, @mproSummary L 
  WHERE L.detCostCode = A.actCode AND L.detCostCode NOT IN (SELECT costCode from @ptsSummary);

UPDATE @ptsSummary 
  SET approvedAmt=(SELECT SUM(lawActAmount) 
  FROM @lawsonApproved 
  WHERE lawActCostCode=costCode 
  GROUP BY lawActCostCode);

UPDATE @ptsSummary 
  SET finalCost = (SELECT SUM(userEstimate) 
  FROM @ptsUserSummary 
  WHERE UserCostCode=costCode 
  GROUP BY userCostCode);

UPDATE @ptsSummary 
  SET commitTotal = (SELECT mproTotal FROM @mproSummary WHERE detCostCode=costCode);

INSERT INTO @ptsSummary (costCodeDesc, costCode, userDesc, stotal, finalCost) 
  SELECT LEFT(A.description, 20), U.userCostCode, U.userDescribe, '0', U.userEstimate 
  FROM @ptsUserSummary U, dbo.mpro_actCodes A 
  WHERE U.userCostCode = A.actCode and userCostCode not in (SELECT costCode from @ptsSummary);

UPDATE @ptsSummary 
  SET userDesc=(SELECT userDescribe FROM @ptsUserSummary WHERE userCostCode=costCode);

UPDATE @ptsSummary 
  SET lastUserSave=(SELECT MAX(lastModified) FROM dbo.ptsUserHistoryMay09 WHERE afeNumber=@afeNum);

INSERT INTO @ptsUserNoteSummary (noteCostCode, noteText) 
  SELECT costCode, lineNote 
  FROM dbo.ptsUserNoteTable 
  WHERE afeNumber=@afeNum 
  ORDER BY costCode ASC;

UPDATE @ptsSummary 
  SET noteID=(SELECT userNoteID FROM @ptsUserNoteSummary WHERE noteCostCode=costCode);

UPDATE @ptsSummary 
  SET estCost=(finalCost - stotal);

UPDATE @ptsSummary 
  SET estCost=0 WHERE estCost IS NULL;

UPDATE @ptsSummary 
  SET finalCost=0 WHERE finalCost IS NULL;

UPDATE @ptsSummary 
  SET approvedAmt=0 WHERE approvedAmt IS NULL;

UPDATE @ptsSummary SET updateIndicator=
    CASE
        WHEN lastInvoiceTran Is NULL THEN 0
        WHEN costCode = '99998' THEN 0
        WHEN CAST(lastInvoiceTran AS DATETIME) &lt;= CAST(lastUserSave AS DATETIME) THEN 0
        ELSE 1
    END;

UPDATE @ptsSummary SET amountDiff= 
    CASE 
        WHEN ((stotal+estCost)&lt;approvedAmt) THEN (approvedAmt*-1)+(stotal+estCost)
        ELSE (stotal+estCost) - approvedAmt
    END;

UPDATE @ptsSummary SET percentDiff=
    CASE 
        WHEN (approvedAmt != 0) THEN amountDiff/(approvedAmt/100)
        ELSE '0'
    END;

SELECT costCode + ' - ' + costCodeDesc AS costCodeDesc, costCode, userDesc, CAST(approvedAmt AS decimal(18,0)) AS approvedAmt, CAST(commitTotal AS decimal(18,0)) AS commitTotal, CAST(stotal AS decimal(18,0)) AS stotal, CAST(estCost AS decimal(18,0)) AS estCost, CAST(finalCost AS decimal(18,0)) AS finalCost, CAST(amountDiff AS decimal(18,0)) AS amountDiff, CAST(percentDiff AS decimal(18,0)) AS percentDiff, noteID, updateIndicator 
FROM @ptsSummary 
ORDER BY costCode ASC;

END
</code></pre>

<p>Can this Stored Procedure be written as a View?</p>

<p>No? Then what parts can be cleaned up so that the developers that are left here know how to read it? Everyone seems to be getting lost in all of the temporary tables that are being created in RAM.</p>

<p>Some parts of it I don't understand, like this <code>INSERT</code> command:</p>

<pre><code>INSERT INTO @ptsSummary (costCodeDesc, costCode, stotal, lastInvoiceTran) 
  SELECT LEFT(A.description, 20), L.acctCategory, CONVERT(money, SUM(L.tranAmount)), MAX(L.runDate) 
  FROM dbo.lawAPdata L, dbo.mpro_actCodes A 
  WHERE activity = @afeNum and L.acctCategory = A.actCode 
  GROUP BY A.description, L.acctCategory;
</code></pre>

<p>Is this the sort of join those two tables getting?</p>

<pre><code>FROM dbo.lawAPdata L JOIN dbo.mpro_actCodes A ON (L.acctCategory=A.actCode)
</code></pre>

<p>It would be great if some SQL guro could look at this and say, "Oh yeah! That's easy to rewrite. It factors down to something simple like this...."</p>

## Answers
### Answer ID: 27696208
<p>Her we go</p>

<p>1- change this statement</p>

<pre><code>UPDATE @ptsSummary 
  SET commitTotal=(SELECT mproTotal FROM @mproSummary WHERE detCostCode=costCode);
</code></pre>

<p>to</p>

<pre><code>UPDATE s set s.commitTotal=p.mproTotal
FROM  @ptsSummary s 
INNER JOIN @mproSummary p on p.detCostCode=s.costCode
</code></pre>

<p>2- change the following statement</p>

<pre><code>UPDATE @ptsSummary 
  SET approvedAmt=(SELECT SUM(lawActAmount) 
  FROM @lawsonApproved 
  WHERE lawActCostCode=costCode 
  GROUP BY lawActCostCode);
</code></pre>

<p>to</p>

<pre><code>UPDATE s set s.approvedAmt=p.Total
FROM @ptsSummary s
INNER JOIN (SELECT lawActCostCode,SUM(lawActAmount) as Total
            FROM @lawsonApproved 
            GROUP BY lawActCostCode) as p
WHERE p.lawActCostCode=s.costCode;
</code></pre>

<p>3- this statement was repeated twice, delete the second one</p>

<pre><code>UPDATE @ptsSummary 
  SET commitTotal = (SELECT mproTotal FROM @mproSummary WHERE detCostCode=costCode);
</code></pre>

<p>4- change the following statement</p>

<pre><code>UPDATE @ptsSummary 
  SET finalCost = (SELECT SUM(userEstimate) 
  FROM @ptsUserSummary 
  WHERE UserCostCode=costCode 
  GROUP BY userCostCode);
</code></pre>

<p>to</p>

<pre><code>UPDATE s set s.finalCost=p.Total
FROM @ptsSummary s
INNER JOIN (SELECT userCostCode, SUM(userEstimate) as Total
  FROM @ptsUserSummary 
  GROUP BY userCostCode) as p
WHERE p.UserCostCode=s.costCode 
</code></pre>

<p>and you can apply this to all the updates that contains group by</p>

<p>and regarding to this statement</p>

<pre><code>INSERT INTO @ptsSummary (costCodeDesc, costCode, stotal, lastInvoiceTran) 
  SELECT LEFT(A.description, 20), L.acctCategory, CONVERT(money, SUM(L.tranAmount)), MAX(L.runDate) 
  FROM dbo.lawAPdata L, dbo.mpro_actCodes A 
  WHERE activity = @afeNum and L.acctCategory = A.actCode 
  GROUP BY A.description, L.acctCategory;
</code></pre>

<p>it seems that A is just a lookup table used to get the description field and this can be re-written in this way</p>

<pre><code>INSERT INTO @ptsSummary (costCodeDesc, costCode, stotal, lastInvoiceTran) 
  SELECT LEFT(A.description, 20), L.acctCategory, CONVERT(money, SUM(L.tranAmount)), MAX(L.runDate) 
  FROM dbo.lawAPdata L
  INNER JOIN dbo.mpro_actCodes A ON L.acctCategory= A.actCode
  WHERE activity = @afeNum
  GROUP BY A.description, L.acctCategory;
</code></pre>

<p><strong>EDITED HERE</strong></p>

<p>these statements can be trimmed and use constraints and default values in the declarations</p>

<pre><code>UPDATE @ptsSummary 
  SET estCost=(finalCost - stotal);

UPDATE @ptsSummary 
  SET estCost=0 WHERE estCost IS NULL;

UPDATE @ptsSummary 
  SET finalCost=0 WHERE finalCost IS NULL;

UPDATE @ptsSummary 
  SET approvedAmt=0 WHERE approvedAmt IS NULL;
</code></pre>

<p>hope this will help a little, but i need time to decrypt this code :P </p>

