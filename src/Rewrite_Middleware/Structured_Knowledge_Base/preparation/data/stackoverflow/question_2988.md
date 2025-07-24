# Slow SQL query when upgrading to COMPATIBILITY_LEVEL 120
[Link to question](https://stackoverflow.com/questions/61224416/slow-sql-query-when-upgrading-to-compatibility-level-120)
**Creation Date:** 1586939237
**Score:** 0
**Tags:** sql-server, query-performance, compatibility-level
## Question Body
<p>We have been running our databases in COMPATIBILITY_LEVEL &lt; 120 for a while now since we can't pinpoint why some queries run really slow.
Not I feel like it's a perfect cure for the covid-19 boredom to fix this and hence I try to tackle the problems the new (ehh... not so new anymore) CE.</p>

<p>So, I've got a fairly simple query involving 3 tables and 2 Table value parameters</p>

<pre><code>declare @spIDs as table (id int not null primary key);
INSERT INTO @spIDs values(1),(2); -- 169 in my sql script

DECLARE @subscriptionProductGroupMapping AS table
( 
    subscriptionProductID int not null,
    groupID int not null,
    primary key(subscriptionProductID, groupID)
);
INSERT INTO @subscriptionProductGroupMapping (subscriptionProductID, groupID) 
VALUES(101,101); -- 168 in my script

SELECT
    [dbo].[User].[userID]
FROM
    [dbo].[User]
    LEFT JOIN
    (
        SELECT DISTINCT [UserValidThrough].userID 
        FROM 
            [dbo].[UserValidThrough] 
            INNER JOIN @spIDs spIDs on(spIDs.id = [dbo].[UserValidThrough].subscriptionProductID)
    ) AS [uvt] ON [uvt].[userID] = [User].userID
    INNER JOIN 
    (
        SELECT DISTINCT userID
        FROM 
        GroupMembership
        INNER JOIN
        @subscriptionProductGroupMapping as SPIAndGroup ON(GroupMembership.groupID = SPIAndGroup.groupID)
    ) gms ON(gms.userID = [User].userID) 
WHERE
    [User].permissionType NOT IN(8, 16, 32, 64, 128) AND
    [User].deleteDate IS NULL AND
    [User].userTypeID IN(@userTypeID_0) AND
    [uvt].[userID] IS NULL 
</code></pre>

<p>When running this query with compatibility level 110 the query is lightning fast, less than 0.3 seconds. 
When changing to compatibility level 120 the query takes about 8-9 seconds to execute! :(</p>

<p>When investigating the actual execution plan I see that there is one clustered index seek that's allocating about 7 seconds, hence I focus on that part</p>

<p><a href="https://i.sstatic.net/EgHs3.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/EgHs3.png" alt="Actual execution plan"></a>
<a href="https://i.sstatic.net/Mt7kb.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/Mt7kb.png" alt="Explanation of slow clustered Index seek"></a></p>

<p>I've tried to break out this query into another Table value parameter and then the query is fast again. This would however imply that I have to rewrite my application on many places and I'd really like to know why this is slow and what to do about it. </p>

<p>Can anyone shed some light over this problem?</p>

<p>Edit 2020-04-15 12:57 CET
This is a debug script that reproduces a simplified scenario:
1. Create debug tables and debug data</p>

<pre><code>create table temp_User 
(
    userID int not null,
    -- Additional columns ommited for readability
    primary key (useriD)
);

create table temp_UserValidThrough 
(
    userID int not null,
    subscriptionProductID int not null,
    -- Additional columns ommited for readability
    primary key(userID, subscriptionProductID)
);

create table temp_GroupMembership
(
    userID int not null,
    groupID int not null,
    primary key(userID, groupID)
);


CREATE NONCLUSTERED INDEX temp_GroupMembership_GroupIDWithUserID 
ON [dbo].[temp_GroupMembership] ([groupID])
INCLUDE ([userID])

-- populate User
-- populate UserValidThrough
-- populate GroupMembership
declare @noUsers as int = 120000;
declare @noGroups as int = 400;

SET NOCOUNT ON;

declare @n as int = 0;
while @n &lt; @noUsers
begin
    insert into temp_User values(@n);

    declare @rand as int = rand() * @noGroups;
    insert into temp_UserValidThrough VALUES(@n, @rand);
    insert into temp_GroupMembership VALUES(@n, @rand); 

    SET @n = @n + 1;
end;
</code></pre>

<ol start="2">
<li>This query can be executed with different COMPATIBILITY_LEVEL settings and the performance will differ much. </li>
</ol>

<pre><code>DECLARE @userTypeID_0 AS Int;
SET @userTypeID_0 = '1';

declare @spIDs as table (id int not null primary key);
insert into @spIDs
select distinct groupID from temp_GroupMembership;

DECLARE @subscriptionProductGroupMapping AS table
( 
    subscriptionProductID int not null,
    groupID int not null,
    primary key(subscriptionProductID, groupID)
);
insert into @subscriptionProductGroupMapping
SELECT
    T.groupID as subscriptionProductID,
    T.groupID
FROM
    (select distinct groupID from temp_GroupMembership) AS T;


SELECT
    [User].[userID]
FROM
    [dbo].[temp_User] AS [User]
    --LEFT JOIN
    --(
    --  SELECT DISTINCT [UserValidThrough].userID 
    --  FROM 
    --      [dbo].[UserValidThrough] 
    --      INNER JOIN @spIDs spIDs on(spIDs.id = [dbo].[UserValidThrough].subscriptionProductID)
    --) AS [uvt] ON [uvt].[userID] = [User].userID
    INNER JOIN 
    (
        SELECT DISTINCT userID
        FROM 
        temp_GroupMembership as GroupMembership
        INNER JOIN
        @subscriptionProductGroupMapping as SPIAndGroup ON(GroupMembership.groupID = SPIAndGroup.groupID)
    ) gms ON(gms.userID = [User].userID) 
WHERE
    --[User].permissionType NOT IN(8, 16, 32, 64, 128) AND
    --[User].deleteDate IS NULL AND
    --[User].userTypeID IN(@userTypeID_0) AND
    NOT EXISTS 
    (
        SELECT DISTINCT [UserValidThrough].userID 
        FROM 
            [dbo].[UserValidThrough] 
            --INNER JOIN @spIDs spIDs on(spIDs.id = [dbo].[UserValidThrough].subscriptionProductID)
        WHERE
            [UserValidThrough].userID = [User].userID
            AND
            [UserValidThrough].subscriptionProductID IN(SELECT id from @spIDs)
    )
    --[uvt].[userID] IS NULL 

declare @lvl as varchar (10) = (SELECT compatibility_level FROM sys.databases WHERE name = DB_NAME());

print 'COMPATIBILITY_LEVEL: ' + @lvl
-- COMPATIBILITY_LEVEL 110 time: average 242 ms
-- COMPATIBILITY_LEVEL 120 time: average 40 s! (200 times slower!)
</code></pre>

## Answers
### Answer ID: 61224662
<p>Try this:</p>

<pre><code>CREATE TABLE #spIDs 
(
    id int not null primary key
);

CREATE TABLE #subscriptionProductGroupMapping
( 
    subscriptionProductID int not null,
    groupID int not null,
    primary key(subscriptionProductID, groupID)
);

CREATE TABLE #Users
(
    UserID int not null primary key
);

INSERT INTO #subscriptionProductGroupMapping (subscriptionProductID, groupID) 
VALUES(101,101); -- 168 in my script

INSERT INTO #spIDs values(1),(2); -- 169 in my sql script

INSERT INTO #Users (UserID)
SELECT DISTINCT userID
FROM GroupMembership
INNER JOIN #subscriptionProductGroupMapping as SPIAndGroup
    ON(GroupMembership.groupID = SPIAndGroup.groupID)

SELECT
    [dbo].[User].[userID]
FROM
    [dbo].[User]
    INNER JOIN #Users gms 
        ON gms.userID = [User].userID
    LEFT JOIN
    (
        SELECT DISTINCT [UserValidThrough].userID 
        FROM [dbo].[UserValidThrough] 
        INNER JOIN #spIDs spIDs 
            on spIDs.id = [dbo].[UserValidThrough].subscriptionProductID
    ) AS [uvt] ON [uvt].[userID] = [User].userID
WHERE
    [User].permissionType NOT IN(8, 16, 32, 64, 128) AND
    [User].deleteDate IS NULL AND
    [User].userTypeID IN(@userTypeID_0) AND
    [uvt].[userID] IS NULL 
</code></pre>

