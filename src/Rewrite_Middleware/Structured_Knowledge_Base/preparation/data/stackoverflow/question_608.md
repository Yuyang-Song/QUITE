# Oracle 12c interprets SQL in a strange way (Inner Query)
[Link to question](https://stackoverflow.com/questions/33412327/oracle-12c-interprets-sql-in-a-strange-way-inner-query)
**Creation Date:** 1446116203
**Score:** 4
**Tags:** sql, oracle-database, oracle12c, dbms-metadata
## Question Body
<p>We've recently migrated our Oracle database from 10g to 12c (12.1.0.1.0). After considering an issue with some queries we deceided to further clean up the database and drop all unneeded objects.<br>
Therefore I wrote a query that searches the database DDL for a certain text to show up, where a particular view or function is used.</p>

<pre><code>SELECT 
  object_name, object_type, DBMS_METADATA.GET_DDL(object_type, object_name) as ddl_txt 
FROM user_objects 
WHERE object_type IN ( 'FUNCTION', 'VIEW', 'PROCEDURE', 'TRIGGER') 
  AND UPPER( DBMS_METADATA.GET_DDL(object_type, object_name) ) LIKE upper('%myFunction%')
</code></pre>

<p>This results in the following exception:</p>

<pre><code>ORA-31600: invalid input value TYPE BODY for parameter OBJECT_TYPE in function GET_DDL
ORA-06512: at "SYS.DBMS_METADATA", line 5746
ORA-06512: at "SYS.DBMS_METADATA", line 8333
ORA-06512: at line 1
31600. 00000 -  "invalid input value %s for parameter %s in function %s"
*Cause:    A NULL or invalid value was supplied for the parameter.
*Action:   Correct the input value and try the call again.
</code></pre>

<p>The exeption occures because we have 'Body Type' objects in our database and they do not provide a ddl with the <code>DBMS_METADATA.GET_DDL()</code>. Running the query below brings out the exact same exception as from the initial query.</p>

<pre><code>select dbms_metadata.get_ddl('TYPE BODY', 'myBodyStringType') from dual
</code></pre>

<p>So, I try to create an inner list to first reduce the list of all user object to the once I do really care by rewriting my query as followed:</p>

<pre><code>select
  lst.*,
  DBMS_METADATA.GET_DDL(lst.object_type, lst.object_name) as ddl_txt 
from (
      SELECT 
        object_name, object_type
      FROM user_objects 
      WHERE object_type IN ( 'FUNCTION', 'VIEW', 'PROCEDURE', 'TRIGGER') 
) lst
where upper(DBMS_METADATA.GET_DDL(lst.object_type, lst.object_name)) like upper('%myFunction%')
</code></pre>

<p>The funny point is, that it brings out the same exception as shown above. I do not understand why that happens.</p>

<p>I expect Oracle to create the inner list first and consume the <code>DBMS_METADATA.GET_DLL()</code> function only with the remaining values since same values will result in an exception. Why is Oracle doing something else here?</p>

<p>To solve that particular issue I have to add an <code>ORDER BY</code> in the inner query what looks stupid to me. Why do I have to force Oracle to create an inner query first with using an <code>ORDER BY</code>?</p>

<pre><code>select
  lst.*,
  DBMS_METADATA.GET_DDL(lst.object_type, lst.object_name) as ddl_txt 
from (
      SELECT 
        object_name, object_type
      FROM user_objects 
      WHERE object_type IN ( 'FUNCTION', 'VIEW', 'PROCEDURE', 'TRIGGER')
      ORDER BY ROWNUM ASC
) lst
where upper(DBMS_METADATA.GET_DDL(lst.object_type, lst.object_name)) like upper('%myFunction%')
</code></pre>

<p>Thanks in advance for any explanation on why that happens? - I have in mind, that the later query was running without any issues on Oracle 10g.<br>
(I'm worried to have the same behavior on other reports that do calculation which might be wrong because of that behavior!).</p>

## Answers
### Answer ID: 36544800
<p><b>It's a bug.</b> Oracle Support just confirmed to me that the exception occures due to a bug in Oracle Version 12.1.0.<b>1</b> only.<p></p>

<p>There are two options to choose from:<br>
1) update to Oracle Version 12.1.0.<b>2</b> and the bug is fixed.<br>
2) wait a couple weeks for a patch that Oracle is starting to work on soon. The patch will fix this issue in Oracle Version 12.1.0.<b>1</b>.<br>
<br>
We did not decided which option we are taking, but I'm very confident that one or the other will work since Oracle Support did reproduce my problem.</p>

### Answer ID: 33412921
<p>Most likely it's predicate pushing (I can't find a simple explanation sorry) </p>

<p>It's not running the inner recordset first then evaluating the remainder. It's pushing the outside where into the inside derived table. The query plan will tell you for sure.</p>

<p>By using <code>ROWNUM</code> you're forcing it to evaluate the inner recordset first. It's not the <code>ORDER BY</code> its the <code>ROWNUM</code> doing that. Instead of <code>ORDER BY</code> you could also do <code>AND ROWNUM &gt; 0</code> and it would do the same thing because it has to evaluate every row before it can evaluate the <code>ROWNUM</code> expression.</p>

