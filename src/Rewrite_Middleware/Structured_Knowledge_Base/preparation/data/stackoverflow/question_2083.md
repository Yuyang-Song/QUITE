# How do I structure Java classes for this Android project to represent a child relationship in the database?
[Link to question](https://stackoverflow.com/questions/18250286/how-do-i-structure-java-classes-for-this-android-project-to-represent-a-child-re)
**Creation Date:** 1376560478
**Score:** 1
**Tags:** java, android, orm, relational-database, greendao
## Question Body
<p>I'm learning Android by forking and modifying an open source app, FrontlineSMS for Android.  Here's <a href="https://github.com/robhawkins/frontlinesms-for-android" rel="nofollow">my copy</a>!</p>

<p>I want to add a few tables, Poll and PollResponse, to the database, where Poll->PR is a one-to-many relationship.</p>

<p>I've added classes for Poll to the project.  What is the "right" way to define the PollResponse object?</p>

<p>Saving the Poll data happens on <a href="https://github.com/robhawkins/frontlinesms-for-android/blob/master/src/net/frontlinesms/android/activity/Keyword.java#L562" rel="nofollow">line 562 of Keyword.java</a>, and somehow in there a row is added to the database with a new ID created for that row.  This is the place where I also want to save a few rows into PollResponse (which doesn't exist yet) and assign their id_poll field the value from the newly created Poll row.  Is there a clean way to accomplish this child relationship, as some part of src/net/frontlinesms/android/model/Poll.java or /src/net/frontlinesms/android/model/PollDao.java?  Or do I need to create completely separate PollResponse objects, save the data for the Poll, then query the database for the newly created ID and save that in PollResponses?  The latter is the only way I can think to do it but it seems ugly.  I also tried searching around for solutions to this but I may not have the right keywords in mind.</p>

<p>I discovered how to create a new table Poll by creating Poll.java and PollDao.java and adding the class to /src/net/frontlinesms/android/db/FrontlineSmsSqliteHelper.java , but I'm largely fumbling around this project, reading Android development guides and trial and error.  Sorry for the lack of links, I'm only allowed 2 until I get more than 10 reputation.  Thanks for your help!</p>

<p>*EDIT - Could there be a case for rewriting this project to use an ORM like greenDAO?  Again I'm still learning Android so I'm not sure if the project uses any packaged ORM.  It seems like it's custom written.</p>

