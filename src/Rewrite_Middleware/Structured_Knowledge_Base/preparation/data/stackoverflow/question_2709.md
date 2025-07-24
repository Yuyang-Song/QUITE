# Loops in Database vs in application
[Link to question](https://stackoverflow.com/questions/48458836/loops-in-database-vs-in-application)
**Creation Date:** 1516959742
**Score:** 1
**Tags:** java, mysql, sql, vb.net, loops
## Question Body
<p>Soon I'm planning to rewrite my application to Java (from VB.NET) and since I got that chance I'm planning to do a lot of code cleanup in the new app as the one written in VB.NET is my first application and it gone pretty big for one person. </p>

<p>Anyway, I've been thinking about using loops in MySQLs Stored Procedures (which I hate, I can't really tell why) and if maybe it is better to query database for data I need to perform loop with then use client PC to perform all those operations and then send the data back to database.</p>

<p>An example of operation: in my applications there are goods coming in and out. When I'm selling goods I need to connect sells with previously bought goods with First in First out rule. For example I bought 10 bananas, then another 10 and then 20. Then I want to sell 30 of them so I link first 10 bananas and it leaves me with 20 so I link it with another 10 so it leaves me with 10 and then I link it with the last batch of bananas but I don't use all of them so I got 20 bananas left on me.</p>

<p>The way I see it:</p>

<ol>
<li><p>Loops in Stored Procedures should be faster because it got all the data in one place but I'm not sure if it is a good practice to perform this kind of operations in database.</p></li>
<li><p>Loops in application needs to get data from database and then send it back so that may make it bad but personally I think loops in other languages than SQL are easier to read and debug.</p></li>
</ol>

<p>What do you think?</p>

## Answers
### Answer ID: 48463172
<p>Trying to answer objectively I'd say: It depends on the complexity of your query, the quantity of Data you need to  process, and the DBMS you're using. </p>

<p>I'd also like to add that just because data is processed within the database, it doesn't has to be faster than you're application - The main quality of databases lies within SQL set-based operations, as Gordon Linoff already wrote.</p>

<p>If you're not analyzing several hundredthousands of datasets, then probably you don't need to worry about performance much, but more about which is the most maintainable way.</p>

<p>In my experience a combination of simple selects providing filtered Data and smart loops processing them within in my application always did a good Job, as it was maintainable and reasonably fast. </p>

<p>In your Example this means: Use SQL to get your stock filtered for Bananas and sort them by date (obviously). Then loop through your results in the application and stop once you got the desired quantity of Bananas</p>

<p>Using windowed Sum-Function you might even limit the query results to the point, that the cumlative sum of the quantity passes a certain value.</p>

