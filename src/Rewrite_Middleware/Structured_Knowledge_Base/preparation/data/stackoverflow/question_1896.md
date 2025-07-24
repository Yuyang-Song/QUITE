# SQL Server XML shredding performance
[Link to question](https://stackoverflow.com/questions/11488577/sql-server-xml-shredding-performance)
**Creation Date:** 1342313964
**Score:** 5
**Tags:** xml, performance, sql-server-2008-r2
## Question Body
<p>I am working with NOAA's current observation XML (example: <a href="http://w1.weather.gov/xml/current_obs/WASD2.xml" rel="noreferrer">Washington DC</a>) and am shredding the files for the 4000+ stations into a SQL Server 2008 R2 table.  After trying many different approaches, I have one that I am moving forward with.  </p>

<p>This question is about the performance between the different methods and most importantly why is it so drastic.</p>

<p><strong>First Attempt</strong></p>

<p>Working in C# I parsed all files with Linq to XML and wrote the resulting records to the database with Linq to SQL.  The code for this is predictable, so I won't bore you with it.</p>

<p>Rewriting with linq to Entity Framework didn't help.</p>

<p>This resulted in the application taking running for over an hour and having only processed 1600 or so files.  The slowness is the result of both Linq to SQL and Linq to Entities executing an insert and select for each record.</p>

<p><strong>Second Attempt</strong></p>

<p>Still working in C# I attempted to speed it up by using the bulk insert methods available online (example: <a href="http://blog.tanneryd.com/2011/11/speeding-up-inserts-using-linq-to-sql.html" rel="noreferrer">Speeding up inserts using Linq-to-SQL - Part 1</a>).</p>

<p>Still slow, although noticably faster than first attempt.</p>

<p>At this point I moved to using a stored procedure to handle the XML shredding and insert with the C# code concatenating the files into one XML string and adding a wrapper tag.</p>

<p><strong>Third Attempt</strong></p>

<p>Using SQL Server's XML Query similar to this (@xml is the xml file) [from memory]:</p>

<pre><code>select credit = T.observation.value('credit[1]', 'varchar(256)')
       ,... -- the rest of the elements possible in the file.
from @xml.nodes('wrapper') W(station)
    cross apply W.station.nodes('current_observation') T(observation)
</code></pre>

<p>I let it run for 15 minutes and cancelled with 250 or so records processed.</p>

<p><strong>Fourth Attempt</strong></p>

<p>I changed the query to use OpenXML:</p>

<pre><code>declare $idoc int

exec sp_xml_preparedocument @idoc output, @xml

select Credit
       ,... -- the rest of the elements
from openxml(@idoc, '/wrapper/current_observations', 2)
    with (
        Credit varchar(256) 'credit'
        ,...) -- the rest of the elements

exec sp_xml_removedocument @idoc
</code></pre>

<p>This processed all 4000+ records in 10 seconds! Quite acceptable.</p>

<p>While I expected some differences between the methods, I didn't expect the difference to be so dramatic. </p>

<p>So my question is simply, </p>

<p><em>'Why is there such a drastic difference in performance between the different methods?'</em></p>

<p>I am quite happy to be shown that I was using the first 3 wrong.</p>

## Answers
### Answer ID: 11506271
<p>Did you try the text accessor?  I got a 15-20% improvement in my repro against a 6MB xml file with 4,096 records in it, although this only applies to untyped XML (no XSD associated in SQL Server).</p>

<p>I also found my query running in 10-12 seconds so am still slightly mystified by your 43 seconds.  What version/service pack of SQL Server are you using?  I remember there used to be a problem in SQL 2005 when inserting into a table variable, but thought this was fixed.</p>

### Answer ID: 11495831
<p>Can you confirm you're not using the parent axis ('..') in your query?  This can destroy performance.  You can also add the text() accessor which should also improve performance as below:</p>

<pre><code>select
o.c.value('(credit/text())[1]', 'varchar(max)'),
--...
from @xml.nodes('wrapper/current_observation') o(c)
</code></pre>

### Answer ID: 11490361
<p>One thing you <em>might</em> be able to do to speed up the XQuery option is to avoid the cross join.</p>

<p>I can't see what your XML looks like - that Washington DC sample only contains a single node - but assuming the XML just contains a <code>&lt;wrapper&gt;</code> and then a list of <code>&lt;current_observation&gt;</code> inside that, then you could optimize your XQuery to read:</p>

<pre><code>select 
    credit = T.observation.value('credit[1]', 'varchar(256)')
    ,... -- the rest of the elements possible in the file.
from 
    @xml.nodes('wrapper/current_observation') T(observation)
</code></pre>

<p>and that should work a lot faster than the speed you've seen in your tests.</p>

<p>If you have the time to try this - I'd be most interested in knowing how this modified approach stacks up - against your original XQUery and against the <code>OPENXML</code> solution.</p>

