# Use Multi-Line Table Function or Stored Procedure
[Link to question](https://stackoverflow.com/questions/6998635/use-multi-line-table-function-or-stored-procedure)
**Creation Date:** 1312903397
**Score:** 2
**Tags:** sql-server, function, ms-access, stored-procedures
## Question Body
<p>I am in the process of rewriting an Access database and I have some awful MS Access queries that I need to rewrite.  They basically consist of the following set up</p>

<pre><code>SELECT *
FROM Query1, Query2, Query,...
</code></pre>

<p>These queries are used in 2 existing databases and typically consist of a Count/Sum of data.  Then we use the totals for reporting. Most of the subqueries are like this or something similar</p>

<pre><code>SELECT Count(Account), Reason, Sum(Amount)
FROM table1
GROUP BY Reason
</code></pre>

<p>This is easy enough to rewrite and that isn't my problem.  My problem is that I have about 20-30 of these queries that need to be rewritten.  One of the requests that the users have now is to be have the option to get the Counts of the accounts as well as the List of accounts that make up the total.  So now my 20-30 queries double because they want the lists as well.  </p>

<p>So I am trying to determine the best way to design this to be able to provide the count or list for any particular day they want</p>

<p>I was thinking of creating a multi-statement table function to do this but I don't know if that would be better than a stored proc or a view or anything else</p>

<p>I created the following function which allows them to search by any date and they can get either the list of accounts or the counts. </p>

<pre><code>CREATE FUNCTION [udf_GeBreakdown]  
(
    @BusinessDate       datetime
    , @ListOfAccounts   bit
)
RETURNS @TableCount
TABLE 
(
    Account int, ReasonName varchar(50), Amount money
)
AS
BEGIN

    DECLARE @PreviousDate smalldatetime
    SET @PreviousDate = udf_GetNextImportDate(@BusinessDate, -1);

    IF @ListOfAccounts = 0
        BEGIN       
            INSERT INTO @TableCount
            SELECT Count(Account), R.ReasonName, Sum(Amount)
            FROM Debs.Resolved RS
            INNER JOIN Debs.Reason R
                ON RS.ReasonId = R.ReasonId
            WHERE RS.DebitDate = @PreviousDate
                AND RS.StatusId NOT IN (15, 17)
            GROUP BY R.ReasonName
        END
    ELSE
        BEGIN
            INSERT INTO @TableCount
            SELECT Account, R.ReasonName, Amount
            FROM Debs.Resolved RS
            INNER JOIN Debs.Reason R
                ON RS.ReasonId = R.ReasonId
            WHERE RS.DebitDate = @PreviousDate
                AND RS.StatusId NOT IN (15, 17)

        END

    RETURN 
END
</code></pre>

<p>I don't know if this is a waste of time doing it this way or if I should just provide a list of accounts and then get my Count/Sum when I query this.  I am looking for some help and or direction on how best to proceed with this. </p>

## Answers
### Answer ID: 7001919
<p>Performance is going to be an issue in this multi-statement UDF.  </p>

<p>If you read from the system more than you write, I would try creating an <a href="http://msdn.microsoft.com/en-us/library/ms187864.aspx" rel="nofollow">indexed view</a> similar to the following.  </p>

<pre><code>CREATE VIEW V1 WITH SCHEMABINDING AS
SELECT RS.DebitDate, Account, R.ReasonName, Amount
FROM Debs.Resolved RS
INNER JOIN Debs.Reason R
    ON RS.ReasonId = R.ReasonId
WHERE RS.StatusId NOT IN (15, 17)

CREATE INDEX X on V1 -- based on usage
</code></pre>

<p>Then, use the following statement in a SP or single statement UDF to get the list of accounts.  The statement becomes pretty trivial at that point. (you will have to do your previous day logic here...don't store that function in the view)</p>

<pre><code>SELECT Count(Account), ReasonName, Sum(Amount)
FROM V1 with(noexpand)
GROUP BY DebitDate, ReasonName  -- or use DebitDate in the where clause
</code></pre>

<p>I would still try this if your system is write intensive, however this indexed view will slow down inserts on the tables that are schemabound to it.  Indexing views does come at a cost so you might be well served just creating a normal view. </p>

