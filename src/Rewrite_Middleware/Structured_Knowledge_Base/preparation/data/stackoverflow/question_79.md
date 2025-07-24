# Sub Query is too slow when select top 1 record for each parent
[Link to question](https://stackoverflow.com/questions/12116345/sub-query-is-too-slow-when-select-top-1-record-for-each-parent)
**Creation Date:** 1345840867
**Score:** 2
**Tags:** sql-server, performance, sql-server-2008-r2, database-performance
## Question Body
<p>I am trying to locate the last record within the selected date using the sub query method. The problem is the query is too slow. I am wondering if anyone have any ideas on how to rewrite this query to improve the performance. My server is dying because of this.<br>
To make it easier for testing I have created a table variable to generate fake data for testing purposes. To test this script please run usp_ExtractData'400000'</p>

<p>My concern is at ---SECTION B 
My result was 18 seconds for 400000*3 = 1200000 records. On the real database i do index it and re-index nightly.</p>

<pre><code>--Store proceedure with table variable data

ALTER PROCEDURE [dbo].[usp_ExtractData](
@TotalRecord int--Create random records for each product
)

AS
BEGIN
    --MS SQL 2008
    SET NOCOUNT ON;

    --SECTION 1--Create test data--- GO TO SECTION 2
        --Create Variable table to Products fake data
        DECLARE @Product TABLE
        (
          ProductID int primary  key not null
          ,SKU varchar(100) not null
        )
        --Insert couple records into @Product table
        INSERT INTO @Product(ProductID, SKU) VALUES     (100,'CUP100')
        INSERT INTO @Product(ProductID, SKU) VALUES     (101,'CUP101')
        INSERT INTO @Product(ProductID, SKU) VALUES     (102,'MUG101')

        --Create Variable table to hold Products History data
        DECLARE @History TABLE
        (
           ID int identity not null
          ,ProductID int not null
          ,VisitedDatetime datetime not null
        )

        --Generate random record for testing
        WHILE @TotalRecord&gt;0
            BEGIN
                INSERT INTO  @History( ProductID, VisitedDatetime) VALUES (100,DATEADD(minute,rand()*100,GETDATE()))
                INSERT INTO  @History( ProductID, VisitedDatetime) VALUES (101,DATEADD(minute,rand()*100,GETDATE()))
                INSERT INTO  @History( ProductID, VisitedDatetime) VALUES (102,DATEADD(minute,rand()*100,GETDATE()))
                set @TotalRecord=@TotalRecord-1
            END
    --SECTION 1--Finised creating test data



    ---SECTION B 

      --SELECTION B1- SEE DATA
      SELECT * FROM @History         ORDER BY ProductID, VisitedDatetime DESC
        --Run query to find the last visit per each ProductID

        --THIS IS TOO SLOW
        DECLARE @TestPerformanceDatetime datetime--Test performance
        SET @TestPerformanceDatetime= GETDATE()
        SELECT  *, (select top(1) VisitedDatetime FROM @History as t2 WHERE t2.ProductID=ProductID and VisitedDatetime BETWEEN GETDATE() AND GETDATE()+10 ORDER BY VisitedDatetime DESC) as LastVistiDate
        FROM     @Product

        --Display the performance
        SELECT  DATEDIFF(SECOND, @TestPerformanceDatetime,getdate()) AS TotalSeconds
    ---SECTION B - End
END
</code></pre>

## Answers
### Answer ID: 12118127
<p>On my notebook I'm seeing about 102,346 ms to generate the history, 5,120 ms for the first search and 643 ms for the second.  OTOH, it's BOINCing Rosetta@Home flat out at the same time.</p>

<pre><code>declare @HistoryRecordsPerProduct int = 400000

set nocount on

-- drop table #Product
-- drop table #History

-- Create the test tables.

create table #Product
  ( ProductId Int primary key not null, SKU VarChar(100) not null )

insert into #Product ( ProductId, SKU ) values
  ( 100, 'CUP100' ), ( 101, 'CUP101' ), ( 102, 'MUG102' )

create table #History 
  ( Id Int identity not null, ProductId Int not null, VisitedDatetime DateTime not null )
-- EDIT: Note the following index on both columns. 
create index History_Product_VisitedDateTime on #History ( ProductId, VisitedDateTime desc )

-- Populate the history table.
declare @Start as DateTime = GetDate()

while @HistoryRecordsPerProduct &gt; 0
  begin
  insert into #History ( ProductId, VisitedDatetime ) values ( 100, DateAdd( minute, rand() * 100, GetDate() ) ) 
  insert into #History ( ProductId, VisitedDatetime ) values ( 101, DateAdd( minute, rand() * 100, GetDate() ) ) 
  insert into #History ( ProductId, VisitedDatetime ) values ( 102, DateAdd( minute, rand() * 100, GetDate() ) ) 
  set @HistoryRecordsPerProduct = @HistoryRecordsPerProduct - 1 
  end 

select DateDiff( ms, @Start, GetDate() ) as 'Elapsed History Generation (ms)'

-- Query the data.
set @Start = GetDate()
declare @End as DateTime = @Start + 10 -- Days.

select @Start as [Start], @End as [End]

select ProductId, SKU,
  ( select Max( VisitedDateTime ) from #History where ProductId = #Product.ProductId and
    @Start &lt;= VisitedDatetime and VisitedDatetime &lt;= @End ) as VDT
  from #Product

select DateDiff( ms, @Start, GetDate() ) as 'Elapsed Search (ms)'

-- And again with the data cached.

set @Start = GetDate()
set @End = @Start + 10 -- Days.

select @Start as [Start], @End as [End]

select ProductId, SKU,
  ( select Max( VisitedDateTime ) from #History where ProductId = #Product.ProductId and
    @Start &lt;= VisitedDatetime and VisitedDatetime &lt;= @End ) as VDT
  from #Product

select DateDiff( ms, @Start, GetDate() ) as 'Elapsed Search (ms)'
</code></pre>

### Answer ID: 12118129
<p>Use a <code>cross apply</code> and <code>max()</code>.</p>

<pre><code>select *
from @Product p
cross apply (
    select MAX(VisitedDatetime) LastVisitedDatetime
    from @History
    where VisitedDatetime BETWEEN GETDATE() AND GETDATE()+10
        and ProductID = p.ProductID
) h
</code></pre>

### Answer ID: 12117044
<p>I was getting 0 seconds with original version of this query, so I upped the number of random test records from 400,000 to 4,000,000.</p>

<pre><code>CREATE PROCEDURE [dbo].[usp_ExtractData_test](
@TotalRecord int--Create random records for each product
)

AS
BEGIN
    --MS SQL 2008
    SET NOCOUNT ON;

    --SECTION 1--Create test data--- GO TO SECTION 2
        --Create Variable table to Products fake data
        DECLARE @Product TABLE
        (
          ProductID int primary  key not null
          ,SKU varchar(100) not null
        )
        --Insert couple records into @Product table
        INSERT INTO @Product(ProductID, SKU) VALUES     (100,'CUP100')
        INSERT INTO @Product(ProductID, SKU) VALUES     (101,'CUP101')
        INSERT INTO @Product(ProductID, SKU) VALUES     (102,'MUG101')

        --Create Variable table to hold Products History data
        DECLARE @History TABLE
        (
           ID int identity not null
          ,ProductID int not null
          ,VisitedDatetime datetime not null
        )

        --Generate random record for testing
        WHILE @TotalRecord&gt;0
            BEGIN
                INSERT INTO  @History( ProductID, VisitedDatetime) VALUES (100,DATEADD(minute,rand()*100,GETDATE()))
                INSERT INTO  @History( ProductID, VisitedDatetime) VALUES (101,DATEADD(minute,rand()*100,GETDATE()))
                INSERT INTO  @History( ProductID, VisitedDatetime) VALUES (102,DATEADD(minute,rand()*100,GETDATE()))
                set @TotalRecord=@TotalRecord-1
            END
    --SECTION 1--Finised creating test data



    ---SECTION B 
        --Run query to find the last visit per each ProductID
        --THIS IS TOO SLOW
        DECLARE @TestPerformanceDatetime datetime--Test performance
        SET @TestPerformanceDatetime= GETDATE()
        SELECT  P.*, LastVisitDate.VisitedDatetime
        FROM     @Product P
        LEFT
        JOIN  (select top(1) T2.VisitedDatetime FROM @History as t2
               ORDER BY T2.VisitedDatetime DESC) as LastVisitDate
          ON  LastVisitDate.VisitedDatetime BETWEEN GETDATE() AND GETDATE()+10

        --Display the performance
        SELECT  DATEDIFF(SECOND, @TestPerformanceDatetime,getdate()) AS TotalSeconds
    ---SECTION B - End
END
</code></pre>

<p><img src="https://i.sstatic.net/8PrAN.jpg" alt="Proof"></p>

