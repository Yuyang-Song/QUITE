# Large Database Schema vs Small Schema and a BLOB/CLOB XML
[Link to question](https://stackoverflow.com/questions/16905929/large-database-schema-vs-small-schema-and-a-blob-clob-xml)
**Creation Date:** 1370293978
**Score:** 0
**Tags:** sql-server, database, orm, mfc, large-data
## Question Body
<p>I have searched around on StackOverflow and I have not found this discussion so I would like to post it here to get opinions from the community.  I also think this discussion is probably applicable to other teams out there as well so hopefully this turns out to be a useful post.  If this is a duplicate topic, please let me know and I will remove it.</p>

<p><strong>Background:</strong>
I work on a fairly large contracted software project that is now about 15 years old.   This system is a client-server style application with an SQL Server database and a thick client written in MFC/C++ running on Windows.  The API of this application is entirely flat and non-object oriented because it is entirely encapsulated in COM.  The database roughly has 780 tables and the application has over 7 million lines of code.  Over the past 8 years or so, the majority of the tables have been added and with the new enhancement requests in the pipeline, we do not see this slowing down anytime soon.  The original architectural approach was to store everything in tables/columns represented as it would be in the class hierarchy.  Exactly how ORM frameworks work (Hibernate, Entity, etc.) for persisting data.<br>
Over the past few years our client has expressed the desire to rearchitect the system and do a total rewrite of the application since the system has essentially out-grown itself and is heavily limited by COM.  We have the chance to rearchitect the modernize the system, one question we have is about the scalability of our database.  </p>

<p><strong>Main Question:</strong>
Since we have 780 tables now and we foresee breaking 1000 tables in the not so distant future, would it make sense for us to continue using this architectural approach or create 10 to 20 tables and have almost all of the data stored in a BLOB column as XML? Probably 600 of the 700ish tables are for a single parent class that has tons of children and children of children and so on.</p>

<p><strong>My Thoughts:</strong>
I have written programs both ways and I think there is a major performance gain by storing data as XML in a blob because there aren’t 100s or 1000s of queries being fired off to insert and retrieve data. It is been from my experience that the performance of parsing the XML is much faster than dealing with a database of 1000 tables.  Another advantage of the XML approach is it won’t normally require schema changes.  On the other hand there are performance issues with XML as well. </p>

<p>Please post ideas, facts and any studies on this topic if you know of any.  All information would be helpful and appreciated.</p>

<p>Thanks in advance!</p>

## Answers
### Answer ID: 16906988
<p>Having worked with large data systems in various database technologies, I would recommend not using XML for the task.</p>

<p>The good news is that SQL Server of course supports the XML data type and you can actually run quite complex queries on XML in TSQL. So you don't even need to suck the XML out into your application to make a stored procedure as an example.</p>

<p>The problems I've seen with storing serialized data as XML in a relational data store:</p>

<ol>
<li><p>It is slow. Run some tests with the XML data type in SQL Server and you'll see that examining it in TSQL is quite a bit slower than just bringing back "regular" data.</p></li>
<li><p>It is too verbose. The size of XML is quite a bit larger than a format like JSON. You'll lose the ability to query the data in TSQL going with JSON, but when objects get big, it's nice to save space.</p></li>
<li><p>I can't tell you how many times I've banged my head against a wall when maintaining a legacy app that stored XML in SQL Server. It's so frustrating if the code that originally serialized/deserialized the XML can't be found. It might not seem like an issue now, but when you bring other new developers into the system in the next few years it will become a problem.</p></li>
<li><p>This is maybe personal preference, but no one is using XML these days for data storage. JSON is the latest and greatest. Document databases like CouchDB, MongoDB, Elastic Search all use JSON as their lingua franca. All the tools these days use JSON as well. It still allows you to serialize/deserialize objects easily and it's lighter and in my opinion not so ugly to read. =)</p></li>
</ol>

<p>Bottom line:</p>

<p>I'd at least consider going all the way with a document database (MongoDB, CouchDB, Couchbase, Riak, Elastic Search). Different mindset, but might make life easier.</p>

<p>If not, then I would still use blobs but strongly consider JSON instead.</p>

<p>Failing those two, I would only use the XML data type in SQL Server for storing the XML objects.</p>

