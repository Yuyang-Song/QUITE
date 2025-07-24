# Extra whitespace in XML file read from Oracle database - why?
[Link to question](https://stackoverflow.com/questions/15474875/extra-whitespace-in-xml-file-read-from-oracle-database-why)
**Creation Date:** 1363603407
**Score:** 1
**Tags:** xml, oracle-database, xmltype
## Question Body
<p>I am experimenting with Python and Oracle XML DB. I have a table with an XMLType column and an ID column in an Oracle 11g database. The storage model for the XML column is object relational. Sometimes I need to get a whole XML file, and often it is longer than 4000 characters, so I use this query to get a CLOB:</p>

<pre><code>select t.representation.getclobval()
from myxmldocs t 
where id=:documentId
</code></pre>

<p>When I run this query the output includes extra whitespace, with newlines and tabs between XML elements that were definitely not there in the XML docs I inserted. The effect is of some kind of formatting, so that the output looks like this:</p>

<pre><code>&lt;A&gt;\n
\t&lt;B&gt;&lt;/B&gt;\n
\t\t&lt;C&gt;Some text&lt;/C&gt;\n
\t\t&lt;C&gt;Some more text&lt;/C&gt;\n
\t&lt;B&gt;&lt;/B&gt;\n
...
</code></pre>

<p>and so on. Quite pretty and readable, but why am I getting it? It also messes other libraries that I am using that choke on the extra whitespaces.</p>

<p>If I remove getclobval() my Python client does not get a CLOB but an Object and I don't know what to do with it.</p>

<p>This appears consistent; I get this problem using the sqlplus command line client, and also creating other tables using different XML Schemas, and then querying them. In a previous version of my prototype I had the XMLType column use a CLOB storage model and didn't have this problem. </p>

<p>How should I rewrite the query to just get a CLOB with the XML file without the extra formatting?</p>

<hr>

<p>Update: as requested in the comments, this is the output I get running the query <code>select dump(t.representation) from myxmldocs t where id=:documentId</code> from the command line client (replacing of course :documentId with an actual, existing ID from the database):</p>

<pre><code>DUMP(T.REPRESENTATION)
--------------------------------------------------------------------------------
Typ=58 Len=218: 32,156,148,1,0,0,0,0,80,193,223,20,0,0,0,0,216,15,47,21,0,0,0,0,
80,44,55,21,0,0,0,0,0,202,154,59,160,15,0,0,160,15,0,0,1,0,4,0,220,190,195,71,1,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,174,33,65,0,15,0,72,0,1,0,0,0,0,0,0,0,49,0
,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
,0,0,0,0,0,0,0,0
</code></pre>

## Answers
### Answer ID: 15476505
<p>in 11g you can use <code>xmlserialize</code> (in fact you should not use <code>getclobval</code> anymore. it's not recommended for performance reasons)</p>

<pre><code> SQL&gt; select t.test.getclobval() from testxml t where id = 1;

T.TEST.GETCLOBVAL()
--------------------------------------------------------------------------------
&lt;A&gt;
  &lt;B&gt;
    &lt;C&gt;foo&lt;/C&gt;
    &lt;C&gt;foo2&lt;/C&gt;
  &lt;/B&gt;
&lt;/A&gt;


SQL&gt; select xmlserialize(document t.test as clob no indent) from testxml t where id = 1;

XMLSERIALIZE(DOCUMENTT.TESTASCLOBNOINDENT)
--------------------------------------------------------------------------------
&lt;A&gt;&lt;B&gt;&lt;C&gt;foo&lt;/C&gt;&lt;C&gt;foo2&lt;/C&gt;&lt;/B&gt;&lt;/A&gt;
</code></pre>

### Answer ID: 15476476
<p>The <code>getClobVal()</code> method shouldn't modify the indentation of data. Your XML may have been formatted during or before the insertion.</p>

<p>You can <a href="http://docs.oracle.com/cd/E11882_01/appdev.112/e25788/t_xml.htm#i1009783" rel="nofollow">transform</a> the XMLType to remove whitespaces:</p>

<pre><code>SQL&gt; SELECT XMLTYPE.createxml(
  2  '&lt;a&gt;
  3     &lt;b&gt;&lt;c&gt;&lt;/c&gt;&lt;/b&gt;
  4  &lt;/a&gt;'
  5  ).transform(XMLTYPE(
  6  '&lt;?xml version="1.0"?&gt;
  7  &lt;xsl:stylesheet version="1.0"
  8     xmlns:xsl="http://www.w3.org/1999/XSL/Transform" &gt;
  9     &lt;xsl:output method="xml" indent="no"/&gt;
 10     &lt;xsl:strip-space elements="*"/&gt;
 11     &lt;xsl:template match="@*|node()"&gt;
 12     &lt;xsl:copy&gt;
 13        &lt;xsl:apply-templates select="@*|node()"/&gt;
 14     &lt;/xsl:copy&gt;
 15  &lt;/xsl:template&gt;
 16  &lt;/xsl:stylesheet&gt;
 17  ')).getClobVal() FROM dual;

&lt;?xml version="1.0" encoding="utf-8"?&gt; 
&lt;a&gt;&lt;b&gt;&lt;c&gt;&lt;/c&gt;&lt;/b&gt;&lt;/a&gt;
</code></pre>

