# Batch read from DBs
[Link to question](https://stackoverflow.com/questions/71634692/batch-read-from-dbs)
**Creation Date:** 1648368881
**Score:** 0
**Tags:** sql, go, batching
## Question Body
<p>Im a bit confused on how golangs sql package reads large datasets into memory. In this previous stackoverflow question - <a href="https://stackoverflow.com/questions/55704072/how-to-set-fetch-size-in-golang/55705575#comment126602506_55705575">How to set fetch size in golang?</a>, there seems to be conflicting ideas on whether batching of large datasets on read happens or not.</p>
<p>I am writing a go binary that connects to different remote DBs based on input params given and fetches resutls and subsequently converts them to a csv file. Suppose I have a query that returns a lot of rows; say 20 million rows. Loading this all at once in memory would be very exhaustive. Does the library batch the results automatically and only on <code>row.Next()</code> load the next batch into memory ?</p>
<p>If the db/sql package does not handle it, are there options in the various driver packages ?</p>
<p><a href="https://github.com/golang/go/issues/13067" rel="nofollow noreferrer">https://github.com/golang/go/issues/13067</a> - From this issue and discussion, I understand that the general idea is to have the driver packages handle this. As mentioned in the issue and also in this blog <a href="https://oralytics.com/2019/06/17/importance-of-setting-fetched-rows-size-for-database-query-using-golang/" rel="nofollow noreferrer">https://oralytics.com/2019/06/17/importance-of-setting-fetched-rows-size-for-database-query-using-golang/</a>, I found out that golangs oracle driver package has this option that I can pass for batching. But am not able to find an equivalent in the other driver packages.</p>
<p>To summarize -</p>
<ol>
<li><p>Does db/sql batch read results automatically.</p>
<ul>
<li>If yes, then my 2nd &amp; 3rd question does not matter</li>
</ul>
</li>
<li><p>If no, are there options that I can pass to the various driver pacakges to set the batch size and where can I find what these options are. I have already tried looking at <a href="https://github.com/jackc/pgx" rel="nofollow noreferrer"><code>pgx</code></a> docs and cannot find anything there that sets a batch size.</p>
</li>
<li><p>Is there any other way to batch reads like a prepared statement with configuration specifying the batch size ?</p>
</li>
</ol>
<p>Some clarifications:</p>
<p>My question is when the a query returns a large dataset, is the entire dataset loaded into memory or is it batched whether internally by some code that is called downstream from <code>rows.Next</code> or not.</p>
<p>From what I can see there is a chunk reader that gets created with a default 8kb size and is used to chunk. Are there cases where this does not happen ? Or are the results from db always chunked.</p>
<p>Is there any way this 8kb buffer size that the chunk reader uses configurable ?</p>
<p>For more clarity, I am adding what is existing in java. This is what already exists and I am looking to rewrite it in golang.</p>
<pre class="lang-java prettyprint-override"><code>
private static final int RESULT_SIZE = 10000;
private void generate() {
... //connection and other code...

  Statement stmt = connection.createStatement(ResultSet.TYPE_FORWARD_ONLY, 
  ResultSet.CONCUR_READ_ONLY);
  stmt.setFetchSize(RESULT_SIZE);
  ResultSet resultset = stmt.executeQuery(dataQuery);
  String fileInHome = getFullFileName(filePath, manager, parentDir);
  rsToCSV(resultset, new BufferedWriter(new FileWriter(fileInHome)));
}

private void rsToCSV(ResultSet rs, BufferedWriter os) throws SQLException {
    ResultSetMetaData metaData = rs.getMetaData();
    int columnCount = metaData.getColumnCount();
    try (PrintWriter pw = new PrintWriter(os)) {
      readHeaders(metaData, columnCount, pw);
      if (rs.next()) {
        readRow(rs, metaData, columnCount, pw);
        while (rs.next()) {
          pw.println();
          readRow(rs, metaData, columnCount, pw);
        }
      }
    }
  }
</code></pre>
<p>The <code>stmt.setFetchSize(RESULT_SIZE);</code> sets the number of rows to return in each result set which is then processed one by one to a csv.</p>

