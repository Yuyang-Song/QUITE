# .NET XmlReader with &#39;FOR XML&#39; data
[Link to question](https://stackoverflow.com/questions/1035877/net-xmlreader-with-for-xml-data)
**Creation Date:** 1245801489
**Score:** 1
**Tags:** c#, .net, generics, data-access, for-xml
## Question Body
<p>Recently, in company we got some MSSQL database from some old project which we have to integrate in current solution.</p>

<p>Database has about 100-150 stored procedures that use FOR XML AUTO clause, so that queries return complete object-graph as XML instead of rows.</p>

<p>Quickest solution (for us in company) was to create serializable classes (with xsd-tool) based on the xml data returned from database. </p>

<p>This is code we use to instatiate those objects:</p>

<pre><code> public static T GetObjectFromXml&lt;T&gt;(DbCommand command)
    {
        SqlDatabase db = (SqlDatabase)DB;
        XmlReader xmlReader = null;
        T returnValue;

        xmlReader = db.ExecuteXmlReader(command);
        xmlReader.MoveToContent();

        XmlSerializer serializer = new XmlSerializer(typeof(T));

        returnValue = (T)serializer.Deserialize(xmlReader);

        xmlReader.Close();

        return returnValue;


    }
</code></pre>

<p>DB represents Database class from enterprise library.</p>

<p>When sp returns lots of data (for example some big collection of objects with lots of children,grandchildren,grandgrndchldrn...objects in it) execution of this method lasts very long.</p>

<p>The data in application will surrely continue to grow, and I must think of optimizing this. </p>

<p>So, I'm wondering if this is bad practice (using FORXML, XmlReader and Deserialize), or we should rewrite stored procedures  and use SqlDataReaders or Linq2Sql, or there is some perf.issue within this snippet (improper use of generics or something else) ?</p>

<hr>

<p><strong>Edit</strong>
I know that it is bad practice to load big ammount of data at once, and I know that load process should be splitted to smaller chunks, but I'm just wondering if something is wrong with this particular piece of code.</p>

## Answers
### Answer ID: 1035921
<p>You need to analyze this problem in terms of what's <em>in</em> the XML being returned. Is the XML returning data that doesn't need to be in memory all at once? Then deserializing it all into memory is probably not the best thing. If you only need to process the data a little at a time, then you should perhaps process the XML as XML and keep the XmlReader around to read a little at a time.</p>

