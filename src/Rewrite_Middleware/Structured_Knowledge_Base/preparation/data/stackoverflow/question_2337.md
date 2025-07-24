# Oracle Blob to XLS worksheet
[Link to question](https://stackoverflow.com/questions/29907274/oracle-blob-to-xls-worksheet)
**Creation Date:** 1430174690
**Score:** 2
**Tags:** java, excel, oracle11g, apache-poi, ibatis
## Question Body
<p>Edit: Solved.  I circumvented the ibatis/ApachePOI by writing a jdbc connector to the database, getting the blob, and dumping it to a file.  Someday, I'd like to know exactly why it was screwing up - but today I'm happy to have this behind me.</p>

<p>Summary: I'm getting Oracle blobs and using Apache POI to reconstitute Excel binaries to pass through a SOAP service layer.  The .Net client is writing these to .xls files just fine, but has corrupt files when writing to a UNIX directory.</p>

<p>Detail:
I have Excel blobs stored in an oracle table.  These blobs are written using iBatis, and pulled using this (truncated) result map.</p>

<pre><code>&lt;resultMap id="report" class="Report"&gt;      
  &lt;result column="content" property ="content" typeHandler="BlobByteArrayTypeHandler"/&gt;
</code></pre>

<p>The excel reports are generated using Apache.POI by our Java services.  At the moment, our Client (.net) queries the service for a byte array, which is written to a Windows machine without error - just dumping the bytes to a file.</p>

<p>These excel files are just fine.</p>

<p>The problem I'm having is that we have a new requirement that we should be writing these files out to a UNIX file system, for further processing.</p>

<p>All attempts at this have failed.  Here are some code samples:</p>

<pre><code>private void writeReportDumpBytes(Report report) {
    File file = new File("report.xls");
    FileOutputStream fileOutputStream;
    try {
        fileOutputStream = new FileOutputStream(file);
        fileOutputStream.write(report.getContent());
        fileOutputStream.flush();
        fileOutputStream.close();
    } catch (FileNotFoundException e) {
        e.printStackTrace();
    } catch (IOException e) {
        e.printStackTrace();
    }   
}

private void writeReportWithEncoding(Report report, String encoding) {
    File file = new File("Report.xls");
    FileOutputStream fileOutputStream;
    try {
        fileOutputStream = new FileOutputStream(file);
        OutputStreamWriter outputStreamWriter = new OutputStreamWriter(fileOutputStream, encoding);         
        Writer out = new BufferedWriter(outputStreamWriter);
        String reportBytes = new String(report.getContent());
        out.write(reportBytes.toCharArray());
        out.flush();
        out.close();
    } catch (FileNotFoundException e) {
        e.printStackTrace();
    } catch (UnsupportedEncodingException e) {
        e.printStackTrace();
    } catch (IOException e) {
        e.printStackTrace();
    }               
}

public void writeReportHssfPoifileSystem(Report report) {
    try {
        InputStream byteStream = new ByteArrayInputStream(report.getContent());
        POIFSFileSystem fs = new POIFSFileSystem(byteStream);
        HSSFWorkbook workbook = new HSSFWorkbook(fs);           
        FileOutputStream fileOut = new FileOutputStream("Report.xls");
        workbook.write(fileOut);
        fileOut.flush();
        fileOut.close();
    } catch (IOException e) {
        log.error(e.getMessage(), e);
    }
}

private void writeReportApacheIO(Report report) {
    File file = new File("Report.xls");
    try {           
        logReportBytes(report, "Apache IO");            
        FileUtils.writeByteArrayToFile(file, report.getContent());
    } catch (IOException e) {
        log.error("Caught IOException", e);
    }               
}
</code></pre>

<p>In order to diagnose this, I have tried grabbing the blob from Oracle, and saving it to a file.  In a bare-bones jar executable, I have been able to read the bytes from this file, and rewrite it using the above methods on our UNIX box - and they all work.</p>

<p>However, from our code, the excel files are all corrupt, or missing header information from Apache.POI.  Opening the corrupt/bad binaries in a text editor shows a repeating pattern of 64 bytes.  It is not a valid xls binary.</p>

<p>Something is going sideways.  The blob is a valid xls binary, and we are just getting the bytes (using the iBatis above) and passing them back through a HSSFWorkbook object, and trying to write using the methods as I've shown them.</p>

<pre><code>    /**
 * Return the byte array based on the workbook.
 * 
 * @return
 * @throws IOException
 */
public byte[] getContent() throws IOException
{
    ByteArrayOutputStream bos = new ByteArrayOutputStream();
    this.workBook.write(bos);   
    return bos.toByteArray();
}
</code></pre>

<p>The specific error I'm getting when using Apache POI is:</p>

<pre><code>java.io.IOException: block[ 0 ] already removed
at org.apache.poi.poifs.storage.BlockListImpl.remove(BlockListImpl.java:97)
at org.apache.poi.poifs.storage.BlockAllocationTableReader.fetchBlocks(BlockAllocationTableReader.java:190)
at org.apache.poi.poifs.storage.BlockListImpl.fetchBlocks(BlockListImpl.java:130)
at org.apache.poi.poifs.property.PropertyTable.&lt;init&gt;(PropertyTable.java:79)
at org.apache.poi.poifs.filesystem.POIFSFileSystem.&lt;init&gt;(POIFSFileSystem.java:171)
</code></pre>

## Answers
### Answer ID: 29954764
<p>I wrote a jdbc call directly to the DB ignoring all the nonsense of ibatis and apache poi.  Worked just fine using a variety of disk write methods.</p>

