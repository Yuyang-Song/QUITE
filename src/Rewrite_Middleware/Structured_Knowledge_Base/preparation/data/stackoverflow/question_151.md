# T-SQL UPSERT table with multiple values from TVP
[Link to question](https://stackoverflow.com/questions/14639859/t-sql-upsert-table-with-multiple-values-from-tvp)
**Creation Date:** 1359693734
**Score:** 1
**Tags:** t-sql, sql-server-2012, upsert, table-valued-parameters
## Question Body
<p>I use SQL Server 2012, and T-SQL as query language.</p>

<p>I need help updating/inserting multiple columns in [cross_function_user] using one ID value passed as a parameter (@userGroupID) and lots of function id's. They are List in C#, and passed to the sproc as Table Valued Parameter - with just one column of int, named Item.</p>

<pre><code>ALTER PROCEDURE [whatever]
    @userGroupID INT,
    @listID AS IntList READONLY
AS
BEGIN   
        SET NOCOUNT ON;
    MERGE INTO [dbo].[cross_function_user] USING @listID
    ON [dbo].[cross_function_user].id_group_user = @userGroupID
    WHEN MATCHED THEN
        UPDATE SET [cross_function_user].id_group_user = @userGroupID,
                   [cross_function_user].id_function = (SELECT Item FROM @listID)
    WHEN NOT MATCHED THEN
        INSERT (id_group_user, id_function) 
        VALUES (@userGroupID, (SELECT Item FROM @listID) );

END
</code></pre>

<p>First, it errors 'subquery returned more than one result' of course, but I lack skill to rewrite this, and I'm not really sure if my upsert is written right way. Any help would be highly appreciated.</p>

## Answers
### Answer ID: 14640877
<p>Try this:</p>

<p>You need to replace YourColumn with the name of the column in your TVP.</p>

<pre><code>ALTER PROCEDURE [whatever]
@userGroupID INT,
@listID AS IntList READONLY
AS
BEGIN   
    SET NOCOUNT ON;
    MERGE INTO [dbo].[cross_function_user] USING @listID
    ON [dbo].[cross_function_user].id_group_user = @userGroupID
    WHEN MATCHED THEN
        UPDATE SET [cross_function_user].id_function = S.YourColumn
    WHEN NOT MATCHED THEN
        INSERT (id_group_user, id_function) 
        VALUES (@userGroupID, S.YourColumn);

END
</code></pre>

