# INSERT INTO dynamically added columns
[Link to question](https://stackoverflow.com/questions/15144107/insert-into-dynamically-added-columns)
**Creation Date:** 1362080071
**Score:** 2
**Tags:** sql-server-2008, sql-server-2005
## Question Body
<p>Running SQL Server 2005/2008, I am rewriting my query to be cleaner and more compliant to not include bad habits. I used to have lots of <code>IF</code> statements and <code>PIVOT</code> to do this, but found a better way to achieve it now and just need a last bit to make it almost perfect.</p>

<pre><code>DECLARE @startdate DATETIME;
DECLARE @enddate DATETIME;
DECLARE @showstore INT;
DECLARE @showcashier INT;
DECLARE @showregister INT;
DECLARE @showdate INT;
DECLARE @sql NVARCHAR(MAX);
DECLARE @result0 NVARCHAR(MAX);

SET @startdate = '1/1/2012';
SET @enddate = '2/28/2013';
SET @showdate = 1;
SET @showstore = 0;
SET @showcashier = 1;
SET @showregister = 0;
SET @startdate = DATEADD(DAY, DATEDIFF(DAY, 0, @startdate), 0);
SET @enddate = DATEADD(DAY, DATEDIFF(DAY, 0, @enddate), 0);

SET @sql = N'CREATE TABLE ##a13 (' + SUBSTRING(
CASE WHEN @showdate = 1 THEN ',[Transaction Date] DATETIME' ELSE '' END + 
CASE WHEN @showstore = 1 THEN ',[Store ID] VARCHAR(10)' ELSE '' END + 
CASE WHEN @showcashier = 1 THEN ',[Cashier] VARCHAR(100)' ELSE '' END + 
CASE WHEN @showregister = 1 THEN ',[Register] VARCHAR(20)' ELSE '' END, 2, 2000);

DECLARE myCursor CURSOR FOR
    SELECT DISTINCT c.CurrencyDesc 
    FROM dbo.Currencies AS c INNER JOIN dbo.rpPay AS p ON c.POSCurrency = p.PayType 
        INNER JOIN dbo.RPTrs AS r ON r.ReceiptNO = p.ReceiptNo
    WHERE
        c.CurrencyDesc &lt;&gt; 'Testing' AND c.CurrencyDesc &lt;&gt; 'Cash Change' AND
        r.TRSDate &gt;= @startdate AND r.TRSDate &lt;= @enddate
OPEN myCursor
FETCH NEXT FROM myCursor INTO @result0
WHILE @@FETCH_STATUS = 0
    BEGIN
        SET @sql = @sql + ',[' + @result0 + '] INT'
        FETCH NEXT FROM myCursor INTO @result0
    END
CLOSE myCursor
DEALLOCATE myCursor

SET @sql = @sql + ')'
EXECUTE sp_executesql @sql, N'@startdate DATETIME, 
    @enddate DATETIME',@startdate, @enddate;

SET @sql = 'SELECT * FROM ##a13; DROP TABLE ##a13'
EXECUTE sp_executesql @sql
</code></pre>

<p>This Returns a table empty of rows. (know that the Currencies tables has more CurrencyDesc then shown here because these are just the ones used in the date range provided)</p>

<p><img src="https://i.sstatic.net/whpfP.jpg" alt="enter image description here"></p>

<p>Which is exactly what I expect from it. Great so far so good. Now I need to add rows of data to it based on a Date Range (<code>@startdate &gt;= and &lt;= @enddate</code>) and depending on what they have checked off from the 4 possible options (<code>@showstore, @showcashier, @showdate, @showregister</code>)</p>

<p>Example : Date from 1/1/2013 till 2/28/2013 and show Register only (as seen in the picture) should have this DATA :</p>

<pre><code>  | Register | Cash  | House Acct | MasterCard | Visa/MC
--------------------------------------------------------
1 | 01       | 20.00 | 235.25     | 1235.32    | 135.23
2 | 02       | 30.00 | 3542.42    | 323.52     | 523.64
3 | 03       | 23.35 | 100.32     | 3267.24    | 235.25
</code></pre>

<p>Reason for 2005/2008 is because some of the clients this is executed against, still use 2005 and in order to use <code>PIVOT</code> I would have to change the compatibility level on each database that is 2005.</p>

<p>PS. Before I get yelled at again, if I use #a13 instead of the global ##a13 it gives me </p>

<pre><code>Msg 208, Level 16, State 0, Line 1
Invalid object name '#a13'.
</code></pre>

<p>What can I do about that so I don't use global temp tables?</p>

## Answers
### Answer ID: 15144413
<p>If I am incorrect here, please clarify.</p>

<p>I BELIEVE you are asking how to populate a table with dynamic columns based on user input.  The <strong>right</strong> answer here is, <strong>don't do that!</strong></p>

<p>The best practice for this kind of thing is to have ALL the fields in your output table, then in your application/display layer you only show the fields that the user has requested.</p>

<p>Customizing a table layout within TSQL just to make a clean presentation introduces a lot of unnecessary complexity.  This complexity comes with an increased performance cost as well.</p>

<p>If you have a static output table then it's trivial to return your data using the parameters given.</p>

