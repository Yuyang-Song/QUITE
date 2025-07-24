# convert sql server query to be used in Access database
[Link to question](https://stackoverflow.com/questions/40904473/convert-sql-server-query-to-be-used-in-access-database)
**Creation Date:** 1480575899
**Score:** -6
**Tags:** sql, sql-server, delphi, ms-access
## Question Body
<p>I have found this query to work with the SQL server very well.
So I tought to port this to an Access database.Fields are the same.</p>

<pre><code>Rate_Start_Date = DateTime
Rate_End_Date = DateTime
Room_Type = char
Rate = Currency
Price_List_Code = Integer
</code></pre>

<p>However, the sql syntax is beyond my knowledge.
Can someone help me rewrite this so it works with an Access database ?</p>

<p>The code :</p>

<pre><code>    use MYDATABASE
DECLARE @StartDate  DATETIME,
        @EndDate    DATETIME,
        @RoomType   VARCHAR(6),
        @PriceListCode    INT
;

 SELECT @StartDate  = :a2,
        @EndDate    = :a3,
        @RoomType   = :a1,
        @PriceListCode  = :a4
;
WITH 
cteStayDates AS
( 
 SELECT RoomType  = Room_Type,
        StartDate = CASE WHEN Rate_Start_Date &lt; @StartDate THEN @StartDate ELSE Rate_Start_Date END,
        EndDate   = CASE WHEN Rate_End_Date   &gt; @EndDate   THEN @EndDate   ELSE Rate_End_Date   END,
        Rate
   FROM dbo.Room_Rates
  WHERE @RoomType  = Room_Type
    AND @StartDate &lt; Rate_End_Date
    AND @EndDate  &gt;= Rate_Start_Date
    AND @PriceListCode = PRICE_LIST_CODE
) 
 SELECT RoomType, StartDate, EndDate, Rate, 
        Days = DATEDIFF(dd,StartDate,EndDate)
             + CASE WHEN EndDate = @EndDate THEN 0 ELSE 0 END
   FROM cteStayDates
  ORDER BY StartDate
;
</code></pre>

## Answers
### Answer ID: 40906435
<p>In Access SQL should be something like this:</p>

<pre><code>PARAMETERS parmStartDate DATETIME
    ,parmEndDate DATETIME
    ,parmPriceList Short
    ,parmRoomType TEXT (6);

SELECT RoomType
    ,StartDate
    ,EndDate
    ,Price
    ,DATEDIFF("d", StartDate, EndDate) AS Days
FROM (
    SELECT Room_Type AS RoomType
        ,iif(Rate_Start_Date &lt; parmStartDate, parmStartDate, Rate_Start_Date) AS StartDate
        ,iif(Rate_End_Date &gt; parmEndDate, parmEndDate, Rate_End_Date) AS EndDate
        ,Price
    FROM dbo.Room_Rates
    WHERE parmRoomType = Room_Type
        AND parmPriceList = Price_List
        AND parmStartDate &lt; Rate_End_Date
        AND parmEndDate &gt;= Rate_Start_Date
    )
ORDER BY StartDate;
</code></pre>

