# Deploying large amounts of static data with Android application
[Link to question](https://stackoverflow.com/questions/7056548/deploying-large-amounts-of-static-data-with-android-application)
**Creation Date:** 1313321467
**Score:** 3
**Tags:** android, database, json, sqlite, loading
## Question Body
<p>I have an Android app that needs to work offline and requires a lot of static data. </p>

<p>Currently I'm using a JSON file in the /res/raw and loading it with the Jackson parser into my POJO scheme. It works really well since I have an external program that will be generating this data and once in a while when there is a change I'll just publish new version to the Market so I don't have to deal with running an update server and so on.</p>

<p>However, right now my JSON file is about 2.5MB with limited dataset for testing, in the end it'll be about 5-10MB.</p>

<p>The issue is that it already takes about 3-5 seconds to parse the file and this needs to be done every time the application is restarted.</p>

<p>So, what are my options here? I could put the data to a sqlite database, but that would require rewriting the external application and changing the data structure quite a bit. But then I could only query the things I need at the moment and not loading the entire thing at once.</p>

<p>Is there some easier/better way? Also, is there a good way to publish the app with the sqlite database? All the articles I've found talk about creating the database for user data at first startup, but this is not user data and I need it to be deployed from the Market.</p>

## Answers
### Answer ID: 7057408
<p>JSON feels like the wrong approach for this - it's a good way to encode data to transfer, but that's pretty much it.</p>

<p>It'd be nice to have a bit more info on what exactly your app does, but I'm struggling to imagine a use-case where having several MB of POJOs in memory is an efficient solution. I think it'd be much better to use SQLite, and this is why:</p>

<blockquote>
  <p>I could put the data to a sqlite database, but that would require rewriting the external application and changing the data structure quite a bit.</p>
</blockquote>

<p>You can still use your other program's JSON output, but instead of loading everything into POJOs with Jackson, you could populate the database on first app launch. This way, the app boot time is negligible if the dataset is unchanged. </p>

<p>If you still want to work with POJOs in the rest of your app, it'd be trivial to write a query that retrieved data from the database, and created objects in the same manner as Jackson.</p>

<blockquote>
  <p>But then I could only query the things I need at the moment and not loading the entire thing at once.</p>
</blockquote>

<p>What're you doing that requires access to all the data at once? Searching or ordering a set of objects is always going to be slower than a SQL query to achieve the same thing.</p>

<blockquote>
  <p>Also, is there a good way to publish the app with the sqlite database?</p>
</blockquote>

<p>You can definitely ship your app with a database, though I've not done so personally. This is a relevant question:</p>

<p><a href="https://stackoverflow.com/questions/4078745/by-default-load-some-data-into-our-database-sqlite">By Default load some data into our database sqlite</a></p>

<p>Hope that's of some help.</p>

### Answer ID: 7057814
<p>There's an excellent API called JExcel (just google it) that works with .xls spreadsheets. If you're not going to be doing any selecting and just loading data from a source, I like to use JExcel because it's more manageable from a desktop and produces easier-to-read code.</p>

<p>Not sure of any performance differences, however. Just throwing in my 2 cents :p</p>

