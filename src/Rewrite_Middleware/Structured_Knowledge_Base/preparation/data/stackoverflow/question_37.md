# UTL_MATCH-like function to work with CLOB
[Link to question](https://stackoverflow.com/questions/10703609/utl-match-like-function-to-work-with-clob)
**Creation Date:** 1337695228
**Score:** 3
**Tags:** sql, oracle-database, pattern-matching, string-matching, clob
## Question Body
<p><strong>My question is:</strong> Is there a <a href="http://docs.oracle.com/cd/E14072_01/appdev.112/e10577/u_match.htm#CHDGDIDJ" rel="nofollow"><code>UTL_MATCH</code></a>-like function which works with a <code>CLOB</code> rather than a <code>VARCHAR2</code>?</p>

<p><strong>My specific problem is:</strong> I'm on an Oracle database. I have a bunch of pre-written queries which interface with Domo <a href="http://www.domo.com/solutions/centerview" rel="nofollow">CenterView</a>. The queries have variables in them defined by <code>${variableName}</code>. I need to rewrite these queries. I didn't write the original so instead of figuring out what a good value for the variables should be I want to run the queries with the application and get what the query was from <a href="http://docs.oracle.com/cd/B19306_01/server.102/b14237/dynviews_2113.htm" rel="nofollow"><code>V$SQL</code></a>.</p>

<p><strong>So my solution is:</strong> Do a <code>UTL_MATCH</code> on the queries with the variable stuff in it and <code>V$SQL.SQL_FULLTEXT</code>. However, <code>UTL_MATCH</code> is limited to <code>VARCHAR2</code> and the datatype of <code>V$SQL.SQL_FULLTEXT</code> is <code>CLOB</code>. So, this is why I'm looking for a <code>UTL_MATCH</code>-like function which works with a <code>CLOB</code> datatype.</p>

<p><em>Any other tips of how to accomplish this are welcome. Thanks!</em></p>

<p><strong>Edit, about the tips.</strong> If you have a better idea of how to do this, let me just tell you some information I've got at my disposal. I have about 100 queries, they're all in an excel spreadsheet (the ones with the <code>${variableName}</code> in them). So I could pretty easily use excel to write a query for me. I'm hoping to just union all those queries together and copy the output to another sheet. Anyway, maybe that's helpful if you're thinking there's a better way to do this.</p>

<p><strong>An example:</strong> Let's say I have the following query from Domo:</p>

<pre><code>select department.dept_name
from department
where department.id = '${selectedDepartmentId}'
;
</code></pre>

<p>I want to call something like this:</p>

<pre><code>select v.sql_fulltext
from v$sql v
where utl_match.jaro_winkler_similarity(v.sql_fulltext,
'select department.dept_name
from department
where department.id = ''${selectedDepartmentId}''') &gt; 90
;
</code></pre>

<p>And get something like this in return:</p>

<pre><code>SQL_FULLTEXT
------------------------------------------
select department.dept_name
from department
where department.id = '154'
</code></pre>

<p><strong>What I've tried:</strong></p>

<p>I tried substringing the clob and casting it to a varchar. I was really hopeful this would work, but it gives me an error. Here's the code:</p>

<pre><code>select v.sql_fulltext
from v$sql v
where  utl_match.jaro_winkler_similarity( cast( substr (v.sql_fulltext, 0, 4000) as varchar2 (4000)),
'select department.dept_name
from department
where department.id = ''${selectedDepartmentId}''') &gt; 90
;
</code></pre>

<p>And here's the error:</p>

<p><code>ORA-22835: Buffer too small for CLOB to CHAR or BLOB to RAW conversion (actual: 8000, maximum: 4000)</code></p>

<p>However, if I run this it works fine:</p>

<pre><code>select cast(substr(v.sql_fulltext, 0, 4000) as varchar2 (4000))
from v$sql v
;
</code></pre>

<p>So I'm not sure what the problem is with casting the substring...</p>

## Answers
### Answer ID: 10739464
<p>I ended up creating a custom function for it. Here's the code:</p>

<pre><code>CREATE OR REPLACE function match_clob(clob_1 clob, clob_2 clob) return number as

similar number := 0;
sec_similar number := 0;
sections number := 0;
max_length number := 3949;
length_1 number;
length_2 number;
vchar_1 varchar2 (3950);
vchar_2 varchar2 (3950);

begin
  length_1 := length(clob_1);
  length_2 := length(clob_2);
  --dbms_output.put_line('length_1: '||length_1);
  --dbms_output.put_line('length_2: '||length_2);
  IF length_1 &gt; max_length or length_2 &gt; max_length THEN

    FOR x IN 1 .. ceil(length_1 / max_length) LOOP

      --dbms_output.put_line('((x-1)*max_length) + 1'||(x-1)||' * '||max_length||' = '||(((x-1)*max_length) + 1));

      vchar_1 := substr(clob_1, ((x-1)*max_length) + 1, max_length);
      vchar_2 := substr(clob_2, ((x-1)*max_length) + 1, max_length);

--      dbms_output.put_line('Section '||sections||' vchar_1: '||vchar_1||' ==&gt; vchar_2: '||vchar_2);

      sec_similar := UTL_MATCH.JARO_WINKLER_SIMILARITY(vchar_1, vchar_2);

      --dbms_output.put_line('sec_similar: '||sec_similar);

      similar := similar + sec_similar;
      sections := sections + 1;

    END LOOP;

    --dbms_output.put_line('Similar: '||similar||' ==&gt; Sections: '||sections);
    similar := similar / sections;

  ELSE
    similar := UTL_MATCH.JARO_WINKLER_SIMILARITY(clob_1,clob_2);
  END IF;
  --dbms_output.put_line('Overall Similar: '||similar);
   return(similar);
end;
/
</code></pre>

### Answer ID: 10706021
<p>If the text you want to search has length &lt;= 32767, then you can just convert the <code>CLOB</code> to <code>VARCHAR2</code> using <code>DBMS_LOB.SUBSTR</code>:</p>

<pre><code>select v.sql_fulltext 
from v$sql v 
where utl_match.jaro_winkler_similarity(dbms_lob.substr(v.sql_fulltext), 'select department.dept_name from department where department.id = ''${selectedDepartmentId}''') &gt; 90 ;
</code></pre>

### Answer ID: 10703875
<p>UTL_MATCH is a packaging for comparing strings with regards for checking how similar two strings are.  Its functions evaluate strings and return scores.  So all you're going to get is a number indicating (say) how many edits you need to turn <code>${variableName}</code> into "Farmville" or "StackOveflow".    </p>

<p>What you won't get is the actual differences: these two strings of text are identical except at offset 123 where it replaces <code>${variableName}</code> with "Farmville".</p>

<p>Putting it like that suggests an alternative approach.  Using <a href="http://docs.oracle.com/cd/B19306_01/appdev.102/b14258/d_lob.htm#i998546" rel="nofollow">INSTR()</a> and <a href="http://docs.oracle.com/cd/B19306_01/appdev.102/b14258/d_lob.htm#i999349" rel="nofollow">SUBSTR()</a> to locate instances of <code>${variableName}</code> in your Domo CenterView queries and use those offsets to identify the different text in the <code>v$sql.fulltext</code> equivalents.  You can do this with CLOB in PL/SQL with the <a href="http://docs.oracle.com/cd/B19306_01/appdev.102/b14258/d_lob.htm" rel="nofollow">DBMS_LOB package</a>.</p>

