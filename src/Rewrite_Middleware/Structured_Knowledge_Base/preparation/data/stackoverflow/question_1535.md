# PostgreSQL or mySQL best for daily log website?
[Link to question](https://stackoverflow.com/questions/8748408/postgresql-or-mysql-best-for-daily-log-website)
**Creation Date:** 1325791117
**Score:** -2
**Tags:** mysql, postgresql
## Question Body
<p>I know that both these databases are better for different scenarios but in terms of a website where users will login and enter numerical data to a daily log, which one would it be best to use? I read that mySQL is faster to begin with but PostgreSQL is more scalable if the website were to start getting a lot of users?</p>

<p>The downside is that my host only offers mySQL and so to use postgreSQL I would have to purchase VPS hosting which is more expensive. I have also read people advising people to not worry about it to begin with, however it concerns me that I would have to rewrite queries and forms if I later moved to postgreSQL? I would appreciate everyone's thoughts on this.</p>

<p>I don't understand why people have given this question negative marks when I clearly stated that I am from a finance background and only started learning 3 weeks ago. I think you need to remember that everyone has to start somewhere and that we haven't all been doing this as a job/hobby for years. I would love to see some of you come out of your comfort zone and come and do my job for a day as you would be equally as clueless and I can guarantee that I would not be so rude as some of you have been here. You should be trying to create an environment of learning and innovation, rather than an environment of arrogance. If everyone knew everything, what would be the point in this website?</p>

## Answers
### Answer ID: 8749161
<p>Disclaimer: I have worked a lot more with PostgreSQL than with MySQL</p>
<p>From a performance/scalability point of view both are probably pretty much the same. There are workloads where Postgres is better and there are workloads where MySQL is better. Unless you test it in your environment it's hard to tell which one would work better for you.</p>
<p>Postgres seems (seemed?) to be faster in a workload with a lot of concurrent writes, whereas MySQL seems to be better with heavy read-only workload. But those benchmarks are about 3-4 years old now, so they are probably no longer true - especially since InnoDB in MySQL 5.5 improved a lot in that area.</p>
<p>However PostgreSQL's SQL features are far more advanced than MySQL's and MySQL has a tendency to silently ignore things you tell it to do - especially in a default installation (and if you rely on a foreign key to be created that might be a very unpleasant surprise). MySQL still has an advantage in terms of clustering as far as I can tell.</p>
<p>They are both equal when it comes to High Availability solutions.</p>
<p>I strongly disagree with the opinion that one should avoid any DBMS specific features - utilizing all features of a DBMS will make your application more scalable and will increase performance.</p>
<p>Traditionally MySQL wasn't known for stability and quality of their <a href="http://monty-says.blogspot.com/2008/11/oops-we-did-it-again-mysql-51-released.html" rel="nofollow noreferrer">releases</a>, but that seems to have improved since Oracle has taken over.</p>
<p>I still don't like MySQL's release policy where they introduce major changes and features in minor releases. The PostgreSQL dev team has a much more strict policy about what goes into a minor release. Upgrading a minor release (i.e. bugfix releases) is much less &quot;dangerous&quot; in PostgreSQL than it is in MySQL.</p>
<p>Someone once said the big difference between the PG development and MySQL is: the Postgres team first makes sure your data is safe, then it makes sure everything is working correctly, then it makes it fast. Whereas the MySQL team first makes it fast, then correct and finally stable. But that too might have changed since the Oracle takeover.</p>
<p>Personally I'd always prefer PostgreSQL over MySQL because of the much better SQL feature set and the overall quality of the product.</p>

### Answer ID: 8748467
<p>MySQL is the more popular solution and is used by very large companies for very large databases, so MySQL is far from unscalable.</p>

<p>If you want the ability to move between both databases at a later date in case you decide to switch, I would recommend using an ORM (Look at <a href="http://www.doctrine-project.org/" rel="nofollow">http://www.doctrine-project.org/</a>); this way you'll only have to write the queries once and if you change to a different database down the road, you only need to change a config variable. Doctrine will also have you build your database structure in a YAML file which it can convert for you as well.
It's also capable of migrating between database types.</p>

<p>You'll also want to take into account the different MySQL Engines which perform differently as well. I was just looking at a comparison between PostgreSQL and MySQL which in their conclusion, they didn't like the fact that MySQL wasn't built with transactions, however, InnoDB does provide transactional support for MySQL as well as speed and memory improvements in some cases.</p>

<p>So the bottom line is this: If you can make your application in such a way that you can use either database (as mentioned above) run your own benchmarks against your application and your databases and see what kind of a difference it makes to you.</p>

<p>There's certainly other things to think about if you have the budget for it and that's getting DBA's specific to the database you're using and get them to optimize it.</p>

### Answer ID: 8748476
<p>First, SQL is SQL, be sure that you use strict SQL, then you don't rewrite anything. The different between the both dbs is the level of SQL support. PosgreSQL has better support, but the support by MySQL depends on the used storage engine.</p>

<p>Yes, you can better scale your application with PostgeSQL, but how mach load have you on your server? 1GB per day, less more?</p>

