# How do I calculate coverage dates during a period of time in SQL against a transactional table?
[Link to question](https://stackoverflow.com/questions/42445891/how-do-i-calculate-coverage-dates-during-a-period-of-time-in-sql-against-a-trans)
**Creation Date:** 1487961118
**Score:** 2
**Tags:** sql, sql-server, transactions, reporting, gaps-and-islands
## Question Body
<p>I'm attempting to compile a list of date ranges like so:</p>

<p>Coverage Range: 10/1/2016 - 10/5/2016</p>

<p>Coverage Range: 10/9/2016 - 10/31/2016</p>

<p>for each policy in a database table. The table is transactional, and there is one cancellation transaction code, but three codes that can indicate coverage has begun. Also, there can be instances where the codes that indicate start of coverage can occur in sequence (start on 10/1, then another start on 10/5, then cancel on 10/14). Below is an example of a series of transactions that I would like to generate the above results from:</p>

<pre><code>TransID  PolicyID  EffDate
NewBus   1         9/15/2016
Confirm  1         9/17/2016
Cancel   1         10/5/2016
Reinst   1         10/9/2016
Cancel   1         10/15/2016
Reinst   1         10/15/2016
PolExp   1         3/15/2017
</code></pre>

<p>SO in this dataset, I want the following results for the date range 10/1 - 10/31</p>

<p>Coverage Range: 10/1/2016 - 10/5/2016</p>

<p>Coverage Range: 10/9/2016 - 10/31/2016</p>

<p>Note that since the cancel and reinstatement happen on the same day, I'm excluding them from the results set. I tried pairing the transactions with subqueries:</p>

<pre><code>CONVERT(varchar(10), 
        CASE WHEN overall.sPTRN_ID in (SELECT code FROM @cancelTransCodes)
        -- This is a coverage cancellationentry
            THEN -- Set coverage start date using previous paired record                    
                CASE WHEN((SELECT MAX(inn.PD_EffectiveDate) FROM PolicyData inn WHERE inn.sPTRN_ID in (SELECT code FROM @startCoverageTransCodes)
                    and inn.PD_EffectiveDate &lt;= overall.PD_EffectiveDate
                    and inn.PD_PolicyCode = overall.PD_PolicyCode) &lt; @sDate) THEN @sDate 
                        ELSE
                        (SELECT MAX(inn.PD_EffectiveDate) FROM PolicyData inn WHERE inn.sPTRN_ID in (SELECT code FROM @startCoverageTransCodes)
                            and inn.PD_EffectiveDate &lt;= overall.PD_EffectiveDate
                            and inn.PD_PolicyCode = overall.PD_PolicyCode)
                    END
            ELSE -- Set coverage start date using current record
                CASE WHEN (overall.PD_EffectiveDate &lt; @sDate) THEN @sDate ELSE overall.PD_EffectiveDate END END, 101)                   
    as [Effective_Date]
</code></pre>

<p>This mostly works except for the situation I listed above. I'd rather not rewrite this query if I can help it. I have a similar line for expiration date:</p>

<pre><code>ISNULL(CONVERT(varchar(10),                     
        CASE WHEN overall.sPTRN_ID in (SELECT code FROM @cancelTransCodes) -- This is a coverage cancellation entry                 
            THEN  -- Set coverage end date with current record                  
                overall.PD_EffectiveDate            
            ELSE -- check for future coverage end dates             
                CASE WHEN               
                    (SELECT COUNT(*) FROM PolicyData pd WHERE pd.PD_EffectiveDate &gt; overall.PD_EffectiveDate and pd.sPTRN_ID in (SELECT code FROM @cancelTransCodes)) &gt; 1           
                THEN -- There are future end dates          
                    CASE WHEN((SELECT TOP 1 pd.PD_ExpirationDate FROM PolicyData pd         
                        WHERE pd.PD_PolicyCode = overall.PD_PolicyCode      
                        and pd.PD_EntryDate between @sDate and @eDate   
                        and pd.sPTRN_ID in (SELECT code FROM @cancelTransCodes))) &gt; @eDate
                        THEN @eDate 
                        ELSE
                            (SELECT TOP 1 pd.PD_ExpirationDate FROM PolicyData pd       
                                WHERE pd.PD_PolicyCode = overall.PD_PolicyCode      
                                and pd.PD_EntryDate between @sDate and @eDate   
                                and pd.sPTRN_ID in (SELECT code FROM @cancelTransCodes))
                        END

            ELSE -- No future coverage end dates                
                CASE WHEN(overall.PD_ExpirationDate &gt; @eDate) THEN @eDate ELSE overall.PD_ExpirationDate END            
            END             

END, 101), CONVERT(varchar(10), CASE WHEN(overall.PD_ExpirationDate &gt; @eDate) THEN @eDate ELSE overall.PD_ExpirationDate END, 101))                 
as [Expiration_Date]
</code></pre>

<p>I can't help but feel like there's a simpler solution I'm missing here. So my question is: how can I modify the above portion of my query to accomodate the above scenario? OR What is the better answer? If I cam simplify this, I would love to hear how. </p>

<p><strong>Here's the solution I ended up implementing</strong>
I took a simplified table where I boiled all the START transaction codes to START and all the cancel transaction codes to CANCEL. When I viewed the table based on that, it was MUCH easier to watch how my logic affected the results. I ended up using a simplified system where I used CASE WHEN clauses to identify specific scenarios and built my date ranges based on that. I also changed my starting point away from looking at cancellations and finding the related starts, and reversing it (find starts and then related calcellations). So here's the code I implemented:</p>

<pre><code>/* Get Coverage Dates */                

    ,cast((CASE WHEN sPTRN_ID in (SELECT code FROM @startCoverageTransCodes) THEN
                         CASE WHEN (cast(overall.PD_EntryDate as date) &lt;= @sDate) THEN @sDate 
                         WHEN (cast(overall.PD_EntryDate as date) &gt; @sDate AND cast(overall.PD_EntryDate as date) &lt;= @eDate) THEN overall.PD_EntryDate
                         WHEN (cast(overall.PD_EntryDate as date) &gt; @eDate) THEN @eDate 
                         ELSE cast(overall.PD_EntryDate as date) END
                    ELSE
                         null
                    END) as date) as Effective_Date
        ,cast((CASE WHEN sPTRN_ID in (SELECT code FROM @startCoverageTransCodes) THEN
                         CASE WHEN (SELECT MIN(p.PD_EntryDate) FROM PolicyData p WITH (NOLOCK) WHERE p.sPTRN_ID in (SELECT code FROM @cancelTransCodes) AND p.PD_EntryDate &gt; overall.PD_EntryDate AND p.PD_PolicyCOde = overall.PD_PolicyCode) &gt; @eDate THEN @eDate
                         ELSE ISNULL((SELECT MIN(p.PD_EntryDate) FROM PolicyData p WITH (NOLOCK) WHERE p.sPTRN_ID in (SELECT code FROM @cancelTransCodes) AND p.PD_EntryDate &gt; overall.PD_EntryDate AND p.PD_PolicyCOde = overall.PD_PolicyCode), @eDate) END
                    ELSE
                         CASE WHEN (SELECT MAX(p.PD_EntryDate) FROM PolicyData p WITH (NOLOCK) WHERE p.sPTRN_ID in (SELECT code FROM @startCoverageTransCodes) AND p.PD_EntryDate &gt; overall.PD_EntryDate AND p.PD_PolicyCOde = overall.PD_PolicyCode) &gt; @eDate THEN @eDate
                         ELSE (SELECT MAX(p.PD_EntryDate) FROM PolicyData p WITH (NOLOCK) WHERE p.sPTRN_ID in (SELECT code FROM @startCoverageTransCodes) AND p.PD_EntryDate &gt; overall.PD_EntryDate AND p.PD_PolicyCOde = overall.PD_PolicyCode) 
                    END END) as date) as Expiration_Date
</code></pre>

<p>As you can see, I relied on subqueries in this case. I had a lot of this logic as joins, which caused extra rows where I didn't need them. So by making the date range logic based on sub-queries, I ended up speeding the stored procedure up by several seconds, bringing my execution time to under 1 second where before it was between 2-5 seconds. </p>

## Answers
### Answer ID: 42457449
<p>There might be a simpler solution, but I just do not see it right now.</p>

<p>The outline for each step is:</p>

<ol>
<li>Generate dates for date range, which you do not need to do if you have a calendar table.</li>
<li>Transform the incoming data set as you described in your question (skipping start/cancel on the same day); and add the next <code>EffDate</code> for each row.</li>
<li>Explode the data set with a row for each day between the generated ranges of step 2.</li>
<li>Reduce the data set back down based on consecutive days of converage.</li>
</ol>

<p>test setup: <a href="http://rextester.com/GUNSO45644" rel="nofollow noreferrer">http://rextester.com/GUNSO45644</a></p>

<pre><code>/* set date range */
declare @fromdate date = '20161001'
declare @thrudate date = '20161031'
/* generate dates in range -- you can skip this if you have a calendar table */
;with n as (select n from (values(0),(1),(2),(3),(4),(5),(6),(7),(8),(9)) t(n))
, dates as (
  select top (datediff(day, @fromdate, @thrudate)+1) 
    [Date]=convert(date,dateadd(day,row_number() over(order by (select 1))-1, @fromdate))
  from         n as deka
    cross join n as hecto     /* 100 days   */
    cross join n as kilo      /* 2.73 years */
    cross join n as [tenK]    /* 27.3 years */
  order by [Date]
)
/* reduce test table to desired input*/
, pol as (
  select 
      Coverage = case when max(TransId) in ('Cancel','PolExp') 
                  then 0 else 1 end
    , PolicyId
    , EffDate  = case when max(TransId) in ('Cancel','PolExp') 
                  then dateadd(day,1,EffDate) else EffDate end
    , NextEffDate = oa.NextEffDate
  from t
    outer apply (
        select top 1
          NextEffDate = case 
            when i.TransId in ('Cancel','PolExp')
              then dateadd(day,1,i.EffDate) 
            else i.EffDate
            end
        from t as i
        where i.PolicyId = t.PolicyId
          and i.EffDate &gt; t.EffDate
        order by 
            i.EffDate asc
          , case when i.TransId in ('Cancel','PolExp') then 1 else 0 end desc 
        ) as oa
  group by t.PolicyId, t.EffDate, oa.NextEffDate
)
/* explode desired input by day, add row_numbers() */
, e as (
select pol.PolicyId, pol.Coverage, d.Date
    , rn_x = row_number() over (
        partition by pol.PolicyId
        order by d.Date
        )
    , rn_y = row_number() over (
        partition by pol.PolicyId, pol.Coverage 
        order by d.date)
  from pol
    inner join dates as d
      on d.date &gt;= pol.EffDate
     and d.date &lt; pol.NextEffDate
)
/* reduce to date ranges where Coverage = 1 */
select 
    PolicyId
  , FromDate = convert(varchar(10),min(Date),120)
  , ThruDate = convert(varchar(10),max(Date),120)
from e
where Coverage = 1
group by PolicyId, (rn_x-rn_y);
</code></pre>

<p>returns:</p>

<pre><code>+----------+------------+------------+
| PolicyId |  FromDate  |  ThruDate  |
+----------+------------+------------+
|        1 | 2016-10-01 | 2016-10-05 |
|        1 | 2016-10-09 | 2016-10-31 |
+----------+------------+------------+
</code></pre>

