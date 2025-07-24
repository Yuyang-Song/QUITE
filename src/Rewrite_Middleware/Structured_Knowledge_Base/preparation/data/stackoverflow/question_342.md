# Database design for optimisation
[Link to question](https://stackoverflow.com/questions/21477840/database-design-for-optimisation)
**Creation Date:** 1391164422
**Score:** 2
**Tags:** php, mysql, database-design
## Question Body
<p>A couple of years ago I designed a reward system for 11-16yo students in PHP, JavaScript and MySQL.</p>

<p>The premise is straightforward:</p>

<ul>
<li>Members of staff issue points to students under various categories ("Positive attitude and behaviour", "Model citizen", etc)</li>
<li>Students accrue these points then spend them in our online store (iTunes vouchers, etc)</li>
</ul>

<h1>Existing system</h1>

<p>The database structure is also straightforward (probably too much so):</p>

<h2>Transactions</h2>

<h3>239,189 rows</h3>

<pre><code>CREATE TABLE `transactions` (
 `Transaction_ID` int(9) NOT NULL auto_increment,
 `Datetime` date NOT NULL,
 `Giver_ID` int(9) NOT NULL,
 `Recipient_ID` int(9) NOT NULL,
 `Points` int(4) NOT NULL,
 `Category_ID` int(3) NOT NULL,
 `Reason` text NOT NULL,
 PRIMARY KEY  (`Transaction_ID`),
 KEY `Giver_ID` (`Giver_ID`),
 KEY `Datetime` (`Datetime`),
 KEY `DatetimeAndGiverID` (`Datetime`,`Giver_ID`),
 KEY `Recipient_ID` (`Recipient_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=249069 DEFAULT CHARSET=latin1
</code></pre>

<h2>Categories</h2>

<h3>34 rows</h3>

<pre><code>CREATE TABLE `categories` (
 `Category_ID` int(9) NOT NULL,
 `Title` varchar(255) NOT NULL,
 `Description` text NOT NULL,
 `Default_Points` int(3) NOT NULL,
 `Groups` varchar(125) NOT NULL,
 `Display_Start` datetime default NULL,
 `Display_End` datetime default NULL,
 PRIMARY KEY  (`Category_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
</code></pre>

<h2>Rewards</h2>

<h3>82 rows</h3>

<pre><code>CREATE TABLE `rewards` (
 `Reward_ID` int(9) NOT NULL auto_increment,
 `Title` varchar(255) NOT NULL,
 `Description` text NOT NULL,
 `Image_URL` varchar(255) NOT NULL,
 `Date_Inactive` datetime NOT NULL,
 `Stock_Count` int(3) NOT NULL,
 `Cost_to_User` float NOT NULL,
 `Cost_to_System` float NOT NULL,
 PRIMARY KEY  (`Reward_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=91 DEFAULT CHARSET=latin1
</code></pre>

<h2>Purchases</h2>

<h3>5,889 rows</h3>

<pre><code>CREATE TABLE `purchases` (
 `Purchase_ID` int(9) NOT NULL auto_increment,
 `Datetime` datetime NOT NULL,
 `Reward_ID` int(9) NOT NULL,
 `Quantity` int(4) NOT NULL,
 `Student_ID` int(9) NOT NULL,
 `Student_Name` varchar(255) NOT NULL,
 `Date_DealtWith` datetime default NULL,
 `Date_Collected` datetime default NULL,
 PRIMARY KEY  (`Purchase_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=6133 DEFAULT CHARSET=latin1
</code></pre>

<h1>Problems</h1>

<p>The system ran perfectly well for a period of time. It's now starting to slow-down massively on certain queries.</p>

<p>Essentially, every time I need to access a students' reward points total, the required query takes <em>ages</em>. Here is a few example queries and their run-times:</p>

<h3>Top 15 students, excluding attendance categories, across whole school</h3>

<pre><code>SELECT CONCAT( s.Firstname,  " ", s.Surname ) AS  `Student` , s.Year_Group AS `Year Group`, SUM( t.Points ) AS  `Points` 
FROM frog_rewards.transactions t
LEFT JOIN frog_shared.student s ON t.Recipient_ID = s.id
WHERE t.Datetime &gt;  '2013-09-01' AND t.Category_ID NOT IN ( 12, 13, 14, 26 )
GROUP BY t.Recipient_ID
ORDER BY  `Points` DESC 
LIMIT 0 , 15
</code></pre>

<p><img src="https://i.sstatic.net/vbnmW.png" alt="EXPLAIN 1"></p>

<ul>
<li>Run-time: <strong>44.8425 sec</strong></li>
</ul>

<p><code>SELECT Recipient_ID, SUM(points) AS Total_Points FROM</code>transactions<code>GROUP BY Recipient_ID</code></p>

<p><img src="https://i.sstatic.net/j7ePa.png" alt="EXPLAIN 2"></p>

<ul>
<li>Run-time: <strong>9.8698 sec</strong></li>
</ul>

<p>Now I appreciate that, especially with the second query, I shouldn't ever be running a call which would return such a vast quantity of rows but the limitations of the framework within which the system runs meant that I had no other choice if I wanted to display students' total reward points for teachers/tutors/year managers/leadership to view and analyse.</p>

<h1>Time for a solution</h1>

<p>Fortunately the framework we've been forced to use is changing. We'll now be using oAuth rather than a horrible, outdated JavaScript widget format.</p>

<p>Unfortunately - or, I guess, fortunately - it means we'll have to rewrite quite a lot of the system.</p>

<p>One of the main areas I intend to look at when rewriting the system is the database structure. As time goes on it will only get bigger, so I need to do a bit of future-proofing.</p>

<p>As such, my main question is this: <strong>what is the most efficient and effective way of storing students' point totals?</strong></p>

<p>The only idea I can come up with is to have a separate table called <code>totals</code> with <code>Student_ID</code> and <code>Points</code> fields. Every time a member of staff gives out some points, it adds a row into the <code>transactions</code> table but also updates the <code>totals</code> table.</p>

<p>Is that efficient? Would it be efficient to also have a <code>Points_Since_Monday</code> type field? How would I update/keep on top of that?</p>

<p>On top of the main question, if anyone has suggestions for general improvement with regard to optimisation of the database table, please let me know.</p>

<p>Thanks in advance,
Duncan</p>

## Answers
### Answer ID: 21614021
<p>There is nothing particularly wrong with your design which should make it as slow as you have reported. I'm thinking there must be other factors at work, such as the server it is running on being overloaded or slow, for example. Only you will be able to find out if that is the case.</p>

<p>In order to test your design I recreated it on the 2008 SQL Server I have running on my desktop computer. I have a standard computer, single hard disc, not SSD, not raid etc. so on a proper database server the results should be even better. I had to make some changes to the design as you are using MySQL but none of the changes should affect performace, it's just so I can run it on my database.</p>

<p>Here's the table structure I used, I had to guess at what you would have in the <code>Student</code> and <code>Staff</code> tables as you do not descibe those. I also took the liberty of changing the field names in the <code>Transaction</code> table for <code>Giver_ID</code> and <code>Receiver_ID</code> as I assume only staff give points and students receive them.</p>

<p><img src="https://i.sstatic.net/B3Bhp.png" alt="database tables"></p>

<p>I generated random data to fill the tables with the same number of rows as you said you have in your database</p>

<p><img src="https://i.sstatic.net/xstKp.png" alt="data generation"></p>

<p>I ran the two queries you said are taking a long time, I've changed them to suit my design but I (hope) the result is the same</p>

<pre><code>SELECT TOP 15
        Firstname + ' ' + Surname
       ,Year_Group
       ,SUM(Points) AS Points
FROM    points.[Transaction]
        INNER JOIN points.Student ON points.[Transaction].Student_ID = points.Student.Student_ID
WHERE   [Datetime] &gt; '2013-09-01'
        AND Category_ID NOT IN ( 12, 13, 14, 26 )
GROUP BY Firstname + ' ' + Surname
       ,Year_Group
ORDER BY SUM(Points) DESC 


SELECT  Student_ID
       ,SUM(Points) AS Total_Points
FROM    points.[Transaction]
GROUP BY Student_ID
</code></pre>

<p><strong>Both</strong> queries returned results in about 1s. I have not created any additional indexes on the tables other than the <code>CLUSTERED</code> indexes generated by default on the primary keys. Looking at the execution plan the query processor estimates that implementing the following index could improve the query cost by <em>81.0309%</em></p>

<pre><code>CREATE NONCLUSTERED INDEX [&lt;Name of Missing Index&gt;]
ON [points].[Transaction] ([Datetime],[Category_ID])
INCLUDE ([Student_ID],[Points])
</code></pre>

<p><img src="https://i.sstatic.net/ubNoE.png" alt="execution plan"></p>

<p>As others have commented I would look elsewhere for bottlenecks before spending a lot of time redesigning your database.</p>

<p><strong>Update:</strong></p>

<p>I realised I never actually addressed your specific question:</p>

<blockquote>
  <p>what is the most efficient and effective way of storing students'
  point totals?</p>
  
  <p>The only idea I can come up with is to have a separate table called
  totals with Student_ID and Points fields. Every time a member of staff
  gives out some points, it adds a row into the transactions table but
  also updates the totals table.</p>
</blockquote>

<p>I would not recommend keeping a separate point total unless you have explored <em>every other</em> possible way to speed up the database. A separate tally can become out of sync with the transactions and then you have to reconcile everything and track down what went wrong, and what the correct total should be.</p>

<p>You should always focus on maintaining the correctness and consistency of the data before trying to increase speed. Most of the time a correct (normalised) data model will operate quickly enough.</p>

<p>In one place I worked we found the most cost effective way to speed up our database was simply to upgrade the hardware; much quicker and cheaper than spending many man-hours redesigning the database :)</p>

