# How to improve a SCN-based query performance?
[Link to question](https://stackoverflow.com/questions/16565331/how-to-improve-a-scn-based-query-performance)
**Creation Date:** 1368621855
**Score:** 8
**Tags:** oracle-database, oracle10g
## Question Body
<p>In Oracle database there is a <a href="http://docs.oracle.com/cd/B19306_01/server.102/b14200/pseudocolumns007.htm" rel="noreferrer">pseudocolumn which's called <code>ora_rowscn</code></a>. If it's retrieved it shows the SCN of the most recent change to the row (as it's said in the documentation).</p>

<p>Also there's an option <code>rowdependencies</code> of <code>CREATE TABLE</code> which switches on storage of SCN for each row instead of a whole data block (which is default).</p>

<p>So, I'm using values of this column for indicating which rows were updated and are needed to be uploaded to another database.</p>

<p>Let's consider this example:</p>

<ol>
<li><p>There's a table <code>T1</code> in schema <code>S1</code> which contains several millions of records (full scan on the table is not affordable for regular queries).</p>

<pre><code>CREATE TABLE T1 {
  A INTEGER PRIMARY KEY,
  B VARCHAR2(100),
  C DATE
}
/
</code></pre></li>
<li><p>There're schemas <code>S2, S3, S4, S5..</code> and in each of them there's table <code>T2</code>.</p>

<pre><code>CREATE TABLE T2 {
  A INTEGER
}
/
</code></pre></li>
<li><p>There's only one row in <code>T2</code>, but value of <code>T2.A</code> can be different in different schemas.</p></li>
</ol>

<p>So, I need to retrieve in each schema <code>(S2, S3, S4...)</code> all rows from <code>S1.T1</code> which have value of <code>ora_rowscn</code> greater than <code>S*.T2.A</code> (then I use this data block). 
After gettting these rows I rewrite value of <code>S*.T2.A</code> with the current system SCN (<code>dbms_flashback.get_system_change_number</code>).</p>

<p>The following queries for any schema is right here:</p>

<p>Query 1:</p>

<pre><code>SELECT * FROM S1.T1 WHERE ora_rowscn &gt; (SELECT A FROM T2);
</code></pre>

<p>Query 2 (it's performed when I finished work with dataset returned by the previous query):</p>

<pre><code>UPDATE T2 SET A = dbms_flashback.get_system_change_number;
</code></pre>

<p>The problem is that performance of query 1 is unacceptable (full scan on the table <code>S1.T1</code>) and the column <code>ora_rowscn</code> can't be indexed. </p>

<p>The question: <strong>What could be the ways to improve the performance of the query 1?</strong></p>

## Answers
### Answer ID: 16579480
<p>All you care about is, which rows have been inserted or updated since the last time you ran the upload.</p>

<p>Why not add a flag to the table that marks each row as "dirty" - i.e. a before insert trigger would set it to 'X' and a before update trigger would set it to 'X'.</p>

<p>Then, write your upload process to query the table for any row where the flag is NOT NULL, then set the flag to NULL when it succeeds. Note that this means that new rows that get inserted/updated <em>while the upload is in progress</em> will still get marked correctly, and will be picked up the next time the upload runs.</p>

<p>If the number of rows inserted/updated compared with the total rows in the table is a very small ratio, an index on the flag will be useful, because NULL flags will not be stored in the index (i.e. the index will usually be small.</p>

<p>EDIT:</p>

<p>An equivalent solution for situations where multiple schemas need to be updated is to have a separate table which will hold the IDs of rows that have changed. The table should have a flag for each target schema. When all the flags have been set to NULL, delete the row from the table.</p>

### Answer ID: 16565620
<p>You can't index <code>ora_rowscn</code>. Consequently the best plan for query 1 is a <code>FULL TABLE SCAN</code>. </p>

<p>Since this is not acceptable, you will have to use another marker, for example a <code>last_updated</code> <code>date</code> column. This column is indexable but you'll have to update it. You can automatize this update with a small light-weight trigger.</p>

<p>Performance of query 1 against an indexed column will be dependent upon the number of rows retrieved. </p>

