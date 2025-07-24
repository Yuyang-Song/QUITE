# Database sharing/versioning
[Link to question](https://stackoverflow.com/questions/2465018/database-sharing-versioning)
**Creation Date:** 1268851902
**Score:** 1
**Tags:** database, versioning, sharing
## Question Body
<p>I have a question but I'm not sure of the word to use.</p>

<p>My problem: I have an application using a database to stock information. The database can ben in access (local) or in a server (SQL Server or Oracle). We support these 3 kind of database. We want to give the possibility to the user to do what I think we can call versioning.</p>

<p>Let me explain : We have a database 1. This is the master. We want to be able to create a database 2 that will be the same thing as database 1 but we can give it to someone else.</p>

<p>They each work on each other side, adding, modifying and deleting records on this very complex database. After that, we want the database 1 to include the change from database 2, but with the possibility to dismiss some of the change.</p>

<p>For you information, ou application is already multiuser so why don't we just use this multi-user and forget about this versionning? It's because sometimes, we need to give a copy of the database to another company on another site and they can't connect on our server. They work on their side and then, we want to merge.</p>

<p>Is there anyone here with experience with this type of requirement? We have a lot of ideas but most of them require a LOT of work, massive modification to the database or to the existing queries.</p>

<p>This is a 2 millions and growing C++ app, so rewriting it is not possible!</p>

<p>Thanks for any ideas that you may give us! </p>

<p>J-F</p>

## Answers
### Answer ID: 2465132
<p>The term you are looking for is Database <em>Replication</em>.  You can google that to get more information about the topic (my personal experience is limited).</p>

### Answer ID: 2465104
<p>This was already done by ical (an old SunOS calendar app).</p>

<p>What you store/remember/transmit when the app makes the changes is not just the database contents, but the actual change log (e.g. "delete record with ID 1", "update record with ID 2 with these fields", "insert record with these fields")</p>

<p>That way you can apply these changes to master DB later on, AND to filter them before applying</p>

