# MySQL Java getting objects by a distinct field
[Link to question](https://stackoverflow.com/questions/31598102/mysql-java-getting-objects-by-a-distinct-field)
**Creation Date:** 1437685850
**Score:** 0
**Tags:** mysql, jakarta-ee
## Question Body
<p>I need to return <em>java objects</em> from my database by distinct field. In my database I have <em>Country</em>, <em>State</em>, <em>City</em>. Now I have 2 records where they have the same data in the fields, but I only want to return distinct states in a country. </p>

<p>To clarify - I have two records with the same country and state. I only want to return one state instead of Washington twice for example. However, I need the object as opposed to returning the string of washington.</p>

<p>My query: </p>

<pre><code>SELECT DISTINCT r FROM Roster r where r.state = :state AND r.country = :country
</code></pre>

<p>What is happening is it will return all the duplicates because the objects are not distinct, where I just want one of each?</p>

<p>I apologise if I was not very clear.</p>

<p>Any help would be greatly appreciated!</p>

<p>edit: I need the objects because I am using them to populate a results table.</p>

<p>edit2: 
My create table:</p>

<pre><code>CREATE TABLE `roster` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `country` varchar(45) NOT NULL,
  `state` varchar(45) NOT NULL,
  `city` varchar(45) DEFAULT NULL,
  `clientName` varchar(45) NOT NULL,
  `tDomain` varchar(45) NOT NULL,
  `tSubDomain` varchar(45) DEFAULT NULL,
  `tReferenceId` varchar(45) DEFAULT NULL,
  `startDate` date DEFAULT NULL,
  `endDate` date DEFAULT NULL,
  `startTime` time DEFAULT NULL,
  `endTime` time DEFAULT NULL,
  `designation` varchar(45) DEFAULT NULL,
  `role` varchar(45) DEFAULT NULL,
  `name` varchar(45) NOT NULL,
  `surname` varchar(45) NOT NULL,
  `mobileNumber` varchar(45) DEFAULT NULL,
  `officeNumber` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `availability` tinyint(1) NOT NULL,
  `comments` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1
</code></pre>

<p>Everything up to tReferenceID is likely to be common. The rest is going to be unique. I am toying with the idea of splitting the table into two. But that would involve quite a hefty rewrite.</p>

## Answers
### Answer ID: 31598876
<p>I wouldn't know JPA if it fell on my head. So I fumble after this:</p>

<pre><code>SELECT DISTINCT r.Country,r.State,r.City 
FROM Roster r 
where r.state = :state AND r.country = :country
</code></pre>

<p><strong>Edit</strong>:</p>

<p>Ok clearly that was wrong for an object :></p>

<p>how about</p>

<pre><code>create table roster
(
    id int auto_increment primary key,
    country varchar(100) not null,
    state varchar(100) not null,
    city varchar(100) not null
);

insert roster (country,state,city) values ('usa','kentucky','louisville');
insert roster (country,state,city) values ('usa','illinois','chicago');
insert roster (country,state,city) values ('usa','kentucky','louisville');
insert roster (country,state,city) values ('usa','kentucky','blah_blah');
</code></pre>

<p>and for strings I use</p>

<pre><code>select * from roster r
join 
(SELECT min(id) as cheatId
FROM roster
where country='usa' and state='kentucky') inr
on inr.cheatId=r.id

+----+---------+----------+------------+---------+
| id | country | state    | city       | cheatId |
+----+---------+----------+------------+---------+
|  1 | usa     | kentucky | louisville |       1 |
+----+---------+----------+------------+---------+
1 row in set (0.00 sec)
</code></pre>

<p>And for <strong>objects</strong> you use:</p>

<pre><code>select r from roster r
join 
(SELECT min(id) as cheatId
FROM roster
where country=:country and state=:state) inr
on inr.cheatId=r.id
</code></pre>

