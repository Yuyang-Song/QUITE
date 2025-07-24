# MySQL - endless running query on LEFT OUTER JOIN
[Link to question](https://stackoverflow.com/questions/32972548/mysql-endless-running-query-on-left-outer-join)
**Creation Date:** 1444141699
**Score:** 0
**Tags:** php, mysql, sql-server, join
## Question Body
<p>For the past two days i've been messing about with a single query.
I've tried to dissect it's individual parts in a myriad of ways and have discovered the query only breaks when i add in the LEFT OUTER JOINs.
I've tried in many different ways to even have one of my reference tables joined to some of the tables I want to use in my actual statement, but thus far to no avail.</p>

<p>(Note; Column selector has been kept to "*" for readability, there's a ton of rows here normally. Behaviour is the same when I test with the * selector.)</p>

<p>My full query:</p>

<pre><code>SELECT *
        FROM SO_SalesOrder so 
        INNER JOIN SO_Leg as l ON l.SalesOrder = so.SalesOrdernr 
        INNER JOIN SO_Cargo cg ON cg.Cargonr = l.Cargo 
        INNER JOIN SO_Activity ea ON ea.Activitynr = l.EndActivity 
        INNER JOIN SO_Activity ba ON ba.Activitynr = l.BeginActivity 
        LEFT OUTER JOIN RP_TripActivity eta ON eta.Activity = l.EndActivity 
        LEFT OUTER JOIN Product p ON p.Productnr = cg.Product
        WHERE ba.Date BETWEEN '2015-10-01 00:00:00' AND '2015-10-07 23:59:59'
        AND OrderStatus != 2
        AND so.Customer = 95;
</code></pre>

<p>This database has been transferred from a MS-SQL server, hence i'm rewriting the queries to fit this change.
The old query (still) works and used to be as follows:</p>

<pre><code>SELECT *
    FROM dbo.SO_SalesOrder as so 
    INNER JOIN dbo.SO_Leg as l ON l.SalesOrder = so.SalesOrdernr 
    INNER JOIN dbo.SO_Cargo AS cg ON cg.Cargonr = l.Cargo 
    INNER JOIN dbo.SO_Activity AS ea ON ea.Activitynr = l.EndActivity 
    INNER JOIN dbo.SO_Activity AS ba ON ba.Activitynr = l.BeginActivity 
    LEFT OUTER JOIN dbo.RP_TripActivity AS eta ON eta.Activity = l.EndActivity 
    LEFT OUTER JOIN dbo.RP_Trip AS et ON et.Tripnr = eta.Trip 
    LEFT OUTER JOIN dbo.RP_ResourceCombination AS erc ON erc.ResourceCombinationnr = eta.ResourceCombination 
    LEFT OUTER JOIN dbo.RP_Resource AS er1 ON er1.Resourcenr = erc.Truck 
    LEFT OUTER JOIN dbo.RP_ResourceCompany AS erc1 ON erc1.Resource = er1.Resourcenr AND erc1.Company = et.Company 
    LEFT OUTER JOIN dbo.VM_Vehicle AS ev1 ON ev1.Vehiclenr = er1.Vehicle 
    LEFT OUTER JOIN dbo.RP_Resource AS er3 ON er3.Resourcenr = erc.Driver 
    LEFT OUTER JOIN dbo.HR_Employee AS eemp3 ON eemp3.Employeenr = er3.Employee 
    LEFT OUTER JOIN dbo.Product AS p ON p.Productnr = cg.Product 
    WHERE ba.Date BETWEEN '2015-10-01 00:00:00' 
    AND '2015-10-07 23:59:59'
    AND OrderStatus != 2
    AND so.Customer = 95; 
</code></pre>

<p>Would anyone perhaps have any pointers as to where I might screwing up?</p>

<p>Things i've tried:
Removing WHERE-Clauses, adding "AS" keywords (as also done in MSSQL), Attempting a single left outer join and a single inner join on one table.</p>

<p>Edit: It might be worth noting this would be the first time I'm using MySQL instead of MSSQL/T-SQL, I have ofcourse tried to look up other examples, but this hasn't helped me thus far.</p>

## Answers
### Answer ID: 32989635
<p>Looking at your query, having indexes is one thing, having indexes that are better optimized for what you are asking for is another.  Do you have compound indexes ON your tables?  I would assume you have indexes on your primary keys that are based on the JOIN components.  But three in particular I would index on multiple fields for the index.</p>

<pre><code>table           index
SO_SalesOrder   ( customer, orderstatus, salesordernr )
SO_LEG          ( salesorder, beginactivity, endactivity, cargo )
SO_Activity     ( activitynr, date )
</code></pre>

<p>It appears you "SO_Activity" table has "Activity" as the primary key.</p>

<p>One additional option under MySQL.  If these indexes do not help, then I would try adding the keyword "STRAIGHT_JOIN" to tell MySQL to join in the exact order as you have listed the tables as the others are all subject to the primary sales order you are intending which is for the specific customer... which is probably a small set in the scheme of the database content.</p>

<pre><code>SELECT STRAIGHT_JOIN * from ...
</code></pre>

### Answer ID: 32987203
<p>For some odd reason when I tried running the same queries again without 'AS' mentions in them and only a single Left Outer Join (the one i let execute past night still had them in) after 4.5 sec the query seems to run through and fetching is complete after 10 minutes... once I added a second left outer join the fetching time went up to nearly 16 minutes... Might simply have something to do with the massive amount of data which is actually returned...</p>

<p>This makes me assume the issue lies (no longer, or maybe never really was?) in syntax and after all is a performance issue. I'm familiar to employing SQL Server Management Studio for performance debugging but hadn't employed MySQL Workbench for the same purpose yet... seems like these tools are only supported from MySQL 5.6.6+, since both my production and testserver run MySQL 5.5.44 (These systems run on Debian Jessie) I'll have to figure out a way to do this... will probably end up firing up an additional test-vm for this at the end of today..</p>

<p>I'm confused as to how the performance would deter so much from the implementation we have/had on MS-SQL... Will have to research this in-depth.
If anyone passing by happens to have any leads, that'd be tremendously appreciated.</p>

<p>Edit; My sincere apologies, seems like i've simply made some errors while I was recreating my tables and I hadn't made the proper indexes for two of the tables... I feel so stupid.
Thanks for the help!</p>

