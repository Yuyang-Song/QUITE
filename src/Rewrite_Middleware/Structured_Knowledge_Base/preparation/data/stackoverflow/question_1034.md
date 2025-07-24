# How can I sort my friends activities first and keep good performance?
[Link to question](https://stackoverflow.com/questions/55951642/how-can-i-sort-my-friends-activities-first-and-keep-good-performance)
**Creation Date:** 1556797136
**Score:** 2
**Tags:** sql-server, sqlperformance
## Question Body
<p>The code here below will search in the activity-table for users that match a given name. I want it to return top 10 activities with my friends activities first.</p>

<p>If we populate the Activities table with million of records then we can still use index and make the search for activities very fast. However it gets slow when I want to order the result by friends activities at the top.</p>

<p>Consider when the search from the Activities table returns 1000 rows and then we would need to scan the friends table and match with the 1000 rows from the matching table in Activities.</p>

<p>Do you have any suggestions on how to rewrite or re-model this database / query to make it fast? Or should the problem be solved in a different way?
I am looking for a solution that is consistent in speed even as data grow.</p>

<pre><code>declare @Activities as table 
(
    UserId int, ActivityName nvarchar(50), AccountName nvarchar(50), ActivityDate DateTime, Likes int
    INDEX IX NONCLUSTERED (AccountName,ActivityDate,Likes,UserId,ActivityName) 
)
declare @Friends as table 
(
    UserId int, FriendId int
    INDEX IX CLUSTERED (UserId, FriendId)
)

insert into @Activities values (1, 'Activity 1', 'John Doe', '2019-01-01', 10) 
insert into @Activities values (2, 'Activity 2', 'Max Gordon', '2019-02-01', 100)
insert into @Activities values (1, 'Activity 3', 'John Doe', '2019-03-01', 0)
insert into @Activities values (3, 'Activity 4', 'John Roe', '2019-08-01', 40)

insert into @Friends values (1,2) -- John is friend with max
insert into @Friends values (2,1) -- Max is friend with John
insert into @Friends values (1,3) -- John Doe is friend with John Roe

declare @UserId int = 2

select top 10
    a.ActivityName, a.AccountName, a.Likes, case when f.FriendId is null then 0 else 1 end as IsFriend
from 
    @Activities a
    left join @Friends f on f.UserId = @UserId and f.FriendId = a.UserId
where 
    a.AccountName like 'j%'
order by 
    case when f.FriendId is null then 0 else 1 end desc, 
    a.Likes desc,  
    case when a.ActivityDate &gt; getdate() then 0 else 1 end,
    a.ActivityDate
</code></pre>

## Answers
### Answer ID: 55953196
<p>Maybe a correlated subquery can be more effective than Left Join + Case statement</p>

<pre><code>select top 10
    a.ActivityName, a.AccountName, a.Likes, IsFriend
from 
    @Activities a
    outer apply (select 1 as isFriend FROM @Friends f WHERE f.UserId = @UserId and f.FriendId = a.UserId) f
where 
    a.AccountName like 'j%'
order by 
    isFriend desc, 
    a.Likes desc,  
    case when a.ActivityDate &gt; getdate() then 0 else 1 end,
    a.ActivityDate
</code></pre>

### Answer ID: 55952365
<p>Try something like this:</p>

<pre><code>SELECT a.*, COUNT(f.*) AS FriendCount
FROM Activities a
LEFT OUTER JOIN Friends f ON f.FriendId = a.UserId AND f.UserId = @UserId
GROUP BY a.*
ORDER BY SIGN(COUNT(f.*)) DESC, a.LIKES DESC, a.ActivityDate DESC
</code></pre>

