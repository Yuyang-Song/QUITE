# How to store huge number of rows of data while processing.In REST is it valid?
[Link to question](https://stackoverflow.com/questions/61184147/how-to-store-huge-number-of-rows-of-data-while-processing-in-rest-is-it-valid)
**Creation Date:** 1586766806
**Score:** 0
**Tags:** c#, rest, optimization
## Question Body
<p>Looking for a piece of advice......</p>

<p>I am analyzing an old C# web method to rewrite in REST. In the old method I observed that one private method is getting called multiple(nearly 25+) times. This private method connects to database and just calls simple select statement with simple where condition. This returns single row.</p>

<p>In my new method, I am planning to select the entire table content (400 rows approximately) and store in .net side whenever any data needed from this result set thought of querying it by writing LINQ or lambda. Is this the correct way of storing this huge dataset during this main method execution? Is this the correct approach?? How can I optimize? Can I store this data in a static datatable?</p>

## Answers
### Answer ID: 61187223
<p>For your scenario, the approach that I would recommend would be:</p>

<h1>Construct a stored procedure</h1>

<p>Now, you may ask, why another stored procedure when you're already invoking a SELECT statement to the Database. </p>

<ol>
<li>Separation of database logic from business logic. Ideally, your .NET code should only consists of business logic.</li>
<li>Unless you are already using Parameterized Query in your SELECT statement, otherwise, Stored Procedure offers:

<ul>
<li>Better protection against SQL Injection Attacks</li>
<li>Lower network traffic (sending Stored Procedure Name vs Dynamic Query)</li>
<li>SQL able to optimize Stored Procedure in its cached query plan better than Dynamic Query. Optimizing Query Plan</li>
</ul></li>
<li>Retrieval of records via Stored Procedure will perform way better than using foreach/LINQ/Lambda in C#. Database is optimized for searching for data and it has larger memory and better CPU threading to handle these data retrieval operation. This is especially so if you have proper DB index on your search criteria. We will cover this in the next section.</li>
</ol>

<p>Reference: <a href="https://codingsight.com/dynamic-sql-vs-stored-procedure/" rel="nofollow noreferrer">Dynamic SQL vs Stored Procedure</a></p>

<h1>Create a non-clustered index for your search criteria</h1>

<p>If your search criteria is not currently indexed, you may consider creating a non-clustered index for that column. This will further improve your retrieval speed.</p>

<p>With these in place, you can support up to thousands of retrieval to this table without any significant impact to your application performance.</p>

### Answer ID: 61184726
<p>Well it depends.</p>

<p>Calling Sql server select with where 25 times per one method is not good thing. 
Each out of process call consumes much more time comparing with the local one (despite that ADO Net connection caching whatever)</p>

<p>To cache 400 rows looks not a big deal actually if it is the same set for each 25 calls.
It is small enough to be processed by C# linq query in effective way.</p>

<p>However what about scalability? Sql server can handle hundred thousands of rows in effective way using indexes, special caching etc.</p>

<p>Let's imagine that database grows and you have 4M rows to be checked to get the one row. 
I do not think that it is fine to have 4M records to be read by C# and filtered locally in the memory.</p>

<p>So you have to check the data and the code that is written. </p>

<p>The best way is to mix two approaches into the one.</p>

<p>For example you can check why so many db calls are in one method. 
Is it possible to reduce db calls quantity?
Is there any way to do some join or additional calculations on the SQL server side? 
Actually SQL is much more than flat table storage tool.</p>

<p>You can create stored procedure (or two or three) and implement some logic using the SP to reduce db calls. To reduce db calls quantity and keep data on the SQL side at the same time.</p>

