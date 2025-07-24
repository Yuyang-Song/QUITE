# Symfony - Log runnables natives queries when database is out
[Link to question](https://stackoverflow.com/questions/28430183/symfony-log-runnables-natives-queries-when-database-is-out)
**Creation Date:** 1423566627
**Score:** 1
**Tags:** symfony, doctrine-orm
## Question Body
<p>I'am working on a Symfony app that provides a rest web service (simple HTTP Request with JSON).
That service check some rules and inserts few lines in two MySQL table (write only).</p>

<p>For optimize reason, even if Doctrine bundle is available, i use native MySQL Query (with bind params) to insert this lines.</p>

<p>My need is : If for any reason, the database is not available, write "runnables" queries into a log file.</p>

<p>The final purpose is that when database is back, i want to be able to execute directly the file's content on the database.
Note that there is no unique constraint (pk is a generated uuid) and no lock or transaction to handle (simple insert statements).</p>

<p>I write a custom SQLLogger, but when <code>$connection-&gt;insert(...)</code> is called, the connect fail before logger is called.</p>

<p>So, my question is : There is a way to get the final query (with binded parameters) without database connection ?</p>

<p>Or should i rewrite the mecanism that bind params into query and log it myself when database is not available ? </p>

<p>Best regards, </p>

<p>Julien</p>

## Answers
### Answer ID: 45568972
<p>As the final query with parameters is build by the database, <strong>there is just no way to build the query with PHP and to be garanteed that the query will be the same as the database</strong>.</p>

<p>The only way si to build query without binded parameters, but this is clearly not a good practice.</p>

<p>So, i finally decided to store all the JSON (API request body) in a file if the database is not available.</p>

<p>So when the database is back, instead of replay SQL queries, i can replay the original HTTP query.</p>

<p>Hope this late self-anwser will help someone.</p>

<p>Best regards.</p>

