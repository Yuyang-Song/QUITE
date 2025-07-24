# SQL - Compare 2 text fields
[Link to question](https://stackoverflow.com/questions/25921430/sql-compare-2-text-fields)
**Creation Date:** 1411070707
**Score:** 0
**Tags:** sql-server
## Question Body
<p>I’m using a software known as FME Desktop. In this software we can issue SQL commands through an item called a transformer. I’m using a transformer called a SQLExecutor that uses a very simple query to make a comparison. Below is an explanation of what I’m trying to do with this SQL Query and the fact that it does not work when trying to compare 2 text fields.</p>

<p>I believe my issue is a limitation of SQL when used in the SQLExecutor. Let's say I have a layer of data called TEST.LEASE and I want to compare it to a layer called EDIT.LEASE based on one unique ID field. Both of these layers are in the same database. We use SQL Server for our stored data. There is a TEXT field in both layers called GIS_ID. This is a unique ID field. So what happens is we get updates on our LEASE layer and they start off being loaded to TEST.LEASE. When we have done our QA/QC of the data and we are satisfied that they are ready to be uploaded to EDIT.LEASE we then run an FME job that serves as our promotion tool. What this promotion tool does is that it checks various fields in TEST.LEASE to make sure they qualify for being uploaded (this part works 100% without issue).</p>

<p>Right before they are promoted to EDIT.LEASE we need to know if this will be a completely new record, in which case we will do an INSERT with FME. If by chance the GIS_ID already exists then we need to do an UPDATE to those records. The tool we have works perfectly for determining if it is an INSERT or UPDATE, except for one seemingly small thing … IT ONLY WORKS IF THE TEXT FIELD CONTAINS A NUMBER THAT DOESN’T HAVE A LETTER IN IT.</p>

<p>FYI: Someone at our company decided to make the GIS_ID field a text field. In my opinion it should have been an integer field because comparisons would have been super easy. But I can't change that now, it has already been decided by people who make way more money than I do that it will be a text field. </p>

<p>As mentioned … The GIS_ID is a text field (in both layers and they are both the same size, there is no difference in the field in both layers). As you may know, SQL doesn't care if it is a TEXT field or an INTEGER field when all that is contained in that field is a number. It can still compare 202 to 202 to see if they are equal to each other. For my example let's say I have a record in both TEST.LEASE and EDIT.LEASE where both of their GIS_ID fields equal 09198760. When I run the query below it runs perfectly.</p>

<pre><code>select OBJECTID 
from TEST.LEASE_UPDATE_INSERT_WRITER 
where GIS_ID = @Value(GIS_ID)
</code></pre>

<p>It runs perfectly, as I’ve mentioned, on the data if both GIS_ID text fields have only numbers in them. But if just one record contains an actual alpha, the SQL query will error out. </p>

<p>So if GIS_ID has 09198760a01 once the query reaches the “a” in GIS_ID a SQL error is returned. I’m not looking for a way for the job to continue and ignore those records, because I need ALL OF THE RECORDS to load. I need to know if anyone would know how to add to or rewrite the query above so that it loads both “number only text fields” and “numbers containing a letter fields.”</p>

<p>I hope that long explanation is clear. Please let me know if it isn’t. Thanks for any help you might be able to provide for me</p>

<p>Sincerely,
Tex</p>

## Answers
### Answer ID: 25926779
<p>Jeff is right and as a generic answer for regular sql users and even people using sql in their application code, if you are comparing text like the op mentioned, then you need to use single ' quotes '. </p>

<p>Where avalue = 'myvalue'</p>

<p>Otherwise sql server thinks it is an int, hence why it works when the value he's passing in is only numbers. It's not always easy to tell what the problem is when you're passing in parameters. </p>

<p>Where avalue = @myvalue</p>

<p>So you'll need to pay attention to that. Just wanted to mention this so maybe it helps someone else with a similar issue. I figured this out when we were getting errors from a field that had concatenated an id field i.e. it worked when the value = 2, but not 2,3 etc. Wrapping the parameter in single quotes easily fixed that as we were truly only concerned with value = '2' in our case. </p>

<p>Hope this makes sense. </p>

### Answer ID: 25921875
<p>I am assuming that the @value is the function that is causing you problems. I briefly checked their docs. it looks like you need to encapsulate like so '@value(GIS)'</p>

<p><a href="http://fmepedia.safe.com/articles/How_To/Executing-a-Stored-Procedure-on-Microsoft-SQL-Server-with-FME" rel="nofollow">http://fmepedia.safe.com/articles/How_To/Executing-a-Stored-Procedure-on-Microsoft-SQL-Server-with-FME</a></p>

