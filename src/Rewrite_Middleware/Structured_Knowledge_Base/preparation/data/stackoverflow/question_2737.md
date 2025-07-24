# Oracle left join behaving like inner join
[Link to question](https://stackoverflow.com/questions/49874372/oracle-left-join-behaving-like-inner-join)
**Creation Date:** 1523956987
**Score:** 3
**Tags:** sql, oracle-database, oracle12c
## Question Body
<p>I have Two tables:</p>

<pre>
<b>Dates</b>:

  |ReportHeader|
  --------------
  |     2015-04|
  |     2015-05|
  |     2015-06|
<b>Data</b>:
  |ReportHeader|Customer|Sales|
  -----------------------------
  |     2015-04|    Plop|  684|
  |     2015-06|    Plop|  486|
</pre>

<p>I have my query:  </p>

<pre><code>select
    Dates.ReportHeader,
    Data.Customer,
    Data.Sales
from Dates
    left outer join data on Dates.ReportHeader = Data.ReportHeader
</code></pre>

<p>What I would expect back is:</p>

<pre>
  |ReportHeader|Customer|Sales|
  -----------------------------
  |     2015-04|    Plop|  684|
  |     2015-05|    null| null|
  |     2015-06|    Plop|  486|
</pre>

<p>The results that I am getting are:</p>

<pre>
  |ReportHeader|Customer|Sales|
  -----------------------------
  |     2015-04|    Plop|  684|
  |     2015-06|    Plop|  486|
</pre>

<p>Is there any reason to be found why this left join would behave like an inner join? 
Or do I just not understand how a left join is supposed to work.</p>

<p>The Oracle version i am using is:
<i>Oracle Database 12c Standard Edition Release 12.1.0.2.0 - 64bit Production</i></p>

<p>Thanks in advance for any help extended</p>

<p>edit:
It seems i have over simplified the problem so i better put the whole query here:  </p>

<pre><code>WITH
    L0 AS (SELECT 1 C from dual UNION ALL SELECT 1 O from dual),
    L1 AS (SELECT 1 C FROM L0 A CROSS JOIN L0 B),
    L2 AS (SELECT 1 C FROM L1 A CROSS JOIN L1 B),
    L3 AS (SELECT 1 C FROM L2 A CROSS JOIN L2 B),
    L4 AS (SELECT 1 C FROM L3 A CROSS JOIN L3 B),
    Nums AS (SELECT 0 N FROM dual union SELECT ROW_NUMBER() OVER ( ORDER BY (SELECT NULL from dual) ) N FROM L4),
    Dates as (
      select distinct
        to_char(to_date(last_day(current_timestamp + (-1 * N))) , 'yyyy-MM') as ReportHeader,
        to_date(add_months(last_day(current_timestamp + (-1 * N)),-1)+1) as FirstDayOfMonth,
        to_date(current_timestamp + (-1 * N))                               as ReportDate,
        to_date(last_day(current_timestamp + (-1 * N)))                     as LastDayOfMonth
      from Nums
      where N &lt;= 3 * 365
  ), Invoices AS (
    select
      TP.ID,
      TP.Name,
      h.FORMATTEDINVOICENUMBER,
      l.SCHEDULEID,
      to_date(h.INVOICEDUEDATE) as date_due,
      to_date(L.EFFECTIVEDATEFULLYPAID) as date_payed
    from  ODSTHIRDPARTY TP
      LEFT JOIN ODSINVOICELINE L on L.INVCUSID = TP.ID
      LEFT JOIN ODSINVOICEHEADER H  on h.ID = l.INVOICEHEADERID
    where TP.NAME not in ('&lt;None&gt;','&lt;Unknown&gt;')
), data as (
    select distinct
      Invoices.Name as Customer,
      Dates.ReportHeader,
      count(distinct Invoices.SCHEDULEID) over (partition by Dates.ReportHeader, Invoices.Name) as NumContracts,
      floor(avg(
        case
          when Invoices.date_due &gt; Dates.LastDayOfMonth THEN 0
          when coalesce(Invoices.date_payed, current_date) &lt; Dates.FirstDayOfMonth THEN 0
          when Invoices.date_payed &lt; Invoices.date_due then Invoices.date_payed - Invoices.date_due
          else to_date(least(coalesce(Invoices.date_payed, current_date), Dates.LastDayOfMonth )) - to_date(Invoices.date_due)
        end
      ) over (partition by Dates.ReportHeader, Invoices.Name))  past_due,
      Dates.FirstDayOfMonth as ReportStartDate,
      Dates.LastDayOfMonth  as ReportEndDate,
      coalesce(Invoices.date_payed, current_date) as calc_date
    from Dates
      left join Invoices on Dates.ReportDate between Invoices.date_due and coalesce(Invoices.date_payed, current_date)
    where coalesce(Invoices.date_payed, current_date) &gt;= Invoices.date_due
)
    select distinct
      Dates.ReportHeader,
      data.Customer,
      data.NumContracts,
      data.past_due
    from Dates
      left join data on data.ReportHeader = Dates.ReportHeader
 order by data.Customer,dates.ReportHeader
</code></pre>

<p>The troublesome part is the final query. <b>Select from dates left join on data</b></p>

<p>For those interested, as @APC was saying in the comments. Create a testable use case. Doing that triggered me to rewrite the complete query that does work now. My initial premise was wrong and i took an initial approach that was wrong.</p>

<p>Revised query below:</p>

<pre><code>WITH
    L0 AS (SELECT 1 C from dual UNION ALL SELECT 1 O from dual),
    L1 AS (SELECT 1 C FROM L0 A CROSS JOIN L0 B),
    L2 AS (SELECT 1 C FROM L1 A CROSS JOIN L1 B),
    L3 AS (SELECT 1 C FROM L2 A CROSS JOIN L2 B),
    L4 AS (SELECT 1 C FROM L3 A CROSS JOIN L3 B),
    Nums AS (SELECT 0 N FROM dual union SELECT ROW_NUMBER() OVER ( ORDER BY (SELECT NULL from dual) ) N FROM L4),
    Dates as (
      select distinct
        to_char(to_date(last_day(current_timestamp + (-1 * N))), 'yyyy-MM') as ReportHeader,
        to_date(add_months(last_day(current_timestamp + (-1 * N)), -1) + 1) as FirstDayOfMonth,
        to_date(current_timestamp + (-1 * N))                               as ReportDate,
        to_date(last_day(current_timestamp + (-1 * N)))                     as LastDayOfMonth
      from Nums
      where N &lt;= 2 * 365
  ), ThirdParties as (
    select distinct
      TP.ID,
      TP.Name,
      Dates.ReportHeader,
      Dates.FirstDayOfMonth,
      Dates.ReportDate,
      Dates.LastDayOfMonth
    from ODSTHIRDPARTY TP
    cross join Dates
    where TP.NAME not in ('&lt;None&gt;','&lt;Unknown&gt;')
  ), Invoices AS (
    select distinct
      TP.ID,
      TP.Name,
      TP.ReportHeader,
      TP.FirstDayOfMonth,
      OH.FORMATTEDINVOICENUMBER,
      TP.LastDayOfMonth,
      il.SCHEDULEID,
      to_date(il.invoiceReferenceDate)                          as date_due,
      to_date(iL.EFFECTIVEDATEFULLYPAID)                  as date_payed,
      case
        when il.id is null then 0
        else
          case
            when to_date(il.invoiceReferenceDate) &lt;= to_date(coalesce(iL.EFFECTIVEDATEFULLYPAID,least(current_date,tp.LastDayOfMonth))) then
              to_date(coalesce(iL.EFFECTIVEDATEFULLYPAID,least(current_date,tp.LastDayOfMonth))) - to_date(il.invoiceReferenceDate)
            else 0
          end
      end as daysLate
    from  ThirdParties TP
      LEFT JOIN ODSINVOICELINE IL on IL.INVCUSID = TP.ID and TP.ReportDate
                            between il.invoiceReferenceDate and coalesce(il.EFFECTIVEDATEFULLYPAID, current_date)
      left join ODSINVOICEHEADER OH on IL.INVOICEHEADERID = OH.ID
), data as (
    select distinct
      Invoices.ReportHeader,
      Invoices.Name                                                                       as Customer,
      count(distinct Invoices.SCHEDULEID) over (partition by Invoices.ReportHeader, Invoices.Name) as NumContracts,
      floor(avg(
        case
          when Invoices.date_due &gt; Invoices.LastDayOfMonth THEN 0
          when coalesce(Invoices.date_payed, current_date) &lt; Invoices.FirstDayOfMonth THEN 0
          when Invoices.date_payed &lt; Invoices.date_due then Invoices.date_payed - Invoices.date_due
          else to_date(least(coalesce(Invoices.date_payed, current_date), Invoices.LastDayOfMonth )) - to_date(Invoices.date_due)
        end
      ) over (partition by Invoices.ReportHeader, Invoices.Name))  past_due,
      Invoices.FirstDayOfMonth                                                               as ReportStartDate,
      Invoices.LastDayOfMonth                                                                as ReportEndDate,
      coalesce(Invoices.date_payed, current_date)                                         as calc_date
    from Invoices
                           -- and coalesce(Invoices.date_payed, current_date) &gt;= Invoices.date_due
    order by Invoices.Name, Invoices.reportheader
), upvt as (
    select distinct
      row_number()
      over (
        partition by customer
        order by ReportHeader ) as ColNum,
      data.ReportHeader            ColName,
      data.Customer,
      data.NumContracts,
      data.past_due
    from data
), pvt as (
  select * from (
    select Customer, ColName, ColNum, NumContracts, past_due from upvt
  ) pivot (
    MAX(past_due) as DueDays, MAX(NumContracts) as Contracts, Max(ColName) as ColName
                for ColNum in ( '1', '2', '3', '4', '5', '6', '7', '8', '9','10','11','12','13','14','15',
                                       '16','17','18','19','20','21','22','23','24')) pvt
)
select
  row_number() over (order by Customer) as No,
  pvt.*
from pvt;
</code></pre>

## Answers
### Answer ID: 49899845
<p>use below query</p>

<pre><code>select
    Dates.ReportHeader,
    Data.Customer,
    Data.Sales
from 
    Dates, Data
where 
  Dates.ReportHeader = Data.ReportHeader(+)
</code></pre>

