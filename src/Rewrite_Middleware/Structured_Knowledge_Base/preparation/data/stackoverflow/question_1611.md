# How to find rows in one table that have no corresponding row in another table
[Link to question](https://stackoverflow.com/questions/1415438/how-to-find-rows-in-one-table-that-have-no-corresponding-row-in-another-table)
**Creation Date:** 1252771488
**Score:** 77
**Tags:** sql, optimization, h2
## Question Body
<p>I have a 1:1 relationship between two tables. I want to find all the rows in table A that don't have a corresponding row in table B. I use this query:</p>

<pre><code>SELECT id 
  FROM tableA 
 WHERE id NOT IN (SELECT id 
                    FROM tableB) 
ORDER BY id desc
</code></pre>

<p>id is the primary key in both tables. Apart from primary key indices, I also have a index on tableA(id desc).</p>

<p>Using H2 (Java embedded database), this results in a full table scan of tableB. I want to avoid a full table scan.</p>

<p>How can I rewrite this query to run quickly? What index should I should?</p>

## Answers
### Answer ID: 51455832
<pre><code>select parentTable.id from parentTable
left outer join childTable on (parentTable.id = childTable.parentTableID) 
where childTable.id is null
</code></pre>

### Answer ID: 1415481
<p>You have to check every ID in tableA against every ID in tableB.  A fully featured RDBMS (such as Oracle) would be able to optimize that into an INDEX FULL FAST SCAN and not touch the table at all.  I don't know whether H2's optimizer is as smart as that.</p>

<p>H2 does support the MINUS syntax so you should try this</p>

<pre><code>select id from tableA
minus
select id from tableB
order by id desc
</code></pre>

<p>That may perform faster; it is certainly worth benchmarking. </p>

### Answer ID: 4409845
<p>For my small dataset, Oracle gives almost all of these queries the exact same plan that uses the primary key indexes without touching the table.  The exception is the MINUS version which manages to do fewer consistent gets despite the higher plan cost.</p>

<pre><code>--Create Sample Data.
d r o p table tableA;
d r o p table tableB;

create table tableA as (
   select rownum-1 ID, chr(rownum-1+70) bb, chr(rownum-1+100) cc 
      from dual connect by rownum&lt;=4
);

create table tableB as (
   select rownum ID, chr(rownum+70) data1, chr(rownum+100) cc from dual
   UNION ALL
   select rownum+2 ID, chr(rownum+70) data1, chr(rownum+100) cc 
      from dual connect by rownum&lt;=3
);

a l t e r table tableA Add Primary Key (ID);
a l t e r table tableB Add Primary Key (ID);

--View Tables.
select * from tableA;
select * from tableB;

--Find all rows in tableA that don't have a corresponding row in tableB.

--Method 1.
SELECT id FROM tableA WHERE id NOT IN (SELECT id FROM tableB) ORDER BY id DESC;

--Method 2.
SELECT tableA.id FROM tableA LEFT JOIN tableB ON (tableA.id = tableB.id)
WHERE tableB.id IS NULL ORDER BY tableA.id DESC;

--Method 3.
SELECT id FROM tableA a WHERE NOT EXISTS (SELECT 1 FROM tableB b WHERE b.id = a.id) 
   ORDER BY id DESC;

--Method 4.
SELECT id FROM tableA
MINUS
SELECT id FROM tableB ORDER BY id DESC;
</code></pre>

### Answer ID: 1415474
<p>You can also use <code>exists</code>, since sometimes it's faster than <code>left join</code>. You'd have to benchmark them to figure out which one you want to use.</p>

<pre><code>select
    id
from
    tableA a
where
    not exists
    (select 1 from tableB b where b.id = a.id)
</code></pre>

<p>To show that <code>exists</code> can be more efficient than a <code>left join</code>, here's the execution plans of these queries in SQL Server 2008:</p>

<p><strong><code>left join</code></strong> - total subtree cost: 1.09724:</p>

<p><img src="https://i.sstatic.net/aIjy7.png" alt="left join"></p>

<p><strong><code>exists</code></strong> - total subtree cost: 1.07421:</p>

<p><img src="https://i.sstatic.net/nkrCk.png" alt="exists"></p>

### Answer ID: 1415478
<p>I can't tell you which of these methods will be best on H2 (or even if all of them will work), but I did write an article detailing all of the (good) methods available in TSQL.  You can give them a shot and see if any of them works for you:</p>

<p><a href="http://code.msdn.microsoft.com/SQLExamples/Wiki/View.aspx?title=QueryBasedUponAbsenceOfData&amp;referringTitle=Home" rel="nofollow noreferrer">http://code.msdn.microsoft.com/SQLExamples/Wiki/View.aspx?title=QueryBasedUponAbsenceOfData&amp;referringTitle=Home</a></p>

### Answer ID: 1415448
<pre><code>select tableA.id from tableA left outer join tableB on (tableA.id = tableB.id)
where tableB.id is null
order by tableA.id desc 
</code></pre>

<p>If your db knows how to do index intersections, this will only touch the primary key index</p>

