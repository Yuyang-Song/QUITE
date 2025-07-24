# Oracle: Max, Partition by, or even rownum?
[Link to question](https://stackoverflow.com/questions/43997299/oracle-max-partition-by-or-even-rownum)
**Creation Date:** 1494926393
**Score:** 0
**Tags:** oracle-database, subquery, query-optimization, rownum
## Question Body
<p>I am from SQL Server background, so my skill in Oracle is minimum. It looks like <code>Partition by</code> is better than <code>max</code> in terms of performance. Or do I use <code>rownum</code> to archive my result table?</p>

<p>I have the following table - TableW. </p>

<pre><code>| P_TYPE      | TRX_DATE       | PROGRAM_NO | REF_NO    | SEQ_ID |  Select 
|-------------|----------------|------------|-----------|--------|
| 'Local'     | 2016/9/5 14:37 | C1         | null      | E1     |  Yes (latest in Sept 5)
| 'Local'     | 2016/9/5 14:36 | C1         | null      | E1     |
| 'Local'     | 2016/9/5 11:08 | C1         | null      | E1     |
|-------------|----------------|------------|-----------|--------|
| 'Local'     | 2016/9/2 15:16 | C1         | null      | E1     |  Yes (latest in Sept 2)
|-------------|----------------|------------|-----------|--------|
| 'Local'     | 2016/9/1 15:20 | C1         | null      | E1     |  Yes (latest in Sept 1)
| 'Local'     | 2016/9/1 14:33 | C1         | null      | E1     |
|-------------|----------------|------------|-----------|--------|
| '3rd Party' | 2016/9/4 18:00 | null       | D1        | E2     |  Yes
| '3rd Party' | 2016/9/4 17:55 | null       | D1        | E2     |
</code></pre>

<p>Here is what I want to get:</p>

<p>For column P_TYPE, if it is value of 'Local', use column PROGRAM_NO and SEQ_ID. Otherwise, use REF_NO and SEQ_ID.
If value in column P_TYPE is same, check TRX_DATE. If column TRX_DATE indicates the same date, pick the one with latest time stamp. Another day? Another entry with latest time stamp.</p>

<pre><code>| P_TYPE      | TRX_DATE       | PROGRAM_NO | REF_NO    | SEQ_ID |
|-------------|----------------|------------|-----------|--------|
| 'Local'     | 2016/9/5 14:37 | C1         | null      | E1     |  
| 'Local'     | 2016/9/2 15:16 | C1         | null      | E1     |  
| 'Local'     | 2016/9/1 15:20 | C1         | null      | E1     |  
| '3rd Party' | 2016/9/4 18:00 | null       | D1        | E2     |  
</code></pre>

<p>A script that I receive is to use <code>SELECT MAX</code> in the <code>WHERE clause</code>:</p>

<pre><code>SELECT *
FROM TableW a
WHERE TRX_DATE = 
    CASE P_TYPE
        WHEN 'Local' THEN
            (SELECT MAX(TRX_DATE) FROM TableW
                WHERE PROGRAM_NO = a.PROGRAM_NO AND SEQ_ID = a.SEQ_ID)
        ELSE
            (SELECT MAX(TRX_DATE) FROM TableW
                WHERE REF_NO = a.REF_NO AND SEQ_ID = a.SEQ_ID)
    END
ORDER BY TRX_DATE desc, REF_NO ASC, SEQ_ID;
</code></pre>

<p>It does the job. However with some research, it seems like <code>partition by</code> is not that costly. Refer: <a href="https://asktom.oracle.com/pls/asktom/f?p=100:11:0::::P11_QUESTION_ID:7251902693483" rel="nofollow noreferrer">Tune SQL statement with max subquery</a>  </p>

<p>I try to rewrite the query as: </p>

<pre><code>SELECT *
FROM (
SELECT *,
    CASE P_TYPE 
        WHEN 'Local' THEN 
            MAX(TRX_DATE) OVER (PARTITION BY PROGRAM_NO, SEQ_ID)
        ELSE
            MAX(TRX_DATE) OVER (PARTITION BY REF_NO, SEQ_ID)
    END AS MAX_TRX_DATE
FROM TableW
WHERE P_TYPE = 'Local'
)
WHERE TRX_DATE = MAX_TRX_DATE
</code></pre>

<p>However, I get only this:</p>

<pre><code>| P_TYPE      | TRX_DATE       | PROGRAM_NO | REF_NO    | SEQ_ID |
|-------------|----------------|------------|-----------|--------|
| 'Local'     | 2016/9/5 14:37 | C1         | null      | E1     |  
</code></pre>

<p>Any guideline please. If possible, please illustrate your suggestion with statistics. Thanks.</p>

<p><strong>EDIT</strong>: It looks like using row_number and partition by will greatly reduce the execution plan and even the time?</p>

<pre><code>| CASE             | OPERATION        | CARDINALITY | COST | LAST CR     | LAST ELAPSED  |
|                  |                  |             |      | BUFFER GETS | TIME          |
|------------------|------------------|-------------|------|-------------|---------------|
| 1 - max() in     | SELECT STATEMENT |             |  76  |             |               |
|     where clause | SORT (ORDER BY)  |      1      |  76  |     477     |      3602     |
|------------------|------------------|-------------|------|-------------|---------------|
| 2 - row_number   | SELECT STATEMENT |             |  18  |             |               |
|                  | SORT (ORDER BY)  |      8      |  18  |      53     |       607     |
|------------------|------------------|-------------|------|-------------|---------------|
</code></pre>

## Answers
### Answer ID: 43997961
<p>For the <code>Local</code> rows you need to include the day when defining the window partition as all values for <code>PROGRAM_NO, REF_NO</code> are identical for those rows:</p>

<pre><code>select *
from (
  SELECT *,
         CASE P_TYPE
           when 'Local' then 
              row_number() over (partition by program_no, seq_id, trunc(trx_date) order by trx_date desc)
           else 
              row_number() over (partition by ref_no, seq_id order by trx_date desc)
         end as rn
  FROM TableW a
) t
where rn = 1;
</code></pre>

<p>Online example: <a href="http://rextester.com/CZTY80559" rel="nofollow noreferrer">http://rextester.com/CZTY80559</a></p>

<p>(The example uses Postgres, but apart from the different way of "ignoring" the time part of a timestamp, it will be the same in Oracle)</p>

