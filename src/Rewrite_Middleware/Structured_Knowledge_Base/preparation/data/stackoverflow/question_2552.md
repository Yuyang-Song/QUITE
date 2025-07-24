# Java/MYSQL - data processing within resultset
[Link to question](https://stackoverflow.com/questions/39612727/java-mysql-data-processing-within-resultset)
**Creation Date:** 1474450394
**Score:** 0
**Tags:** java, mysql
## Question Body
<p>My Java program retrieves a large amount of data from my database (localhost / MYSQL). I do 100-200 queries where the result set returned from each query contains 3000-10000 rows. Each rows has 8 columns that contains timeStamp, double, Bigdecimal etc. </p>

<p>After each query I run through each row and depending on row data do some calculations. I am the only one using the database so too many connections and queries is not a factor.</p>

<p>At this point I do the data processing within the result set / while-loop. It works fine, however I need to extend the number of calculations. Among other things I need to do some comparing of data between rows. </p>

<p>Before I rewrite the entire code one question: would it be smarter to create a class and then for each row within the result set, create an object -> put it into an Array </p>

<ul>
<li>close connection to DB </li>
<li>do the calculation </li>
<li>save result (in a file or DB) </li>
<li>do query number 2 </li>
<li>create an object for each row </li>
<li>add to array</li>
<li>close connection and so on.... </li>
</ul>

<p>My project will not end up as final product. The purpose of the project is to test a number of hypothesis.</p>

<p>Thank you for your time.  </p>

