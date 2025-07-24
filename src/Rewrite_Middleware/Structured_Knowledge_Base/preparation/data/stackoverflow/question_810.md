# How to write SQL query to count values that meets multiple column conditions with multiple column exclusions?
[Link to question](https://stackoverflow.com/questions/43398259/how-to-write-sql-query-to-count-values-that-meets-multiple-column-conditions-wit)
**Creation Date:** 1492104128
**Score:** 0
**Tags:** mysql, sql
## Question Body
<p>I'm using MySQL as the database.</p>

<p>I have a joined table with two fields ItemGroupID and CheckNumber that apply to this query.</p>

<p>A CheckNumber can contain multiple ItemGroupIDs, and ItemGroupIDs can contain multiple CheckNumbers</p>

<p>I'm attempting to count the number of checks that meet multiple conditions (has item group 281 and item group 274, but does not have item group 280 or 34 in any record. Here's a snippet of the joined table.</p>

<pre><code>ItemGroupID | CheckNumber
-----------   -----------
    281           101
    274           101
    103           101
    281           101
    280           102
    281           102
    274           102
    281           103
</code></pre>

<p>For the above table, the query should only return a count of 1 for CheckNumber 101 since it has both id 281 and 274, and it doesn't contain 280 or 34.The other check numbers should not return a count. CheckNumber 102 has an excluded GroupID on the check. CheckNumber 103 doesn't contain 281 AND 274.</p>

<p>Below is the query I've written. The issue with the query is that it doesn't exclude the checks with the ItemGroupID 280 or 34. I believe it's an issue with the Count function in GROUP BY. But I'm unsure how to rewrite it to fix this issue. </p>

<pre><code>SELECT COUNT(id.CheckNumber) AS Total
FROM ItemGroupMember igm
    INNER JOIN ItemDetail id ON igm.ItemID = id.ItemID
WHERE igm.ItemGroupID IN (281,274)
    AND NOT igm.ItemGroupID IN (280,34)
    AND id.DOB BETWEEN 3/14/2017 AND 3/14/2017
    AND id.LocationID = 22
GROUP BY id.CheckNumber HAVING COUNT(DISTINCT igm.ItemGroupID) = 2
</code></pre>

<p>Appreciate the help.</p>

## Answers
### Answer ID: 43398729
<p>how about:</p>

<p>Data:</p>

<pre><code>create table exp (
  ItemGroupID int,
  CheckNumber int
  );

  Insert into exp values (281, 101) ;
  Insert into exp values (274, 101) ;
  Insert into exp values (103, 101) ;
  Insert into exp values (281, 101) ;
  Insert into exp values (280, 102) ;
  Insert into exp values (281, 102) ;
  Insert into exp values (274, 102) ;
  Insert into exp values (281, 103) ;
</code></pre>

<p>Query:</p>

<pre><code>Select checknumber, count(*)
From exp
Where
exists (Select e1.ItemGroupID From exp e1 Where e1.checknumber = exp.checknumber and e1.ItemGroupID in (281))
and exists (Select e1.ItemGroupID From exp e1 Where e1.checknumber = exp.checknumber and e1.ItemGroupID in (274))
and not exists (Select e1.ItemGroupID From exp e1 Where e1.checknumber = exp.checknumber and e1.ItemGroupID in (280, 34))
Group by checknumber
</code></pre>

<p>Real data:</p>

<pre><code>Select checknumber, count(*)
From (Select * From ItemGroupMember igm INNER JOIN ItemDetail id ON igm.ItemID = id.ItemID WHERE id.DOB BETWEEN 3/14/2017 AND 3/14/2017 AND id.LocationID = 22) exp
Where
    exists (Select e1.ItemGroupID From (Select * From ItemGroupMember igm INNER JOIN ItemDetail id ON igm.ItemID = id.ItemID WHERE id.DOB BETWEEN 3/14/2017 AND 3/14/2017 AND id.LocationID = 22) e1 Where e1.checknumber = exp.checknumber and e1.ItemGroupID in (281))
    and exists (Select e1.ItemGroupID From (Select * From ItemGroupMember igm INNER JOIN ItemDetail id ON igm.ItemID = id.ItemID WHERE id.DOB BETWEEN 3/14/2017 AND 3/14/2017 AND id.LocationID = 22) e1 Where e1.checknumber = exp.checknumber and e1.ItemGroupID in (274))
    and not exists (Select e1.ItemGroupID From (Select * From ItemGroupMember igm INNER JOIN ItemDetail id ON igm.ItemID = id.ItemID WHERE id.DOB BETWEEN 3/14/2017 AND 3/14/2017 AND id.LocationID = 22) e1 Where e1.checknumber = exp.checknumber and e1.ItemGroupID in (280, 34))
Group by checknumber
</code></pre>

### Answer ID: 43398893
<pre><code>SELECT COUNT(id.CheckNumber) AS Total
FROM ItemDetail id
JOIN ItemGroupMember igm ON igm.ItemID = id.ItemID AND igm.ItemGroupID IN (281,274)
LEFT JOIN ItemGroupMember igm2 ON igm2.ItemID = id.ItemID AND igm2.ItemGroupID IN (280,34)
WHERE 
    id.DOB BETWEEN 3/14/2017 AND 3/14/2017
    AND id.LocationID = 22
    AND igm2.ItemID is null -- Make sure that you exclude any where the groupID is 280 or 34
group by id.CheckNumber having Total = 2;
</code></pre>

