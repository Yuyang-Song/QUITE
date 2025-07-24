# Best place to put SQL statements in Java
[Link to question](https://stackoverflow.com/questions/18232243/best-place-to-put-sql-statements-in-java)
**Creation Date:** 1376484640
**Score:** 3
**Tags:** java, sql, spring, architecture
## Question Body
<p>I know there are pros and cons to each approach, but is there a best practice on where to put the SQL statements?  I've always put them inside of the Java classes, but I came on to a project where they are injected via Spring string constructors.  The reason is that if the SQL statements are in an application context, you don't have to remove all of the " and + to get the SQL to copy/paste on the server.  I don't think that's a good reason, but that's what I stepped in to for the moment.
I know this can also be done with properties.</p>

<p>So my question is should the SQL statements go in the application context, Java file, properties file, or some place I'm not thinking of?</p>

<hr>

<p>Update:</p>

<p>From the replies I got, it seems that prepared statements are the best place for SQL statements.  But what about SQL statements that are generated on the fly dynamically?  The code will have many different strings that will all be concatenated together to make a query depending on what is passed in.  If we have a method with 6 input parameters that could be passed in (or not), I would need an incredible amount of prepared statements to account for all the possibilities.</p>

<p>I've considered using an ORM tool such as Hibernate, but I'm working with an iSeries database and the tables are not well constructed.  Perhaps someday I can rewrite Hibernate in and write out the 900 line SQL statements... but one step at a time.</p>

## Answers
### Answer ID: 18238183
<p>There's no rule about where is the best place : it's somehow like "where's the best place to put my keys at home".</p>

<p>If your project needs require you to have the SQL accessible from outside the app, then why not putting them in properties files. In that case, you may want to check that changes in the Sql are still compatible with your app by doing some JUnit tests.</p>

<p>Stored procedures are good because of their execution speed, but bad because they split your app configuration in two places. In addition they are tightly coupled with the database software (which again depending on the project can be a good or bad thing)</p>

<p>Hope my answer helped you asking your self the right questions in your own context.</p>

<p>Best Regards,
Zied</p>

### Answer ID: 18232408
<p>Agree with Thiharas answer, but why not go one step further and save them in .sql files within the application. With each query having its own file it becomes easier to manage.</p>

<p>That is of course if an ORM framework like Hibernate will not be suitable for your application.</p>

### Answer ID: 18232359
<p>That's not the only reason. When the SQL statements are out side of the Java code you can change it without having to re compile and deploy your application. If the queries are periodically loaded from the files (say once every 8 hours) then you don't even have to do a server restart. That will be very beneficial for the people doing production application support.</p>

<p>Also regarding the first reason you don't consider a good reason; when you have to debug a big assed SQL statement and need to paste it in a query executor removing all <code>+</code> and '"' signs I'm sure you will change your mind :-)</p>

