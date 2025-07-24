# Splitting multiple fields by delimiter
[Link to question](https://stackoverflow.com/questions/49733475/splitting-multiple-fields-by-delimiter)
**Creation Date:** 1523278419
**Score:** 2
**Tags:** sql-server, t-sql
## Question Body
<p>I have to write an SP that can perform Partial Updates on our databases, the changes are stored in a record of the PU table. A values fields contains all values, delimited by a fixed delimiter. A tables field refers to a Schemes table containing the column names for each table in a similar fashion in a Colums fiels.</p>

<p>Now for my SP I need to split the Values field and Columns field in a temp table with Column/Value pairs, this happens for each record in the PU table.</p>

<p>An example:</p>

<p>Our PU table looks something like this:</p>

<pre><code>CREATE TABLE [dbo].[PU](
    [Table] [nvarchar](50) NOT NULL,
    [Values] [nvarchar](max) NOT NULL
)
</code></pre>

<p><a href="https://i.sstatic.net/12wrg.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/12wrg.png" alt="The PU table"></a></p>

<p>Insert SQL for this example:</p>

<pre><code>INSERT INTO [dbo].[PU]([Table],[Values]) VALUES ('Person','John Doe;26');
INSERT INTO [dbo].[PU]([Table],[Values]) VALUES ('Person','Jane Doe;22');
INSERT INTO [dbo].[PU]([Table],[Values]) VALUES ('Person','Mike Johnson;20');
INSERT INTO [dbo].[PU]([Table],[Values]) VALUES ('Person','Mary Jane;24');
INSERT INTO [dbo].[PU]([Table],[Values]) VALUES ('Course','Mathematics');
INSERT INTO [dbo].[PU]([Table],[Values]) VALUES ('Course','English');
INSERT INTO [dbo].[PU]([Table],[Values]) VALUES ('Course','Geography');
INSERT INTO [dbo].[PU]([Table],[Values]) VALUES ('Campus','Campus A;Schools Road 1;Educationville');
INSERT INTO [dbo].[PU]([Table],[Values]) VALUES ('Campus','Campus B;Schools Road 31;Educationville');
INSERT INTO [dbo].[PU]([Table],[Values]) VALUES ('Campus','Campus C;Schools Road 22;Educationville');
</code></pre>

<p>And we have a Schemes table similar to this:</p>

<pre><code>CREATE TABLE [dbo].[Schemes](
    [Table] [nvarchar](50) NOT NULL,
    [Columns] [nvarchar](max) NOT NULL
)
</code></pre>

<p><a href="https://i.sstatic.net/1V9Dt.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/1V9Dt.png" alt="The Schemes table"></a></p>

<p>Insert SQL for this example:</p>

<pre><code>INSERT INTO [dbo].[Schemes]([Table],[Columns]) VALUES ('Person','[Name];[Age]');
INSERT INTO [dbo].[Schemes]([Table],[Columns]) VALUES ('Course','[Name]');
INSERT INTO [dbo].[Schemes]([Table],[Columns]) VALUES ('Campus','[Name];[Address];[City]');
</code></pre>

<p>As a result the first record of the PU table should result in a temp table like:</p>

<p><a href="https://i.sstatic.net/9pGsY.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/9pGsY.png" alt="John"></a></p>

<p>The 5th will have:</p>

<p><a href="https://i.sstatic.net/x0BsR.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/x0BsR.png" alt="Mathematics"></a></p>

<p>Finally, the 8th PU record should result in:</p>

<p><a href="https://i.sstatic.net/2usO0.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/2usO0.png" alt="Campus A"></a></p>

<p>You get the idea.
I tried use the following query to create the temp tables, but alas it fails when there's more that one value in the PU record:</p>

<pre><code>DECLARE @Fields TABLE
(
    [Column] INT,
    [Value] VARCHAR(MAX)
)

INSERT INTO @Fields
    SELECT TOP 1
        (SELECT Value FROM STRING_SPLIT([dbo].[Schemes].[Columns], ';')), 
        (SELECT Value FROM STRING_SPLIT([dbo].[PU].[Values], ';'))
    FROM [dbo].[PU] INNER JOIN [dbo].[Schemes] ON [dbo].[PU].[Table] = [dbo].[Schemes].[Table]
</code></pre>

<p>TOP 1 correctly gets the first PU record as each PU record is removed once processed.</p>

<p>The error is:</p>

<p>Subquery returned more than 1 value. This is not permitted when the subquery follows =, !=, &lt;, &lt;= , >, >= or when the subquery is used as an expression.</p>

<p>In the case of a Person record, the splits are indeed returning 2 values/colums at a time, I just want to store the values in 2 records instead of getting an error.</p>

<p>Any help on rewriting the above query?</p>

<p>Also do note that the data is just generic nonsense. Being able to have 2 fields that both have delimited values, always equal in amount (e.g. a 'person' in the PU table will always have 2 delimited values in the field), and break them up in several column/header rows is the point of the question.</p>

<h3>UPDATE: Working implementation</h3>

<p>Based on the (accepted) answer of Sean Lange, I was able to work out followin implementation to overcome the issue:</p>

<p>As I need to reuse it, the combine column/value functionality is performed by a new function, declared as such:</p>

<pre><code>CREATE FUNCTION [dbo].[JoinDelimitedColumnValue]
        (@splitValues VARCHAR(8000), @splitColumns VARCHAR(8000),@pDelimiter CHAR(1))
RETURNS TABLE WITH SCHEMABINDING AS
 RETURN
  WITH MyValues AS
(
    SELECT ColumnPosition = x.ItemNumber,
        ColumnValue = x.Item
    FROM  dbo.DelimitedSplit8K(@splitValues, @pDelimiter) x
)

, ColumnData AS
(
    SELECT ColumnPosition = x.ItemNumber,
        ColumnName = x.Item
    FROM  dbo.DelimitedSplit8K(@splitColumns, @pDelimiter) x
)

SELECT cd.ColumnName,
    v.ColumnValue
FROM MyValues v
JOIN ColumnData cd ON cd.ColumnPosition = v.ColumnPosition
;
</code></pre>

<p>In case of the above sample data, I'd call this function with the following SQL:</p>

<pre><code>DECLARE @FieldValues VARCHAR(8000), @FieldColumns VARCHAR(8000)
SELECT TOP 1 @FieldValues=[dbo].[PU].[Values], @FieldColumns=[dbo].[Schemes].[Columns] FROM [dbo].[PU] INNER JOIN [dbo].[Schemes] ON [dbo].[PU].[Table] = [dbo].[Schemes].[Table]

INSERT INTO @Fields
SELECT [Column] = x.[ColumnName],[Value] = x.[ColumnValue] FROM [dbo].[JoinDelimitedColumnValue](@FieldValues, @FieldColumns, @Delimiter) x
</code></pre>

## Answers
### Answer ID: 49740766
<p>I recommended not storing values like this in the first place.  I recommend having a key value in the tables and preferably not using Table and Columns as a composite key.  I recommend to avoid using reserved words.  I also don't know what version of SQL you are using.  I am going to assume you are using a fairly recent version of Microsoft SQL Server that will support my provided stored procedure.</p>

<p>Here is an overview of the solution:
1) You need to convert both the PU and the Schema table into a table where you will have each "column" value in the list of columns isolated in their own row.  If you can store the data in this format rather than the provided format, you will be a little better off.</p>

<p>What I mean is</p>

<pre><code>Table|Columns
Person|Jane Doe;22
</code></pre>

<p>needs converted to </p>

<pre><code>Table|Column|OrderInList
Person|Jane Doe|1
Person|22|2
</code></pre>

<p>There are multiple ways to do this, but I prefer an xml trick that I picked up.  You can find multiple split string examples online so I will not focus on that.  Use whatever gives you the best performance.  Unfortunately, You might not be able to get away from this table-valued function.</p>

<p><strong>Update:</strong>
Thanks to Shnugo's performance enhancement comment, I have updated my xml splitter to give you the row number which reduces some of my code.  I do the exact same thing to the Schema list.</p>

<p>2) Since the new Schema table and the new PU table now have the order each column appears, the PU table and the schema table can be joined on the "Table" and the OrderInList</p>

<pre><code>CREATE FUNCTION [dbo].[fnSplitStrings_XML]
(
   @List       NVARCHAR(MAX),
   @Delimiter  VARCHAR(255)
)
RETURNS TABLE
AS
   RETURN 
   (
      SELECT y.i.value('(./text())[1]', 'nvarchar(4000)') AS Item,ROW_NUMBER() OVER(ORDER BY (SELECT NULL)) as RowNumber
      FROM 
      ( 
        SELECT CONVERT(XML, '&lt;i&gt;' 
          + REPLACE(@List, @Delimiter, '&lt;/i&gt;&lt;i&gt;') 
          + '&lt;/i&gt;').query('.') AS x
      ) AS a CROSS APPLY x.nodes('i') AS y(i)
   );
GO
CREATE Procedure uspGetColumnValues
 as
 Begin

--Split each value in PU
select p.[Table],p.[Values],a.[Item],CHARINDEX(a.Item,p.[Values]) as LocationInStringForSorting,a.RowNumber
into #PuWithOrder
from PU p
cross apply [fnSplitStrings_XML](p.[Values],';') a  --use whatever string split function is working best for you (performance wise)

--Split each value in Schema
select s.[Table],s.[Columns],a.[Item],CHARINDEX(a.Item,s.[Columns]) as LocationInStringForSorting,a.RowNumber
into #SchemaWithOrder
from Schemes s
cross apply [fnSplitStrings_XML](s.[Columns],';') a  --use whatever string split function is working best for you (performance wise)



DECLARE @Fields TABLE  --If this is an ETL process, maybe make this a permanent table with an auto incrementing Id and reference this table in all steps after this.
(
[Table] NVARCHAR(50),
[Columns] NVARCHAR(MAX),
    [Column] VARCHAR(MAX),
    [Value] VARCHAR(MAX),
    OrderInList int
)
INSERT INTO @Fields([Table],[Columns],[Column],[Value],OrderInList)
Select pu.[Table],pu.[Values] as [Columns],s.Item as [Column],pu.Item as [Value],pu.RowNumber
from #PuWithOrder pu
join #SchemaWithOrder s on pu.[Table]=s.[Table] and pu.RowNumber=s.RowNumber

Select [Table],[Columns],[Column],[Value],OrderInList
from @Fields
order by [Table],[Columns],OrderInList

   END
   GO

   EXEC uspGetColumnValues

   GO
</code></pre>

<p><strong>Update:</strong>
Since your working implementation is a table-valued function, I have another recommendation.  The problem I see is that your using a table valued function which ultimately handles one record at a time.  You are going to have better performance with set based operations and batching as needed.  With a tabled valued function, you are likely going to be looping through each row.  If this is some sort of ETL process, your team will be better off if you have a stored procedure that processes the rows in bulk.  It might make sense to stage the results into a better table that your team can work with down stream rather than have them use a potentially slow table-valued function.</p>

### Answer ID: 49737966
<p>This data structure makes this way more complicated than it should be. You can leverage the splitter from Jeff Moden here. <a href="http://www.sqlservercentral.com/articles/Tally+Table/72993/" rel="nofollow noreferrer">http://www.sqlservercentral.com/articles/Tally+Table/72993/</a> The main difference of that splitter and all the others is that his returns the ordinal position of each element. Why all the other splitters don't do this is beyond me. For things like this it is needed. You have two sets of delimited data and you must ensure that they are both reassembled in the correct order. </p>

<p>The biggest issue I see is that you don't have anything in your main table to function as an anchor for ordering the results correctly. You need something, even an identity to ensure the output rows stay "together". To accomplish I just added an identity to the PU table.</p>

<pre><code>alter table PU add RowOrder int identity not null
</code></pre>

<p>Now that we have an anchor this is still a little cumbersome for what should be a simple query but it is achievable.</p>

<p>Something like this will now work.</p>

<pre><code>with MyValues as
(
    select p.[Table]
        , ColumnPosition = x.ItemNumber
        , ColumnValue = x.Item
        , RowOrder
    from PU p
    cross apply dbo.DelimitedSplit8K(p.[Values], ';') x
)

, ColumnData as
(
    select ColumnName = replace(replace(x.Item, ']', ''), '[', '') 
        , ColumnPosition = x.ItemNumber
        , s.[Table]
    from Schemes s
    cross apply dbo.DelimitedSplit8K(s.Columns, ';') x
)

select cd.[Table]
    , v.ColumnValue
    , cd.ColumnName
from MyValues v
join ColumnData cd on cd.[Table] = v.[Table] 
    and cd.ColumnPosition = v.ColumnPosition
order by v.RowOrder
    , v.ColumnPosition
</code></pre>

