# Grouping ranges of data
[Link to question](https://stackoverflow.com/questions/72221836/grouping-ranges-of-data)
**Creation Date:** 1652387945
**Score:** -2
**Tags:** sql
## Question Body
<p>I have segmented linear data to identify the minimum and maximum begin and end values of each range, now I want to consolidate overlapping ranges.  This is easy if the data is easy.  For example, if the data is always increasing for both the begin and end values.  (see the first 4 rows in my sample input below)  But where the data is not as uniform, I'm having trouble computing the begin and end of a group of overlapping rows by relating data sets.</p>
<p>It's possible I'm headed down a rabbit hole because of an early decision about how to structure my inputs.  The source data doesn't contain the rangebegin and rangeend columns I'm using for inputs.  This was my choice to try to help me analyze the data.  There may be other options.</p>
<p>Since the volume of information below may be an XY problem, here are the basics of what I'm trying to solve.</p>
<p>In my case, I'm trying to identify one-mile segments of roadway where there have been at least 5 crashes, then combine overlapping ranges to draw as a single geometric feature on a map.  So...</p>
<p>Given this data:<br />
Crash A at mile 2.22<br />
Crash B at mile 2.24<br />
Crash C at mile 3.10<br />
Crash D at mile 3.92<br />
Crash E at mile 5.03<br />
Crash F at mile 5.21</p>
<p>I would have a segment from 2.22 to 3.92 because there is less than a mile between each crash in that range.  Then there's a gap of more than a mile, then the last two crashes are within a mile of each other.  So the output would look like</p>
<div class="s-table-container">
<table class="s-table">
<thead>
<tr>
<th>begin</th>
<th>end</th>
</tr>
</thead>
<tbody>
<tr>
<td>2.22</td>
<td>3.92</td>
</tr>
<tr>
<td>5.03</td>
<td>5.21</td>
</tr>
</tbody>
</table>
</div>
<p>Because of some other variables, the way I am combining the data thus far has produced some ranges that are not sequential.  Some of the ranges are included in other ranges.  That seems to be causing my biggest problems.</p>
<p>I'm using SQL Server (mostly 2016), but the concept should hold for any database system.</p>
<p>--- <strong>Update</strong> ---</p>
<p>I am rewriting the question to refer to a &quot;known good&quot; solution as a starting point.</p>
<p>SO moderators:  If rewriting this question after receiving answers is wrong, let's fix it.</p>
<p><strong>tl;dr:</strong>  I'm developing a query that will likely ultimately be written as a <strong>series of common table expressions</strong> to serve as a data set for a reporting system.  I am using a reporting system, not a database management tool like SSMS, so I can't run a &quot;batch&quot;.  I also don't believe a temporary stored procedure is appropriate, nor do I want to create objects (stored procedures, functions,...) on the database server to solve this single reporting problem.  I do realize that the nature of the problem may dictate that I do these things, but <strong>I am searching for a query-only solution first.</strong></p>
<p>On the surface, this problem appears to be a classic gaps-and-islands problem, for which I have been using a similar solution for years.  But this one involves not only overlapping ranges, but also ranges that don't sort well and so don't work with the classic solution.  Starting with <a href="https://bertwagner.com/posts/gaps-and-islands/" rel="nofollow noreferrer">https://bertwagner.com/posts/gaps-and-islands/</a>, as recommended by Josh presents a problem.  Other overlapping gaps-and-islands solutions I have seen appear to be the same, and so have the same problem.  Replacing the last line of inputs in Bert Wagner's solution with...</p>
<pre><code>SELECT '11/2/2017', '11/4/2017' UNION ALL
SELECT '10/27/2017', '11/15/2017' UNION ALL
SELECT '11/5/2017', '11/10/2017'
</code></pre>
<p>...helps demonstrate my problem.</p>
<p>Bert's solution is written as a deeply-nested set of subqueries.  To improve readability, I would do this as a series of common table expressions.</p>
<p>In an attempt to demonstrate the problem and keep each step in my attempt simple and reproducible, I have broken this down to a series of temporary tables, each with its own outputs.  These temporary tables equate to the common table expressions.</p>
<pre><code>DROP TABLE IF EXISTS #OverlappingDateRanges;
CREATE TABLE #OverlappingDateRanges (StartDate date, EndDate date);

INSERT INTO #OverlappingDateRanges
SELECT '8/24/2017', '9/23/2017'  UNION ALL
SELECT '8/24/2017', '9/20/2017'  UNION ALL 
SELECT '9/23/2017', '9/27/2017'  UNION ALL 
SELECT '9/25/2017', '10/10/2017' UNION ALL
SELECT '10/17/2017','10/18/2017' UNION ALL 
SELECT '10/25/2017','11/3/2017'  UNION ALL
SELECT '11/2/2017', '11/4/2017' UNION ALL
SELECT '10/27/2017', '11/15/2017' UNION ALL
SELECT '11/5/2017', '11/10/2017'

SELECT * FROM #OverlappingDateRanges;
</code></pre>
<pre><code>StartDate  EndDate
---------- ----------
2017-08-24 2017-09-23
2017-08-24 2017-09-20
2017-09-23 2017-09-27
2017-09-25 2017-10-10
2017-10-17 2017-10-18
2017-10-25 2017-11-03
2017-11-02 2017-11-04
2017-10-27 2017-11-15
2017-11-05 2017-11-10
</code></pre>
<pre><code>DROP TABLE IF EXISTS #Groups;
SELECT ROW_NUMBER() OVER(ORDER BY StartDate,EndDate) AS RN
, StartDate
, EndDate
, LAG(EndDate,1) OVER (ORDER BY StartDate, EndDate) AS PreviousEndDate
INTO #Groups
FROM #OverlappingDateRanges;

SELECT *
FROM #Groups;
</code></pre>
<pre><code>RN     StartDate  EndDate    PreviousEndDate
------ ---------- ---------- ---------------
1      2017-08-24 2017-09-20 NULL
2      2017-08-24 2017-09-23 2017-09-20
3      2017-09-23 2017-09-27 2017-09-23
4      2017-09-25 2017-10-10 2017-09-27
5      2017-10-17 2017-10-18 2017-10-10
6      2017-10-25 2017-11-03 2017-10-18
7      2017-10-27 2017-11-15 2017-11-03
8      2017-11-02 2017-11-04 2017-11-15
9      2017-11-05 2017-11-10 2017-11-04    &lt;-- Notice PreviousEndDate &lt; StartDate
</code></pre>
<pre><code>DROP TABLE IF EXISTS #Islands;
SELECT *
, CASE WHEN PreviousEndDate &gt;= StartDate THEN 0 ELSE 1 END AS IslandStartInd
, SUM(CASE WHEN PreviousEndDate &gt;= StartDate THEN 0 ELSE 1 END) OVER (ORDER BY RN) AS IslandId
INTO #Islands
FROM #Groups g;

SELECT *
FROM #Islands;
</code></pre>
<pre><code>RN     StartDate  EndDate    PreviousEndDate IslandStartInd IslandId
------ ---------- ---------- --------------- -------------- -----------
1      2017-08-24 2017-09-20 NULL            1              1
2      2017-08-24 2017-09-23 2017-09-20      0              1
3      2017-09-23 2017-09-27 2017-09-23      0              1
4      2017-09-25 2017-10-10 2017-09-27      0              1
5      2017-10-17 2017-10-18 2017-10-10      1              2
6      2017-10-25 2017-11-03 2017-10-18      1              3
7      2017-10-27 2017-11-15 2017-11-03      0              3
8      2017-11-02 2017-11-04 2017-11-15      0              3
9      2017-11-05 2017-11-10 2017-11-04      1              4        &lt;-- This is within IslandId = 3
</code></pre>
<pre><code>SELECT MIN(StartDate) AS IslandStartDate
, MAX(EndDate) AS IslandEndDate
FROM #Islands
GROUP BY IslandId
ORDER BY IslandStartDate;
</code></pre>
<pre><code>IslandStartDate IslandEndDate
--------------- -------------
2017-08-24      2017-10-10
2017-10-17      2017-10-18
2017-10-25      2017-11-15
2017-11-05      2017-11-10   &lt;-- This is not a distinct island.
</code></pre>
<p>As you can see, the 4th island should be included in the third.</p>
<p>And reviewing Bert's example again in detail, and rewriting it (I'm a tactile learner) has given me some other thoughts regarding how I might solve this.  I am posting this here first to be fair to others who may have spent time reading and working on this and care about SO points.</p>

## Answers
### Answer ID: 72266739
<p>Since we're sorting by StartDate and EndDate, we should be able to use the minimum of this and all future start dates and the maximum of this and all past end dates.  This is just one more step beyond <a href="https://bertwagner.com/posts/gaps-and-islands/" rel="nofollow noreferrer">what Bert Wagner published</a>.</p>
<pre><code>DROP TABLE IF EXISTS #OverlappingDateRanges;
CREATE TABLE #OverlappingDateRanges (StartDate date, EndDate date);

INSERT INTO #OverlappingDateRanges
SELECT '8/24/2017', '9/23/2017'  UNION ALL
SELECT '8/24/2017', '9/20/2017'  UNION ALL 
SELECT '9/23/2017', '9/27/2017'  UNION ALL 
SELECT '9/25/2017', '10/10/2017' UNION ALL
SELECT '10/17/2017', '10/18/2017' UNION ALL 
SELECT '10/25/2017', '11/3/2017'  UNION ALL
SELECT '11/2/2017', '11/4/2017' UNION ALL
SELECT '10/27/2017', '11/15/2017' UNION ALL
SELECT '11/5/2017', '11/10/2017'


;
WITH
Ranges as (
    SELECT MIN(StartDate) OVER (ORDER BY StartDate, EndDate ROWS BETWEEN 0 FOLLOWING AND UNBOUNDED FOLLOWING) as StartDate
    , MAX(EndDate) OVER (ORDER BY StartDate, EndDate ROWS BETWEEN UNBOUNDED PRECEDING AND 0 PRECEDING) as EndDate
    FROM #OverlappingDateRanges
),
Groups as (
    SELECT StartDate
    , EndDate
    , LAG(StartDate,1) OVER (ORDER BY StartDate, EndDate) AS PreviousStartDate
    , LAG(EndDate,1) OVER (ORDER BY StartDate, EndDate) AS PreviousEndDate
    FROM Ranges
),
Islands as (
    SELECT StartDate
    , EndDate
    , CASE WHEN PreviousEndDate &gt;= StartDate THEN 0 ELSE 1 END AS IslandStartInd
    , SUM(CASE WHEN PreviousEndDate &gt;= StartDate THEN 0 ELSE 1 END) OVER (ORDER BY StartDate, EndDate) AS IslandId
    FROM Groups
)

SELECT MIN(StartDate) AS IslandStartDate
, MAX(EndDate) AS IslandEndDate
FROM Islands
GROUP BY IslandId
ORDER BY IslandStartDate;
</code></pre>
<pre><code>IslandStartDate IslandEndDate
--------------- -------------
2017-08-24      2017-10-10
2017-10-17      2017-10-18
2017-10-25      2017-11-15
</code></pre>
<p>I'm not finding any start/end combinations that are causing problems.  I'll let this marinate for a few days before marking it as correct in case somebody can poke some holes in it.</p>

### Answer ID: 72230799
<p>Adding a column to <code>#a</code> and adding a few more data rows to address some scenarios not covered in original data set:</p>
<pre><code>drop table if exists #a

create table #a
(pass        int
,category    varchar(5)
,rangebegin  int
,rangeend    int)

insert #a
values 
  (0, 'a', 1, 19)
, (0, 'a', 1, 27)
, (0, 'a', 9, 37)
, (0, 'a', 14, 42)
, (0, 'a', 45, 65)
, (0, 'a', 47, 70)
, (0, 'a', 52, 62)
, (0, 'a', 65, 65)

, (0, 'a', 81, 83)       -- standalone row/range
, (0, 'a', 95, 95)       -- standalone row/range; begin == end

, (0, 'b', 3, 33)
, (0, 'b', 17, 22)
, (0, 'b', 21, 44)

, (0, 'c', 30, 35)       -- no two rows
, (0, 'c', 33, 40)       -- define the
, (0, 'c', 39, 42)       -- entire range
</code></pre>
<p>One idea using a loop to iteratively consolidate ranges:</p>
<pre><code>declare @pass           int,
        @prevcount      int,
        @currcount      int

select  @pass = 0,
        @prevcount = (select count(*) from #a where pass = 0),
        @currcount = 0

while   @currcount != @prevcount
begin
        insert  #a
                (pass, category, rangebegin, rangeend)
        select  distinct
                @pass + 1,
                a1.category,
                (select min(a2.rangebegin)
                 from   #a a2
                 where  a2.category     = a1.category
                 and    a2.pass         = @pass
                 and    (       a1.rangebegin   between  a2.rangebegin and a2.rangeend
                         or     a1.rangeend     between  a2.rangebegin and a2.rangeend)),
                (select max(a3.rangeend)
                 from   #a a3
                 where  a3.category     = a1.category
                 and    a3.pass         = @pass
                 and    (       a1.rangebegin   between  a3.rangebegin and a3.rangeend
                         or     a1.rangeend     between  a3.rangebegin and a3.rangeend))
        from    #a a1
        where   a1.pass = @pass

        select  @pass      = @pass + 1,
                @prevcount = @currcount,
                @currcount = (select count(*) from #a where pass = @pass+1)

--      print '############# %1!', @pass
--      select  * from #a where pass = @pass order by 2,3,4
end

select  category,
        rangebegin,
        rangeend
from    #a
where   pass = @pass
order by 1,2,3
</code></pre>
<p>This generates:</p>
<pre><code> category rangebegin  rangeend
 -------- ----------- -----------
 a                  1          42
 a                 45          70
 a                 81          83
 a                 95          95
 b                  3          44
 c                 30          42
</code></pre>
<p><strong>NOTES:</strong></p>
<ul>
<li>the 'final' solution is actually determined twice due to looping until <code>@currcount = @prevcount</code></li>
<li>designed/tested on a <code>SAP(Sybase) ASE 16</code> instance (<code>ASE</code> does not have support for windows functions)</li>
<li>then verified the code also works in <code>SQL Server 2019</code> <a href="https://dbfiddle.uk/?rdbms=sqlserver_2019&amp;fiddle=7ebba2f17b0d9b886dff9c7c984c96ed" rel="nofollow noreferrer">(fiddle)</a></li>
<li>it may be possible to rewrite this using a recursive CTE ... maybe? yes? no? <em>shrug</em> (I'm a bit rusty with recursive CTEs)</li>
<li>for larger volumes of data OP may want to look at indexing <code>#a</code></li>
<li>once a new set of data is inserted into <code>#a</code> the 'previous' set of data could be deleted as said data will no longer be needed ... OP's choice</li>
</ul>

### Answer ID: 72225737
<p>I'm not sure how to put everything in one query but using adhoc/Stored procedure can solve this problem.</p>
<p>I have tested in my Sybase ASE, please try same approach with your SQL/Oracle.</p>
<p>Hope this help.</p>
<p><strong>1. Add column SEQ (auto increment id) into source table</strong></p>
<div class="s-table-container">
<table class="s-table">
<thead>
<tr>
<th>SEQ</th>
<th>RANGE</th>
</tr>
</thead>
<tbody>
<tr>
<td>1</td>
<td>2.22</td>
</tr>
<tr>
<td>2</td>
<td>2.24</td>
</tr>
<tr>
<td>3</td>
<td>3.10</td>
</tr>
<tr>
<td>4</td>
<td>3.92</td>
</tr>
<tr>
<td>5</td>
<td>5.03</td>
</tr>
<tr>
<td>6</td>
<td>5.21</td>
</tr>
</tbody>
</table>
</div>
<p><strong>2. Looping and calculate difference between 2 records</strong></p>
<pre><code> CREATE TABLE TEST_RESULT
(
    BEGIN_MILE NUMERIC(10,2),
    END_MILE NUMERIC(10,2)
)

--Begin ad-hoc code
DECLARE @iLoop numeric(10), @recNo numeric(10), @sMsg VARCHAR(100), @tRANGE numeric(10,2), @rangebegin numeric(10,2), @rangeend numeric(10,2)

SET @recNo = (SELECT COUNT(*) FROM LLE_TEST_SEQ)
SET @iLoop = 3

--Set 1st begin
SET @rangebegin = (SELECT RANGE FROM LLE_TEST_SEQ WHERE SEQ = 1)
--Set 1st end
SET @rangeend = (SELECT RANGE FROM LLE_TEST_SEQ WHERE SEQ = 2)

WHILE (@iLoop &lt;= @recNo)
    BEGIN
        SET @tRANGE = (SELECT RANGE FROM LLE_TEST_SEQ WHERE SEQ = @iLoop)
        
        --Display for testing
        PRINT '*****'
        SET @sMsg = CONVERT(VARCHAR, @rangeend)
        PRINT @sMsg     
        SET @sMsg = CONVERT(VARCHAR, @tRANGE)
        PRINT @sMsg
        PRINT '*****'
        
        --If delta &lt; 1, increase end point
        IF @tRANGE - @rangeend &lt; 1
            BEGIN
                SET @rangeend = @tRANGE
            END
        --Otherwise, break, insert and create new set
        ELSE
            BEGIN
                INSERT INTO TEST_RESULT (BEGIN_MILE, END_MILE) VALUES (@rangebegin, @rangeend)
                SET @rangebegin = @tRANGE
                SET @rangeend = @tRANGE
            END     
        
        
        SET @iLoop = @iLoop + 1
        
    END
INSERT INTO TEST_RESULT (BEGIN_MILE, END_MILE) VALUES (@rangebegin, @rangeend)
--End ad-hoc code
</code></pre>
<p>Output</p>
<pre><code>SELECT * FROM TEST_RESULT
</code></pre>
<div class="s-table-container">
<table class="s-table">
<thead>
<tr>
<th>BEGIN_MILE</th>
<th>END_MILE</th>
</tr>
</thead>
<tbody>
<tr>
<td>2.22</td>
<td>3.92</td>
</tr>
<tr>
<td>5.03</td>
<td>5.21</td>
</tr>
</tbody>
</table>
</div>
