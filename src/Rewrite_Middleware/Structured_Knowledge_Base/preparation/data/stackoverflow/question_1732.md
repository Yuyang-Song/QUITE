# Rearchitecture ASP.NET app by replacing SQL Server with NoSQL
[Link to question](https://stackoverflow.com/questions/5461994/rearchitecture-asp-net-app-by-replacing-sql-server-with-nosql)
**Creation Date:** 1301329252
**Score:** 2
**Tags:** asp.net, mongodb, nosql
## Question Body
<p>We have an ASP.NET app with SQL Server &amp; it is a photo &amp; video sharing site. 
Details of photos and videos are stored in tables &amp; the files are in the file system.</p>

<p>Database has 75 tables and 225 stored procedures. The app will be ready for production deployment within next 6 months.</p>

<p>Due to longer time growth concerns, we decided to switch to NoSQL (<strong>MongoDB</strong>) database.</p>

<p>We have few questions regarding the best way to approach this:</p>

<ul>
<li><p>Is it better to deploy the app with SQL Server backend and migrate to NoSQL later?</p></li>
<li><p>OR re-architecture now and rewrite/recreate database, tables, procedures and data layer</p></li>
<li><p>How difficult will it be re-architecture/recode with MongoDB? Any tools or BKMs?</p></li>
</ul>

<p><strong>EDIT:</strong>
Our app is Youtube+Flickr type site where user will share photos and videos with lots of comments, tags and ratings (photo\video &amp; comments). </p>

<p>Is NoSQL a better database to move to? Reason for moving: cost + read query speed</p>

<p>Please help me with you valuable advise.</p>

<p>Thank you very much.</p>

## Answers
### Answer ID: 5469154
<p>I've done such a migration a few month ago, during the early developement stage of a website in ASP.NET. It was a hard decision, but I could concentrate on that migration. The reason why I did this migration was the ORM that I couldn't trust anymore and some very slow queries that I had no idea how to optimize.</p>

<p>During coding phase, what I figured out was : I was spending a lot of time with the data model in SQL Server (using Entity) and all the plumbery code. 
Now, no more store procedures (C# and Linq code instead), no more 2 layers to maintain (the code is the model). </p>

<p>My small experience says : The earlier the better but don't get me wrong, before migrating you really have to think in Document rather than in RDBMS. This means you may have to partially change the businness DataModel to correctly utilize MongoDB features, otherwise you could get bad performances and Mongo DB is useless for bad models.</p>

<p>Another point is the admin stuff. You'll have to quickly learn Mongo DB admin to be up to speed. And even if the tools are good, they completely differ from SQL Server tools.</p>

<p>In conclusion, If you're convinced MongoDB is your future data store and search database, 
(and it was in my case), read documentation, take time to do some Proof Of Concept. Then you can think Document and load test you new model.</p>

### Answer ID: 5463736
<p>This question raises more questions than answers.</p>

<ol>
<li>Have you benchmarked your current implementation in terms of requests/responses?</li>
<li>Why MongoDB out of all possible NoSQL databases? (Don't get me wrong, I love Mongo, but love and hype should not weigh in technology choices)</li>
<li>Are you certain you will get the large userbase you're expecting? Why are you so certain?</li>
<li>Using stored procs seems to tip off that you aren't using an ORM? Why not?</li>
</ol>

<p>Generally, I'm against these types of re-architectures. Firstly, you need to get your whole team acclimated to how Mongo affects development. Secondly, your ops team needs to get acclimated to how to deploy and maintain a Mongo installation. More likely than not, this will prevent you from launching in a timeline you want to launch.</p>

<p>I'd say that you should probably launch as is, fix the ORM part if you aren't using one, benchmark your app, benchmark a prototype of your app backed by Mongo and if the performance advantages are so big that it warrants the pain of re-architecture do it.</p>

<p>To your latter question, there aren't any tools right now, as far as I can tell, that'll automate or semi-automate the database import/export from SQL Server to Mongo. There are barely tools to do that for MySQL.</p>

### Answer ID: 5462167
<p>I agree. Switching now is better, if only to avoid the data migration headache switching post-deployment will require.</p>

### Answer ID: 5462140
<p>Change is always exponentially more expensive the later it is introduced to a project.  This is a core principle of software engineering.  You should do this now.</p>

<p>That said, I question your long-term vision.  Relational databases, used properly, have a lot of performance in them.</p>

### Answer ID: 5462095
<p>Your core question appears to be whether to make the switch to MongoDB now, or deploy on SQL and go to MongoDB in a future release.  </p>

<p>You do not appear to be using an ORM (e.g. NHibernate, Entity Framework.)  Setting other concerns aside, if you're convinced that you want to go to NoSQL, then I would do it now rather than later.  Unless you integrate a Provider model for your data access, changing the underlying data access strategy after it is already established would be difficult.</p>

