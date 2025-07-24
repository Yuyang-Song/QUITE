# iSeries query changes selected RRN of subquery result rows
[Link to question](https://stackoverflow.com/questions/22519174/iseries-query-changes-selected-rrn-of-subquery-result-rows)
**Creation Date:** 1395266833
**Score:** 1
**Tags:** sql, db2, ibm-midrange, db2-400
## Question Body
<p>I'm trying to make an optimal SQL query for an iSeries database table that can contain millions of rows (perhaps up to 3 million per month). The only key I have for each row is its RRN (relative record number, which is the physical record number for the row).</p>

<p>My goal is to join the table with another small table to give me a textual description of one of the numeric columns. However, the number of rows involved can exceed 2 million, which typically causes the query to fail due to an out-of-memory condition. So I want to rewrite the query to avoid joining a large subset with any other table. So the idea is to select a single page (up to 30 rows) within a given month, and <em>then</em> join that subset to the second table. </p>

<p>However, I ran into a weird problem. I use the following query to retrieve the RRNs of the rows I want for the page:</p>

<pre><code>    select t.RRN2    -- Gives correct RRNs
    from (
      select row_number() over() as SEQ,
        rrn(e2) as RRN2, e2.*
      from TABLE1 as e2
      where e2.UPDATED between '2013-05-01' and '2013-05-31'
      order by e2.UPDATED, e2.ACCOUNT
    ) as t
    where t.SEQ &gt; 270 and t.SEQ &lt;= 300    -- Paging
    order by t.UPDATED, t.ACCOUNT
</code></pre>

<p>This query works just fine, returning the correct RRNs for the rows I need. However, when I attempted to join the result of the subquery with another table, <em>the RRNs changed</em>. So I simplified the query to a subquery within a simple outer query, without any join:</p>

<pre><code>select rrn(e) as RRN, e.*
  from TABLE1 as e
  where rrn(e) in (
    select t.RRN2    -- Gives correct RRNs
    from (
      select row_number() over() as SEQ,
        rrn(e2) as RRN2, e2.*
      from TABLE1 as e2
      where e2.UPDATED between '2013-05-01' and '2013-05-31'
      order by e2.UPDATED, e2.ACCOUNT
    ) as t
    where t.SEQ &gt; 270 and t.SEQ &lt;= 300    -- Paging
    order by t.UPDATED, t.ACCOUNT
  )
  order by e.UPDATED, e.ACCOUNT
</code></pre>

<p>The outer query simply grabs all of the columns of each row selected by the subquery, using the RRN as the row key. But this query <em>does not work</em> - it returns rows with completely different RRNs.</p>

<p>I need the actual RRN, because it will be used to retrieve more detailed information from the table in a subsequent query.</p>

<p>Any ideas about why the RRNs end up different?</p>

<p><strong>Resolution</strong></p>

<p>I decided to break the query into two calls, one to issue the simple subquery and return just the RRNs (rows-IDs), and the second to do the rest of the JOINs and so forth to retrieve the complete info for each row. (Since the table gets updated only once a day, and rows never get deleted, there are no potential timing problems to worry about.)</p>

<p>This approach appears to work quite well.</p>

<p><strong>Addendum</strong></p>

<p>As to the question of why an out-of-memory error occurs, this appears to be a limitation on only <em>some</em> of our test servers. Some can only handle up to around 2m rows, while others can handle much more than that. So I'm guessing that this is some sort of limit imposed by the admins on a server-by-server basis.</p>

## Answers
### Answer ID: 22533593
<p>Trying to use RRN as a primary key is asking for trouble.</p>

<p>I find it hard to believe there isn't a key available.  </p>

<p>Granted, there may be no explicit primary key defined in the table itself.  But is there a unique key defined in the table?  </p>

<p>It's possible there's no keys defined in the table itself ( a practice that is 20yrs out of date) but in that case there's usually a logical file with a unique key defined that is by the application as the de-facto primary key to the table.</p>

<p>Try looking for related objects via green screen (DSPDBR) or GUI (via "Show related").  Keyed logical files show in the GUI as views.  So you'd need to look at the properties to determine if they are uniquely keyed DDS logicals instead of non-keyed SQL views.  </p>

<p>A few times I've run into tables with no existing de-facto primary key. Usually, it was possible to figure out what could be defined as one from the existing columns.</p>

<p>When there truly is no PK, I simply add one.  Usually a generated identity column.  There's a technique you can use to easily add columns without having to recompile or test any heritage RPG/COBOL programs.  (and note LVLCHK(*NO) is NOT it!)</p>

<p>The technique is laid out in Chapter 4 of the modernizing Redbook
<a href="http://www.redbooks.ibm.com/abstracts/sg246393.html" rel="noreferrer">http://www.redbooks.ibm.com/abstracts/sg246393.html</a></p>

<p>1) Move the data to a new PF (or SQL table)
2) create new LF using the name of the existing PF
3) repoint existing LF to new PF (or SQL table)</p>

<p>Done properly, the record format identifiers of the existing objects don't change and thus you don't have to recompile any RPG/COBOL programs.</p>

### Answer ID: 22522009
<p>Unless you can specifically control it, e.g., via ALWCPYDTA(*NO) for STRSQL, SQL may make copies of result rows for any intermediate set of rows. The RRN() function always accesses <strong>physical record number</strong>, as contrasted with the ROW_NUMBER() function that returns a logical row number indicating the relative position in an ordered (or unordered) set of rows. If a copy is generated, there is no way to guarantee that RRN() will remain consistent.</p>

<p>Other considerations apply over time; but in this case it's as likely to be simple copying of intermediate result rows as anything.</p>

### Answer ID: 22521248
<p>I find it hard to believe that querying a table of mere 3 million rows, even when joined with something else, should cause an out-of-memory condition, so in my view you should address this issue first (or cause it to be addressed).</p>

<p>As for your question of <em>why the RRNs end up different</em> I'll take the liberty of quoting <a href="http://pic.dhe.ibm.com/infocenter/iseries/v6r1m0/topic/db2/rbafzscarrn.htm" rel="nofollow">the manual</a>:</p>

<blockquote>
  <p>If the argument identifies a view, common table expression, or nested table expression derived from more than one base table, the function returns the relative record number of the first table in the outer subselect of the view, common table expression, or nested table expression.</p>
</blockquote>

<p>A construct of the type <code>...where something in (select somethingelse...)</code> typically translates into a join, so there.</p>

