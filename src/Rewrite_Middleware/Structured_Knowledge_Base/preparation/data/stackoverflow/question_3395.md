# How to create controller with OData function but without DBSet in EF Core 8
[Link to question](https://stackoverflow.com/questions/78383713/how-to-create-controller-with-odata-function-but-without-dbset-in-ef-core-8)
**Creation Date:** 1714038254
**Score:** 0
**Tags:** c#, odata, webapi, .net-8.0, ef-core-8.0
## Question Body
<p>is it possible to create a controller in .net 8 that would work with OData, I mean the $filter, $select, $count, $skip capabilities, so as to finally provide the client with two GET endpoints: &quot;/api/name/&quot; and &quot; /api/name/$count&quot;, standardly as ODataControler does, but I don't want to rely strictly on an object from the database, I don't want to have a DBSet with a mapping of a given table. The assumption is that the client knows what the columns are and can prepare the appropriate OData request. However, the query result is to be returned in the form ICollection&lt;IDictionary&lt;string, object&gt;&gt; where we have a list of rows and the name of the column and its value in the dictionary.</p>
<p>Ultimately, I do not want to be rigidly based on one table structure, because depending on the client, I will want to present a different set of data in a table on the website, different parameters.</p>
<p>I mentioned OData because I would rather not have to rewrite pagination, filtering, etc. myself. But maybe there is another library that will help me achieve something like this?</p>

