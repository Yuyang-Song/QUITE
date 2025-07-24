# Formatting problems with csv file
[Link to question](https://stackoverflow.com/questions/10306461/formatting-problems-with-csv-file)
**Creation Date:** 1335303917
**Score:** 1
**Tags:** java, excel, csv, jersey, jax-rs
## Question Body
<p>Ok, I've checked <a href="https://stackoverflow.com/questions/137359/excel-csv-number-cell-format">this SO question</a>, but it has not helped me at all.  </p>

<p>I need to get a csv file to a user, so they can export it into PeopleSoft.  One of the fields (batch_id) has to be 4 digits exactly, and currently Excel keeps dropping those leading zeroes.  I've also opened the csv file in TextPad and verified that those zeroes are gone.</p>

<p>So heres the process: </p>

<p>Browser is pointed to myapp/Batch/course as shown below:</p>

<pre><code>    @GET
    @Path( "Batch/{course}" )
    @Produces( "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" )
    @HttpHeader( values="Content-Disposition=attachment;filename=Batch.csv" ) 
    public String getNextBatch ( @PathParam( "course" ) String course )
    {
      ...
    }
</code></pre>

<p>Within that method, an Oracle database is queried and gets data sent back as XML (In the XML, batch_id has the correct number of digits). That XML is then processed into one long comma separated String via StringBuffer.append(), which the method then returns.  The @Produces attribute takes that String and makes sure Excel handles it, and the file is downloaded.</p>

<p>I can get it to appear as 4 digits by appending tabs after each comma, but then it bombs when its loaded into PeopleSoft.  I can also get it to appear with the correct 4 digits if I single quote it (either a single leading quote, or quoting the entire batch_id), but again theres the problem of the PeopleSoft upload.</p>

<p>More info: I'm appending the data as such (but in a loop):</p>

<pre><code>    NodeList participants = XmlUtil.selectNodeList( doc, "Batch/row" );
    buffer.append( "\t" + item.getAttribute( "batchid" ) );
</code></pre>

<p>Does anyone have any idea how to get Excel to behave correctly?</p>

<p>Edit: I marked a solution, because in any other case it would work.  Trying to spit out the data to Excel like I am now is just a kludge, so I'm just going to rewrite it a different way.</p>

## Answers
### Answer ID: 10308239
<p>You can open that file in excel without losing the zeroes.</p>

<p>Do as follows:</p>

<p>1 - Open Excel;
2 - Click - File->Import and Select the CSV File you want to view in Excel;
3 - Select Delimited and Click Next;
4 - Select Comma as Delimiter and click Next;
5 - Mark Column Data as Text at the column you don't want to lose the zeroes on the left;
6 - Finish.</p>

### Answer ID: 10308147
<p>Save the file locally, and then open it with TextPad directly, the leading zeroes will be there.</p>

<p>Do not open the CSV file in Excel.
Excel will reformat it and strip the leading zeros.</p>

<p>Try it yourself, make a simple CSV file by hand in TextPad, save it, and then open it in Excel. The leading zeroes will be stripped.</p>

<p>If you need it to open properly in Excel, then use a format designed for Excel.
Have the user download an XLS file or XLSX file. Libraries like Apache POI <a href="http://poi.apache.org/spreadsheet/quick-guide.html" rel="nofollow">http://poi.apache.org/spreadsheet/quick-guide.html</a> are a good place to start.</p>

