# Most effective way of storing and managing moderate number of users
[Link to question](https://stackoverflow.com/questions/29836840/most-effective-way-of-storing-and-managing-moderate-number-of-users)
**Creation Date:** 1429836550
**Score:** 0
**Tags:** c#
## Question Body
<p>In a current project of mine I need to manage and store a moderate number (from 10-100 to 5000+) of users (ID, username, and some other data). </p>

<p>This means I have to be able to find users quickly at runtime, and I have to be able to save and restore the database to continue statistics after a restart of the program. I will also need to register every connect/disconnect/login/logout of a user for the statistics. (And some other data as well, but you get the idea).</p>

<p>In the past, I saved settings and other stuff in encoded textfiles, or serialized the needed objects and wrote them down. But these methods require me to rewrite the whole database on each change, and that's increasingly slowing it down (especially with a growing number of users/entries), isn't it?</p>

<p>Now the question is: What is the best way to do this kind of thing in C#?</p>

<p>Unfortunately, I don't have any experience in SQL or other query languages (except for a bit of LINQ), but that's not posing any problem for me, as I have the time and motivation to learn one (or more if required) for this task.</p>

## Answers
### Answer ID: 29837017
<p>Most effective is highly subjective based on who you ask even if narrowing down this question to specific needs.  If you are storing non-relational data Mongo or some other NoSQL type of database such as Raven DB would be effective.  If your data has a relational shape then an RDBMS such as MySQL, SQL Server, or Oracle would be effective.  Relational databases are ideal if you are going to have heavy reporting requirements as this allows non-developers more ease of access in writing simple SQL queries against it. But also keeping in mind performance with disk cache persistence that databases provide. Commonly accessed data is stored in memory to save the round trips to the disk (with hybrid drives I suppose accessing some files directly accomplishes the same thing however SSD's are still not as fast as RAM access). So you really need to ask yourself some questions to identify the best solution for you; What is the shape of your data (flat, relational, etc), do you have reporting requirements where less technical team members need to be able to query the data repository, and what are your performance metrics?  </p>

